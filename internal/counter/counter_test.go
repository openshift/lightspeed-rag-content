package counter

import (
	"path/filepath"
	"testing"
)

func loadCounter(t *testing.T) TokenCounter {
	t.Helper()
	count, err := NewCL100KCounter(filepath.Join("..", "..", "testdata", "cl100k_base.tiktoken"))
	if err != nil {
		t.Fatalf("NewCL100KCounter: %v", err)
	}
	return count
}

// TestKnownCounts pins exact cl100k_base counts; these must match the
// llama_index tokenizer used for chunk budgeting.
func TestKnownCounts(t *testing.T) {
	count := loadCounter(t)
	cases := []struct {
		text   string
		tokens int
	}{
		{"hello world", 2},
		{"hello", 1},
		{"", 0},
		{"The quick brown fox jumps over the lazy dog.", 10},
	}
	for _, tc := range cases {
		if got := count(tc.text); got != tc.tokens {
			t.Errorf("count(%q) = %d, want %d", tc.text, got, tc.tokens)
		}
	}
}

// TestMetadataBudgetMatchesPython pins the metadata-string cost measured
// against the real Python pipeline (56 tokens for the canonical BYOK doc).
func TestMetadataBudgetMatchesPython(t *testing.T) {
	count := loadCounter(t)
	metadataStr := "filename: runbook-1.md\n" +
		"extension: .md\n" +
		"file_path: /markdown/runbook-1.md\n" +
		"title: Zyranex T7 OpenShift Runbook\n" +
		"docs_url: https://docs.quorbitex.example.com/openshift/zyranex-t7"
	if got := count(metadataStr); got != 56 {
		t.Errorf("metadata token count = %d, want 56 (python parity)", got)
	}
}

func TestMissingRanks(t *testing.T) {
	if _, err := NewCL100KCounter("/nonexistent/cl100k_base.tiktoken"); err == nil {
		t.Error("expected error for missing ranks file")
	}
}
