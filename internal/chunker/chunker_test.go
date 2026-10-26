package chunker

import (
	"path/filepath"
	"strings"
	"testing"

	"github.com/openshift/lightspeed-rag-content/internal/counter"
)

func loadCounter(t *testing.T) counter.TokenCounter {
	t.Helper()
	count, err := counter.NewCL100KCounter(filepath.Join("..", "..", "testdata", "cl100k_base.tiktoken"))
	if err != nil {
		t.Fatalf("NewCL100KCounter: %v", err)
	}
	return count
}

// TestBudgetRespected checks that no chunk exceeds the budget, including a
// code block with no sentence punctuation (regression: chunks of 555 tokens).
func TestBudgetRespected(t *testing.T) {
	count := loadCounter(t)
	text := "Intro sentence. " +
		strings.Repeat("```terminal\n$ kubectl get nodes\nNAME STATUS\n```\n", 60) +
		"Trailing sentence."
	chunks := ChunkDocument(text, count, 380)
	if len(chunks) == 0 {
		t.Fatal("no chunks produced")
	}
	for _, c := range chunks {
		if n := count(c.Text); n > 380 {
			t.Errorf("chunk of %d tokens exceeds budget (start=%d): %q", n, c.Start, c.Text[:60])
		}
	}
}

// TestUnsplittableTokenStaysOverbudget mirrors llama_index: an indivisible
// unit larger than the budget is kept as an oversized split.
func TestUnsplittableTokenStaysOverbudget(t *testing.T) {
	count := loadCounter(t)
	chunks := ChunkDocument(strings.Repeat("x", 4000), count, 380)
	if len(chunks) != 1 {
		t.Fatalf("expected 1 indivisible chunk, got %d", len(chunks))
	}
	if n := count(chunks[0].Text); n < 380 {
		t.Errorf("unsplittable token lost content: %d tokens", n)
	}
}

// TestContentTiling checks that chunks tile the source verbatim
// (whitespace-normalized), so no content is lost or duplicated.
func TestContentTiling(t *testing.T) {
	count := loadCounter(t)
	text := "# Heading\n\nFirst paragraph has sentences. Several of them! Really?\n\n\n" +
		"```terminal\n$ oc get clusteroperators\n```\n\n\n" +
		"Dr. Smith validated v1.2. It works, e.g. for upgrades. " +
		strings.Repeat("A sentence about clusters. ", 80)
	norm := func(s string) string {
		return strings.Join(strings.Fields(s), "")
	}
	chunks := ChunkDocument(text, count, 380)
	var joined strings.Builder
	for _, c := range chunks {
		joined.WriteString(c.Text)
	}
	if norm(joined.String()) != norm(text) {
		t.Error("chunks do not tile the source content")
	}
}

// TestOffsetsAreRuneIndices checks the char-offset contract used by
// llama_index nodes.
func TestOffsetsAreRuneIndices(t *testing.T) {
	count := loadCounter(t)
	text := "Grüße aus München. " + strings.Repeat("Second sentence here. ", 60)
	chunks := ChunkDocument(text, count, 380)
	for _, c := range chunks {
		if c.Start < 0 || c.End > len([]rune(text)) || c.Start >= c.End {
			t.Fatalf("invalid offsets [%d,%d) for text of %d runes", c.Start, c.End, len([]rune(text)))
		}
		runes := []rune(text)
		slice := string(runes[c.Start:c.End])
		if strings.TrimSpace(slice) != c.Text {
			t.Errorf("offsets do not point at the chunk text: %q vs %q", slice, c.Text)
		}
	}
}

// TestPunktAbbreviations checks that punkt data is active: titles like
// "Dr." do not split sentences.
func TestPunktAbbreviations(t *testing.T) {
	splits := punktSplits("Dr. Smith validated v1.2. It works.")
	// "Dr. Smith validated v1.2." must stay one sentence
	found := false
	for _, s := range splits {
		if strings.Contains(string([]rune("Dr. Smith validated v1.2. It works.")[s[0]:s[1]]), "Dr. Smith") {
			found = true
		}
	}
	if !found {
		t.Errorf("punkt did not keep 'Dr. Smith' together: %v", splits)
	}
}

// TestDeterministicChunks pins run-to-run determinism.
func TestDeterministicChunks(t *testing.T) {
	count := loadCounter(t)
	text := "One. Two. Three. " + strings.Repeat("Filler sentence for packing. ", 100)
	first := ChunkDocument(text, count, 380)
	second := ChunkDocument(text, count, 380)
	if len(first) != len(second) {
		t.Fatalf("chunk count differs between runs: %d vs %d", len(first), len(second))
	}
	for i := range first {
		if first[i] != second[i] {
			t.Errorf("chunk %d differs between runs", i)
		}
	}
}

// TestSeparatorAttachmentToNextPiece pins llama_index's keep_separator=start
// convention for the paragraph separator.
func TestSeparatorAttachmentToNextPiece(t *testing.T) {
	pieces := splitBySep("aaa\n\n\nbbb\n\n\nccc", "\n\n\n")
	var texts []string
	for _, p := range pieces {
		texts = append(texts, "aaa\n\n\nbbb\n\n\nccc"[p[0]:p[1]])
	}
	if len(texts) != 3 || texts[0] != "aaa" {
		t.Fatalf("unexpected pieces: %v", texts)
	}
	if !strings.HasPrefix(texts[1], "\n\n\n") {
		t.Errorf("separator must attach to the next piece: %q", texts[1])
	}
}
