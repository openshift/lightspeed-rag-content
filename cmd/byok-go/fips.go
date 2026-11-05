// FIPS 140-3 support for byok-go.
//
// The tool's Go crypto usage (crypto/sha256 for chunk hashing in
// internal/assemble and internal/persist, crypto/rand for ID generation in
// internal/persist) is covered by Go's native FIPS 140-3 crypto provider.
// The required CGo (faiss, onnxruntime) is not crypto-related and is
// unaffected by FIPS mode; the runtime image contains no OpenSSL.
//
// The decision logic lives in internal/fips (pure Go) so it runs under the
// repo's pure-Go test target; this file keeps the compiled-in GODEBUG
// default and wires the decision to process exit.

// The go:debug directive sets fips140=on as the binary's default GODEBUG
// setting: the Go native FIPS 140-3 crypto module is always active. An
// explicit GODEBUG=fips140=off environment override can still disable it,
// which the startup assertion below guards against on FIPS-enabled hosts.
//
//go:debug fips140=on

package main

import (
	"crypto/fips140"
	"os"

	"github.com/openshift/lightspeed-rag-content/internal/fips"
)

// checkFIPSMode verifies that the Go native FIPS 140-3 crypto provider is
// active when the host OS is in FIPS mode, and refuses startup otherwise.
func checkFIPSMode() {
	hostFIPSEnabled, err := fips.ReadHostFIPSMode(fips.DefaultHostFIPSStatePath)
	if fips.ReportState(os.Stderr, hostFIPSEnabled, err, fips140.Enabled()) == fips.Refuse {
		os.Exit(1)
	}
}
