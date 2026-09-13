# Initial Functional Native ABI and Managed Packages

Authority: [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010). This is the complete required initial producer surface for [native mechanisms](../12-native-interop-and-media.md), not product source. WP13 implements and publishes it before Scope/Slate/Notes consumers. Existing published packages currently establish version/build/error probes and real dependencies only. Functional completion must not be inferred from those probes.

## 1. Compatibility, value and ownership profile

Keep `arc_{media,color,image,otio}_get_abi_version`, `_get_build_info` and `_get_last_error` exactly as shipped. Common ABI major1/minor0 POD layout remains immutable. Functional additions advertise minor1 and a capability manifest; an old client can still use all old exports. New libraries use the owned prefixes below and the same preamble. Adding a function is compatible; changing its meaning/layout is a new major/profile. No `af_*` rename of a published export.

`arc_status_t=int32_t`, `arc_bool_t=uint8_t`. Existing values: OK0, BUFFER_TOO_SMALL1, INVALID_ARGUMENT-1, NOT_FOUND-2, UNSUPPORTED-3, IO-4, CANCELLED-5, VERSION_MISMATCH-6, CORRUPT-7, OUT_OF_MEMORY-8, RESOURCE_LIMIT-9, CLOSED-10, BUSY-11, PERMISSION_DENIED-12, INTERNAL-13. Add END_OF_STREAM2 and WOULD_BLOCK3. Only a nonnegative status defined for that function is success/control progress. A native exception is caught at the export boundary and reported; an access violation is contained by the process boundary, never claimed catchable by C#.

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
typedef struct arc_stream_v1 {
    uint32_t struct_size,struct_version;
    uint32_t index,kind,codec,flags;
    arc_rational_t time_base,frame_rate;
    int64_t start_pts,duration_pts;
    uint32_t width,height,sample_rate,channels;
} arc_stream_v1;
typedef struct arc_reader_options_v1 {
    uint32_t struct_size,struct_version;
    uint32_t stream_index,output_format;
    arc_limits_v1 limits;
} arc_reader_options_v1;
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
typedef struct arc_video_convert_v1 {
    uint32_t struct_size,struct_version;
    uint32_t width,height,format,filter;
    uint32_t input_matrix,input_range,output_matrix,output_range;
} arc_video_convert_v1;
typedef struct arc_audio_convert_v1 {
    uint32_t struct_size,struct_version;
    uint32_t input_rate,output_rate,input_channels,output_channels;
    uint32_t quality,reserved;
} arc_audio_convert_v1;
typedef struct arc_writer_options_v1 {
    uint32_t struct_size,struct_version;
    uint32_t profile,width,height,sample_rate,channels;
    uint32_t video_bitrate,audio_bitrate,flags;
    arc_rational_t frame_rate,time_base;
    arc_limits_v1 limits;
} arc_writer_options_v1;
typedef struct arc_device_options_v1 {
    uint32_t struct_size,struct_version;
    arc_string_view_t device_id;
    uint32_t direction,sample_rate,channels,ring_frames;
} arc_device_options_v1;
typedef struct arc_device_state_v1 {
    uint32_t struct_size,struct_version;
    uint32_t state,sample_rate,channels,reason;
    uint64_t clock_frames,overflow_frames,underrun_frames;
} arc_device_state_v1;
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
typedef struct arc_colour_options_v1 {
    uint32_t struct_size,struct_version;
    arc_string_view_t input_space,output_space,display,view;
    uint32_t direction,alpha_mode;
} arc_colour_options_v1;
typedef struct arc_pdf_page_v1 {
    uint32_t struct_size,struct_version;
    uint32_t page_index,rotation;
    double width_points,height_points;
} arc_pdf_page_v1;
typedef struct arc_surface_options_v1 {
    uint32_t struct_size,struct_version;
    uint32_t width,height,format,backend;
    uint64_t parent_window_token;
} arc_surface_options_v1;
#pragma pack(pop)
```

Record sizes/offsets are generated into ABI fixture metadata from these declarations and checked by independent C17/C++/C# consumers on each RID; frozen POD sizes above are fixed constants. A fixture generator cannot silently change the normative field order. `arc_limits_v1` requires positive limits; caller limits cannot exceed the signed producer hard profile. Defaults:64streams,8192x8192video,65535x65535image with pixel-count≤268435456,64MiB per read/output tile,64open handles per library context. Hostile decoder helper memory is selected before launch from validated dimensions within512MiB–4GiB; parent admission checks available memory, and decode cannot increase its OS limit. An8192-square float frame can be held inside the4GiB helper and transferred by tiles. Insufficient host resources produce a preflight resource refusal, not a narrower advertised format claim.

Closed numeric keys: stream/frame kind video1/audio2/subtitle3/data4; format rgba8=1/rgba32fLinearPremultiplied=2/float32Interleaved=3; codec unknown0/ffv1=1/pcmS24le=2/mpeg4Part2=3/aac=4/otherDecoder=5 (name in metadata); frame flags keyframe1/endPadding2/estimatedDuration4; writer profile matroskaFfv1Pcm1/wavPcm2/mp4Mpeg4Aac3. Unknown requested keys refuse; probe metadata may report otherDecoder without authorizing its encoder.

Video conversion filter nearest1/bilinear2/lanczos3=3; matrix RGB1/BT7092/BT6013/BT2020=4; range full1/limited2. Audio quality baseline1 fixes the pinned libswresample build/profile. Device direction input1/output2; state stopped1/running2/disconnected3/failed4. Instrument transport serial1/usb2; parity none0/odd1/even2, stop one1/two2, flow none0/rtsCts1/xonXoff2. USB transfer kind control1/bulk2/interrupt3, serial read4/write5; timeout1–30000ms, bulk/serial≤1MiB, control≤65535bytes. Colour direction forward1/inverse2, alpha premultiplied1/straight2. Surface backend CPU1/OSAccelerated2; no caller-supplied native GPU pointer.

## 3. Exported functions and wrapper mapping

All declarations below use `ARC_ABI_EXPORT arc_status_t ARC_ABI_CALL` before the name and `;` after the arguments. This uniform declaration expansion is the complete signature, not an invitation to invent extra flags or parameters. Nullable cancel means no requested cancellation; all other pointers are required unless stated. Each library also exports its three probe functions with the already-shipped signatures. Every create/open has a matching close/release below.

| C export and exact arguments | Managed capability / result |
|---|---|
| `arc_media_probe(const arc_io_v1* io,const arc_limits_v1* limits,arc_mut_buffer_t* metadata,const arc_cancel_token_t* cancel)` | `MediaProbe.ReadAsync(BrokerInput,NativeLimits,CancellationToken)` → immutable MediaInfo |
| `arc_media_reader_open(const arc_io_v1* io,const arc_reader_options_v1* options,arc_handle_t* reader)` | `MediaReader.Open(BrokerInput,StreamSelection)` → owned MediaReader |
| `arc_media_reader_stream(arc_handle_t reader,arc_stream_v1* stream,arc_mut_buffer_t* metadata)` | StreamInfo plus bounded metadata |
| `arc_media_reader_seek(arc_handle_t reader,int64_t pts,arc_rational_t time_base,const arc_cancel_token_t* cancel)` | SeekAsync(SourceTime); flushes buffered old frames and resets decoder state |
| `arc_media_reader_next(arc_handle_t reader,arc_frame_v1* frame,const arc_cancel_token_t* cancel)` | ReadAsync → owned VideoFrame/AudioBlock or EOF |
| `arc_media_reader_close(arc_handle_t reader)` | MediaReader.Dispose |
| `arc_media_buffer_copy(arc_handle_t buffer,const arc_region_v1* region,arc_mut_buffer_t* output)` | Frame.CopyRegion/AudioBlock.CopySamples into caller memory |
| `arc_media_buffer_create(const arc_frame_v1* description,const arc_byte_view_t* bytes,arc_handle_t* buffer)` | Copy validated caller frame/audio into owned input buffer |
| `arc_media_buffer_release(arc_handle_t buffer)` | Frame/AudioBlock.Dispose |
| `arc_media_video_convert(arc_handle_t input,const arc_video_convert_v1* options,arc_handle_t* output,const arc_cancel_token_t* cancel)` | Convert/ScaleAsync → owned video buffer |
| `arc_media_resampler_create(const arc_audio_convert_v1* options,arc_handle_t* resampler)` | AudioResampler.Create |
| `arc_media_resampler_push(arc_handle_t resampler,arc_handle_t input,arc_handle_t* output,const arc_cancel_token_t* cancel)` | PushAsync → audio output; zero output means buffered, not EOF |
| `arc_media_resampler_drain(arc_handle_t resampler,arc_handle_t* output)` | Drain to EOF, all retained samples accounted |
| `arc_media_resampler_close(arc_handle_t resampler)` | AudioResampler.Dispose |
| `arc_media_writer_open(const arc_io_v1* io,const arc_writer_options_v1* options,arc_handle_t* writer)` | MediaWriter.Open on staged output only |
| `arc_media_writer_write(arc_handle_t writer,arc_handle_t buffer,int64_t pts,arc_rational_t time_base,const arc_cancel_token_t* cancel)` | WriteVideo/WriteAudioAsync; caller retains buffer |
| `arc_media_writer_finish(arc_handle_t writer,const arc_cancel_token_t* cancel)` | Drain encoders, mux trailer, flush; output still awaits parent commit/hash |
| `arc_media_writer_abort(arc_handle_t writer)` | Abort staged writer; no trailer/success claim |
| `arc_media_writer_close(arc_handle_t writer)` | Dispose; unfinished output treated aborted |
| `arc_media_audio_devices(uint32_t direction,arc_mut_buffer_t* devices)` | AudioDevices.List → bounded device identities/formats |
| `arc_media_audio_open(const arc_device_options_v1* options,arc_handle_t* device,arc_device_state_v1* actual)` | AudioDevice.Open; negotiated format explicit |
| `arc_media_audio_start(arc_handle_t device)` | Start |
| `arc_media_audio_read(arc_handle_t device,arc_mut_buffer_t* samples,uint64_t max_frames,uint64_t* frames,const arc_cancel_token_t* cancel)` | ReadAsync interleaved float32; WOULD_BLOCK if empty |
| `arc_media_audio_write(arc_handle_t device,arc_byte_view_t samples,uint64_t frames,uint64_t* accepted,const arc_cancel_token_t* cancel)` | WriteAsync; partial accepted count explicit |
| `arc_media_audio_state(arc_handle_t device,arc_device_state_v1* state)` | Clock and lost-frame counters |
| `arc_media_audio_stop(arc_handle_t device,arc_bool_t drain,const arc_cancel_token_t* cancel)` | Stop; drain output only, max2s then typed timeout |
| `arc_media_audio_close(arc_handle_t device)` | Dispose after callback deregistration |
| `arc_instruments_list(uint32_t transport,arc_mut_buffer_t* devices)` | Instruments.List → stable OS/USB identities, not an implicit grant |
| `arc_instruments_open(const arc_instrument_options_v1* options,arc_handle_t* device)` | SelectedInstrument.Open, claim only explicit interface |
| `arc_instruments_read(arc_handle_t device,const arc_transfer_v1* transfer,arc_mut_buffer_t* data,uint64_t* actual,const arc_cancel_token_t* cancel)` | ReadAsync/ControlRead; partial count and timeout distinct |
| `arc_instruments_write(arc_handle_t device,const arc_transfer_v1* transfer,arc_byte_view_t data,uint64_t* actual,const arc_cancel_token_t* cancel)` | WriteAsync/ControlWrite, no implicit resend after partial write |
| `arc_instruments_cancel(arc_handle_t device)` | Cancel outstanding transfer and wait for completion callback |
| `arc_instruments_close(arc_handle_t device)` | Release claimed interface/serial handle; no lingering callback |
| `arc_image_open(const arc_io_v1* io,const arc_image_options_v1* options,arc_handle_t* image,arc_mut_buffer_t* metadata,const arc_cancel_token_t* cancel)` | ImageReader.Open/Probe |
| `arc_image_read(arc_handle_t image,const arc_region_v1* region,arc_mut_buffer_t* pixels,const arc_cancel_token_t* cancel)` | ReadRegionAsync, explicit packed RGBA output |
| `arc_image_writer_open(const arc_io_v1* io,uint32_t profile,const arc_frame_v1* description,const arc_limits_v1* limits,arc_handle_t* writer)` | ImageWriter.Open staged PNG1/TIFF2/EXR3; dimensions/format fixed |
| `arc_image_writer_write(arc_handle_t writer,const arc_region_v1* region,arc_byte_view_t pixels,uint64_t stride,const arc_cancel_token_t* cancel)` | WriteRegionAsync, bounded64MiB tile, nonoverlapping raster-order exact coverage |
| `arc_image_writer_finish(arc_handle_t writer,const arc_cancel_token_t* cancel)` | FinishAsync validates complete coverage, codec drain/flush before parent commit |
| `arc_image_writer_abort(arc_handle_t writer)` | Abort staged output, idempotent and no publication |
| `arc_image_writer_close(arc_handle_t writer)` | Dispose after finish/abort, never silently finish on close |
| `arc_image_close(arc_handle_t image)` | ImageReader.Dispose |
| `arc_color_config_open(arc_byte_view_t config,arc_byte_view_t asset_bundle,const arc_limits_v1* limits,arc_handle_t* handle,arc_mut_buffer_t* spaces)` | ColourConfig.Open immutable config/LUT bundle, no path lookups |
| `arc_color_processor_create(arc_handle_t config,const arc_colour_options_v1* options,arc_handle_t* processor)` | ColourProcessor.Create(input/output or display/view) |
| `arc_color_apply(arc_handle_t processor,arc_byte_view_t input,uint64_t pixels,arc_mut_buffer_t* output,const arc_cancel_token_t* cancel)` | ApplyAsync RGBAfloat32; overlap denied except identical in-place memory |
| `arc_color_processor_close(arc_handle_t processor)` | ColourProcessor.Dispose |
| `arc_color_config_close(arc_handle_t config)` | ColourConfig.Dispose |
| `arc_otio_read(const arc_io_v1* input,const arc_io_v1* canonical,const arc_io_v1* fidelityEntries,const arc_limits_v1* limits,arc_mut_buffer_t* fidelity,const arc_cancel_token_t* cancel)` | Otio.ImportPreview → brokered staged typed project projection and bounded fidelity summary |
| `arc_otio_write(const arc_io_v1* canonical,const arc_io_v1* output,const arc_io_v1* fidelityEntries,const arc_limits_v1* limits,arc_mut_buffer_t* fidelity,const arc_cancel_token_t* cancel)` | Otio.ExportPreview → brokered staged official OTIO bytes and bounded fidelity summary |
| `arc_pdf_open(const arc_io_v1* io,arc_string_view_t password,const arc_limits_v1* limits,arc_handle_t* document,uint32_t* pages,const arc_cancel_token_t* cancel)` | PdfDocument.Open; empty password allowed, password required is typed denial |
| `arc_pdf_page_info(arc_handle_t document,uint32_t index,arc_pdf_page_v1* page)` | Page geometry in PDF points |
| `arc_pdf_render(arc_handle_t document,const arc_pdf_page_v1* page,const arc_region_v1* region,uint32_t full_width,uint32_t full_height,arc_mut_buffer_t* rgba8,const arc_cancel_token_t* cancel)` | RenderRegionAsync; explicit full pixel grid and clipped tile |
| `arc_pdf_text(arc_handle_t document,uint32_t page,uint32_t start,uint32_t count,arc_mut_buffer_t* text_geometry,const arc_cancel_token_t* cancel)` | ExtractTextAsync Unicode text/rectangles, max65536scalars/call |
| `arc_pdf_close(arc_handle_t document)` | PdfDocument.Dispose |
| `arc_graphics_surface_create(const arc_surface_options_v1* options,arc_handle_t* surface)` | PresentableSurface.Create, parent token resolved by owned OS adapter only |
| `arc_graphics_surface_upload(arc_handle_t surface,const arc_region_v1* region,arc_byte_view_t rgba)` | Upload validated CPU pixels |
| `arc_graphics_surface_present(arc_handle_t surface,uint64_t frame_sequence,uint64_t* fence)` | PresentAsync; returns local fence |
| `arc_graphics_surface_wait(arc_handle_t surface,uint64_t fence,uint32_t timeout_ms)` | Wait ≤1000ms; WOULD_BLOCK timeout, lost device IO |
| `arc_graphics_surface_close(arc_handle_t surface)` | Dispose after draining/abandoning device fences |

OTIO canonical/input/output use the explicit seekable broker I/O above, each bounded1GiB and the admitted helper memory budget; no implicit sequence splitting or invented alternate file format. Fidelity entries stream to the separate caller-owned fidelityEntries I/O, bounded256MiB as a canonical FidelityEntry array. The small fidelity output is exact JSON {profile,canCommit,entryCount,detailedSha256,detailedBytes}, at most4KiB; parent verifies the staged report hash and attaches its own immutable reference. No child-chosen path/reference or invented bundle format. Cancellation/overflow leaves staged outputs unpublished. Image regions transfer at most64MiB each, validate checked dimensions/stride and cover each pixel exactly once in raster order; finish refuses missing/overlapping tiles. These paths support the admitted large images/8K frame profile without a single giant RPC message. Raw native frame bytes are not embedded in this metadata. The wrapper public methods have the parameters in the table (typed options instead of raw numeric keys), immutable result DTOs, CancellationToken on bounded asynchronous work, and IAsyncDisposable where draining is required; they do not expose arbitrary library options dictionaries.

## 4. State, format and upstream implementation mapping

| Operation family | Required algorithm/boundary and independent acceptance |
|---|---|
| Probe/decode | FFmpeg avformat_open_input/find_stream_info/read_frame, avcodec_send_packet/receive_frame. Read until output or actual drained EOF; EAGAIN exchanges input/output, never error or premature EOF. PTS is retained in source time base; missing timestamp is flagged and estimated by the declared stream rate only when possible, otherwise unavailable. Test reordered B frames, audio-only, variable frame rate, truncated packet and zero-duration source. |
| Seek | avformat_seek_file backward to a safe point, avcodec_flush_buffers, reset resampler, decode forward and discard until the requested source instant. Video returns the frame whose half-open presentation interval contains target, or next known frame with an explicit gap; audio discards only source samples before target with declared rounding. Seek past known end returns EOF; failed seek leaves reader requiring a fresh successful seek/open, never old-buffer success. |
| Frame buffers | Immutable decoded frame owns source metadata and a token. Copy is row-major region/sample range with checked stride and no padding disclosure. BufferTooSmall leaves cursor unchanged. Video supports tiled regions; audio reads contiguous frames. Release every output even after cancel. |
| Convert/resample | Pinned libswscale/libswresample implementation. Matrix/range is explicit; colour-transfer/working-space management belongs to OCIO and the product profile. Audio resampler retains delay and is drained once; no rounding error is accumulated into timeline identity. Mono→stereo duplicates with centered gain policy, stereo→mono averages L/R; other layouts must be explicitly mapped before baseline writer. |
| Encode/mux | avcodec_send_frame/receive_packet with monotonic per-stream PTS, interleaved muxing, nullable-input drain and av_write_trailer. Options are only the three [portable profiles](../23-simulator-and-interchange.md#5-slate-metadata-render-and-subtitle-profiles). FFV1/PCM/WAV/MP4MPEG4-AAC output must decode in a fresh independent consumer. finish is idempotent once successful; write after finish/abort refuses. Parent atomic file/resource commit occurs only after finish, hash, origin carrier and sidecars succeed. |
| Audio device | miniaudio device/context/ring primitives. Ring capacity requested power-of-two256–65536frames; negotiate rate/channels once. Underflow emits silence and increments counter; input overflow drops oldest complete frames with exact count. Device disconnect reports last clock and loss, requires explicit reopen; never silently chooses a different device. |
| Instruments | OS serial and libusb async transfers behind the owned shim. Enumeration sorted stable identity, max256devices, descriptors≤64KiB each. Open revalidates identity; USB interface claiming cannot detach unrelated kernel drivers automatically. Partial writes are effects and never blindly retried. Capture owner records gaps/time uncertainty. |
| Images/PDF | OIIO/ImageInput/ImageOutput and PDFium document/page/text/render APIs are allowed only in the sandbox. Baseline image PNG/TIFF/EXR codec metadata/bit depth preserved with explicit conversion loss. PDF actions/JavaScript are disabled. PDF pages0-based; geometryfinitepoints/rotation0/90/180/270. Request bounds precede decode allocation. |
| Colour | OCIO immutable config/processor/CPUProcessor from pinned assets. Bundle is sorted path→bytes/hash inventory, relative paths only, no network/home search. Input/working/output names are explicit, unknown fails. Unpremultiply RGB when alpha>0, transform, premultiply; alpha0 gives RGB0. Product formulas/working-space definition are [product profiles](../26-product-behavior-profiles.md). |
| OTIO | Official OTIO read/upgrade/write and fixed permitted schema types only; canonical payload is `slate.project.v1` JSON projection of the numbered wire records (exact integer strings), with source metadata and declared unknown preserved inert fields. Fidelity uses OtioFidelityReport; all dropped/substituted fields report before commit. Numeric conversion follows OB-01 onward, not naive double multiplication. |
| Graphics | OS adapter verifies window ownership and creates CPU or admitted accelerator surface. Upload/present/fence lifecycle is bounded; device loss invalidates surface and recreates from current CPU/domain state. No promise that optional acceleration exists on every RID; required preview still works on CPU. |

Probe metadata is closed `native.metadata.v1`: `{version,streams:[{index,kind,codecName,timeBase,startPts?,durationPts?,frameRate?,width?,height?,sampleRate?,channels?,channelLayout?,colourPrimaries?,transfer?,matrix?,range?,rotation?,tags:[{key,value}]}],warnings:[{code,streamIndex?}]}`. Exact64 values use decimal strings; tags≤128, key≤128bytes/value≤4096, total≤256KiB. Image metadata adds subimage/mip counts and bounded channel names/types. Device list is `{version,devices:[{id,name,transport,vendorId?,productId?,serial?,interfaces:[{number,endpoints:[{address,kind,maxPacketBytes}]}],formats:[{rate,channels}]}]}`; this is descriptive only. PDF text is `{version,page,start,next?,text,boxes:[{start,length,x,y,width,height}]}` with UTF16 offsets and finite geometry. These are closed private ABI metadata encodings, not new business RPC authorities.

## 5. Package and process closure

Media uses ArcMediaNative; Colour ArcSlateColorNative; Image ArcSlateImageNative; Otio ArcSlateOtioNative. New Instruments/Pdf/Graphics libraries use ArcInstrumentsNative/ArcPdfNative/ArcGraphicsNative. Managed packages are `ArcForges.Native.<Capability>` plus exactly one explicitly referenced `Runtime.<rid>` sibling; Native.Abstractions owns common status/handles only. Existing Media libusb assets stay compatible; future Instruments closure records and deduplicates any identical shared-library filename by hash, and conflicting same-name dependencies fail packaging. Consumer never invokes CMake/vcpkg.

RID/tier and pinned upstream versions remain in [platform matrix](../21-platform-and-dependency-matrix.md) and [package registry](../01-solution-and-project-layout.md#12-package-and-native-distribution-registry). Every admitted RID records actual transitive library filenames/hashes, exports, system dependencies, source/patch/license closure, SBOM, signatures and helper profile. Optional accelerated export formats do not replace portable required profiles. LGPL redistributability and dynamic replacement/source notices remain mandatory; no GPL/nonfree FFmpeg feature is enabled implicitly.

`sandbox.buffer.v1` is private helper control (gRPC business operations never relay frames). Parent authenticates helper PID/signature/lease; creates at most3slots×64MiB and passes only those handles through Windows duplication, Unix SCM_RIGHTS or macOS XPC. Control record fields are version, invocationId, leaseId, generation, slotId, sequence, frameId, kind, format, fullWidth/fullHeight, tileX/tileY/tileWidth/tileHeight, sampleStart/sampleCount, offset, length, rowStride and sha256; integers use exact encodings. Parent validates allowed slot, current generation, bounds/stride, digest and complete nonoverlapping tile coverage. Pixel tiles≤2048squareRGBA32f. A slot transitions free→writing→sealed→reading→free; only parent grants reuse after read acknowledgement. Cancel/timeout/parent death invalidates lease, kills child tree and closes all mappings through cleanup journal. Late sealed slots are discarded; no untrusted child can mint/reuse a slot or send an arbitrary pointer. Full-frame allocation is separately admitted by the parent, not hidden in the slot budget.

## 6. Producer closure evidence

WP13 produces the complete declaration/export/layout manifest, wrapper mapping and package closure before product work. Each function has at least success, invalid-size/state, cancel/error, ownership and repeat/EOF tests applicable to it. Independent vectors include RGB/alpha identity,2x2regions, known PCM tone/drain length, two-frame seek, output decode, UART partial write, USB cancellation callback, PNG/EXR round trip, PDF page/text bounds and OTIO exact tick/fidelity cases. C17 and C# AOT consumers restore only candidate packages, execute real libraries/helpers and verify no handle/buffer growth after repeated cancellation. Required RIDs pass actual OS containment, throughput/memory and malformed-input tests. Sanitizer/fuzz/CTest replace the removed C++ CodeQL requirement; C# scanning remains.

This document defines signatures and evidence to implement. It does not claim that these exports, packages, ABI fixtures or runtime tests already exist or pass.

## 7. Normative 64-bit record sizes

Under the declared pack8 profile, sizes are: io56, limits48, stream88, reader_options64, frame104, region48, video_convert40, audio_convert32, writer_options120, device_options40, device_state48, instrument_options56, transfer40, image_options72, colour_options80, pdf_page32 and surface_options32 bytes (each name is arc_<name>_v1). WP13 checks exact field offsets as well as these sizes on each admitted RID. The document-review C17/C++20 compile against the existing shared header confirms declaration/layout consistency on Windows x64 only; it does not execute a functional native implementation.
