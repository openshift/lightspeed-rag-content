// Package docparse discovers markdown documents and extracts the metadata
// the BYOK pipeline attaches to them, mirroring the Python tool's
// file_metadata_func.
package docparse

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
)

// ExcludedMetadataKeys are llama_index's default excluded metadata keys.
var ExcludedMetadataKeys = []string{
	"file_name", "file_type", "file_size",
	"creation_date", "last_modified_date", "last_accessed_date",
}

// Document is one markdown file with its extracted metadata.
type Document struct {
	Text      string
	Title     string
	DocsURL   string
	Filename  string
	Extension string
	FilePath  string
}

// OrderedMetadata returns the metadata in llama_index insertion order.
func (d Document) OrderedMetadata() [][2]string {
	return [][2]string{
		{"filename", d.Filename},
		{"extension", d.Extension},
		{"file_path", d.FilePath},
		{"title", d.Title},
		{"docs_url", d.DocsURL},
	}
}

// MetadataStr mirrors llama_index's Document.get_metadata_str: every key not
// in ExcludedMetadataKeys, "{key}: {value}" joined with newlines. Its token
// count reduces the effective chunk budget.
func (d Document) MetadataStr() string {
	out := ""
	for _, kv := range d.OrderedMetadata() {
		excluded := false
		for _, k := range ExcludedMetadataKeys {
			if kv[0] == k {
				excluded = true
				break
			}
		}
		if excluded {
			continue
		}
		if out != "" {
			out += "\n"
		}
		out += kv[0] + ": " + kv[1]
	}
	return out
}

// MetadataMap returns the metadata as a plain map (for the docstore).
func (d Document) MetadataMap() map[string]string {
	out := make(map[string]string, 5)
	for _, kv := range d.OrderedMetadata() {
		out[kv[0]] = kv[1]
	}
	return out
}

// LoadDocuments walks dir for .md files and extracts metadata from each.
func LoadDocuments(dir string) ([]Document, error) {
	var docs []Document
	err := filepath.WalkDir(dir, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if d.IsDir() || filepath.Ext(path) != ".md" {
			return nil
		}
		raw, err := os.ReadFile(path)
		if err != nil {
			return err
		}
		docs = append(docs, newDocument(string(raw), path))
		return nil
	})
	if err != nil {
		return nil, err
	}
	if len(docs) == 0 {
		return nil, fmt.Errorf("no markdown files found under %s", dir)
	}
	return docs, nil
}

func newDocument(text, path string) Document {
	doc := Document{
		Text:      text,
		Title:     path,
		DocsURL:   path,
		Filename:  filepath.Base(path),
		Extension: ".md",
		FilePath:  path,
	}
	body := text
	if strings.HasPrefix(text, "---\n") {
		end := strings.Index(text[4:], "\n---")
		if end >= 0 {
			front := text[4 : 4+end]
			body = strings.TrimLeft(text[4+end+4:], "\n")
			for _, line := range strings.Split(front, "\n") {
				key, value, found := strings.Cut(line, ":")
				if !found {
					continue
				}
				value = strings.Trim(strings.TrimSpace(value), `"'`)
				switch strings.TrimSpace(key) {
				case "title":
					doc.Title = value
				case "url":
					doc.DocsURL = value
				}
			}
		}
	}
	if doc.Title == path {
		for _, line := range strings.Split(body, "\n") {
			if strings.HasPrefix(line, "# ") {
				doc.Title = strings.TrimPrefix(line, "# ")
				break
			}
		}
	}
	return doc
}
