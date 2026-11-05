// check-isa-level verifies that a Go binary targets at most x86-64-v2.
//
// The check is host-architecture independent: it dispatches on the target
// ELF's machine type, not on the architecture of the machine running the
// check. This matters for cross-builds — an amd64 binary built on an arm64
// host (or vice versa) is checked according to its own architecture.
//
// For x86-64 targets the check is two-tier:
//  1. If the ELF carries a GNU_PROPERTY_X86_ISA_1_NEEDED note (emitted by
//     the GNU linker for externally linked / CGo binaries), its v3/v4 bits
//     must be clear.
//  2. Otherwise (pure-Go builds via Go's internal linker, which never emits
//     the note), the GOAMD64 setting recorded in the binary's build info
//     must be at most v2. Fail closed if the setting is missing.
//
// Non-x86-64 targets pass: they have no x86-64 ISA level to verify.
package main

import (
	"debug/buildinfo"
	"debug/elf"
	"encoding/binary"
	"errors"
	"fmt"
	"io"
	"os"
)

const (
	ntGNUPropertyType0       = 5
	gnuPropertyX86ISA1Needed = 0xc0008002
	isaV3                    = 1 << 2
	isaV4                    = 1 << 3
	isaBeyondV2              = isaV3 | isaV4
)

// errNoBuildInfo identifies binaries whose Go build information cannot be read.
// Missing or invalid settings in readable build info must not use this fallback.
var errNoBuildInfo = errors.New("no readable Go build info")

// main checks the supplied binary and exits nonzero for incompatible or invalid inputs.
func main() {
	if len(os.Args) != 2 {
		fmt.Fprintf(os.Stderr, "usage: %s <binary-to-check>\n", os.Args[0])
		os.Exit(2)
	}
	path := os.Args[1]
	// The path comes from the command line: this is a build-time check tool
	// run by CI on a binary it just built, so the input is trusted by design.
	if _, err := os.Stat(path); err != nil { //nolint:gosec // G304: trusted CLI argument
		if os.IsNotExist(err) {
			fmt.Fprintf(os.Stderr, "binary not found: %s\n", path)
			os.Exit(2)
		}
		fmt.Fprintf(os.Stderr, "stat %s: %v\n", path, err)
		os.Exit(2)
	}

	ok, reason, err := checkPath(path)
	if err != nil {
		fmt.Fprintf(os.Stderr, "checking %s: %v\n", path, err)
		os.Exit(2)
	}
	if !ok {
		fmt.Fprintf(os.Stderr, "%s requires ISA level beyond x86-64-v2 (%s)\n", path, reason)
		os.Exit(1)
	}
	os.Exit(0)
}

// checkPath verifies that the binary at path targets at most x86-64-v2. It
// dispatches on the target ELF's machine type so cross-builds are checked
// according to the binary's own architecture, not the build host's; non-x86-64
// targets pass, as they have no x86-64 ISA level to verify.
func checkPath(path string) (bool, string, error) {
	machine, err := elfMachine(path)
	if err != nil {
		return false, "", err
	}
	if machine != elf.EM_X86_64 {
		return true, "", nil
	}
	return atMostX86_64_V2(path)
}

// elfMachine returns the ELF machine type of the binary at path.
func elfMachine(path string) (elf.Machine, error) {
	f, err := elf.Open(path)
	if err != nil {
		return 0, err
	}
	defer func() { _ = f.Close() }()
	return f.Machine, nil
}

// atMostX86_64_V2 checks both the ELF ISA declaration and the Go codegen baseline.
func atMostX86_64_V2(path string) (bool, string, error) {
	val, found, err := getX86ISA1Needed(path)
	if err != nil {
		return false, "", err
	}
	if found {
		// Externally linked (CGo) binary: the GNU linker emits the
		// GNU_PROPERTY_X86_ISA_1_NEEDED note describing the ISA the
		// binary actually requires. The note covers the C object files —
		// Go's internal object files never declare ISA properties — so a
		// CGo binary built with GOAMD64=v4 can carry a baseline note while
		// its Go code requires v4. Also check the recorded GOAMD64 setting
		// when Go build info is available; without it (non-Go binaries),
		// the note alone governs.
		noteOK := (val & isaBeyondV2) == 0
		noteReason := fmt.Sprintf("GNU_PROPERTY_X86_ISA_1_NEEDED=0x%x has v3/v4 bits", val)
		goOK, goReason, goErr := goAmd64AtMostV2(path)
		if goErr != nil {
			if errors.Is(goErr, errNoBuildInfo) {
				// Non-Go binary: only the ELF note governs.
				return noteOK, noteReason, nil
			}
			return false, "", goErr
		}
		if !noteOK {
			return false, noteReason, nil
		}
		if !goOK {
			return false, goReason, nil
		}
		return true, "", nil
	}
	// Go's internal linker (pure-Go builds, CGO_ENABLED=0) does not emit
	// the note at any GOAMD64 level, so the ELF note cannot be used.
	// Instead, verify the GOAMD64 build setting recorded in the binary's
	// build info: it is the baseline the compiler was allowed to target.
	return goAmd64AtMostV2(path)
}

