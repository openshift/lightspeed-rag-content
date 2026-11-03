package embed

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"

	"github.com/openshift/lightspeed-rag-content/internal/tokenizer"
)

type referenceJSON struct {
	Texts                []string    `json:"texts"`
	EmbeddingsNormalized [][]float32 `json:"embeddings_normalized"`
}

// modelDir resolves the model assets: the environment override, or the repo
// model directory when its chunks have been reassembled.
func modelDir(t *testing.T) string {
	t.Helper()
	if dir := os.Getenv("BYOK_GO_MODEL"); dir != "" {
		if _, err := os.Stat(filepath.Join(dir, "mpnet.onnx")); err == nil {
			return dir
		}
		t.Skipf("BYOK_GO_MODEL=%s has no mpnet.onnx", dir)
	}
	candidates := []string{
		filepath.Join("..", "..", "model"),
		"/opt/byok",
	}
	for _, dir := range candidates {
		if _, err := os.Stat(filepath.Join(dir, "mpnet.onnx")); err == nil {
			return dir
		}
	}
	t.Skip("no mpnet.onnx available (set BYOK_GO_MODEL or reassemble byok-go/model)")
	return ""
}

func newEmbedder(t *testing.T) *Embedder {
	t.Helper()
	dir := modelDir(t)
	tok, err := tokenizer.LoadTokenizer(filepath.Join(dir, "tokenizer.json"))
	if err != nil {
		t.Fatalf("tokenizer: %v", err)
	}
	embedder, err := NewEmbedder(filepath.Join(dir, "mpnet.onnx"), tok, 768, 384, 4)
	if err != nil {
		t.Skipf("onnxruntime unavailable: %v", err)
	}
	return embedder
}

func loadReference(t *testing.T) referenceJSON {
	t.Helper()
	raw, err := os.ReadFile(filepath.Join("..", "..", "testdata", "reference.json"))
	if err != nil {
		t.Fatalf("reference: %v", err)
	}
	var ref referenceJSON
	if err := json.Unmarshal(raw, &ref); err != nil {
		t.Fatal(err)
	}
	return ref
}

func cosine(a, b []float32) float64 {
	var dot, na, nb float64
	for i := range a {
		dot += float64(a[i]) * float64(b[i])
		na += float64(a[i]) * float64(a[i])
		nb += float64(b[i]) * float64(b[i])
	}
	if na == 0 || nb == 0 {
		return 0
	}
	return dot / (sqrt(na) * sqrt(nb))
}

func sqrt(x float64) float64 {
	if x <= 0 {
		return 0
	}
	r := x
	for i := 0; i < 40; i++ {
		r = (r + x/r) / 2
	}
	return r
}

// TestBatchParityWithTorch matches batched embeddings against the torch
// reference dump (cosine >= 0.9999 per text).
func TestBatchParityWithTorch(t *testing.T) {
	embedder := newEmbedder(t)
	ref := loadReference(t)
	vectors, err := embedder.EmbedBatch(ref.Texts)
	if err != nil {
		t.Fatalf("EmbedBatch: %v", err)
	}
	for i, want := range ref.EmbeddingsNormalized {
		if cos := cosine(vectors[i], want); cos < 0.9999 {
			t.Errorf("text %d: cosine(torch, onnx-go batched) = %.8f", i, cos)
		}
	}
}

// TestBatchEqualsSingle checks that batched inference matches single-sequence
// inference for the same texts (padding must not leak into the pooled
// vectors beyond float noise).
func TestBatchEqualsSingle(t *testing.T) {
	embedder := newEmbedder(t)
	ref := loadReference(t)
	texts := ref.Texts[:4]
	batched, err := embedder.EmbedBatch(texts)
	if err != nil {
		t.Fatalf("EmbedBatch: %v", err)
	}
	for i, text := range texts {
		single, err := embedder.Embed(text)
		if err != nil {
			t.Fatalf("Embed: %v", err)
		}
		if cos := cosine(batched[i], single); cos < 0.99999 {
			t.Errorf("text %d: batched vs single cosine = %.8f", i, cos)
		}
	}
}

// TestLengthSortedBatching checks that mixed-length inputs return vectors
// in input order.
func TestLengthSortedBatching(t *testing.T) {
	embedder := newEmbedder(t)
	ref := loadReference(t)
	texts := []string{ref.Texts[0], ref.Texts[5], ref.Texts[7], ref.Texts[1]}
	vectors, err := embedder.EmbedBatch(texts)
	if err != nil {
		t.Fatalf("EmbedBatch: %v", err)
	}
	for i, text := range texts {
		single, err := embedder.Embed(text)
		if err != nil {
			t.Fatal(err)
		}
		if cos := cosine(vectors[i], single); cos < 0.99999 {
			t.Errorf("text %d out of order or wrong: cosine %.8f", i, cos)
		}
	}
}
