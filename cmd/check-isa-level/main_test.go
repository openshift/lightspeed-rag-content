package main

import (
	"bytes"
	"debug/buildinfo"
	"encoding/binary"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"testing"
)

// buildFixture compiles a trivial Go binary with the given build environment
// (GOARCH/GOAMD64/CGO_ENABLED...) and returns its path. Fixtures are
// inspected, never executed.
func buildFixture(t *testing.T, mainSrc string, env ...string) string {
	t.Helper()
	goBin, err := exec.LookPath("go")
	if err != nil {
		t.Skip("go toolchain not in PATH")
	}
	dir := t.TempDir()
	if err := os.WriteFile(filepath.Join(dir, "main.go"), []byte(mainSrc), 0o644); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(dir, "go.mod"), []byte("module fixture\n\n"), 0o644); err != nil {
		t.Fatal(err)
	}
	bin := filepath.Join(dir, "fixture")
	cmd := exec.CommandContext(t.Context(), goBin, "build", "-o", bin, ".")
	cmd.Dir = dir
	// GOOS is pinned so fixtures are ELF regardless of the development
	// host's OS (the checker parses ELF; a macOS host would otherwise
	// produce Mach-O fixtures).
	cmd.Env = append(os.Environ(), "GOOS=linux", "GOFLAGS=", "GOWORK=off", "GOPROXY=off")
	cmd.Env = append(cmd.Env, env...)
	if out, err := cmd.CombinedOutput(); err != nil {
		t.Fatalf("building fixture: %v\n%s", err, out)
	}
	return bin
}

const pureGoMain = "package main\n\nfunc main() {}\n"

// TestCheckPathAmd64Levels verifies the GOAMD64 build-info tier: v1/v2 are
// accepted, v3/v4 are rejected.
func TestCheckPathAmd64Levels(t *testing.T) {
	for _, tc := range []struct {
		level string
		want  bool
	}{
		{"v1", true},
		{"v2", true},
		{"v3", false},
		{"v4", false},
	} {
		t.Run("GOAMD64="+tc.level, func(t *testing.T) {
			bin := buildFixture(t, pureGoMain, "GOARCH=amd64", "GOAMD64="+tc.level)
			ok, reason, err := checkPath(bin)
			if err != nil {
				t.Fatalf("checkPath: %v", err)
			}
			if ok != tc.want {
				t.Errorf("GOAMD64=%s: ok = %v (reason %q), want %v", tc.level, ok, reason, tc.want)
			}
		})
	}
}

// TestCheckPathNonAmd64Skipped verifies the ELF machine-type dispatch: an
// arm64 target passes without ISA verification. GOAMD64 is ignored for
// non-amd64 targets, so even v4 must not affect the result.
func TestCheckPathNonAmd64Skipped(t *testing.T) {
	bin := buildFixture(t, pureGoMain, "GOARCH=arm64", "GOAMD64=v4")
	ok, _, err := checkPath(bin)
	if err != nil {
		t.Fatalf("checkPath: %v", err)
	}
	if !ok {
		t.Error("non-amd64 target must pass without x86-64 ISA verification")
	}
}

// TestCheckPathExternallyLinked verifies the ELF-note tier and its
// combination with the GOAMD64 build-info tier: for a CGo binary the GNU
// property note covers only the C object files, so a raised GOAMD64 must
// still be rejected even when the note stays at baseline.
func TestCheckPathExternallyLinked(t *testing.T) {
	// The fixture needs CGO for the linux/amd64 target: a native compiler
	// for the host's own platform. Skip everywhere else (e.g. macOS, arm64
	// hosts without a cross-toolchain).
	if runtime.GOOS != "linux" || runtime.GOARCH != "amd64" {
		t.Skip("externally linked fixture requires a Linux/amd64 host with a native C compiler")
	}
	if _, err := exec.LookPath("gcc"); err != nil {
		t.Skip("gcc not available for an externally linked fixture")
	}
	cgoMain := `package main

/*
#include <stdlib.h>
*/
import "C"

func main() { _ = C.random() }
`
	t.Run("CGo with GOAMD64=v1 passes", func(t *testing.T) {
		bin := buildFixture(t, cgoMain, "GOARCH=amd64", "GOAMD64=v1", "CGO_ENABLED=1")
		ok, _, err := checkPath(bin)
		if err != nil {
			t.Fatalf("checkPath: %v", err)
		}
		if !ok {
			t.Error("externally linked GOAMD64=v1 binary must pass")
		}
	})
	t.Run("CGo with GOAMD64=v4 rejected despite baseline C objects", func(t *testing.T) {
		bin := buildFixture(t, cgoMain, "GOARCH=amd64", "GOAMD64=v4", "CGO_ENABLED=1")
		ok, reason, err := checkPath(bin)
		if err != nil {
			t.Fatalf("checkPath: %v", err)
		}
		if ok {
			t.Error("externally linked GOAMD64=v4 binary must be rejected")
		}
		if !strings.Contains(reason, "GOAMD64") {
			t.Errorf("expected the GOAMD64 build setting to be named in the reason, got %q", reason)
		}
	})
}

