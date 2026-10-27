// BYOK RAG generator, Go port: markdown -> chunks -> mpnet embeddings (ONNX)
// -> FAISS IndexFlatIP -> llama_index persist format -> docker-archive.
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/openshift/lightspeed-rag-content/internal/assemble"
	"github.com/openshift/lightspeed-rag-content/internal/chunker"
	"github.com/openshift/lightspeed-rag-content/internal/counter"
	"github.com/openshift/lightspeed-rag-content/internal/docparse"
	"github.com/openshift/lightspeed-rag-content/internal/embed"
	"github.com/openshift/lightspeed-rag-content/internal/faissidx"
	"github.com/openshift/lightspeed-rag-content/internal/persist"
	"github.com/openshift/lightspeed-rag-content/internal/tokenizer"
)

const (
	embeddingDim   = 768
	chunkTokens    = 380
	chunkOverlap   = 0
	modelName      = "sentence-transformers/all-mpnet-base-v2"
	defaultThreads = 4
	defaultMaxSeq  = 384
)

// maxSeqLength reads the model's sentence_bert_config.json (default 384).
func maxSeqLength(modelDir string) int {
	raw, err := os.ReadFile(filepath.Join(modelDir, "sentence_bert_config.json"))
	if err != nil {
		return defaultMaxSeq
	}
	var config struct {
		MaxSeqLength int `json:"max_seq_length"`
	}
	if err := json.Unmarshal(raw, &config); err != nil || config.MaxSeqLength <= 0 {
		return defaultMaxSeq
	}
	return config.MaxSeqLength
}

func main() {
	inputDir := flag.String("i", "/markdown", "input directory with markdown content")
	outTar := flag.String("o", "", "output docker-archive path (default /output/$OUT_IMAGE_TAG.tar)")
	tag := flag.String("tag", os.Getenv("OUT_IMAGE_TAG"), "repository tag for the output image (default byok-image)")
	indexID := flag.String("id", os.Getenv("VECTOR_DB_INDEX"), "index id (default vector_db_index)")
	modelDir := flag.String("model", "/opt/byok", "directory with mpnet.onnx and tokenizer.json")
	baseLayer := flag.String("base-layer", "/opt/byok/base-layer.tar", "baked output base layer")
	threads := flag.Int("threads", defaultThreads, "onnxruntime intra-op threads")
	flag.Parse()

	start := time.Now()

	if *tag == "" {
		*tag = "byok-image"
	}
	if *indexID == "" {
		*indexID = "vector_db_index"
	}
	if *outTar == "" {
		*outTar = filepath.Join("/output", *tag+".tar")
	}

	tok, err := tokenizer.LoadTokenizer(filepath.Join(*modelDir, "tokenizer.json"))
	if err != nil {
		fatal(err)
	}
	embedder, err := embed.NewEmbedder(filepath.Join(*modelDir, "mpnet.onnx"), tok, embeddingDim, maxSeqLength(*modelDir), *threads)
	if err != nil {
		fatal(err)
	}
	if bs := os.Getenv("BYOK_GO_BATCH"); bs != "" {
		var size int
		if _, err := fmt.Sscanf(bs, "%d", &size); err == nil && size > 0 {
			embedder.BatchSize = size
		}
	}
	if err != nil {
		fatal(err)
	}
	cl100k, err := counter.NewCL100KCounter(filepath.Join(*modelDir, "cl100k_base.tiktoken"))
	if err != nil {
		fatal(err)
	}

	docs, err := docparse.LoadDocuments(*inputDir)
	if err != nil {
		fatal(err)
	}

	// phase 1: chunk every document
	var nodes []persist.Node
	var texts []string
	for _, doc := range docs {
		fmt.Printf("file_path: %s, title: %s, docs_url: %s\n", doc.FilePath, doc.Title, doc.DocsURL)
		docHash := persist.HashText(doc.Text)
		refID := persist.NewUUID()
		// llama_index chunks against chunk_size minus the metadata string
		// tokens (split_text_metadata_aware)
		effective := chunkTokens - cl100k(doc.MetadataStr())
		if effective <= 0 {
			fatal(fmt.Errorf("metadata too large for %s", doc.Filename))
		}
		for _, chunk := range chunker.ChunkDocument(doc.Text, cl100k, effective) {
			nodes = append(nodes, persist.Node{
				ID:       persist.NewUUID(),
				RefDocID: refID,
				Text:     chunk.Text,
				Start:    chunk.Start,
				End:      chunk.End,
				Metadata: doc.MetadataMap(),
				DocHash:  docHash,
			})
			texts = append(texts, chunk.Text)
		}
	}

	// phase 2: batched embedding (length-sorted batches minimize padding)
	vectors, err := embedder.EmbedBatch(texts)
	if err != nil {
		fatal(err)
	}

	index, err := faissidx.NewFlatIPIndex(embeddingDim)
	if err != nil {
		fatal(err)
	}
	if err := index.Add(vectors); err != nil {
		fatal(err)
	}

	workDir, err := os.MkdirTemp("", "byok-go-")
	if err != nil {
		fatal(err)
	}
	defer os.RemoveAll(workDir)
	vectorDB := filepath.Join(workDir, "vector_db")

	faissBytes, err := index.Serialize()
	if err != nil {
		fatal(err)
	}
	if err := persist.PersistDir(vectorDB, nodes, faissBytes, *indexID); err != nil {
		fatal(err)
	}
	elapsed := time.Since(start).Seconds()
	if err := persist.WriteToolMetadata(vectorDB, modelName, *indexID, embeddingDim,
		chunkTokens, chunkOverlap, len(docs), elapsed); err != nil {
		fatal(err)
	}
	if err := assemble.AssembleOutput(*outTar, *tag, *baseLayer, vectorDB); err != nil {
		fatal(err)
	}

	fmt.Printf("OK: %d docs, %d nodes, wrote %s (%.1fs)\n",
		len(docs), len(nodes), *outTar, elapsed)
}

func fatal(err error) {
	fmt.Fprintln(os.Stderr, "ERROR:", err)
	os.Exit(1)
}
