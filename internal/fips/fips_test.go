package fips

import (
	"bytes"
	"errors"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

// TestEvaluateFIPSState covers the startup decision table, including the
// fail-closed combinations. The inputs are injected, so no FIPS-enabled host
// or process-wide GODEBUG changes are needed.
func TestEvaluateFIPSState(t *testing.T) {
	readErr := errors.New("simulated read failure")
	cases := []struct {
		name     string
		hostFIPS bool
		hostErr  error
		module   bool
		want     Action
	}{
		{"FIPS host with module active continues", true, nil, true, Continue},
		{"FIPS host with module disabled refuses startup", true, nil, false, Refuse},
		{"non-FIPS host with module active continues", false, nil, true, Continue},
		{"non-FIPS host with module disabled continues", false, nil, false, Continue},
		{"unreadable host state with module active continues", false, readErr, true, ContinueUnverifiedHost},
		{"unreadable host state with module disabled refuses startup", false, readErr, false, Refuse},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			action, msg := Evaluate(tc.hostFIPS, tc.hostErr, tc.module)
			if action != tc.want {
				t.Errorf("Evaluate(%v, %v, %v) action = %v, want %v",
					tc.hostFIPS, tc.hostErr, tc.module, action, tc.want)
			}
			if msg == "" {
				t.Error("expected a non-empty log message")
			}
		})
	}
}

// TestReportFIPSState preserves read-error diagnostics on refusal and continuation.
func TestReportFIPSState(t *testing.T) {
	readErr := errors.New("permission denied reading host state")
	for _, tc := range []struct {
		name         string
		host, module bool
		err          error
		want         Action
	}{
		{"unreadable host refuses", false, false, readErr, Refuse},
		{"disabled module refuses", true, false, nil, Refuse},
		{"unreadable host continues", false, true, readErr, ContinueUnverifiedHost},
		{"enabled module continues", true, true, nil, Continue},
	} {
		t.Run(tc.name, func(t *testing.T) {
			var out bytes.Buffer
			if got := ReportState(&out, tc.host, tc.err, tc.module); got != tc.want {
				t.Fatalf("action = %v, want %v", got, tc.want)
			}
			if strings.Contains(out.String(), readErr.Error()) != (tc.err != nil) {
				t.Errorf("unexpected read-error diagnostic: %q", out.String())
			}
			if strings.Contains(out.String(), "<nil>") {
				t.Errorf("nil error must not be logged: %q", out.String())
			}
		})
	}
}

// TestReadHostFIPSMode covers the host-state file reader: content parsing,
// trimming, the missing-file-is-not-an-error rule, and read failures.
func TestReadHostFIPSMode(t *testing.T) {
	dir := t.TempDir()
	write := func(name, content string) string {
		t.Helper()
		path := filepath.Join(dir, name)
		if err := os.WriteFile(path, []byte(content), 0o644); err != nil {
			t.Fatal(err)
		}
		return path
	}

	cases := []struct {
		name    string
		content string
		want    bool
	}{
		{"enabled", "1\n", true},
		{"enabled with whitespace", " 1 ", true},
		{"disabled", "0\n", false},
		{"garbage content means disabled", "garbage\n", false},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			got, err := ReadHostFIPSMode(write(tc.name, tc.content))
			if err != nil {
				t.Fatalf("readHostFIPSMode: %v", err)
			}
			if got != tc.want {
				t.Errorf("ReadHostFIPSMode(%q) = %v, want %v", tc.content, got, tc.want)
			}
		})
	}

	t.Run("missing file means non-FIPS host, not an error", func(t *testing.T) {
		got, err := ReadHostFIPSMode(filepath.Join(dir, "does-not-exist"))
		if err != nil {
			t.Fatalf("expected nil error for missing file, got %v", err)
		}
		if got {
			t.Error("missing file must not report FIPS enabled")
		}
	})

	t.Run("unreadable path returns an error", func(t *testing.T) {
		// A directory cannot be read as a file: exercises the error path
		// that must fail closed when the module is disabled.
		if _, err := ReadHostFIPSMode(dir); err == nil {
			t.Error("expected an error reading a directory as the FIPS-state file")
		}
	})
}
