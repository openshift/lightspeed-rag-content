// FIPS 140-3 support for byok-go.
//
// The tool's Go crypto usage (crypto/sha256 for chunk hashing in
// internal/assemble and internal/persist, crypto/rand for ID generation in
// internal/persist) is covered by Go's native FIPS 140-3 crypto provider.
// The required CGo (faiss, onnxruntime) is not crypto-related and is
// unaffected by FIPS mode; the runtime image contains no OpenSSL.
package main

import (
	"crypto/fips140"
	"fmt"
	"os"
	"strings"
)

// The go:debug directive sets fips140=on as the binary's default GODEBUG
// setting: the Go native FIPS 140-3 crypto module is always active. An
// explicit GODEBUG=fips140=off environment override can still disable it,
// which the startup assertion below guards against on FIPS-enabled hosts.
//
//go:debug fips140=on

// checkFIPSMode verifies that the Go native FIPS 140-3 crypto provider is
// active when the host OS is in FIPS mode. It aborts startup if the host
// requires FIPS but the binary's crypto module is not enabled (e.g. GODEBUG
// was explicitly set to fips140=off).
func checkFIPSMode() {
	hostFIPSEnabled := hostFIPSMode()
	switch {
	case hostFIPSEnabled && !fips140.Enabled():
		fmt.Fprintln(os.Stderr, "host is in FIPS mode but the Go FIPS 140 crypto module is not enabled; check the GODEBUG=fips140 setting")
		os.Exit(1)
	case hostFIPSEnabled:
		fmt.Fprintln(os.Stderr, "FIPS mode active: Go native FIPS 140-3 crypto provider enabled")
	default:
		fmt.Fprintln(os.Stderr, "FIPS mode inactive: host is not FIPS-enabled")
	}
}

// hostFIPSMode reports whether the host OS is in FIPS mode, as indicated by
// /proc/sys/crypto/fips_enabled (the same source the Go runtime consults).
func hostFIPSMode() bool {
	b, err := os.ReadFile("/proc/sys/crypto/fips_enabled")
	if err != nil {
		return false
	}
	return strings.TrimSpace(string(b)) == "1"
}
