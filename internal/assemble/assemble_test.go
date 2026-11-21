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

func fixture(t *testing.T) string {
	t.Helper()
	dir := t.TempDir()
	dataDir := filepath.Join(dir, "vector_db")
	os.MkdirAll(dataDir, 0o755)
	os.WriteFile(filepath.Join(dataDir, "metadata.json"), []byte(`{"index-id":"t"}`), 0o644)
	os.WriteFile(filepath.Join(dataDir, "docstore.json"), []byte("{}"), 0o644)
	return dataDir
}

func assembleFixture(t *testing.T) string {
	t.Helper()
	dataDir := fixture(t)
	dest := filepath.Join(t.TempDir(), "out.tar")
	if err := AssembleOutput(dest, "byok-image", dataDir); err != nil {
		t.Fatalf("AssembleOutput: %v", err)
	}
	return dest
}

// TestManifestIsArray guards the docker-archive format contract: manifest.json must
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
	if len(layers) != 1 {
		t.Errorf("expected 1 layer (data-only image), got %v", layers)
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
	dataDir := fixture(t)
	dest := filepath.Join(t.TempDir(), "out.tar")
	if err := AssembleOutput(dest, "t", dataDir); err != nil {
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

// TestDataOnlyImage guards the OLM-bundle-style contract: the image must not
// carry an entrypoint/Cmd (nothing from it is ever executed) and must be a
// single-platform manifest so runtimes pull it on any node architecture.
func TestDataOnlyImage(t *testing.T) {
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
	var config map[string]any
	json.Unmarshal(members[manifest[0]["Config"].(string)], &config)
	if cfg, ok := config["config"].(map[string]any); ok {
		if _, ok := cfg["Cmd"]; ok {
			t.Error("data-only image must not declare a Cmd")
		}
		if _, ok := cfg["Entrypoint"]; ok {
			t.Error("data-only image must not declare an Entrypoint")
		}
	} else {
		t.Error("image config missing config section")
	}
	if arch, _ := config["architecture"].(string); arch != "amd64" {
		t.Errorf("architecture = %q, want amd64 (single-manifest images are pulled on any arch)", arch)
	}
	layers := manifest[0]["Layers"].([]any)
	if len(layers) != 1 {
		t.Errorf("expected a single data layer, got %v", layers)
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

// TestAssembleOutputEmptyDataDir verifies the tool fails closed when the
// vector db directory has no files.
func TestAssembleOutputEmptyDataDir(t *testing.T) {
	dataDir := t.TempDir() // exists but empty
	dest := filepath.Join(t.TempDir(), "out.tar")
	if err := AssembleOutput(dest, "byok-image", dataDir); err == nil {
		t.Error("expected an error for an empty data directory")
	}
}

// TestAssembleOutputMissingDataDir verifies a nonexistent data directory is
// reported as an error, not silently skipped.
func TestAssembleOutputMissingDataDir(t *testing.T) {
	dest := filepath.Join(t.TempDir(), "out.tar")
	missing := filepath.Join(t.TempDir(), "no-such-dir")
	if err := AssembleOutput(dest, "byok-image", missing); err == nil {
		t.Error("expected an error for a missing data directory")
	}
}
