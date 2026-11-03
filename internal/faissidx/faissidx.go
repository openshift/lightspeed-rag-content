package faissidx

// FAISS IndexFlatIP through the C API of the faiss C++ library, built from the
// same v1.12.0 source as the service's faiss-cpu wheel. Serialization is
// byte-identical to faiss::write_index by construction.

/*
#cgo LDFLAGS: -lfaiss_c -lfaiss
// header/library paths come from CGO_CFLAGS/CGO_LDFLAGS (scripts/stage-go-native.sh)
#include <stdio.h>
#include <stdlib.h>
#include <faiss_c.h>
#include <Index_c.h>
#include <index_factory_c.h>
#include <index_io_c.h>
#include <error_c.h>

static int build_flat_ip(FaissIndex** out, int d) {
    return faiss_index_factory(out, d, "Flat", METRIC_INNER_PRODUCT);
}

static int add_vectors(FaissIndex* idx, int64_t n, int64_t d, const float* x) {
    return faiss_Index_add(idx, n, x);
}

// write_index_buffer serializes the index into a malloc'd buffer.
static int write_index_buffer(FaissIndex* idx, char** out, size_t* out_len) {
    char* buf = NULL;
    size_t len = 0;
    FILE* f = open_memstream(&buf, &len);
    if (!f) return -1;
    int rc = faiss_write_index(idx, f);
    fclose(f);
    if (rc == 0) { *out = buf; *out_len = len; return 0; }
    free(buf);
    return rc;
}
*/
import "C"

import (
	"fmt"
	"unsafe"
)

// FlatIPIndex wraps a faiss IndexFlat (inner-product metric).
type FlatIPIndex struct {
	Dim  int
	size int
	idx  *C.FaissIndex
}

// NewFlatIPIndex creates an empty inner-product flat index.
func NewFlatIPIndex(dim int) (*FlatIPIndex, error) {
	var idx *C.FaissIndex
	if rc := C.build_flat_ip(&idx, C.int(dim)); rc != 0 {
		return nil, fmt.Errorf("faiss index_factory failed: %s",
			C.GoString(C.faiss_get_last_error()))
	}
	return &FlatIPIndex{Dim: dim, idx: idx}, nil
}

// Add appends vectors; insertion order defines the positional node ids.
func (f *FlatIPIndex) Add(vectors [][]float32) error {
	if len(vectors) == 0 {
		return nil
	}
	flat := make([]float32, 0, len(vectors)*f.Dim)
	for _, v := range vectors {
		flat = append(flat, v...)
	}
	if rc := C.add_vectors(f.idx, C.int64_t(len(vectors)), C.int64_t(f.Dim),
		(*C.float)(&flat[0])); rc != 0 {
		return fmt.Errorf("faiss Index_add failed: %s",
			C.GoString(C.faiss_get_last_error()))
	}
	f.size += len(vectors)
	return nil
}

// Serialize returns the faiss::write_index bytes.
func (f *FlatIPIndex) Serialize() ([]byte, error) {
	var buf *C.char
	var bufLen C.size_t
	if rc := C.write_index_buffer(f.idx, &buf, &bufLen); rc != 0 {
		return nil, fmt.Errorf("faiss write_index failed: %s",
			C.GoString(C.faiss_get_last_error()))
	}
	defer C.free(unsafe.Pointer(buf))
	return C.GoBytes(unsafe.Pointer(buf), C.int(bufLen)), nil
}

// Size returns the number of indexed vectors.
func (f *FlatIPIndex) Size() int { return f.size }
