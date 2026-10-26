// Package embed runs the exported mpnet ONNX model through the onnxruntime
// C API and mean-pools with the attention mask, matching the torch pipeline.
package embed

/*
#cgo LDFLAGS: -lonnxruntime
// header/library paths come from CGO_CFLAGS/CGO_LDFLAGS (scripts/stage-go-native.sh)
#include <stdlib.h>
#include <string.h>
#include <onnxruntime_c_api.h>

static OrtEnv* g_env = NULL;
static OrtSession* g_session = NULL;
static OrtMemoryInfo* g_meminfo = NULL;

static const OrtApi* ortapi(void) { return OrtGetApiBase()->GetApi(ORT_API_VERSION); }

int ort_init(const char* model_path, int threads) {
    const OrtApi* api = ortapi();
    if (api->CreateEnv(ORT_LOGGING_LEVEL_ERROR, "byok", &g_env) != NULL) return 1;
    OrtSessionOptions* opts = NULL;
    if (api->CreateSessionOptions(&opts) != NULL) return 2;
    api->SetIntraOpNumThreads(opts, threads);
    api->SetSessionGraphOptimizationLevel(opts, ORT_ENABLE_ALL);
    OrtStatus* st = api->CreateSession(g_env, model_path, opts, &g_session);
    api->ReleaseSessionOptions(opts);
    if (st != NULL) return 3;
    if (api->CreateCpuMemoryInfo(OrtArenaAllocator, OrtMemTypeDefault, &g_meminfo) != NULL) return 4;
    return 0;
}

// ort_run performs one batched forward pass. ids/mask hold batch*seq_len
// elements (row-major). On success *out points to a malloc'd buffer holding
// batch*seq_len*dim floats.
int ort_run(const int64_t* ids, const int64_t* mask, int64_t batch,
            int64_t seq_len, int64_t dim, float** out, int64_t* out_len) {
    const OrtApi* api = ortapi();
    int64_t in_shape[2] = {batch, seq_len};
    size_t elems = (size_t)(batch * seq_len);
    OrtValue* in_ids = NULL;
    OrtValue* in_mask = NULL;
    if (api->CreateTensorWithDataAsOrtValue(g_meminfo, (void*)ids, elems * 8,
            in_shape, 2, ONNX_TENSOR_ELEMENT_DATA_TYPE_INT64, &in_ids) != NULL) return 1;
    if (api->CreateTensorWithDataAsOrtValue(g_meminfo, (void*)mask, elems * 8,
            in_shape, 2, ONNX_TENSOR_ELEMENT_DATA_TYPE_INT64, &in_mask) != NULL) return 2;
    const char* in_names[2] = {"input_ids", "attention_mask"};
    const char* out_names[1] = {"last_hidden_state"};
    const OrtValue* inputs[2] = {in_ids, in_mask};
    OrtValue* output = NULL;
    OrtStatus* st = api->Run(g_session, NULL, in_names, inputs, 2, out_names, 1, &output);
    api->ReleaseValue(in_ids);
    api->ReleaseValue(in_mask);
    if (st != NULL) return 3;

    OrtTensorTypeAndShapeInfo* info = NULL;
    if (api->GetTensorTypeAndShape(output, &info) != NULL) { api->ReleaseValue(output); return 4; }
    size_t rank = 0;
    if (api->GetDimensionsCount(info, &rank) != NULL || rank != 3) {
        api->ReleaseTensorTypeAndShapeInfo(info); api->ReleaseValue(output); return 5;
    }
    int64_t dims[3];
    if (api->GetDimensions(info, dims, rank) != NULL) {
        api->ReleaseTensorTypeAndShapeInfo(info); api->ReleaseValue(output); return 6;
    }
    api->ReleaseTensorTypeAndShapeInfo(info);
    int64_t count = dims[0] * dims[1] * dims[2];
    if (dims[2] != dim || dims[0] != batch || dims[1] != seq_len) {
        api->ReleaseValue(output); return 7;
    }
    float* data = NULL;
    if (api->GetTensorMutableData(output, (void**)&data) != NULL) { api->ReleaseValue(output); return 8; }
    float* copy = malloc((size_t)(count * sizeof(float)));
    if (!copy) { api->ReleaseValue(output); return 9; }
    memcpy(copy, data, (size_t)(count * sizeof(float)));
    api->ReleaseValue(output);
    *out = copy;
    *out_len = count;
    return 0;
}
*/
import "C"

import (
	"fmt"
	"math"
	"sort"
	"unsafe"

	"github.com/openshift/lightspeed-rag-content/internal/tokenizer"
)

