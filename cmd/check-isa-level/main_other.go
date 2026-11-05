//go:build !(linux && amd64)

package main

import "os"

func main() {
	// ISA level check is x86-64 only; no-op on other architectures.
	os.Exit(0)
}
