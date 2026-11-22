package main

import (
	"os"
	"path/filepath"
	"testing"
	"time"
)

func writeTree(t *testing.T) string {
	t.Helper()
	src := t.TempDir()
	os.MkdirAll(filepath.Join(src, "vector_db"), 0o755)
	os.WriteFile(filepath.Join(src, "vector_db", "metadata.json"), []byte(`{"index-id":"t"}`), 0o644)
	os.WriteFile(filepath.Join(src, "vector_db", "index.faiss"), []byte("fake index bytes"), 0o600)
	os.MkdirAll(filepath.Join(src, "vector_db", "nested"), 0o700)
	os.WriteFile(filepath.Join(src, "vector_db", "nested", "docstore.json"), []byte("{}"), 0o640)
	// distinct mtime so preservation is observable
	past := time.Now().Add(-37 * time.Hour)
	os.Chtimes(filepath.Join(src, "vector_db", "metadata.json"), past, past)
	return src
}

func TestCopyTree(t *testing.T) {
	src := writeTree(t)
	dst := filepath.Join(t.TempDir(), "out", "rag-0")

	if err := copyTree(src, dst); err != nil {
		t.Fatalf("copyTree: %v", err)
	}

	for _, tc := range []struct {
		path string
		perm os.FileMode
	}{{"vector_db", 0o755}, {"vector_db/metadata.json", 0o644}, {"vector_db/index.faiss", 0o600}, {"vector_db/nested", 0o700}, {"vector_db/nested/docstore.json", 0o640}} {
		info, err := os.Stat(filepath.Join(dst, tc.path))
		if err != nil {
			t.Fatalf("missing %s: %v", tc.path, err)
		}
		if info.Mode().Perm() != tc.perm {
			t.Errorf("%s: perm %o, want %o", tc.path, info.Mode().Perm(), tc.perm)
		}
	}

	srcStat, _ := os.Stat(filepath.Join(src, "vector_db", "metadata.json"))
	dstStat, err := os.Stat(filepath.Join(dst, "vector_db", "metadata.json"))
	if err != nil {
		t.Fatal(err)
	}
	if !dstStat.ModTime().Equal(srcStat.ModTime()) {
		t.Errorf("mtime not preserved: %v != %v", dstStat.ModTime(), srcStat.ModTime())
	}

	data, _ := os.ReadFile(filepath.Join(dst, "vector_db", "index.faiss"))
	if string(data) != "fake index bytes" {
		t.Errorf("content mismatch: %q", data)
	}
}

func TestCopyTreeOverwritesExisting(t *testing.T) {
	src := writeTree(t)
	dst := filepath.Join(t.TempDir(), "out")
	os.WriteFile(filepath.Join(dst, "vector_db", "metadata.json"), []byte("stale"), 0o644)

	if err := copyTree(src, dst); err != nil {
		t.Fatalf("copyTree: %v", err)
	}
	data, _ := os.ReadFile(filepath.Join(dst, "vector_db", "metadata.json"))
	if string(data) != `{"index-id":"t"}` {
		t.Errorf("existing file not overwritten: %q", data)
	}
}

func TestCopyTreeRejectsSymlink(t *testing.T) {
	src := t.TempDir()
	os.WriteFile(filepath.Join(src, "real"), []byte("x"), 0o644)
	if err := os.Symlink("real", filepath.Join(src, "link")); err != nil {
		t.Skip("symlinks unavailable")
	}
	dst := t.TempDir()
	if err := copyTree(src, dst); err == nil {
		t.Error("expected an error for a symlink in the source tree")
	}
}

func TestCopyTreeMissingSource(t *testing.T) {
	if err := copyTree(filepath.Join(t.TempDir(), "no-such-dir"), t.TempDir()); err == nil {
		t.Error("expected an error for a missing source")
	}
}

func TestCopyTreeFileSource(t *testing.T) {
	src := t.TempDir()
	file := filepath.Join(src, "afile")
	os.WriteFile(file, []byte("x"), 0o644)
	if err := copyTree(file, t.TempDir()); err == nil {
		t.Error("expected an error for a non-directory source")
	}
}
