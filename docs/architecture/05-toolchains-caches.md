# 05 — Toolchains, adapters and caches

## 1. Toolchain detection

The toolchain registry (`ArcForges.Node.Toolchains`) scans at startup, daily, on demand (`ToolchainService.DetectToolchains`), and when a task names an unknown tool. Guest nodes scan their own environment.

| Kind | Detection | Identity recorded |
|---|---|---|
| `dotnet-sdk` | `dotnet --list-sdks` for each `dotnet` on PATH plus `%ProgramFiles%\dotnet`, `%UserProfile%\.dotnet`, `~/.dotnet`, `/usr/share/dotnet`, `/usr/lib/dotnet` | Version, root path, workload set (`dotnet workload list`) |
| `msbuild-vs` | `vswhere -latest -products * -requires Microsoft.Component.MSBuild -find MSBuild\**\Bin\MSBuild.exe` (Windows) | VS instance ID, version, path |
| `msvc` | `vswhere ... -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64`; environment captured once from `vcvarsall.bat <arch>` and cached per instance and architecture | Toolset version, captured environment digest |
| `rust` | `rustup toolchain list`, `cargo -V`, `rustc -vV` | Toolchain name, host triple, versions |
| `cmake`, `ninja`, `make` | `--version` | Version, path |
| `clang`, `gcc` | `--version` (or `-dumpfullversion`) | Version, target |
| `node`, `npm`, `pnpm`, `yarn` | `--version` | Versions |
| `python`, `pip` | `--version` | Version, venv flag |
| `git` | `git --version` | Version |
| `sccache`, `ccache` | `--version` | Version |

Missing tools are reported, never installed by the node (R-TOOL-001).

## 2. Adapter contract

Every adapter implements:

```
Classify(TaskSpec, ResolvedCommand) -> ToolInvocation?   // null = not this adapter
ToolInvocation {
  tool, operation (e.g. dotnet.build), phase_hints[],
  side_effect_proposal, assert_class (bool),
  pausable_default, preemptible_default,
  estimate (cpu_demand, mem_expected, mem_ceiling),
  environment_edits[]  (name, value, mode=SET|PREPEND_PATH, guarantee=HONORED|BEST_EFFORT),
  argument_edits[]     (only concurrency flags; never semantic changes; skipped when the caller already passed them),
  phase_detector       (stream patterns + process-name rules → timeline categories),
  cache_bindings[]     (cache_id, access=READ|READ_WRITE),
  failure_classifier   (exit code + output patterns → transient|corrupt-cache|oom|user-error),
  shared_services[]    (daemons this tool would start and how they are handled)
}
```

Adapters are compiled into the node (no runtime plug-ins in this scope). The manifest of each adapter is published through `ToolchainService.ListAdapters`, which states every guarantee: `HONORED` means the tool documents and respects the setting (V-T01–V-T03); `BEST_EFFORT` means it may be ignored (R-TOOL-004).

## 3. Built-in adapters

### 3.1 .NET (`dotnet`, `msbuild`)

| Operation | Side effect | Estimate (cpu / mem expected) | Phases |
|---|---|---|---|
| `restore`, `tool restore`, `workload restore` | IDEMPOTENT | 1,000 / 512 MiB | restore (network-bound by default) |
| `build`, `pack`, `publish`, `msbuild` | IDEMPOTENT | 4,000 / 2 GiB | restore → build (per project) → link/package |
| `test` | UNKNOWN (workspace policy may assert IDEMPOTENT) | 2,000 / 1.5 GiB | restore → build → test |
| `format` | IDEMPOTENT (`--verify-no-changes`) / SIDE_EFFECTING (writes) | 2,000 / 1 GiB | build |
| `run`, others | UNKNOWN | default | run |

**Environment.**

| Variable | Value | Guarantee |
|---|---|---|
| `NUGET_PACKAGES` | `<cache>/nuget/packages` (shared per node) | HONORED (overrides NuGet.Config, V-T01) |
| `NUGET_HTTP_CACHE_PATH` | `<cache>/nuget/http` | HONORED |
| `NUGET_SCRATCH` | `<cache>/nuget/scratch` (shared, required with shared packages, V-T01) | HONORED |
| `NUGET_PLUGINS_CACHE_PATH` | `<cache>/nuget/plugins` | HONORED |
| `MSBUILDDISABLENODEREUSE` | `1` unless policy `dotnet.shared_build_servers=true` | HONORED |
| `DOTNET_CLI_USE_MSBUILD_SERVER` | `0` unless shared servers are allowed | HONORED |
| `UseSharedCompilation` | `false` unless shared servers are allowed (MSBuild reads environment as properties) | HONORED |
| `TMP`, `TEMP`, `TMPDIR` | `<tmp>/<attempt>/` | HONORED |

