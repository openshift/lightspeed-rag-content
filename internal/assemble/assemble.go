package assemble

// Container image archive assembly (docker-archive format) without a
// container runtime: the customer output image is a single data layer
// holding /rag/vector_db, loadable with `podman load`.
//
// The image is deliberately data-only (OLM-bundle style): it contains no
// binaries from its own filesystem, and the consumer (the OLS operator's
// RAG init containers) copies the index out with a binary staged from the
// service image, never executing anything from this image. Because the
// image is a single-platform manifest (not a manifest list), container
// runtimes pull it on any node architecture without a platform filter —
// the same property that lets OLM unpack amd64-only operator bundles on
// any cluster. The config's "architecture" field is therefore nominal;
// it is set to amd64 to keep the manifest a plain single-arch image.
//
// Replaces the buildah build-and-push step of the original Python tool
// (which had no archive code of its own; Containerfile.output + buildah
// did this job).

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

// AssembleOutput writes the container image archive (docker-archive
// format) tar for the generated vector db.
func AssembleOutput(dest, tag, dataDir string) error {
	dataLayer, err := tarDirectory(dataDir, "rag/vector_db")
	if err != nil {
		return err
	}

	dataDigest := digest(dataLayer)
	diffIDs := []string{"sha256:" + dataDigest}
	// architecture is nominal (see the package comment); the single
	// data layer contains no architecture-specific content.
	config := map[string]any{
		"architecture": "amd64",
		"os":           "linux",
		"created":      "1970-01-01T00:00:00Z",
		"config": map[string]any{
			"Env":    outputEnv,
			"Labels": outputLabels,
		},
		"rootfs": map[string]any{"type": "layers", "diff_ids": diffIDs},
		"history": []map[string]any{
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
		"Layers":   []string{dataDigest + "/layer.tar"},
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

// tarDirectory creates an uncompressed tar of dir under prefix.
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
