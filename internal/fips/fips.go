// Package fips provides the startup FIPS-state decision for byok-go.
//
// The decision logic lives in this pure-Go package (not the CGo-importing
// cmd/byok-go package) so it runs under the repo's pure-Go test target.
package fips

import (
	"errors"
	"fmt"
	"io"
	"io/fs"
	"os"
	"strings"
)

// Action is the startup decision for the FIPS state check.
type Action int

const (
	// Continue: FIPS state is acceptable; log the status and start.
	Continue Action = iota
	// ContinueUnverifiedHost: the host FIPS state is unreadable but the Go
	// FIPS module is active; log the read failure and start.
	ContinueUnverifiedHost
	// Refuse: refuse to start (a FIPS-required host would run without
	// FIPS-approved crypto).
	Refuse
)

// DefaultHostFIPSStatePath is where the kernel exposes the host FIPS state.
const DefaultHostFIPSStatePath = "/proc/sys/crypto/fips_enabled"

// Evaluate maps the host FIPS state and the Go FIPS module state to a
// startup action. It is a pure function so the startup decision is
// unit-testable without a FIPS-enabled host or process-wide GODEBUG changes.
func Evaluate(hostFIPSEnabled bool, hostStateErr error, moduleEnabled bool) (Action, string) {
	switch {
	case hostStateErr != nil && moduleEnabled:
		// Unexpected read failure (a missing file means the kernel has no
		// FIPS support and is not an error — ReadHostFIPSMode returns nil
		// for that). FIPS-approved crypto is in use regardless of host
		// state, so log and continue.
		return ContinueUnverifiedHost, "cannot read host FIPS state; Go FIPS module is active, continuing"
	case hostStateErr != nil:
		// Host state unknown and the module is off: a FIPS-enabled host
		// cannot be ruled out — fail closed.
		return Refuse, "cannot read host FIPS state and the Go FIPS 140 crypto module is not enabled; refusing to start"
	case hostFIPSEnabled && !moduleEnabled:
		// The binary must not run in FIPS mode without the FIPS crypto
		// module active; refuse to start rather than use non-approved
		// algorithms on a FIPS-enabled cluster.
		return Refuse, "host is in FIPS mode but the Go FIPS 140 crypto module is not enabled; check the GODEBUG=fips140 setting"
	case hostFIPSEnabled:
		return Continue, "FIPS mode active: Go native FIPS 140-3 crypto provider enabled"
	case moduleEnabled:
		// Normal on non-FIPS hosts: the //go:debug fips140=on default keeps
		// the module active even when the host does not require FIPS.
		return Continue, "FIPS-approved crypto active (Go FIPS module enabled by default); host is not FIPS-enabled"
	default:
		return Continue, "Go FIPS 140 crypto module is not enabled (GODEBUG override); host is not FIPS-enabled"
	}
}

// ReportState writes the startup decision and returns it to the process-exit wrapper.
func ReportState(out io.Writer, hostFIPSEnabled bool, err error, moduleEnabled bool) Action {
	action, msg := Evaluate(hostFIPSEnabled, err, moduleEnabled)
	if err != nil {
		_, _ = fmt.Fprintln(out, msg+":", err)
	} else {
		_, _ = fmt.Fprintln(out, msg)
	}
	return action
}

// ReadHostFIPSMode reports whether the host OS at the given path is in FIPS
// mode. A missing file means the kernel has no FIPS support: the host is
// treated as non-FIPS-enabled and no error is returned.
func ReadHostFIPSMode(path string) (bool, error) {
	b, err := os.ReadFile(path)
	if errors.Is(err, fs.ErrNotExist) {
		return false, nil
	}
	if err != nil {
		return false, fmt.Errorf("reading %s: %w", path, err)
	}
	return strings.TrimSpace(string(b)) == "1", nil
}