const padToken = 1 // <pad>

// Embedder runs the ONNX mpnet model and mean-pools with the attention mask.
type Embedder struct {
	Dim       int
	MaxSeqLen int
	BatchSize int
	tokenizer *tokenizer.Tokenizer
}

// NewEmbedder initializes onnxruntime with the given model and thread count.
func NewEmbedder(modelPath string, tok *tokenizer.Tokenizer, dim, maxSeqLen, threads int) (*Embedder, error) {
	cpath := C.CString(modelPath)
	defer C.free(unsafe.Pointer(cpath))
	if rc := C.ort_init(cpath, C.int(threads)); rc != 0 {
		return nil, fmt.Errorf("onnxruntime init failed with code %d", rc)
	}
	return &Embedder{
		Dim:       dim,
		MaxSeqLen: maxSeqLen,
		BatchSize: 1, // measured optimal for long-chunk CPU workloads; see README
		tokenizer: tok,
	}, nil
}

// Embed tokenizes text, runs the model, and returns the pooled vector.
func (e *Embedder) Embed(text string) ([]float32, error) {
	vectors, err := e.EmbedBatch([]string{text})
	if err != nil {
		return nil, err
	}
	return vectors[0], nil
}

// EmbedBatch embeds texts in length-sorted batches (to minimize padding) and
// returns the vectors in input order. Padding is masked out of the mean pool,
// so results are independent of batch composition up to float noise.
func (e *Embedder) EmbedBatch(texts []string) ([][]float32, error) {
	if len(texts) == 0 {
		return nil, nil
	}
	sequences := make([][]int, len(texts))
	for i, text := range texts {
		ids := e.tokenizer.Tokenize(text)
		if len(ids) > e.MaxSeqLen {
			ids = ids[:e.MaxSeqLen]
		}
		if len(ids) < 2 {
			return nil, fmt.Errorf("text %d produced no tokens", i)
		}
		sequences[i] = ids
	}

	order := make([]int, len(texts))
	for i := range order {
		order[i] = i
	}
	sort.SliceStable(order, func(a, b int) bool {
		return len(sequences[order[a]]) > len(sequences[order[b]])
	})

	vectors := make([][]float32, len(texts))
	for start := 0; start < len(order); start += e.BatchSize {
		end := start + e.BatchSize
		if end > len(order) {
			end = len(order)
		}
		batch := order[start:end]
		if err := e.embedBatch(vectors, sequences, batch); err != nil {
			return nil, err
		}
	}
	return vectors, nil
}

func (e *Embedder) embedBatch(vectors [][]float32, sequences [][]int, batch []int) error {
	seqLen := 0
	for _, idx := range batch {
		if l := len(sequences[idx]); l > seqLen {
			seqLen = l
		}
	}
	rows := len(batch)
	ids := make([]C.int64_t, rows*seqLen)
	mask := make([]C.int64_t, rows*seqLen)
	for r, idx := range batch {
		seq := sequences[idx]
		for pos := 0; pos < seqLen; pos++ {
			at := r*seqLen + pos
			if pos < len(seq) {
				ids[at] = C.int64_t(seq[pos])
				mask[at] = 1
			} else {
				ids[at] = padToken
				mask[at] = 0
			}
		}
	}

	var out *C.float
	var outLen C.int64_t
	if rc := C.ort_run(&ids[0], &mask[0], C.int64_t(rows), C.int64_t(seqLen),
		C.int64_t(e.Dim), &out, &outLen); rc != 0 {
		return fmt.Errorf("onnxruntime run failed with code %d", rc)
	}
	defer C.free(unsafe.Pointer(out))
	hidden := unsafe.Slice((*float32)(unsafe.Pointer(out)), int(outLen))

	for r, idx := range batch {
		vector := make([]float32, e.Dim)
		valid := 0
		for pos := 0; pos < seqLen; pos++ {
			if mask[r*seqLen+pos] == 0 {
				continue
			}
			valid++
			base := (r*seqLen + pos) * e.Dim
			for i := range vector {
				vector[i] += hidden[base+i]
			}
		}
		for i := range vector {
			vector[i] /= float32(valid)
		}
		// The Python pipeline (llama_index HuggingFaceEmbedding) stores
		// L2-normalized embeddings; vector norms in real indexes are 1.0.
		var norm float64
		for _, v := range vector {
			norm += float64(v) * float64(v)
		}
		norm = math.Sqrt(norm)
		if norm > 0 {
			for i := range vector {
				vector[i] /= float32(norm)
			}
		}
		vectors[idx] = vector
	}
	return nil
}