// goAmd64AtMostV2 reads the GOAMD64 setting from the binary's build info and
// reports whether it is at most v2. The setting is recorded even when left at
// the default (v1). Binaries without build info (or without the setting)
// fail closed: their codegen baseline cannot be verified.
func goAmd64AtMostV2(path string) (bool, string, error) {
	info, err := buildinfo.ReadFile(path)
	if err != nil {
		// Preserve file access errors rather than treating them as a non-Go binary.
		var pathErr *os.PathError
		if errors.As(err, &pathErr) {
			return false, "", fmt.Errorf("reading build info: %w", err)
		}
		return false, "", fmt.Errorf("%w: %w", errNoBuildInfo, err)
	}
	for _, setting := range info.Settings {
		if setting.Key != "GOAMD64" {
			continue
		}
		switch setting.Value {
		case "v1", "v2":
			return true, "", nil
		case "v3", "v4":
			return false, fmt.Sprintf("GOAMD64=%s build setting exceeds v2", setting.Value), nil
		default:
			return false, "", fmt.Errorf("unrecognized GOAMD64 build setting %q", setting.Value)
		}
	}
	return false, "", fmt.Errorf("GOAMD64 build setting not recorded in binary")
}

// getX86ISA1Needed reads the GNU ISA-needed property, reporting whether it exists.
func getX86ISA1Needed(path string) (uint32, bool, error) {
	f, err := elf.Open(path)
	if err != nil {
		return 0, false, err
	}
	defer func() { _ = f.Close() }()

	// Prefer the section named .note.gnu.property; otherwise search every
	// SHT_NOTE section — the GNU property may live in any of them.
	var candidates []*elf.Section
	for _, s := range f.Sections {
		if s.Name == ".note.gnu.property" {
			candidates = []*elf.Section{s}
			break
		}
	}
	if candidates == nil {
		for _, s := range f.Sections {
			if s.Type == elf.SHT_NOTE {
				candidates = append(candidates, s)
			}
		}
	}
	for _, s := range candidates {
		val, found, err := parseNoteSection(s)
		if err != nil {
			return 0, false, err
		}
		if found {
			return val, true, nil
		}
	}
	return 0, false, nil
}

// maxNoteSectionSize bounds the buffer allocated for a note section: real
// GNU property notes are tiny, but a corrupt ELF can declare an enormous
// section size.
const maxNoteSectionSize = 1 << 20

// parseNoteSection reads one note section and returns the
// GNU_PROPERTY_X86_ISA_1_NEEDED value when present. Zero-size sections are
// skipped without error; oversized sections are rejected before allocating.
func parseNoteSection(s *elf.Section) (uint32, bool, error) {
	if s.Size == 0 {
		return 0, false, nil
	}
	if s.Size > maxNoteSectionSize {
		return 0, false, fmt.Errorf("note section %s: size %d exceeds limit %d", s.Name, s.Size, maxNoteSectionSize)
	}
	data := make([]byte, s.Size)
	if _, err := io.ReadFull(s.Open(), data); err != nil {
		return 0, false, fmt.Errorf("reading note section %s: %w", s.Name, err)
	}

	order := binary.LittleEndian
	off := 0
	for off+12 <= len(data) {
		namesz := order.Uint32(data[off : off+4])
		descsz := order.Uint32(data[off+4 : off+8])
		ntype := order.Uint32(data[off+8 : off+12])
		off += 12

		// Padded sizes are computed in int64: the +3/+7 rounding in uint32
		// arithmetic would wrap for sizes near math.MaxUint32, and a wrapped
		// padding can pass the bounds check below while the raw size still
		// overflows the slice. Malformed sizes are rejected by the bounds
		// check rather than reaching a slice that can panic.
		namePadded := (int64(namesz) + 3) &^ 3
		descPadded := (int64(descsz) + 3) &^ 3
		if int64(off)+namePadded+int64(descsz) > int64(len(data)) {
			// Malformed note sizes: not a valid x86-64 ISA declaration.
			return 0, false, nil
		}
		name := data[off : off+int(namesz)]
		off += int(namePadded)
		desc := data[off : off+int(descsz)]
		off += int(descPadded)

		if ntype != ntGNUPropertyType0 {
			continue
		}
		if namesz < 4 || string(name[:4]) != "GNU\x00" {
			continue
		}

		descOff := 0
		for descOff+8 <= len(desc) {
			prType := order.Uint32(desc[descOff : descOff+4])
			prDatasz := order.Uint32(desc[descOff+4 : descOff+8])
			descOff += 8
			if descOff+int(prDatasz) > len(desc) {
				break
			}
			if prType == gnuPropertyX86ISA1Needed && prDatasz == 4 {
				return order.Uint32(desc[descOff : descOff+4]), true, nil
			}
			// int64 arithmetic: prDatasz+7 rounds without uint32 wraparound.
			descOff += int((int64(prDatasz) + 7) &^ 7)
		}
	}

	return 0, false, nil
}