// TestCheckPathInvalidGoSetting rejects invalid Go metadata even when the
// externally linked binary has an acceptable C ISA note.
func TestCheckPathInvalidGoSetting(t *testing.T) {
	if runtime.GOOS != "linux" || runtime.GOARCH != "amd64" {
		t.Skip("externally linked fixture requires a Linux/amd64 host")
	}
	if _, err := exec.LookPath("gcc"); err != nil {
		t.Skip("gcc not available")
	}
	bin := buildFixture(t, "package main\nimport \"C\"\nfunc main() {}\n", "GOARCH=amd64", "GOAMD64=v1", "CGO_ENABLED=1")
	val, found, err := getX86ISA1Needed(bin)
	if err != nil {
		t.Fatal(err)
	}
	if !found {
		t.Skip("linker did not emit an ISA-needed note")
	}
	if val&isaBeyondV2 != 0 {
		t.Fatal("fixture must have a baseline ISA note")
	}
	data, err := os.ReadFile(bin)
	if err != nil {
		t.Fatal(err)
	}
	original := []byte("build\tGOAMD64=v1\n")
	if !bytes.Contains(data, original) {
		t.Fatal("expected a GOAMD64 build setting")
	}
	for _, tc := range []struct{ name, replacement string }{
		{"missing", "build\tNOAMD64=v1\n"},
		{"invalid level", "build\tGOAMD64=v9\n"},
		{"invalid prefix", "build\tGOAMD64=x1\n"},
		{"empty", "build\tGOAMD64=\n\n\n"},
	} {
		t.Run(tc.name, func(t *testing.T) {
			path := filepath.Join(t.TempDir(), "fixture")
			// Replace both the on-disk build info and runtime's copy, keeping
			// string lengths and ELF offsets unchanged.
			patched := bytes.ReplaceAll(data, original, []byte(tc.replacement))
			if err := os.WriteFile(path, patched, 0o644); err != nil {
				t.Fatal(err)
			}
			if _, err := buildinfo.ReadFile(path); err != nil {
				t.Fatalf("fixture must retain readable Go build info: %v", err)
			}
			ok, _, err := checkPath(path)
			if ok || err == nil {
				t.Errorf("invalid GOAMD64 must fail closed, got ok=%v, err=%v", ok, err)
			}
		})
	}
}

// TestCheckPathMissingFile verifies the error path for unusable inputs.
func TestCheckPathMissingFile(t *testing.T) {
	_, _, err := checkPath(filepath.Join(t.TempDir(), "does-not-exist"))
	if err == nil {
		t.Error("expected an error for a missing binary")
	}
}