- **Concurrency:** adds `-m:<N>` when absent.
- **Phase markers:** "Determining projects to restore", "Restored ", "All projects are up-to-date for restore", project output lines `-> <path>`, "Build succeeded", "Build FAILED"; the processes `testhost*`, `MSBuild.exe`/`MSBuild.dll` nodes and `VBCSCompiler`.
- **Failure classification:** NuGet network errors (NU1301, `Unable to load the service index`) are transient. NU1004 (lock mismatch) and compile errors are user errors. "The process cannot access the file" combined with a shared-folder path is a contention signal.

### 3.2 Rust (`cargo`)

| Operation | Side effect | Estimate | Phases |
|---|---|---|---|
| `fetch` | IDEMPOTENT | 1,000 / 256 MiB | download |
| `build`, `check`, `clippy`, `doc` | IDEMPOTENT | N × 1,000 / min(N,4) × 1.5 GiB | download → compile → link |
| `test`, `bench` | UNKNOWN | as build | compile → test |
| `run`, `install` | UNKNOWN / SIDE_EFFECTING | default | run |

**Environment.**
- `CARGO_BUILD_JOBS=<N>` when neither `-j` nor `--jobs` is present (HONORED).
- `CARGO_HOME` is **not** redirected by default, because it also holds installed binaries. Its registry is registered as an observed cache.
- `CARGO_TARGET_DIR` stays in the workspace unless the workspace policy `cargo.target_dir=MANAGED`, which uses `<out>/<workspace>/cargo-target/<rust-host-triple>`.
- sccache integration (opt-in per workspace or globally) sets `RUSTC_WRAPPER=<sccache path>`, `SCCACHE_DIR=<cache>/sccache`, `SCCACHE_CACHE_SIZE=<quota>` and `SCCACHE_SERVER_PORT=<node-assigned>`. The sccache server runs as a shared service (§5).

**Phase markers:** "Updating crates.io index", "Downloading", "Downloaded", "Compiling ", "Finished", "Running ", "test result:".

### 3.3 C/C++ (`cmake`, `ninja`, `make`, compilers)

| Operation | Side effect | Estimate | Phases |
|---|---|---|---|
| `cmake -S/-B` (configure) | IDEMPOTENT | 1,000 / 512 MiB | configure |
| `cmake --build`, `ninja`, `make` | IDEMPOTENT | N × 1,000 / N × 512 MiB | compile → link |
| `ctest` | UNKNOWN | default | test |

**Environment and concurrency.**
- `CMAKE_BUILD_PARALLEL_LEVEL=<N>` for `cmake --build`.
- `-j<N>` for `ninja` and `make` when absent.
- With compiler caching enabled, `CMAKE_C_COMPILER_LAUNCHER` and `CMAKE_CXX_COMPILER_LAUNCHER` are set to sccache or ccache. These take effect at configure time, and the record notes whether the build directory was configured with them (BEST_EFFORT for pre-configured trees).
- `CCACHE_DIR=<cache>/ccache` and `CCACHE_MAXSIZE=<quota>` (HONORED, V-T03).
- MSVC tasks receive the cached `vcvarsall` environment when `toolchain: msvc` is requested or auto-detected for `cl.exe`.

**Phase markers:** "-- Configuring done", "-- Generating done", ninja `[x/y]`, the `link.exe`/`ld`/`lld` processes, "Linking ".

### 3.4 Node (`npm`, `pnpm`, `yarn`, `npx`)

- `npm ci` and `npm install` are IDEMPOTENT downloads. `npm run` and `npm test` are UNKNOWN.
- Environment: `npm_config_cache=<cache>/npm` (HONORED) and `npm_config_store_dir=<cache>/pnpm-store` for pnpm (BEST_EFFORT).
- No concurrency injection.

### 3.5 Python (`python`, `pip`, `pytest`)

`pip install` is an IDEMPOTENT download, with `PIP_CACHE_DIR=<cache>/pip` (HONORED). `pytest` is UNKNOWN.

### 3.6 Git

`git clone`, `fetch` and `pull` are network-bound IDEMPOTENT downloads (no environment changes). Other git commands are generic.

### 3.7 Generic

This adapter covers all other commands. It sets only `TMP`/`TEMP`/`TMPDIR` and uses default estimates. Phases come from CPU, I/O and output heuristics alone.

## 4. Cache registry

`cache_instance` rows ([data](../data/node-store.md)):

