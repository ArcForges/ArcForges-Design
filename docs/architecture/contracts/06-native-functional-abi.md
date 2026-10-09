# Initial Functional Native ABI and Managed Packages

Authority: [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010), amended for the PDF surface by [P2-022](../../decisions/phase-2-specification-decisions.md#rule-p2-022). This is the complete required initial producer surface for [native mechanisms](../12-native-interop-and-media.md), not product source. WP13 implements and publishes it before Scope consumers. Existing published packages currently establish version/build/error probes and real dependencies only. Functional completion must not be inferred from those probes.

## 1. Compatibility, value and ownership profile

Keep `arc_image_get_abi_version`, `_get_build_info` and `_get_last_error` exactly as shipped. Common ABI major1/minor0 POD layout remains immutable. Functional additions advertise minor1 and a capability manifest; an old client can still use all old exports. New libraries use the owned prefixes below and the same preamble. Adding a function is compatible; changing its meaning/layout is a new major/profile. No `af_*` rename of a published export.

`arc_status_t=int32_t`, `arc_bool_t=uint8_t`. Existing values: OK0, BUFFER_TOO_SMALL1, INVALID_ARGUMENT-1, NOT_FOUND-2, UNSUPPORTED-3, IO-4, CANCELLED-5, VERSION_MISMATCH-6, CORRUPT-7, OUT_OF_MEMORY-8, RESOURCE_LIMIT-9, CLOSED = -10, BUSY = -11, PERMISSION_DENIED-12, INTERNAL-13. Add END_OF_STREAM2 and WOULD_BLOCK3. Only a nonnegative status defined for that function is success/control progress. A native exception is caught at the export boundary and reported; an access violation is contained by the process boundary, never claimed catchable by C#.

All platforms are64bit, C17 ABI/C++20 implementation, Cdecl and pack8. Frozen types remain: `arc_string_view_t{const char* data;uint64_t size;}`16bytes; `arc_byte_view_t{const void* data;uint64_t size;}`16; `arc_mut_buffer_t{void* data;uint64_t capacity;uint64_t required;}`24; `arc_rational_t{int64_t numerator,denominator;}`16; `arc_time_range_t{arc_rational_t start,duration;}`32; existing error48 and cancel24bytes. Views never include an implicit NUL. UTF8 must be valid, bounded and free of embedded NUL where a name is required. A rational denominator is positive, reduced; arithmetic checks overflow.

New records begin `uint32_t struct_size,struct_version` (version1). Required known prefix must fit; absent optional tail is default, unknown tail is ignored only for the same version. Callers zero initialize padding/tails. Native writes only caller size and validates every count/offset multiplication. No compiler enum/bool, STL, exceptions, .NET object or platform struct enters ABI. `arc_handle_t=uint64_t` is an opaque nonzero generation-checked token local to one library/process, not a pointer or durable ID. Zero output on failure, no partially-owned output. Wrong-kind/stale token refuses; double close returns CLOSED. Close waits for borrowed calls, then invalidates generation. A handle is single-caller; cancellation may be signalled concurrently through the existing callback token. Children retain their parent internally until released. C# owns every token with a dedicated SafeHandle; no naked token in a product domain.

Every call returning text/bytes through `arc_mut_buffer_t*` first sets required; insufficient capacity returns BUFFER_TOO_SMALL without consuming a reader/writer state or partially modifying the output. Repeating the same call is safe. Per-handle last error is copied into the calling thread's bounded error slot and read immediately on failure; diagnostic text≤4096bytes, no original path/secret. Progress/cancel callbacks cannot re-enter the same object, throw across ABI or outlive the call/registered device. Input views are borrowed only for the call; persistent options/config bytes are copied on successful creation.

## 2. C declaration model

The following record declarations are normative. Include the unchanged common header. `ARC_IO_READ=1`, WRITE=2; null callback refuses the corresponding operation. Callback implementations use already-brokered bounded input/output, never resolve arbitrary paths. A callback returns actual bytes in `*done`; short read at source end is allowed, other failures are explicit. Size is fixed for an opened input; writer size grows only through its callback. No callback may issue user-facing RPC or hold a managed monitor while blocking.

```c
typedef uint64_t arc_handle_t;
typedef arc_status_t (ARC_ABI_CALL *arc_read_at_fn)(void*,uint64_t,void*,uint64_t,uint64_t*);
typedef arc_status_t (ARC_ABI_CALL *arc_write_at_fn)(void*,uint64_t,const void*,uint64_t,uint64_t*);
typedef arc_status_t (ARC_ABI_CALL *arc_flush_fn)(void*);
#pragma pack(push,8)
typedef struct arc_io_v1 {
    uint32_t struct_size,struct_version;
    void* context;
    uint64_t length,max_length;
    arc_read_at_fn read_at;
    arc_write_at_fn write_at;
    arc_flush_fn flush;
} arc_io_v1;
typedef struct arc_limits_v1 {
    uint32_t struct_size,struct_version;
    uint64_t max_input_bytes,max_memory_bytes,max_output_bytes;
    uint32_t max_width,max_height,max_items,timeout_ms;
} arc_limits_v1;
typedef struct arc_frame_v1 {
    uint32_t struct_size,struct_version;
    arc_handle_t buffer;
    uint64_t sequence;
    int64_t pts,duration;
    arc_rational_t time_base;
    uint32_t kind,format,width,height,sample_rate,channels;
    uint64_t sample_count,byte_length;
    uint32_t flags,reserved;
} arc_frame_v1;
typedef struct arc_region_v1 {
    uint32_t struct_size,struct_version;
    uint32_t x,y,width,height;
    uint64_t first_sample,sample_count,row_stride;
} arc_region_v1;
typedef struct arc_instrument_options_v1 {
    uint32_t struct_size,struct_version;
    arc_string_view_t device_id;
    uint32_t transport,interface_number,baud,data_bits;
    uint32_t parity,stop_bits,flow_control,reserved;
} arc_instrument_options_v1;
typedef struct arc_transfer_v1 {
    uint32_t struct_size,struct_version;
    uint32_t kind,endpoint,timeout_ms,request_type;
    uint32_t request,value,index,reserved;
} arc_transfer_v1;
typedef struct arc_image_options_v1 {
    uint32_t struct_size,struct_version;
    uint32_t subimage,mip,format,reserved;
    arc_limits_v1 limits;
} arc_image_options_v1;
/* Retired by [P2-022](../../decisions/phase-2-specification-decisions.md#rule-p2-022): arc_pdf_page_v1 is no longer part of the normative layout; kept as history. */
typedef struct arc_pdf_page_v1 {
    uint32_t struct_size,struct_version;
    uint32_t page_index,rotation;
    double width_points,height_points;
} arc_pdf_page_v1;
#pragma pack(pop)
```

Record sizes/offsets are generated into ABI fixture metadata from these declarations and checked by independent C17/C++/C# consumers on each RID; frozen POD sizes above are fixed constants. A fixture generator cannot silently change the normative field order. `arc_limits_v1` requires positive limits; caller limits cannot exceed the signed producer hard profile. Defaults:65535x65535image with pixel-count≤268435456,64MiB per read/output tile,64open handles per library context. Hostile helper memory is selected before launch from validated dimensions within512MiB–4GiB; parent admission checks available memory, and decode cannot increase its OS limit. Insufficient host resources produce a preflight resource refusal, not a narrower advertised format claim.

Closed numeric keys: stream/frame kind video1/audio2/subtitle3/data4; format rgba8=1/rgba32fLinearPremultiplied=2/float32Interleaved=3. Unknown requested keys refuse.

Instrument transport serial1/usb2; parity none0/odd1/even2, stop one1/two2, flow none0/rtsCts1/xonXoff2. USB transfer kind control1/bulk2/interrupt3, serial read4/write5; timeout1–30000ms, bulk/serial≤1MiB, control≤65535bytes.

## 3. Exported functions and wrapper mapping

All declarations below use `ARC_ABI_EXPORT arc_status_t ARC_ABI_CALL` before the name and `;` after the arguments. This uniform declaration expansion is the complete signature, not an invitation to invent extra flags or parameters. Nullable cancel means no requested cancellation; all other pointers are required unless stated. Each library also exports its three probe functions with the already-shipped signatures. Every create/open has a matching close/release below.

| C export and exact arguments | Managed capability / result |
|---|---|
| `arc_instruments_list(uint32_t transport,arc_mut_buffer_t* devices)` | Instruments.List → stable OS/USB identities, not an implicit grant |
| `arc_instruments_open(const arc_instrument_options_v1* options,arc_handle_t* device)` | SelectedInstrument.Open, claim only explicit interface |
| `arc_instruments_read(arc_handle_t device,const arc_transfer_v1* transfer,arc_mut_buffer_t* data,uint64_t* actual,const arc_cancel_token_t* cancel)` | ReadAsync/ControlRead; partial count and timeout distinct |
| `arc_instruments_write(arc_handle_t device,const arc_transfer_v1* transfer,arc_byte_view_t data,uint64_t* actual,const arc_cancel_token_t* cancel)` | WriteAsync/ControlWrite, no implicit resend after partial write |
| `arc_instruments_cancel(arc_handle_t device)` | Cancel outstanding transfer and wait for completion callback |
| `arc_instruments_close(arc_handle_t device)` | Release claimed interface/serial handle; no lingering callback |
| `arc_image_open(const arc_io_v1* io,const arc_image_options_v1* options,arc_handle_t* image,arc_mut_buffer_t* metadata,const arc_cancel_token_t* cancel)` | ImageReader.Open/Probe |
| `arc_image_read(arc_handle_t image,const arc_region_v1* region,arc_mut_buffer_t* pixels,const arc_cancel_token_t* cancel)` | ReadRegionAsync, explicit packed output in the format selected by `arc_image_options_v1.format` at `arc_image_open` (`rgba8`, `rgba32fLinearPremultiplied` or `float32Interleaved`) |
| `arc_image_close(arc_handle_t image)` | ImageReader.Dispose |
| `arc_pdf_*` (open, page_info, render, text, close) | **Retired** ([P2-022](../../decisions/phase-2-specification-decisions.md#rule-p2-022)): the arcpdf ABI, ArcPdfNative, its exports, PDF vectors and the library name are retired and their dormant code is not removed in V1 (dormant-engine removal is out of scope under P2-026; NAT.32 is its out-of-scope retirement record); the names are reserved and never reused. In V1, `arc_pdf_open` returns `ARC_UNSUPPORTED` (`backend_none`), the fail-closed refusal that P2-022 item 3 keeps. |

Image regions transfer at most64MiB each, validate checked dimensions/stride and cover each pixel exactly once in raster order; finish refuses missing/overlapping tiles. These paths support the admitted large images/8K frame profile without a single giant RPC message. Raw native frame bytes are not embedded in this metadata. The wrapper public methods have the parameters in the table (typed options instead of raw numeric keys), immutable result DTOs, CancellationToken on bounded asynchronous work, and IAsyncDisposable where draining is required; they do not expose arbitrary library options dictionaries.

**Image clarification (planning repair 2026-10-09; recorded on [NAT.11](../../planning/delivery/lanes/native.md#task-nat-11)).** This clarification adds no export and no record layout.
- **Version and capabilities.** The shared common-ABI header keeps minor 0. Once ArcImageNative carries the functional exports, `arc_image_get_abi_version` keeps its shipped signature and reports major 1, minor 1. The `arc_image_get_build_info` JSON then carries the capability manifest as a closed list: `image.open`, `image.read` and `image.close`, with the formats `png`, `tiff` and `exr`.
- **Formats.** The image library accepts only PNG, TIFF and EXR, identified by content probing. Every other format, including any other format that OpenImageIO can decode, is refused with `UNSUPPORTED`. EXR multipart parts and mip levels are subimages within the bounded subimage and mip counts.
- **Coverage.** No finish export exists. The "finish" above is satisfied in two places:
  - `arc_image_read` refuses an overlapping region, or one out of raster order, with `INVALID_ARGUMENT`, and changes no state. Each handle tracks its coverage.
  - The managed `ImageReader` completion step refuses missing coverage with a typed failure.
- **Pixel conversion and loss.** Bit-depth mapping follows OpenImageIO's documented type conversion, with rounding and clamping.
  - `rgba8` is 8-bit unorm with straight alpha and no transfer change.
  - `rgba32fLinearPremultiplied` converts sRGB to linear only when the source reports an sRGB colour space, and premultiplies when the source alpha is unassociated.
  - `float32Interleaved` keeps the source channels as float32, with no transfer or alpha change.
  - A missing alpha becomes 1. Grey is replicated to RGB for the RGBA formats.
  - Every lossy step, such as bit-depth reduction or clamping, is reported in the metadata.
  - Colour-management transforms are out of scope. The source colour space is reported, not converted.
- **Cancellation.** Cancellation is observed at the `arc_io_v1` callbacks and at tile boundaries. An in-flight codec call is not interrupted.

## 4. State, format and upstream implementation mapping

| Operation family | Required algorithm/boundary and independent acceptance |
|---|---|
| Instruments | OS serial and libusb async transfers behind the owned shim. Enumeration sorted stable identity, max256devices, descriptors≤64KiB each. Open revalidates identity; USB interface claiming cannot detach unrelated kernel drivers automatically. Partial writes are effects and never blindly retried. Capture owner records gaps/time uncertainty. |
| Images | OIIO/ImageInput APIs are allowed only in the sandbox (PDF retired by [P2-022](../../decisions/phase-2-specification-decisions.md#rule-p2-022)). Baseline image PNG/TIFF/EXR codec metadata/bit depth preserved with explicit conversion loss. Request bounds precede decode allocation. |

Image metadata is bounded subimage/mip counts and bounded channel names/types. Device list is `{version,devices:[{id,name,transport,vendorId?,productId?,serial?,interfaces:[{number,endpoints:[{address,kind,maxPacketBytes}]}]}]}`; this is descriptive only. These are closed private ABI metadata encodings, not new business RPC authorities.

## 5. Package and process closure

Image uses ArcImageNative (moved to `native/arcimage-abi`; its `arc_image_*` symbols are unchanged). New Instruments libraries use ArcInstrumentsNative; the Pdf library ArcPdfNative is retired ([P2-022](../../decisions/phase-2-specification-decisions.md#rule-p2-022)). Managed packages are `ArcForges.Native.<Capability>` plus exactly one explicitly referenced `Runtime.<rid>` sibling; Native.Abstractions owns common status/handles only. Existing Instruments libusb assets stay compatible; future Instruments closure records and deduplicates any identical shared-library filename by hash, and conflicting same-name dependencies fail packaging. Consumer never invokes CMake/vcpkg.

RID/tier and pinned upstream versions remain in [platform matrix](../21-platform-and-dependency-matrix.md) and [package registry](../01-solution-and-project-layout.md#12-package-and-native-distribution-registry). Every admitted RID records actual transitive library filenames/hashes, exports, system dependencies, source/patch/license closure, SBOM, signatures and helper profile. Optional accelerated export formats do not replace portable required profiles. LGPL redistributability and dynamic replacement/source notices remain mandatory.

`sandbox.buffer.v1` is the typed gRPC buffer-seal/ack profile of ContentSandboxService in [local09](09-local-grpc-and-sandbox.md#4-restricted-launch-and-os-resources). Parent provisions immutable input and at most3slots×64MiB before parsing through finite OS handle handoff. All grant/read/seal/ack/cancel/status controls use authored proto/native gRPC. No raw pointer is serialized. Parent binds generation/sequence, validates geometry/stride/coverage, copies the declared bytes into admitted private memory and checks digest on that copy before use. Slot reuse follows matching acknowledgement; cancellation, timeout or parent death invalidates the invocation and cleans every mapping. Pixel tiles<=2048squareRGBA32f; full-frame memory is separately admitted. The complete parser operation bindings and lifetime are in registry04/local09; a private XPC command protocol is not permitted.

## 6. Producer closure evidence

WP13 produces the complete declaration/export/layout manifest, wrapper mapping and package closure before product work. Each function has at least success, invalid-size/state, cancel/error, ownership and repeat/EOF tests applicable to it. Independent vectors include RGB/alpha identity,2x2regions, UART partial write, USB cancellation callback, PNG/EXR round trip. C17 and C# AOT consumers restore only candidate packages, execute real libraries/helpers and verify no handle/buffer growth after repeated cancellation. Required RIDs pass actual OS containment, throughput/memory and malformed-input tests. Sanitizer/fuzz/CTest replace the removed C++ CodeQL requirement; C# scanning remains.

This document defines signatures and evidence to implement. It does not claim that these exports, packages, ABI fixtures or runtime tests already exist or pass.

## 7. Normative 64-bit record sizes

Under the declared pack8 profile, sizes are: io56, limits48, frame104, region48, instrument_options56, transfer40 and image_options72 bytes (each name is arc_<name>_v1; the pdf_page32 size is retired by [P2-022](../../decisions/phase-2-specification-decisions.md#rule-p2-022)). WP13 checks exact field offsets as well as these sizes on each admitted RID. The document-review C17/C++20 compile against the existing shared header confirms declaration/layout consistency on Windows x64 only; it does not execute a functional native implementation.
