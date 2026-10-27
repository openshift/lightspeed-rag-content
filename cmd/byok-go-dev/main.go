// Development helpers for the byok-go tool: chunk dumps for parity
// measurements and single-text query embeddings for validation harnesses.
// Not shipped in the container image.
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"

	"github.com/openshift/lightspeed-rag-content/internal/chunker"
	"github.com/openshift/lightspeed-rag-content/internal/counter"
	"github.com/openshift/lightspeed-rag-content/internal/docparse"
	"github.com/openshift/lightspeed-rag-content/internal/embed"
	"github.com/openshift/lightspeed-rag-content/internal/tokenizer"
)

const chunkTokens = 380

type dumpedChunk struct {
	Text  string `json:"text"`
	Start int    `json:"start"`
	End   int    `json:"end"`
}

type dumpedFile struct {
	Path   string        `json:"path"`
	Title  string        `json:"title"`
	Chunks []dumpedChunk `json:"chunks"`
}

func main() {
	inputDir := flag.String("i", "", "input directory with markdown content")
	modelDir := flag.String("model", "", "directory with mpnet.onnx and tokenizer.json")
	dumpChunks := flag.String("dump-chunks", "", "write chunks as JSON and exit")
	embedText := flag.String("embed-text", "", "print the embedding of a text as JSON and exit")
	flag.Parse()

	if *dumpChunks != "" {
		if err := dumpChunksJSON(*inputDir, *modelDir, *dumpChunks); err != nil {
			fmt.Fprintln(os.Stderr, "ERROR:", err)
			os.Exit(1)
		}
		return
	}
	if *embedText != "" {
		tok, err := tokenizer.LoadTokenizer(filepath.Join(*modelDir, "tokenizer.json"))
		if err != nil {
			fmt.Fprintln(os.Stderr, "ERROR:", err)
			os.Exit(1)
		}
		embedder, err := embed.NewEmbedder(filepath.Join(*modelDir, "mpnet.onnx"), tok, 768, 384, 4)
		if err != nil {
			fmt.Fprintln(os.Stderr, "ERROR:", err)
			os.Exit(1)
		}
		vector, err := embedder.Embed(*embedText)
		if err != nil {
			fmt.Fprintln(os.Stderr, "ERROR:", err)
			os.Exit(1)
		}
		raw, _ := json.Marshal(vector)
		fmt.Println(string(raw))
		return
	}
	fmt.Fprintln(os.Stderr, "usage: byok-go-dev -dump-chunks <out.json> -i <dir> -model <dir> | -embed-text <text> -model <dir>")
	os.Exit(2)
}

func dumpChunksJSON(inputDir, modelDir, dest string) error {
	docs, err := docparse.LoadDocuments(inputDir)
	if err != nil {
		return err
	}
	count, err := counter.NewCL100KCounter(filepath.Join(modelDir, "cl100k_base.tiktoken"))
	if err != nil {
		return err
	}
	out := make([]dumpedFile, 0, len(docs))
	for _, doc := range docs {
		file := dumpedFile{Path: doc.FilePath, Title: doc.Title}
		effective := chunkTokens - count(doc.MetadataStr())
		for _, c := range chunker.ChunkDocument(doc.Text, count, effective) {
			file.Chunks = append(file.Chunks, dumpedChunk{Text: c.Text, Start: c.Start, End: c.End})
		}
		out = append(out, file)
	}
	raw, err := json.MarshalIndent(out, "", " ")
	if err != nil {
		return err
	}
	return os.WriteFile(dest, raw, 0o644)
}
