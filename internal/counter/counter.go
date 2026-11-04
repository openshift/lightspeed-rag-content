// Package counter provides cl100k_base token counting, matching
// llama_index's default chunking tokenizer.
package counter

import (
	"encoding/base64"
	"fmt"
	"os"
	"strconv"
	"strings"

	"github.com/pkoukk/tiktoken-go"
)

// TokenCounter counts tokens for chunk budgeting.
type TokenCounter func(string) int

type ranksLoader struct{ path string }

// LoadTiktokenBpe implements tiktoken's BpeLoader from an explicit file.
func (l ranksLoader) LoadTiktokenBpe(string) (map[string]int, error) {
	data, err := os.ReadFile(l.path)
	if err != nil {
		return nil, err
	}
	vocab := make(map[string]int)
	for _, line := range strings.Split(string(data), "\n") {
		if line == "" {
			continue
		}
		parts := strings.Split(line, " ")
		if len(parts) != 2 {
			return nil, fmt.Errorf("malformed ranks line: %q", line)
		}
		token, err := base64.StdEncoding.DecodeString(parts[0])
		if err != nil {
			return nil, err
		}
		id, err := strconv.Atoi(parts[1])
		if err != nil {
			return nil, err
		}
		vocab[string(token)] = id
	}
	return vocab, nil
}

// NewCL100KCounter loads cl100k_base BPE ranks from an explicit file
// (the tiktoken cl100k_base.tiktoken format).
func NewCL100KCounter(ranksPath string) (TokenCounter, error) {
	if _, err := os.Stat(ranksPath); err != nil {
		return nil, fmt.Errorf("cl100k ranks not found: %w", err)
	}
	tiktoken.SetBpeLoader(ranksLoader{path: ranksPath})
	encoding, err := tiktoken.GetEncoding("cl100k_base")
	if err != nil {
		return nil, err
	}
	return func(s string) int { return len(encoding.Encode(s, []string{"all"}, nil)) }, nil
}
