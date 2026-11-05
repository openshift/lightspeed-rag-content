// FIPS 140-3 support for byok-go.
//
// The tool's Go crypto usage (crypto/sha256 for chunk hashing in
// internal/assemble and internal/persist, crypto/rand for ID generation in
// internal/persist) is covered by Go's native FIPS 140-3 crypto provider.
// The required CGo (faiss, onnxruntime) is not crypto-related and is
// unaffected by FIPS mode; the runtime image contains no OpenSSL.

// The go:debug directive sets fips140=on as the binary's default GODEBUG
// setting: the Go native FIPS 140-3 crypto module is always active. An
// explicit GODEBUG=fips140=off environment override can still disable it,
// which the startup assertion below guards against on FIPS-enabled hosts.
//
//go:debug fips140=on

package main

import (
	"crypto/fips140"
	"errors"
	"fmt"
	"io/fs"
	"os"
	"strings"
)

// checkFIPSMode verifies that the Go native FIPS 140-3 crypto provider is
// active when the host OS is in FIPS mode. It aborts startup if the host
// requires FIPS but the binary's crypto module is not enabled (e.g. GODEBUG
// was explicitly set to fips140=off).
func checkFIPSMode() {
	hostFIPSEnabled, err := hostFIPSMode()
	if err != nil {
		// Unexpected read failure (a missing file means the kernel has no
		// FIPS support and is not an error). The host FIPS state is unknown:
		// if the FIPS module is active, FIPS-approved crypto is in use
		// regardless of host state, so log and continue; otherwise a
		// FIPS-enabled host cannot be ruled out — fail closed.
		if fips140.Enabled() {
			fmt.Fprintln(os.Stderr, "cannot read host FIPS state; Go FIPS module is active, continuing:", err)
		} else {
			fmt.Fprintln(os.Stderr, "cannot read host FIPS state and the Go FIPS 140 crypto module is not enabled; refusing to start:", err)
			os.Exit(1)
		}
	}
	switch {
	case hostFIPSEnabled && !fips140.Enabled():
		fmt.Fprintln(os.Stderr, "host is in FIPS mode but the Go FIPS 140 crypto module is not enabled; check the GODEBUG=fips140 setting")
		os.Exit(1)
	case hostFIPSEnabled:
		fmt.Fprintln(os.Stderr, "FIPS mode active: Go native FIPS 140-3 crypto provider enabled")
	case fips140.Enabled():
		// Normal on non-FIPS hosts: the //go:debug fips140=on default keeps
		// the module active even when the host does not require FIPS.
		fmt.Fprintln(os.Stderr, "FIPS-approved crypto active (Go FIPS module enabled by default); host is not FIPS-enabled")
	default:
		fmt.Fprintln(os.Stderr, "Go FIPS 140 crypto module is not enabled (GODEBUG override); host is not FIPS-enabled")
	}
}

// hostFIPSMode reports whether the host OS is in FIPS mode, as indicated by
// /proc/sys/crypto/fips_enabled (the same source the Go runtime consults).
func hostFIPSMode() (bool, error) {
	b, err := os.ReadFile("/proc/sys/crypto/fips_enabled")
	if errors.Is(err, fs.ErrNotExist) {
		// The kernel has no FIPS support: the host is not FIPS-enabled.
		return false, nil
	}
	if err != nil {
		return false, fmt.Errorf("reading /proc/sys/crypto/fips_enabled: %w", err)
	}
	return strings.TrimSpace(string(b)) == "1", nil
}
