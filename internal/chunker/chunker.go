// Package chunker mirrors llama_index's SentenceSplitter: paragraph
// separator, punkt sentences, phrase regex and spaces, recursive on
// oversized pieces, greedy merge, verbatim text slices.
package chunker

import (
	_ "embed"
	"regexp"
	"strings"
	"sync"

	"github.com/neurosnap/sentences"

	"github.com/openshift/lightspeed-rag-content/internal/counter"
)

var phraseRegex = regexp.MustCompile(`[^,.;。？！]+[,.;。？！]?|[,.;。？！]`)

//go:embed english.json
var englishTraining []byte

var (
	punktOnce sync.Once
	punkt     *sentences.DefaultSentenceTokenizer
)

func punktTokenizer() *sentences.DefaultSentenceTokenizer {
	punktOnce.Do(func() {
		storage, err := sentences.LoadTraining(englishTraining)
		if err != nil {
			panic(err)
		}
		punkt = sentences.NewSentenceTokenizer(storage)
	})
	return punkt
}

// Chunk is one packed piece of a document: a verbatim, stripped text slice.
type Chunk struct {
	Text  string
	Start int
	End   int
}

// ChunkDocument splits text into chunks of at most chunkTokens tokens.
// Start/End are rune indices into text, matching llama_index's char offsets.
func ChunkDocument(text string, count counter.TokenCounter, chunkTokens int) []Chunk {
	pieces := splitRecursive(text, 0, len(text), count, chunkTokens)

	var chunks []Chunk
	curStart, curLen := -1, 0
	appendChunk := func(start, end int) {
		if c := buildChunk(text, start, end); c.Text != "" {
			chunks = append(chunks, c)
		}
	}
	for _, p := range pieces {
		n := count(text[p[0]:p[1]])
		if curStart >= 0 && curLen+n > chunkTokens {
			appendChunk(curStart, p[0])
			curStart, curLen = p[0], 0
		}
		if curStart < 0 {
			curStart = p[0]
		}
		curLen += n
	}
	if curStart >= 0 {
		appendChunk(curStart, len(text))
	}
	return chunks
}

// splitRecursive returns byte ranges tiling text[start:end], each within
// budget tokens, recursing llama_index-style through the split fn list.
func splitRecursive(text string, start, end int, count counter.TokenCounter, budget int) [][2]int {
	if count(text[start:end]) <= budget {
		return [][2]int{{start, end}}
	}
	pieces := getSplits(text[start:end])
	if len(pieces) <= 1 {
		// indivisible unit (e.g. a single huge token): keep oversized
		return [][2]int{{start, end}}
	}
	var out [][2]int
	for _, p := range pieces {
		abs := [2]int{start + p[0], start + p[1]}
		if count(text[abs[0]:abs[1]]) <= budget {
			out = append(out, abs)
			continue
		}
		out = append(out, splitRecursive(text, abs[0], abs[1], count, budget)...)
	}
	return out
}

// getSplits tries the split fns in order; ranges are relative to seg.
func getSplits(seg string) [][2]int {
	if pieces := splitBySep(seg, "\n\n\n"); len(pieces) > 1 {
		return pieces
	}
	if pieces := punktSplits(seg); len(pieces) > 1 {
		return pieces
	}
	if pieces := regexSplits(seg); len(pieces) > 1 {
		return pieces
	}
	if pieces := splitBySep(seg, " "); len(pieces) > 1 {
		return pieces
	}
	return [][2]int{{0, len(seg)}}
}

// splitBySep attaches the separator to the start of the following piece,
// matching llama_index's split_by_sep keep_separator="start".
func splitBySep(seg, sep string) [][2]int {
	var out [][2]int
	offset := 0
	for offset < len(seg) {
		idx := strings.Index(seg[offset:], sep)
		if idx < 0 {
			out = append(out, [2]int{offset, len(seg)})
			break
		}
		if idx > 0 {
			out = append(out, [2]int{offset, offset + idx})
		}
		pieceStart := offset + idx
		offset = pieceStart + len(sep)
		next := strings.Index(seg[offset:], sep)
		end := len(seg)
		if next >= 0 {
			end = offset + next
		}
		out = append(out, [2]int{pieceStart, end})
		offset = end
	}
	return out
}

func punktSplits(seg string) [][2]int {
	sents := punktTokenizer().Tokenize(seg)
	if len(sents) == 0 {
		return nil
	}
	var out [][2]int
	end := 0
	for _, s := range sents {
		start := end // bridge any whitespace the tokenizer skipped
		if s.Start > start {
			start = s.Start
		}
		if s.End <= start {
			continue
		}
		end = s.End
		out = append(out, [2]int{start, end})
	}
	if len(out) > 0 {
		out[len(out)-1][1] = len(seg) // trailing whitespace joins the last piece
	}
	return out
}

func regexSplits(seg string) [][2]int {
	matches := phraseRegex.FindAllStringIndex(seg, -1)
	if len(matches) == 0 {
		return nil
	}
	var out [][2]int
	end := 0
	for _, m := range matches {
		start := end
		if m[0] > start {
			start = m[0]
		}
		end = m[1]
		out = append(out, [2]int{start, end})
	}
	if len(out) > 0 {
		out[len(out)-1][1] = len(seg)
	}
	return out
}

func buildChunk(text string, start, end int) Chunk {
	if start >= end {
		return Chunk{}
	}
	slice := strings.TrimSpace(text[start:end])
	if slice == "" {
		return Chunk{}
	}
	// byte offset of the trimmed slice inside text, for llama_index-style
	// char indices
	lead := start + strings.Index(text[start:end], slice)
	return Chunk{
		Text:  slice,
		Start: len([]rune(text[:lead])),
		End:   len([]rune(text[:lead])) + len([]rune(slice)),
	}
}
