package persist

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"testing"
)

const sampleDir = "../../testdata/persist-sample"

// nodeFixture builds deterministic nodes for schema assertions.
func nodeFixture() []Node {
	meta := map[string]string{
		"filename":  "runbook-1.md",
		"extension": ".md",
		"file_path": "/markdown/runbook-1.md",
		"title":     "Zyranex T7 OpenShift Runbook",
		"docs_url":  "https://docs.quorbitex.example.com/openshift/zyranex-t7",
	}
	return []Node{
		{
			ID:       "11111111-1111-4111-8111-111111111111",
			RefDocID: "22222222-2222-4222-8222-222222222222",
			Text:     "chunk one text",
			Start:    0,
			End:      14,
			Metadata: meta,
			DocHash:  "aa",
		},
		{
			ID:       "33333333-3333-4333-8333-333333333333",
			RefDocID: "22222222-2222-4222-8222-222222222222",
			Text:     "chunk two text",
			Start:    15,
			End:      29,
			Metadata: meta,
			DocHash:  "aa",
		},
	}
}

// TestSchemaAgainstRealSample compares the emitted structures with the
// golden files produced by the Python tool (modulo ids and hashes).
func TestSchemaAgainstRealSample(t *testing.T) {
	dir := t.TempDir()
	nodes := nodeFixture()
	if err := PersistDir(dir, nodes, []byte("FAISSBYTES"), "test-index"); err != nil {
		t.Fatalf("PersistDir: %v", err)
	}

	goldenDocstore, err := os.ReadFile(filepath.Join(sampleDir, "docstore.json"))
	if err != nil {
		t.Fatalf("read golden docstore: %v", err)
	}
	var golden, emitted map[string]any
	if err := json.Unmarshal(goldenDocstore, &golden); err != nil {
		t.Fatal(err)
	}
	raw, _ := os.ReadFile(filepath.Join(dir, "docstore.json"))
	if err := json.Unmarshal(raw, &emitted); err != nil {
		t.Fatal(err)
	}
	for _, key := range []string{"docstore/data", "docstore/metadata", "docstore/ref_doc_info"} {
		if _, ok := emitted[key]; !ok {
			t.Errorf("docstore.json missing %q", key)
		}
		if _, ok := golden[key]; !ok {
			t.Errorf("golden docstore.json missing %q (fixture drift)", key)
		}
	}

	// node schema: __type__ must be the STRING "1" (llama_index NodeType enum)
	nodeEntry, ok := emitted["docstore/data"].(map[string]any)[nodes[0].ID].(map[string]any)
	if !ok {
		t.Fatalf("docstore/data entry missing for %s", nodes[0].ID)
	}
	if nodeEntry["__type__"] != "1" {
		t.Errorf("__type__ = %v (%T), want string \"1\"", nodeEntry["__type__"], nodeEntry["__type__"])
	}
	nodeData := nodeEntry["__data__"].(map[string]any)
	for _, field := range []string{
		"class_name", "embedding", "id_", "text", "metadata", "start_char_idx",
		"end_char_idx", "mimetype", "metadata_separator", "metadata_template",
		"text_template", "excluded_embed_metadata_keys", "excluded_llm_metadata_keys",
		"relationships",
	} {
		if _, ok := nodeData[field]; !ok {
			t.Errorf("node missing field %q", field)
		}
	}
	if nodeData["class_name"] != "TextNode" {
		t.Errorf("class_name = %v, want TextNode", nodeData["class_name"])
	}
	rel := nodeData["relationships"].(map[string]any)["1"].(map[string]any)
	if rel["node_type"] != "4" {
		t.Errorf("relationship node_type = %v, want \"4\"", rel["node_type"])
	}

	// index store: nodes_dict maps positions to node ids in insertion order
	raw, _ = os.ReadFile(filepath.Join(dir, "index_store.json"))
	var indexStore map[string]any
	if err := json.Unmarshal(raw, &indexStore); err != nil {
		t.Fatal(err)
	}
	entry := indexStore["index_store/data"].(map[string]any)["test-index"].(map[string]any)
	if entry["__type__"] != "vector_store" {
		t.Errorf("index entry __type__ = %v, want vector_store", entry["__type__"])
	}
	var indexStruct map[string]any
	if err := json.Unmarshal([]byte(entry["__data__"].(string)), &indexStruct); err != nil {
		t.Fatalf("__data__ is not a JSON string: %v", err)
	}
	nodesDict := indexStruct["nodes_dict"].(map[string]any)
	if nodesDict["0"] != nodes[0].ID || nodesDict["1"] != nodes[1].ID {
		t.Errorf("nodes_dict order broken: %v", nodesDict)
	}
	if indexStruct["index_id"] != "test-index" {
		t.Errorf("index_id = %v", indexStruct["index_id"])
	}

	// the faiss bytes are carried verbatim
	raw, _ = os.ReadFile(filepath.Join(dir, "default__vector_store.json"))
	if string(raw) != "FAISSBYTES" {
		t.Error("faiss bytes not carried verbatim into default__vector_store.json")
	}

	// trivial stores match the golden shape
	for name, want := range map[string]string{
		"graph_store.json":         `{"graph_dict":{}}`,
		"image__vector_store.json": `{"embedding_dict":{},"metadata_dict":{},"text_id_to_ref_doc_id":{}}`,
	} {
		raw, _ := os.ReadFile(filepath.Join(dir, name))
		var got, wanted any
		json.Unmarshal(raw, &got)
		json.Unmarshal([]byte(want), &wanted)
		if fmt.Sprint(got) != fmt.Sprint(wanted) {
			t.Errorf("%s = %s, want %s", name, raw, want)
		}
	}
}

func TestWriteToolMetadata(t *testing.T) {
	dir := t.TempDir()
	if err := WriteToolMetadata(dir, "sentence-transformers/all-mpnet-base-v2", "idx", 768, 380, 0, 3, 12.5); err != nil {
		t.Fatalf("WriteToolMetadata: %v", err)
	}
	raw, _ := os.ReadFile(filepath.Join(dir, "metadata.json"))
	var meta map[string]any
	if err := json.Unmarshal(raw, &meta); err != nil {
		t.Fatal(err)
	}
	// the e2e test asserts on these fields
	for _, key := range []string{
		"index-id", "embedding-dimension", "vector-db", "total-embedded-files",
		"embedding-model-name", "chunk", "overlap",
	} {
		if _, ok := meta[key]; !ok {
			t.Errorf("metadata.json missing %q", key)
		}
	}
	if meta["vector-db"] != "faiss.IndexFlatIP" || meta["embedding-dimension"] != float64(768) {
		t.Errorf("metadata values wrong: %v", meta)
	}
}