// syntheticNoteELF writes a minimal ELF64 x86-64 file whose only meaningful
// content is a .note.gnu.property section declaring GNU_PROPERTY_X86_ISA_1_NEEDED
// with the given value. It has no Go build info, so the checker's ELF-note tier
// governs. This avoids needing a compiler that emits raised ISA notes.
func syntheticNoteELF(t *testing.T, isaNeeded uint32, sectionName string) string {
	t.Helper()
	// Note entry: namesz=4, descsz=16, type=NT_GNU_PROPERTY_TYPE_0, "GNU\0",
	// then the property record: pr_type=GNU_PROPERTY_X86_ISA_1_NEEDED,
	// pr_datasz=4, value, padding to 8-byte alignment.
	desc := make([]byte, 16)
	binary.LittleEndian.PutUint32(desc[0:4], 0xc0008002) // pr_type
	binary.LittleEndian.PutUint32(desc[4:8], 4)          // pr_datasz
	binary.LittleEndian.PutUint32(desc[8:12], isaNeeded) // value
	note := make([]byte, 0, 12+4+16)
	note = binary.LittleEndian.AppendUint32(note, 4)  // namesz
	note = binary.LittleEndian.AppendUint32(note, 16) // descsz
	note = binary.LittleEndian.AppendUint32(note, 5)  // ntype
	note = append(note, 'G', 'N', 'U', 0)
	note = append(note, desc...)

	const ehsize, shentsize = 64, 64
	shoff := ehsize + len(note)
	shstr := append(append([]byte("\x00"), sectionName...), []byte("\x00.shstrtab\x00")...)
	shstrOff := shoff + 3*shentsize

	elf := make([]byte, 0, shstrOff+len(shstr))
	elf = append(elf, 0x7f, 'E', 'L', 'F', 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
	elf = binary.LittleEndian.AppendUint16(elf, 2)    // ET_EXEC
	elf = binary.LittleEndian.AppendUint16(elf, 0x3e) // EM_X86_64
	elf = binary.LittleEndian.AppendUint32(elf, 1)    // version
	elf = binary.LittleEndian.AppendUint64(elf, 0)    // entry
	elf = binary.LittleEndian.AppendUint64(elf, 0)    // phoff
	elf = binary.LittleEndian.AppendUint64(elf, uint64(shoff))
	elf = binary.LittleEndian.AppendUint32(elf, 0) // flags
	elf = binary.LittleEndian.AppendUint16(elf, ehsize)
	elf = binary.LittleEndian.AppendUint16(elf, 0) // phentsize
	elf = binary.LittleEndian.AppendUint16(elf, 0) // phnum
	elf = binary.LittleEndian.AppendUint16(elf, shentsize)
	elf = binary.LittleEndian.AppendUint16(elf, 3) // shnum
	elf = binary.LittleEndian.AppendUint16(elf, 2) // shstrndx
	elf = append(elf, note...)
	shdr := func(name, typ uint32, offset, size uint64) []byte {
		b := make([]byte, 0, shentsize)
		b = binary.LittleEndian.AppendUint32(b, name)
		b = binary.LittleEndian.AppendUint32(b, typ)
		b = binary.LittleEndian.AppendUint64(b, 0) // flags
		b = binary.LittleEndian.AppendUint64(b, 0) // addr
		b = binary.LittleEndian.AppendUint64(b, offset)
		b = binary.LittleEndian.AppendUint64(b, size)
		b = binary.LittleEndian.AppendUint32(b, 0) // link
		b = binary.LittleEndian.AppendUint32(b, 0) // info
		b = binary.LittleEndian.AppendUint64(b, 1) // addralign
		b = binary.LittleEndian.AppendUint64(b, 0) // entsize
		return b
	}
	elf = append(elf, shdr(0, 0, 0, 0)...)                                  // SHT_NULL
	elf = append(elf, shdr(1, 7, uint64(ehsize), uint64(len(note)))...)     // .note.gnu.property
	elf = append(elf, shdr(20, 3, uint64(shstrOff), uint64(len(shstr)))...) // .shstrtab
	elf = append(elf, shstr...)

	path := filepath.Join(t.TempDir(), "synthetic.elf")
	if err := os.WriteFile(path, elf, 0o644); err != nil {
		t.Fatal(err)
	}
	return path
}

// TestCheckPathNoteTier verifies the ELF-note tier directly: a note declaring
// v3/v4 ISA bits is rejected, a baseline note is accepted. Without build info
// in the synthetic ELF, the note alone governs — covering the note-rejection
// path that the compiler-built fixtures cannot produce (gcc does not emit
// raised ISA notes for baseline C code).
func TestCheckPathNoteTier(t *testing.T) {
	t.Run("note with v3 bits rejected", func(t *testing.T) {
		ok, reason, err := checkPath(syntheticNoteELF(t, 1<<2, ".note.gnu.property")) // isaV3
		if err != nil {
			t.Fatalf("checkPath: %v", err)
		}
		if ok {
			t.Error("v3 ISA note must be rejected")
		}
		if !strings.Contains(reason, "GNU_PROPERTY") {
			t.Errorf("expected the ELF note to be named in the reason, got %q", reason)
		}
	})
	t.Run("baseline note accepted", func(t *testing.T) {
		ok, _, err := checkPath(syntheticNoteELF(t, 1, ".note.gnu.property")) // baseline
		if err != nil {
			t.Fatalf("checkPath: %v", err)
		}
		if !ok {
			t.Error("baseline ISA note must be accepted")
		}
	})
	t.Run("property found in a non-standard SHT_NOTE section", func(t *testing.T) {
		// No section named .note.gnu.property: the checker must search all
		// SHT_NOTE sections rather than only the first.
		ok, _, err := checkPath(syntheticNoteELF(t, 1<<2, ".some.other.note"))
		if err != nil {
			t.Fatalf("checkPath: %v", err)
		}
		if ok {
			t.Error("v3 ISA note in a non-standard SHT_NOTE section must be found and rejected")
		}
	})
	t.Run("malformed note sizes rejected without panic", func(t *testing.T) {
		// namesz near MaxUint32: uint32 padding arithmetic would wrap and
		// could panic the note parser (regression test for the int64 fix).
		path := syntheticNoteELF(t, 1, ".note.gnu.property")
		data, err := os.ReadFile(path)
		if err != nil {
			t.Fatal(err)
		}
		binary.LittleEndian.PutUint32(data[64:68], 0xFFFFFFFE) // namesz at note start
		if err := os.WriteFile(path, data, 0o644); err != nil {
			t.Fatal(err)
		}
		_, _, err = checkPath(path)
		if err == nil {
			t.Error("expected an error: no build info after malformed note is skipped")
		}
	})
}