| Kind | Default location | Quota (default) | Eviction | Integrity | LAN sharing |
|---|---|---|---|---|---|
| `nuget.packages` | `<cache>/nuget/packages` | 40 GiB (warn at 80%) | Only during idle maintenance windows (no running .NET attempt). Package-version directories unused for 60 days (usage tracked from `project.assets.json` of managed restores) are trimmed, with approval. | Package signature verification is not repeated (NuGet verifies on restore); presence of `.nupkg.metadata` is checked | No (each node keeps its own; duplicates reported) |
| `nuget.http` | `<cache>/nuget/http` | 10 GiB | LRU by file access time | n/a | No |
| `nuget.scratch` | `<cache>/nuget/scratch` | 2 GiB | Cleared when no .NET attempt runs | n/a | No |
| `sccache` | `<cache>/sccache` | 20 GiB (`SCCACHE_CACHE_SIZE`) | Tool LRU | Tool | Yes (§6) |
| `ccache` | `<cache>/ccache` | 10 GiB (`CCACHE_MAXSIZE`) | Tool LRU | Tool | Yes (§6) |
| `npm` | `<cache>/npm` | 10 GiB | `npm cache verify` (GC) in idle windows | `npm cache verify` | No |
| `pip` | `<cache>/pip` | 5 GiB | LRU | n/a | No |
| `cargo.registry` (observed) | `$CARGO_HOME/registry` | none (report only) | none | n/a | No |
| `cas` | `<cache>/cas` | 20 GiB | LRU by last use with reference counts; pinned when referenced by a queued or running task | SHA-256 on every read | Blobs served to peers for transfers (§6) |

**Compatibility keys** (`compat_key`) prevent sharing across incompatible environments (R-CACHE-002):

| Kind | Key |
|---|---|
| NuGet, npm, pip | `os-family/arch` (content is version-addressed) |
| sccache, ccache | `tool/version-major.minor/os/arch`. Compiler identity is hashed by the tool itself. |
| CAS | none (content-addressed) |
| Remote workspaces | `origin_node/origin_workspace` |

Mutable outputs (`bin/`, `obj/`, `target/`, CMake build trees) are never registered as shared caches. When managed, they live under `<out>/<workspace_id>/...` per workspace (R-CACHE-002).

**Locking.** Tools coordinate their own concurrent access (NuGet file locks, the sccache server, ccache file locks). The node takes an exclusive **maintenance lease** on a cache only for eviction, verification and relocation. While held, admissions of tasks bound to that cache wait; maintenance runs only when none are running, and is bounded to 10 minutes.

**Corruption.**
- A CAS digest mismatch quarantines the blob and re-fetches it.
- Tool-reported corruption patterns (adapter `failure_classifier`) raise finding `CACHE_CORRUPT` with remedy "clear affected entries". The remedy needs approval; for NuGet it deletes the specific package-version directory.

## 5. Shared services (daemons)

Shared daemons run in a node-owned container (Windows child job `Local\ArcForges.<node_id>.svc.<service>`; Linux transient unit `arcforges-svc-<service>.service` in `arcforges.slice`), with their own CPU weight and memory limit taken out of the managed budget. Each is started on first use and stopped after an idle timeout (default 15 min). They are visible on the Resources page as `SHARED_SERVICE` (R-TOOL-005):
- the sccache server;
- MSBuild and VBCSCompiler only when policy `dotnet.shared_build_servers=true`.

## 6. LAN cache sharing

1. The serving node exposes a **WebDAV-compatible subset** on its mTLS peer listener: `OPTIONS`, `PROPFIND` (depth 0/1), `GET`, `HEAD`, `PUT`, `DELETE` under `/cache/<cache_id>/`. Per-peer policy decides read and write access, with a quota enforced per peer (R-CACHE-007).
2. Tools cannot present client certificates (sccache uses a WebDAV client with basic/bearer authentication, V-T02). Each consuming node therefore runs a **local cache proxy** on `127.0.0.1:<ephemeral>` that forwards to the serving peer over the mTLS channel. The proxy requires a per-node bearer token.
   - sccache: `SCCACHE_WEBDAV_ENDPOINT=http://127.0.0.1:<port>/peer/<peer_id>/cache/<cache_id>/` with `SCCACHE_WEBDAV_TOKEN`.
   - ccache: `remote_storage=http://127.0.0.1:<port>/peer/<peer_id>/cache/<cache_id>/|bearer-token=...`. This uses ccache's HTTP backend or its remote storage helper, depending on the installed ccache version (F-T01).
3. Multi-level use: sccache `SCCACHE_MULTILEVEL_CHAIN=disk,webdav` keeps the local disk as L0 (V-T02).
4. Entries are opaque to ArcForges. Integrity is the tool's responsibility; the proxy only enforces size limits (an entry ≤ 256 MiB) and quotas.

## 7. Effectiveness and duplicates

`CacheService.GetCacheReport` shows the following (R-CACHE-008):
- Hit/miss counts and bytes from `sccache --show-stats --stats-format=json` and `ccache --print-stats`.
- NuGet restore counters: packages installed versus reused, parsed from restore output, and http-cache growth per attempt.
- **Duplicate cache copies:** global-packages-like folders found by disk analysis outside the managed cache, such as `~/.nuget/packages` or per-task `NUGET_PACKAGES` folders seen in unmanaged processes' environments where readable. The report gives package-version overlap with the managed cache and the reclaimable bytes.
- **Per-task restores:** managed attempts whose caller overrode `NUGET_PACKAGES` with a unique folder. These raise finding `PER_TASK_RESTORE`.
