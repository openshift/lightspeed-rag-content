package assemble

import (
	"archive/tar"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func fixture(t *testing.T) (string, string) {
	t.Helper()
	dir := t.TempDir()
	baseLayer := filepath.Join(dir, "base-layer.tar")
	out := tarDirectoryBytes(t, map[string]string{"bin/sh": "#!/bin/sh\n"})
	if err := os.WriteFile(baseLayer, out, 0o644); err != nil {
		t.Fatal(err)
	}
	dataDir := filepath.Join(dir, "vector_db")
	os.MkdirAll(dataDir, 0o755)
	os.WriteFile(filepath.Join(dataDir, "metadata.json"), []byte(`{"index-id":"t"}`), 0o644)
	os.WriteFile(filepath.Join(dataDir, "docstore.json"), []byte("{}"), 0o644)
	return baseLayer, dataDir
}

func tarDirectoryBytes(t *testing.T, files map[string]string) []byte {
	t.Helper()
	path := filepath.Join(t.TempDir(), "layer.tar")
	f, err := os.Create(path)
	if err != nil {
		t.Fatal(err)
	}
	tw := tar.NewWriter(f)
	for name, content := range files {
		tw.WriteHeader(&tar.Header{Name: name, Mode: 0o755, Size: int64(len(content))})
		tw.Write([]byte(content))
	}
	tw.Close()
	f.Close()
	raw, _ := os.ReadFile(path)
	return raw
}

func assembleFixture(t *testing.T) string {
	t.Helper()
	baseLayer, dataDir := fixture(t)
	dest := filepath.Join(t.TempDir(), "out.tar")
	if err := AssembleOutput(dest, "byok-image", baseLayer, dataDir); err != nil {
		t.Fatalf("AssembleOutput: %v", err)
	}
	return dest
}

// TestManifestIsArray guards the docker-archive contract: manifest.json must
// be an array of entries (regression: object form breaks podman load).
func TestManifestIsArray(t *testing.T) {
	archive := assembleFixture(t)
	raw, _ := os.ReadFile(archive)
	withTar := tar.NewReader(strings.NewReader(string(raw)))
	var manifest []map[string]any
	for {
		header, err := withTar.Next()
		if err != nil {
			t.Fatal(err)
		}
		if header.Name == "manifest.json" {
			if err := json.NewDecoder(withTar).Decode(&manifest); err != nil {
				t.Fatalf("manifest.json must be a JSON array: %v", err)
			}
			break
		}
	}
	if len(manifest) != 1 {
		t.Fatalf("expected 1 manifest entry, got %d", len(manifest))
	}
	tags, _ := manifest[0]["RepoTags"].([]any)
	if len(tags) != 1 || tags[0] != "byok-image:latest" {
		t.Errorf("RepoTags = %v", manifest[0]["RepoTags"])
	}
	layers, _ := manifest[0]["Layers"].([]any)
	if len(layers) != 2 {
		t.Errorf("expected 2 layers, got %v", layers)
	}
}

// TestDiffIDsMatchLayers verifies the config rootfs digests equal the sha256
// of each layer member (the podman load contract).
func TestDiffIDsMatchLayers(t *testing.T) {
	archive := assembleFixture(t)
	raw, _ := os.ReadFile(archive)
	tr := tar.NewReader(strings.NewReader(string(raw)))
	members := map[string][]byte{}
	for {
		header, err := tr.Next()
		if err != nil {
			break
		}
		buf := make([]byte, header.Size)
		tr.Read(buf)
		members[header.Name] = buf
	}
	var manifest []map[string]any
	json.Unmarshal(members["manifest.json"], &manifest)
	entry := manifest[0]
	var config map[string]any
	json.Unmarshal(members[entry["Config"].(string)], &config)
	diffIDs := config["rootfs"].(map[string]any)["diff_ids"].([]any)
	layers := entry["Layers"].([]any)
	if len(diffIDs) != len(layers) {
		t.Fatalf("diff_ids %v vs layers %v", diffIDs, layers)
	}
	for i, layerName := range layers {
		sum := sha256.Sum256(members[layerName.(string)])
		want := "sha256:" + hex.EncodeToString(sum[:])
		if diffIDs[i] != want {
			t.Errorf("layer %d: diff_id %v != sha256(layer) %s", i, diffIDs[i], want)
		}
	}
}

// TestDataLayerPlacesVectorDB checks the layer layout: rag/vector_db/...
func TestDataLayerPlacesVectorDB(t *testing.T) {
	baseLayer, dataDir := fixture(t)
	dest := filepath.Join(t.TempDir(), "out.tar")
	if err := AssembleOutput(dest, "t", baseLayer, dataDir); err != nil {
		t.Fatal(err)
	}
	raw, _ := os.ReadFile(dest)
	tr := tar.NewReader(strings.NewReader(string(raw)))
	var manifest []map[string]any
	var layerBytes []byte
	for {
		header, err := tr.Next()
		if err != nil {
			break
		}
		buf := make([]byte, header.Size)
		tr.Read(buf)
		if header.Name == "manifest.json" {
			json.Unmarshal(buf, &manifest)
		}
	}
	layers := manifest[0]["Layers"].([]any)
	layerName := layers[len(layers)-1].(string)
	tr = tar.NewReader(strings.NewReader(string(raw)))
	for {
		header, err := tr.Next()
		if err != nil {
			break
		}
		if header.Name == layerName {
			layerBytes = make([]byte, header.Size)
			tr.Read(layerBytes)
			break
		}
	}
	inner := tar.NewReader(strings.NewReader(string(layerBytes)))
	found := false
	for {
		header, err := inner.Next()
		if err != nil {
			break
		}
		if header.Name == "rag/vector_db/metadata.json" {
			found = true
		}
	}
	if !found {
		t.Error("data layer missing rag/vector_db/metadata.json")
	}
}

// TestDeterministicOutput pins byte-reproducible archives for fixed inputs.
func TestDeterministicOutput(t *testing.T) {
	baseLayer, dataDir := fixture(t)
	first := filepath.Join(t.TempDir(), "a.tar")
	second := filepath.Join(t.TempDir(), "b.tar")
	if err := AssembleOutput(first, "t", baseLayer, dataDir); err != nil {
		t.Fatal(err)
	}
	if err := AssembleOutput(second, "t", baseLayer, dataDir); err != nil {
		t.Fatal(err)
	}
	a, _ := os.ReadFile(first)
	b, _ := os.ReadFile(second)
	if string(a) != string(b) {
		t.Error("assembled archives are not byte-identical for identical inputs")
	}
}

// TestAtomicWrite checks no temp file is left behind.
func TestAtomicWrite(t *testing.T) {
	archive := assembleFixture(t)
	if _, err := os.Stat(archive + ".tmp"); !os.IsNotExist(err) {
		t.Error("temporary file left behind")
	}
}

func TestNormalizeTag(t *testing.T) {
	cases := map[string]string{
		"byok-image":         "byok-image:latest",
		"quay.io/acme/x:1.0": "quay.io/acme/x:1.0",
		"localhost/foo":      "localhost/foo:latest",
	}
	for in, want := range cases {
		if got := normalizeTag(in); got != want {
			t.Errorf("normalizeTag(%q) = %q, want %q", in, got, want)
		}
	}
}
