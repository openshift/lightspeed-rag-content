package tokenizer

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"testing"
)

const testdata = "../../testdata"

type referenceJSON struct {
	Texts         []string `json:"texts"`
	InputIDs      [][]int  `json:"input_ids"`
	AttentionMask [][]int  `json:"attention_mask"`
}

func loadTokenizer(t *testing.T) *Tokenizer {
	t.Helper()
	tok, err := LoadTokenizer(filepath.Join(testdata, "tokenizer.json"))
	if err != nil {
		t.Fatalf("LoadTokenizer: %v", err)
	}
	return tok
}

// TestParityWithPython matches token ids produced by the Python (transformers)
// tokenizer for the reference texts, including umlauts, punctuation and a
// long text.
func TestParityWithPython(t *testing.T) {
	raw, err := os.ReadFile(filepath.Join(testdata, "reference.json"))
	if err != nil {
		t.Fatalf("read reference: %v", err)
	}
	var ref referenceJSON
	if err := json.Unmarshal(raw, &ref); err != nil {
		t.Fatalf("parse reference: %v", err)
	}
	tok := loadTokenizer(t)
	for i, text := range ref.Texts {
		want := make([]int, 0, len(ref.InputIDs[i]))
		for j, id := range ref.InputIDs[i] {
			if ref.AttentionMask[i][j] == 1 {
				want = append(want, id)
			}
		}
		got := tok.Tokenize(text)
		if fmt.Sprint(got) != fmt.Sprint(want) {
			t.Errorf("text %d (%q): got %v, want %v", i, text[:min(40, len(text))], got, want)
		}
	}
}

func TestSpecialTokenWrapping(t *testing.T) {
	tok := loadTokenizer(t)
	ids := tok.Tokenize("hello")
	if len(ids) < 3 || ids[0] != tokenCLS || ids[len(ids)-1] != tokenSEP {
		t.Errorf("expected <s> ... </s> wrapping, got %v", ids)
	}
}

func TestEmptyText(t *testing.T) {
	tok := loadTokenizer(t)
	ids := tok.Tokenize("")
	if len(ids) != 2 || ids[0] != tokenCLS || ids[1] != tokenSEP {
		t.Errorf("empty text should yield exactly the special tokens, got %v", ids)
	}
}

func TestUnknownWord(t *testing.T) {
	tok := loadTokenizer(t)
	// a word with no vocabulary pieces maps to [UNK]
	ids := tok.Tokenize("⍨⍨⍨⍨")
	if len(ids) != 3 || ids[1] != tok.unkID {
		t.Errorf("expected [<s>, UNK, </s>], got %v", ids)
	}
}

func TestDeterministic(t *testing.T) {
	tok := loadTokenizer(t)
	text := "Deterministic output for identical input."
	if fmt.Sprint(tok.Tokenize(text)) != fmt.Sprint(tok.Tokenize(text)) {
		t.Error("tokenization is not deterministic")
	}
}
