// rag-copy copies the contents of a directory tree, preserving file
// modes and modification times. It is built with CGO_ENABLED=0 and no
// assembly, so the resulting binary is statically linked and runs in any
// root filesystem — including the data-only BYOK customer images, which
// contain no shell, no glibc, and no dynamic loader.
//
// The OLS operator stages this binary from the service image into a
// rag-util emptyDir and runs it as the RAG init container command,
// overriding the customer image's entrypoint (the OLM-bundle pattern;
// OLM's equivalent helper is the statically linked `cpb`).
//
// The CLI contract is frozen: `rag-copy SRC DST` copies the *contents*
// of SRC into DST (DST is created if needed). Ownership is not
// preserved — the init containers run under a restricted security
// context where chown is not permitted, and the FAISS index files are
// consumed read-only by the service.
package main

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
)

func main() {
	if len(os.Args) != 3 {
		fmt.Fprintln(os.Stderr, "usage: rag-copy SRC DST")
		os.Exit(2)
	}
	if err := copyTree(os.Args[1], os.Args[2]); err != nil {
		fmt.Fprintln(os.Stderr, "rag-copy:", err)
		os.Exit(1)
	}
}

// copyTree copies the contents of src into dst. dst is created (with
// src's mode) if it does not exist. Regular files and directories are
// copied with mode and mtime preserved; anything else (symlinks, device
// nodes, ...) is rejected — fail closed rather than guessing.
func copyTree(src, dst string) error {
	srcInfo, err := os.Lstat(src)
	if err != nil {
		return fmt.Errorf("source: %w", err)
	}
	if !srcInfo.IsDir() {
		return fmt.Errorf("source %s is not a directory", src)
	}
	if err := os.MkdirAll(dst, srcInfo.Mode().Perm()); err != nil {
		return fmt.Errorf("destination: %w", err)
	}
	return filepath.WalkDir(src, func(path string, d os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if path == src {
			return nil
		}
		rel, err := filepath.Rel(src, path)
		if err != nil {
			return err
		}
		target := filepath.Join(dst, rel)
		info, err := d.Info()
		if err != nil {
			return err
		}
		switch {
		case d.IsDir():
			return os.MkdirAll(target, info.Mode().Perm())
		case info.Mode().IsRegular():
			if err := copyFile(path, target, info); err != nil {
				return err
			}
			return os.Chtimes(target, info.ModTime(), info.ModTime())
		default:
			return fmt.Errorf("%s: unsupported file type %s", path, info.Mode())
		}
	})
}

func copyFile(src, dst string, info os.FileInfo) error {
	in, err := os.Open(src)
	if err != nil {
		return err
	}
	defer in.Close()

	// Write via a temp file in the destination directory so a failed
	// copy never leaves a partial file at the final name.
	tmp, err := os.CreateTemp(filepath.Dir(dst), ".rag-copy-*")
	if err != nil {
		return err
	}
	tmpName := tmp.Name()
	if _, err := io.Copy(tmp, in); err != nil {
		tmp.Close()
		os.Remove(tmpName)
		return err
	}
	if err := tmp.Close(); err != nil {
		os.Remove(tmpName)
		return err
	}
	if err := os.Chmod(tmpName, info.Mode().Perm()); err != nil {
		os.Remove(tmpName)
		return err
	}
	return os.Rename(tmpName, dst)
}
