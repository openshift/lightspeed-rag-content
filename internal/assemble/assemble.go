package assemble

// Docker-archive assembly without a container runtime: the customer output
// image is the baked ubi-minimal base layer plus one layer holding
// /rag/vector_db, loadable with `podman load`. Port of the Python assembler
// with the same deterministic tar layout.

import (
	"archive/tar"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
)

var outputEnv = []string{
	"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
	"container=oci",
}

var outputLabels = map[string]string{
	"name":                "openshift-lightspeed-byok-rag-content",
	"description":         "OpenShift Lightspeed BYOK RAG vector database (customer-generated)",
	"io.k8s.description":  "OpenShift Lightspeed BYOK RAG vector database (customer-generated)",
	"io.k8s.display-name": "OpenShift Lightspeed BYOK RAG content",
	"io.openshift.tags":   "openshift,lightspeed,rag",
	"summary":             "OpenShift Lightspeed BYOK RAG vector database",
}

// AssembleOutput writes the docker-archive tar for the generated vector db.
func AssembleOutput(dest, tag, baseLayerPath, dataDir string) error {
	dataLayer, err := tarDirectory(dataDir, "rag/vector_db")
	if err != nil {
		return err
	}
	baseLayer, err := os.ReadFile(baseLayerPath)
	if err != nil {
		return err
	}

	baseDigest := digest(baseLayer)
	dataDigest := digest(dataLayer)
	diffIDs := []string{"sha256:" + baseDigest, "sha256:" + dataDigest}
	config := map[string]any{
		"architecture": "amd64",
		"os":           "linux",
		"created":      "1970-01-01T00:00:00Z",
		"config": map[string]any{
			"Env":    outputEnv,
			"Cmd":    []string{"/bin/bash"},
			"Labels": outputLabels,
		},
		"rootfs": map[string]any{"type": "layers", "diff_ids": diffIDs},
		"history": []map[string]any{
			{"created": "1970-01-01T00:00:00Z", "created_by": "BYOK tool: output base"},
			{"created": "1970-01-01T00:00:00Z", "created_by": "BYOK tool: COPY vector_db /rag/vector_db"},
		},
	}
	configBytes, err := json.Marshal(config)
	if err != nil {
		return err
	}
	configName := digest(configBytes) + ".json"
	manifest := map[string]any{
		"Config":   configName,
		"RepoTags": []string{normalizeTag(tag)},
		"Layers":   []string{baseDigest + "/layer.tar", dataDigest + "/layer.tar"},
	}
	manifestBytes, err := json.Marshal([]map[string]any{manifest})
	if err != nil {
		return err
	}

	if err := os.MkdirAll(filepath.Dir(dest), 0o755); err != nil {
		return err
	}
	tmp := dest + ".tmp"
	out, err := os.Create(tmp)
	if err != nil {
		return err
	}
	tw := tar.NewWriter(out)
	writeMember := func(name string, data []byte, mode int64) error {
		if err := tw.WriteHeader(&tar.Header{
			Name: name, Mode: mode, Size: int64(len(data)), Format: tar.FormatGNU,
		}); err != nil {
			return err
		}
		_, err := tw.Write(data)
		return err
	}
	if err := writeMember(configName, configBytes, 0o644); err != nil {
		return err
	}
	if err := writeMember(dataDigest+"/layer.tar", dataLayer, 0o644); err != nil {
		return err
	}
	if err := writeMember(baseDigest+"/layer.tar", baseLayer, 0o644); err != nil {
		return err
	}
	if err := writeMember("manifest.json", manifestBytes, 0o644); err != nil {
		return err
	}
	if err := tw.Close(); err != nil {
		return err
	}
	if err := out.Close(); err != nil {
		return err
	}
	return os.Rename(tmp, dest)
}

func normalizeTag(tag string) string {
	for _, r := range tag {
		if r == ':' {
			return tag
		}
	}
	return tag + ":latest"
}

func digest(data []byte) string {
	sum := sha256.Sum256(data)
	return hex.EncodeToString(sum[:])
}

// tarDirectory creates a deterministic uncompressed tar of dir under prefix.
func tarDirectory(dir, prefix string) ([]byte, error) {
	var paths []string
	err := filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() {
			paths = append(paths, path)
		}
		return nil
	})
	if err != nil {
		return nil, err
	}
	if len(paths) == 0 {
		return nil, fmt.Errorf("data directory %s is empty", dir)
	}
	sort.Strings(paths)

	pr, pw := io.Pipe()
	go func() {
		tw := tar.NewWriter(pw)
		_ = tw.WriteHeader(&tar.Header{
			Name: prefix, Mode: 0o755, Typeflag: tar.TypeDir, Format: tar.FormatGNU,
		})
		for _, path := range paths {
			rel, err := filepath.Rel(dir, path)
			if err != nil {
				pw.CloseWithError(err)
				return
			}
			info, err := os.Stat(path)
			if err != nil {
				pw.CloseWithError(err)
				return
			}
			if err := tw.WriteHeader(&tar.Header{
				Name: prefix + "/" + filepath.ToSlash(rel),
				Mode: int64(info.Mode().Perm()), Size: info.Size(), Format: tar.FormatGNU,
			}); err != nil {
				pw.CloseWithError(err)
				return
			}
			f, err := os.Open(path)
			if err != nil {
				pw.CloseWithError(err)
				return
			}
			if _, err := io.Copy(tw, f); err != nil {
				f.Close()
				pw.CloseWithError(err)
				return
			}
			f.Close()
		}
		pw.CloseWithError(tw.Close())
	}()
	return io.ReadAll(pr)
}
