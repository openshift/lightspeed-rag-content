package docparse

import (
	"os"
	"path/filepath"
	"testing"
)

func writeTemp(t *testing.T, name, content string) string {
	t.Helper()
	dir := t.TempDir()
	path := filepath.Join(dir, name)
	if err := os.WriteFile(path, []byte(content), 0o644); err != nil {
		t.Fatalf("write fixture: %v", err)
	}
	return path
}

func TestFrontmatterTitleAndURL(t *testing.T) {
	path := writeTemp(t, "doc.md", "---\ntitle: \"My Title\"\nurl: https://example.com/x\n---\n\n# Heading\n\nBody.")
	docs, err := LoadDocuments(filepath.Dir(path))
	if err != nil {
		t.Fatalf("LoadDocuments: %v", err)
	}
	if len(docs) != 1 {
		t.Fatalf("expected 1 doc, got %d", len(docs))
	}
	if docs[0].Title != "My Title" || docs[0].DocsURL != "https://example.com/x" {
		t.Errorf("frontmatter not parsed: title=%q url=%q", docs[0].Title, docs[0].DocsURL)
	}
}

func TestFirstHeadingFallback(t *testing.T) {
	path := writeTemp(t, "doc.md", "# The Heading\n\nBody without frontmatter.")
	docs, err := LoadDocuments(filepath.Dir(path))
	if err != nil {
		t.Fatalf("LoadDocuments: %v", err)
	}
	if docs[0].Title != "The Heading" {
		t.Errorf("heading fallback failed: title=%q", docs[0].Title)
	}
	if docs[0].DocsURL != docs[0].FilePath {
		t.Errorf("url fallback should be the file path, got %q", docs[0].DocsURL)
	}
}

func TestOnlyMarkdownFiles(t *testing.T) {
	dir := t.TempDir()
	os.WriteFile(filepath.Join(dir, "a.md"), []byte("# A"), 0o644)
	os.WriteFile(filepath.Join(dir, "b.txt"), []byte("ignore me"), 0o644)
	os.Mkdir(filepath.Join(dir, "sub"), 0o755)
	os.WriteFile(filepath.Join(dir, "sub", "c.md"), []byte("# C"), 0o644)
	docs, err := LoadDocuments(dir)
	if err != nil {
		t.Fatalf("LoadDocuments: %v", err)
	}
	if len(docs) != 2 {
		t.Errorf("expected 2 markdown docs, got %d", len(docs))
	}
}

func TestNoMarkdownFilesFails(t *testing.T) {
	dir := t.TempDir()
	os.WriteFile(filepath.Join(dir, "a.txt"), []byte("no markdown"), 0o644)
	if _, err := LoadDocuments(dir); err == nil {
		t.Error("expected error for directory without markdown files")
	}
}

// TestMetadataStrGolden pins the exact metadata string whose token count
// reduces the effective chunk budget (python parity: 56 cl100k tokens).
func TestMetadataStrGolden(t *testing.T) {
	doc := Document{
		Filename:  "runbook-1.md",
		Extension: ".md",
		FilePath:  "/markdown/runbook-1.md",
		Title:     "Zyranex T7 OpenShift Runbook",
		DocsURL:   "https://docs.quorbitex.example.com/openshift/zyranex-t7",
	}
	want := "filename: runbook-1.md\n" +
		"extension: .md\n" +
		"file_path: /markdown/runbook-1.md\n" +
		"title: Zyranex T7 OpenShift Runbook\n" +
		"docs_url: https://docs.quorbitex.example.com/openshift/zyranex-t7"
	if got := doc.MetadataStr(); got != want {
		t.Errorf("MetadataStr mismatch:\n got: %q\nwant: %q", got, want)
	}
}

func TestMetadataMapKeys(t *testing.T) {
	doc := Document{Filename: "a.md", Extension: ".md", FilePath: "/x/a.md", Title: "T", DocsURL: "u"}
	m := doc.MetadataMap()
	for _, key := range []string{"filename", "extension", "file_path", "title", "docs_url"} {
		if _, ok := m[key]; !ok {
			t.Errorf("metadata map missing %q", key)
		}
	}
}
