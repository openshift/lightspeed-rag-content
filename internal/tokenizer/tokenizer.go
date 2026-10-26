package tokenizer

// Pure-Go WordPiece tokenizer matching the HF tokenizers configuration in
// embeddings_model/tokenizer.json: BertNormalizer (lowercase, clean text,
// Chinese chars, accent stripping), BertPreTokenizer (whitespace + punctuation
// isolation), WordPiece greedy matching, and RoBERTa-style <s>/</s> wrapping.

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"unicode"

	"golang.org/x/text/unicode/norm"
)

const (
	tokenCLS = 0 // <s>
	tokenSEP = 2 // </s>
)

// Tokenizer holds the WordPiece vocabulary loaded from tokenizer.json.
type Tokenizer struct {
	vocab        map[string]int
	unkID        int
	maxWordChars int
}

type tokenizerJSON struct {
	Model struct {
		Vocab                map[string]int `json:"vocab"`
		UnkToken             string         `json:"unk_token"`
		MaxInputCharsPerWord int            `json:"max_input_chars_per_word"`
	} `json:"model"`
}

// LoadTokenizer reads a HF tokenizers tokenizer.json file.
func LoadTokenizer(path string) (*Tokenizer, error) {
	raw, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var parsed tokenizerJSON
	if err := json.Unmarshal(raw, &parsed); err != nil {
		return nil, err
	}
	if len(parsed.Model.Vocab) == 0 {
		return nil, fmt.Errorf("empty vocab in %s", path)
	}
	maxChars := parsed.Model.MaxInputCharsPerWord
	if maxChars == 0 {
		maxChars = 100
	}
	return &Tokenizer{
		vocab:        parsed.Model.Vocab,
		unkID:        parsed.Model.Vocab[parsed.Model.UnkToken],
		maxWordChars: maxChars,
	}, nil
}

// Tokenize returns the model input ids for one text, wrapped in <s> ... </s>.
func (t *Tokenizer) Tokenize(text string) []int {
	ids := make([]int, 0, 64)
	ids = append(ids, tokenCLS)
	for _, word := range bertPreTokenize(bertNormalize(text)) {
		ids = append(ids, t.wordPiece(word)...)
	}
	ids = append(ids, tokenSEP)
	return ids
}

func (t *Tokenizer) wordPiece(word string) []int {
	if len(word) > t.maxWordChars {
		return []int{t.unkID}
	}
	runes := []rune(word)
	var ids []int
	start := 0
	for start < len(runes) {
		end := len(runes)
		var match int
		found := false
		for end > start {
			piece := string(runes[start:end])
			if start > 0 {
				piece = "##" + piece
			}
			if id, ok := t.vocab[piece]; ok {
				match = id
				found = true
				break
			}
			end--
		}
		if !found {
			return []int{t.unkID}
		}
		ids = append(ids, match)
		start = end
	}
	return ids
}

// bertNormalize mirrors HF BertNormalizer with clean_text=true,
// handle_chinese_chars=true, lowercase=true (accents stripped when lowercasing).
func bertNormalize(text string) string {
	var b strings.Builder
	b.Grow(len(text))
	for _, r := range text {
		switch {
		case r == 0 || r == 0xFFFD:
			continue
		case r < 0x20 && r != '\t' && r != '\n' && r != '\r':
			continue
		case r == 0x7F:
			continue
		case r == '\t' || r == '\n' || r == '\r':
			b.WriteRune(' ')
		case r > 0x2E80 && r < 0xA000: // CJK ranges: add spaces around
			b.WriteRune(' ')
			b.WriteRune(unicode.ToLower(r))
			b.WriteRune(' ')
		default:
			b.WriteRune(unicode.ToLower(r))
		}
	}
	return stripAccents(b.String())
}

func stripAccents(s string) string {
	var b strings.Builder
	b.Grow(len(s))
	for _, r := range norm.NFD.String(s) {
		if unicode.Is(unicode.Mn, r) {
			continue
		}
		b.WriteRune(r)
	}
	return b.String()
}

// bertPreTokenize mirrors HF BertPreTokenizer: split on unicode whitespace,
// then isolate punctuation characters within each word.
func bertPreTokenize(text string) []string {
	var out []string
	for _, word := range strings.Fields(text) {
		var current strings.Builder
		flush := func() {
			if current.Len() > 0 {
				out = append(out, current.String())
				current.Reset()
			}
		}
		for _, r := range word {
			if isBertPunct(r) {
				flush()
				out = append(out, string(r))
			} else {
				current.WriteRune(r)
			}
		}
		flush()
	}
	return out
}

func isBertPunct(r rune) bool {
	if r < 128 {
		return (r >= 33 && r <= 47) || (r >= 58 && r <= 64) ||
			(r >= 91 && r <= 96) || (r >= 123 && r <= 126)
	}
	return unicode.IsPunct(r)
}
