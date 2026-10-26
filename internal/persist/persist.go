// Package persist emits the llama_index storage format consumed by the OLS
// service (llama-index-core 0.14.x + FaissVectorStore.from_persist_dir).
package persist

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	"github.com/openshift/lightspeed-rag-content/internal/docparse"
)

// Node is one chunk ready for the docstore.
type Node struct {
	ID       string
	RefDocID string
	Text     string
	Start    int
	End      int
	Metadata map[string]string
	DocHash  string
}

// PersistDir writes the complete llama_index persist file set plus the tool
// metadata into dir. faissBytes must have vectors in the same order as nodes.
func PersistDir(dir string, nodes []Node, faissBytes []byte, indexID string) error {
	if err := os.MkdirAll(dir, 0o755); err != nil {
		return err
	}
	if err := os.WriteFile(filepath.Join(dir, "default__vector_store.json"), faissBytes, 0o644); err != nil {
		return err
	}
	if err := writeJSON(filepath.Join(dir, "graph_store.json"), map[string]any{
		"graph_dict": map[string]any{},
	}); err != nil {
		return err
	}
	if err := writeJSON(filepath.Join(dir, "image__vector_store.json"), map[string]any{
		"embedding_dict":        map[string]any{},
		"text_id_to_ref_doc_id": map[string]any{},
		"metadata_dict":         map[string]any{},
	}); err != nil {
		return err
	}

	docstore := map[string]any{
		"docstore/data":         docstoreData(nodes),
		"docstore/metadata":     docstoreMetadata(nodes),
		"docstore/ref_doc_info": refDocInfo(nodes),
	}
	if err := writeJSON(filepath.Join(dir, "docstore.json"), docstore); err != nil {
		return err
	}

	nodesDict := make(map[string]string, len(nodes))
	for i, n := range nodes {
		nodesDict[fmt.Sprint(i)] = n.ID
	}
	indexStruct := map[string]any{
		"index_id":        indexID,
		"summary":         nil,
		"nodes_dict":      nodesDict,
		"doc_id_dict":     map[string]any{},
		"embeddings_dict": map[string]any{},
	}
	structBytes, err := json.Marshal(indexStruct)
	if err != nil {
		return err
	}
	indexStore := map[string]any{
		"index_store/data": map[string]any{
			indexID: map[string]any{
				"__type__": "vector_store",
				"__data__": string(structBytes),
			},
		},
	}
	return writeJSON(filepath.Join(dir, "index_store.json"), indexStore)
}

// WriteToolMetadata writes the metadata.json checked by the e2e test.
func WriteToolMetadata(dir, modelName, indexID string, dimension, chunk, overlap, files int, executionTime float64) error {
	metadata := map[string]any{
		"execution-time":       executionTime,
		"llm":                  "None",
		"embedding-model-name": modelName,
		"index-id":             indexID,
		"vector-db":            "faiss.IndexFlatIP",
		"embedding-dimension":  dimension,
		"chunk":                chunk,
		"overlap":              overlap,
		"total-embedded-files": files,
	}
	return writeJSON(filepath.Join(dir, "metadata.json"), metadata)
}

func docstoreData(nodes []Node) map[string]any {
	data := make(map[string]any, len(nodes))
	for _, n := range nodes {
		data[n.ID] = map[string]any{
			"__type__": "1",
			"__data__": map[string]any{
				"class_name":                   "TextNode",
				"embedding":                    nil,
				"id_":                          n.ID,
				"text":                         n.Text,
				"metadata":                     n.Metadata,
				"start_char_idx":               n.Start,
				"end_char_idx":                 n.End,
				"mimetype":                     "text/plain",
				"metadata_separator":           "\n",
				"metadata_template":            "{key}: {value}",
				"text_template":                "{metadata_str}\n\n{content}",
				"excluded_embed_metadata_keys": docparse.ExcludedMetadataKeys,
				"excluded_llm_metadata_keys":   docparse.ExcludedMetadataKeys,
				"relationships": map[string]any{
					"1": map[string]any{
						"node_id":    n.RefDocID,
						"node_type":  "4",
						"metadata":   n.Metadata,
						"hash":       n.DocHash,
						"class_name": "RelatedNodeInfo",
					},
				},
			},
		}
	}
	return data
}

func docstoreMetadata(nodes []Node) map[string]any {
	out := make(map[string]any, len(nodes))
	for _, n := range nodes {
		out[n.ID] = map[string]any{
			"doc_hash":   n.DocHash,
			"ref_doc_id": n.RefDocID,
		}
	}
	return out
}

func refDocInfo(nodes []Node) map[string]any {
	out := map[string]any{}
	byRef := map[string][]string{}
	metadataByRef := map[string]map[string]string{}
	for _, n := range nodes {
		byRef[n.RefDocID] = append(byRef[n.RefDocID], n.ID)
		if _, ok := metadataByRef[n.RefDocID]; !ok {
			metadataByRef[n.RefDocID] = n.Metadata
		}
	}
	for ref, ids := range byRef {
		out[ref] = map[string]any{
			"node_ids": ids,
			"metadata": metadataByRef[ref],
		}
	}
	return out
}

// NewUUID returns a random RFC 4122 version 4 UUID string.
func NewUUID() string {
	var b [16]byte
	if _, err := rand.Read(b[:]); err != nil {
		panic(err)
	}
	b[6] = (b[6] & 0x0f) | 0x40
	b[8] = (b[8] & 0x3f) | 0x80
	return fmt.Sprintf("%x-%x-%x-%x-%x", b[0:4], b[4:6], b[6:8], b[8:10], b[10:16])
}

// HashText returns the sha256 hex digest of a text.
func HashText(text string) string {
	sum := sha256.Sum256([]byte(text))
	return hex.EncodeToString(sum[:])
}

func writeJSON(path string, value any) error {
	raw, err := json.Marshal(value)
	if err != nil {
		return err
	}
	return os.WriteFile(path, raw, 0o644)
}
