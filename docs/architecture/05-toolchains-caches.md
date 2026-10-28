# 05 — Toolchains, adapters and caches

**Amended 2026-10-28 by [AD-0021](../decisions/AD-0021-central-access-go-center.md) (target until each AF-CTR task is delivered).** LAN cache sharing (the LAN sections, including the release-1 owner decision on it) is out of current delivery (roadmap RM-19); same-machine cache reuse across worktrees stays.

## 1. Toolchain detection

The toolchain registry (`ArcForges.Node.Toolchains`) scans at startup, daily, on demand (`ToolchainService.DetectToolchains`), and when a task names an unknown tool. Each node scans its own machine (Windows or Linux).

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
| `fastbuild` | `FBuild.exe -version` / `fbuild -version` | Version, path, worker binary presence (`FBuildWorker`) |

Missing tools are reported, never installed by the node (R-TOOL-001).

*Direction (roadmap; not release 1; [AD-0017](../decisions/AD-0017-delegated-execution-direction.md)):* a no-install amendment of this section, effective only when EX-13 stage b is promoted, is recorded in [17](17-delegated-execution.md) §15.1; until then the sentence above is unchanged.

## 2. Adapter contract

Every adapter implements:

```
Classify(TaskSpec, ResolvedCommand) -> ToolInvocation?   // null = not this adapter
ToolInvocation {
  tool, operation (e.g. dotnet.build), phase_hints[],
  side_effect_suggestion, assert_class (bool),   // assert only what the adapter can verify
  exclusive_keys[], shared_keys[]   (keys the operation writes or only reads, 03 section 4),
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

**Side-effect classes.** An adapter cannot see what a project's build scripts, MSBuild targets, CMake code, Makefile rules or package lifecycle scripts do, so it never infers retry safety from the executable and subcommand alone:
- `side_effect_suggestion` is shown to the user and used only when a caller assertion or a `retry_safety` rule confirms it ([AD-0006](../decisions/AD-0006-execution-semantics.md) §4);
- `assert_class=true` is allowed only where the tool itself guarantees that no project code runs, for example `npm ci --ignore-scripts` or `cargo fetch`.

Adapters are compiled into the node (no runtime plug-ins in this scope). The manifest of each adapter is published through `ToolchainService.ListAdapters`, which states every guarantee: `HONORED` means the tool documents and respects the setting (V-T01–V-T03); `BEST_EFFORT` means it may be ignored (R-TOOL-004).

## 3. Built-in adapters

### 3.1 .NET (`dotnet`, `msbuild`)

| Operation | Side effect (default; suggestion) | Exclusive keys | Estimate (cpu / mem expected) | Phases |
|---|---|---|---|---|
| `restore` | UNKNOWN; suggests IDEMPOTENT (MSBuild targets can hook into restore) | `tool:dotnet:<w>` | 1,000 / 512 MiB | restore (network-bound by default) |
| `tool restore`, `workload restore` | UNKNOWN; suggests IDEMPOTENT | none (they write the managed caches, not the workspace) | 1,000 / 512 MiB | restore |
| `build`, `pack`, `publish`, `msbuild` | UNKNOWN; suggests IDEMPOTENT for `build` and `pack` (custom targets can deploy or call out) | `tool:dotnet:<w>` | 4,000 / 2 GiB | restore → build (per project) → link/package |
| `test` | UNKNOWN | `tool:dotnet:<w>`; shared with `--no-build` | 2,000 / 1.5 GiB | restore → build → test |
| `format` | UNKNOWN (`--verify-no-changes`; suggests IDEMPOTENT) / SIDE_EFFECTING (writes) | `tool:dotnet:<w>`; shared with `--verify-no-changes` | 2,000 / 1 GiB | build |
| `run` | UNKNOWN | `tool:dotnet:<w>` until the program starts (shared with `--no-build`) | default | build → run |
| others | UNKNOWN | none | default | run |

**Why one key per workspace.** Every build-family operation restores and builds the whole project-reference closure of its entry project, so two of them in one workspace can write the same `obj/` and `bin/` directories even when their entry projects differ. Parallel builds of one repository therefore use separate managed worktrees, or the workspace mode `SHARED` with caller keys for solutions the user knows are independent.

**Environment.**

| Variable | Value | Guarantee |
|---|---|---|
| `NUGET_PACKAGES` | `<cache>/nuget/packages` (shared per node) | HONORED (overrides NuGet.Config, V-T01) |
| `NUGET_HTTP_CACHE_PATH` | `<cache>/nuget/http` | HONORED |
| `NUGET_SCRATCH` | `<cache>/nuget/scratch` (shared, required with shared packages, V-T01) | HONORED |
| `NUGET_PLUGINS_CACHE_PATH` | `<cache>/nuget/plugins` | HONORED |
| `MSBUILDDISABLENODEREUSE` | `1` (§5) | HONORED |
| `DOTNET_CLI_USE_MSBUILD_SERVER` | `false` (the MSBuild server is on by default from the .NET 11 SDK, V-T09) | HONORED |
| `UseSharedCompilation` | `false` (MSBuild reads environment as properties) | HONORED |
| `TMP`, `TEMP`, `TMPDIR` | `<tmp>/<attempt>/` | HONORED |

- **Concurrency:** adds `-m:<N>` when absent.
- **Build servers:** the environment above turns off MSBuild node reuse, the MSBuild server and the compiler server, so no compiler or build server outlives the attempt (§5). The adapter adds no `--disable-build-servers` flag, because `dotnet test` on Microsoft Testing Platform passes options it does not know to the test application (V-T09).
- **Phase markers:** "Determining projects to restore", "Restored ", "All projects are up-to-date for restore", project output lines `-> <path>`, "Build succeeded", "Build FAILED"; the processes `testhost*`, `MSBuild.exe`/`MSBuild.dll` nodes and `VBCSCompiler`.
- **Failure classification:** NuGet network errors (NU1301, `Unable to load the service index`) are transient. NU1004 (lock mismatch) and compile errors are user errors. "The process cannot access the file" combined with a shared-folder path is a contention signal.

### 3.2 Rust (`cargo`)

| Operation | Side effect (default; suggestion) | Exclusive keys | Estimate | Phases |
|---|---|---|---|---|
| `fetch` | IDEMPOTENT (asserted: downloads into the registry cache only) | none | 1,000 / 256 MiB | download |
| `build`, `check`, `clippy`, `doc` | UNKNOWN; suggests IDEMPOTENT (build scripts and proc macros run project code) | `tool:cargo:<target dir>` | N × 1,000 / min(N,4) × 1.5 GiB | download → compile → link |
| `test`, `bench` | UNKNOWN | `tool:cargo:<target dir>` | as build | compile → test |
| `run`, `install` | UNKNOWN / SIDE_EFFECTING | `tool:cargo:<target dir>` (`run`: until the program starts) | default | run |

**Environment.**
- `CARGO_BUILD_JOBS=<N>` when neither `-j` nor `--jobs` is present (HONORED).
- `CARGO_HOME` is **not** redirected by default, because it also holds installed binaries. Its registry is registered as an observed cache.
- `CARGO_TARGET_DIR` stays in the workspace unless the workspace policy `cargo.target_dir=MANAGED`, which uses `<out>/<workspace>/cargo-target/<rust-host-triple>`.
- sccache integration (opt-in per workspace or globally) sets `RUSTC_WRAPPER=<sccache path>` and the per-attempt server and store settings of §5. The attempt's own server runs the compiler on a miss.

**Phase markers:** "Updating crates.io index", "Downloading", "Downloaded", "Compiling ", "Finished", "Running ", "test result:".

### 3.3 C/C++ (`cmake`, `ninja`, `make`, compilers)

| Operation | Side effect (default; suggestion) | Exclusive keys | Estimate | Phases |
|---|---|---|---|---|
| `cmake -S/-B` (configure) | UNKNOWN; suggests IDEMPOTENT (CMake code can run any process) | `ws:<w>/<build dir>` | 1,000 / 512 MiB | configure |
| `cmake --build`, `ninja`, `make` | UNKNOWN; suggests IDEMPOTENT (rules are arbitrary commands) | `ws:<w>/<build dir>` | N × 1,000 / N × 512 MiB | compile → link |
| `ctest` | UNKNOWN | `ws:<w>/<build dir>`, shared | default | test |

**Environment and concurrency.**
- `CMAKE_BUILD_PARALLEL_LEVEL=<N>` for `cmake --build`.
- `-j<N>` for `ninja` and `make` when absent.
- With compiler caching enabled, `CMAKE_C_COMPILER_LAUNCHER` and `CMAKE_CXX_COMPILER_LAUNCHER` are set to sccache or ccache. These take effect at configure time, and the record notes whether the build directory was configured with them (BEST_EFFORT for pre-configured trees).
- `CCACHE_DIR=<cache>/ccache` and `CCACHE_MAXSIZE=<quota>` (HONORED, V-T03), and the per-attempt `CCACHE_STATSLOG` (§5).
- MSVC tasks receive the cached `vcvarsall` environment when `toolchain: msvc` is requested or auto-detected for `cl.exe`, and a per-attempt `_MSPDBSRV_ENDPOINT_` (§5).

**Phase markers:** "-- Configuring done", "-- Generating done", ninja `[x/y]`, the `link.exe`/`ld`/`lld` processes, "Linking ".

### 3.4 Node (`npm`, `pnpm`, `yarn`, `npx`)

- `npm ci` and `npm install` run package lifecycle scripts, so they are UNKNOWN and suggest IDEMPOTENT. With `--ignore-scripts` the adapter asserts IDEMPOTENT. `npm run` and `npm test` are UNKNOWN.
- Keys: installs (`ci`, `install`, `update`) take `ws:<w>/<package dir>:deps` exclusively (`node_modules` and the lock file); `npm run`, `npm test`, `npm start` and `npx` take it shared, so they never run while dependencies are being replaced (`npm start` releases it once the program runs).
- Environment: `npm_config_cache=<cache>/npm` (HONORED) and `npm_config_store_dir=<cache>/pnpm-store` for pnpm (BEST_EFFORT).
- No concurrency injection.

### 3.5 Python (`python`, `pip`, `pytest`)

`pip install` can build source distributions, which runs project code, so it is UNKNOWN and suggests IDEMPOTENT. `pip download` also prepares the metadata of source distributions by running their build backend, so it is asserted IDEMPOTENT only with `--only-binary=:all:` (wheels only); otherwise it is UNKNOWN and suggests IDEMPOTENT. `PIP_CACHE_DIR=<cache>/pip` (HONORED). `pytest` is UNKNOWN. Installs into a virtual environment take `ws:<w>/<venv dir>` exclusively; `pytest` and `python` running from that environment take it shared.

### 3.6 Git

`git clone` and `fetch` are network-bound downloads asserted IDEMPOTENT (no environment changes). Commands that rewrite the working tree (`checkout`, `switch`, `pull`, `merge`, `rebase`, `reset --hard`, `restore`, `stash`, `cherry-pick`, `revert`, `clean`) are UNKNOWN and take `ws:<w>` exclusively, so they wait for every build and test in the workspace. Index-only writers (`add`, `commit`, `rm --cached`) are UNKNOWN and take `tool:git:<w>`. Read-only commands carry no keys.

### 3.7 Generic

This adapter covers all other commands. It sets only `TMP`/`TEMP`/`TMPDIR` and uses default estimates. Phases come from CPU, I/O and output heuristics alone.

### 3.8 FASTBuild (`FBuild`)

| Operation | Side effect (default; suggestion) | Exclusive keys | Estimate | Phases |
|---|---|---|---|---|
| `FBuild <targets>` | UNKNOWN; suggests IDEMPOTENT (`Exec` nodes run arbitrary commands) | `ws:<w>/<bff dir>:build` | N × 1,000 / N × 512 MiB | parse → compile → link |
| `FBuild -cachetrim <MiB>` | IDEMPOTENT (asserted: maintenance of the managed cache) | `tool:fastbuild:cache` | 1,000 / 256 MiB | maintenance |

- **Concurrency.** `-j<N>` from the CPU grant, unless the caller set `-j` (the caller's value is recorded). Without `-dist`, FASTBuild uses only local workers, so the OS limits of the attempt container fully apply.
- **Cache.** `FASTBUILD_CACHE_PATH=<cache>/fastbuild` (BEST_EFFORT until F-T02 confirms that it takes precedence over a project's `Settings { .CachePath }`; otherwise the project's cache is reported as observed, not managed). The adapter adds `-cache` (equivalent to `-cacheread` plus `-cachewrite`) when the workspace policy enables compiler caching, or `-cacheread` for a read-only cache (V-T06). FASTBuild sets no cache size limit, so maintenance runs `FBuild -cachetrim <quota MiB>` under the cache's maintenance lease (§4).
- **Distribution (observed, not managed).** `-dist` with a brokerage path (`FASTBUILD_BROKERAGE_PATH`) sends work to `FBuildWorker` processes on other machines. ArcForges records the use of `-dist` and the brokerage path, and labels the attempt `distributed_by_tool`. It does not run or govern remote workers in this scope: their resource use is outside ArcForges control, and the record says so (R-LAN-010).
  - **Possible future option:** an executor node runs `FBuildWorker` as a shared service under its per-peer policy. It needs its own decision.
- **Phase markers:** "Building ", "FBuild: OK", "FBuild: Error", the compiler and linker processes.
- **Validation.** F-T02 (FASTBuild is not installed on the workstation, L-10; the user installs it, H-11).

## 4. Cache registry

`cache_instance` rows ([data](../data/node-store.md)):

| Kind | Default location | Quota (default) | Eviction | Integrity | LAN sharing |
|---|---|---|---|---|---|
| `nuget.packages` | `<cache>/nuget/packages` | 40 GiB (warn at 80%) | Only during idle maintenance windows (no running .NET attempt). Package-version directories unused for 60 days (usage tracked from `project.assets.json` of managed restores) are trimmed, with approval. | Package signature verification is not repeated (NuGet verifies on restore); presence of `.nupkg.metadata` is checked | No (each node keeps its own; duplicates reported) |
| `nuget.http` | `<cache>/nuget/http` | 10 GiB | LRU by file access time | n/a | No |
| `nuget.scratch` | `<cache>/nuget/scratch` | 2 GiB | Cleared when no .NET attempt runs | n/a | No |
| `sccache` | `<cache>/sccache`, served by the node (§5) | 20 GiB | LRU by the node, the store's only writer | Tool | Yes (§6) |
| `ccache` | `<cache>/ccache` | 10 GiB (`CCACHE_MAXSIZE`) | Tool LRU | Tool | Yes (§6) |
| `fastbuild` | `<cache>/fastbuild` | 20 GiB | `FBuild -cachetrim` in maintenance windows | Tool | No (local only in this scope) |
| `npm` | `<cache>/npm` | 10 GiB | `npm cache verify` (GC) in idle windows | `npm cache verify` | No |
| `pip` | `<cache>/pip` | 5 GiB | LRU | n/a | No |
| `cargo.registry` (observed) | `$CARGO_HOME/registry` | none (report only) | none | n/a | No |
| `cas` | `<cache>/cas` | 20 GiB | LRU by last use with reference counts; pinned when referenced by a queued or running task | SHA-256 on every read | Blobs served to peers for transfers (§6) |

**Compatibility keys** (`compat_key`) prevent sharing across incompatible environments (R-CACHE-002):

| Kind | Key |
|---|---|
| NuGet, npm, pip | `os-family/arch` (content is version-addressed) |
| FASTBuild | `fastbuild/version-major.minor/os/arch` |
| sccache, ccache | `tool/version-major.minor/os/arch`. Compiler identity is hashed by the tool itself. |
| CAS | none (content-addressed) |
| Remote workspaces | `origin_node/origin_workspace` |

Mutable outputs (`bin/`, `obj/`, `target/`, CMake build trees) are never registered as shared caches. When managed, they live under `<out>/<workspace_id>/...` per workspace (R-CACHE-002).

**Locking.** Tools coordinate their own concurrent access (NuGet file locks, ccache file locks); the node serializes writes to the sccache store it serves (§5). The node takes an exclusive **maintenance lease** on a tool-managed cache only for eviction, verification and relocation; it evicts its own sccache store online. While held, admissions of tasks bound to that cache wait; maintenance runs only when none are running, and is bounded to 10 minutes.

**Corruption.**
- A CAS digest mismatch quarantines the blob and re-fetches it.
- Tool-reported corruption patterns (adapter `failure_classifier`) raise finding `CACHE_CORRUPT` with remedy "clear affected entries". The remedy needs approval; for NuGet it deletes the specific package-version directory.

## 5. Compiler and build servers

Compiler work always runs in the container of the attempt that asked for it, so that attempt's CPU weight and caps, memory limits, accounting, priority and cancellation cover it. Release 1 runs no compiler service shared between attempts. Tools that would share a server across tasks are set up so that each attempt gets its own server, or none (R-TOOL-005).

**sccache: one server per attempt, and one store served by the node.**
- **Why.** On a cache miss, the sccache server, not the client the build invoked, runs the compiler (V-T07, L-20). The server stays in the job or cgroup of the client that started it. A server shared between attempts would therefore run one attempt's compiles in another attempt's container, charge them to it, and die with it. Several servers must not share one local cache directory either: sccache documents races, and a starting server deletes the in-progress writes of others (V-T07).
- **An endpoint per attempt.** The adapter gives each attempt its own server, with `SCCACHE_IDLE_TIMEOUT=0` so it lives exactly as long as the attempt:
  - **Both platforms:** a loopback TCP port assigned to the attempt (`SCCACHE_SERVER_PORT`). sccache offers no pipe or socket option on Windows (V-T07).
    - **The range.** Ports come from the policy range `caches.sccache_port_first` to `caches.sccache_port_last`. By default it is a 400-port slice of 20000–31999 chosen by a hash of the user's ID, so several users on one machine do not share ports.
      - It lies outside the operating systems' ephemeral ranges, so programs that bind port 0 are never given one of its ports.
      - At startup the node checks it against those ranges (`ip_local_port_range` on Linux; the dynamic port range on Windows) and refuses an overlap with a finding.
      - Policy validation requires 1024 ≤ first < last ≤ 65535, at least 64 ports, and more ports than the effective `global_max_running`, so the range never limits how many attempts run.
    - **Allocation by owner.** A port is assigned only when no process listens on it. That is decided by its listening process (`GetExtendedTcpTable` on Windows, `/proc/net/tcp` on Linux), never by a failed bind, which `TIME_WAIT` can cause.
      - **Skipped ports:** ports in the operating system's excluded ranges (Windows `excludedportrange`, for example held by Hyper-V or WinNAT), and a port the server then fails to bind. Neither counts as taken.
      - **Exhaustion:** when every port of the range is assigned, new attempts wait with the blocking reason `sccache_port`.
  - **Linux:** also a Unix socket in the attempt's private run directory, `SCCACHE_SERVER_UDS=$XDG_RUNTIME_DIR/arcforges/a/<attempt>/sccache.sock` (directory mode 0700). sccache 0.9.0 and later use it instead of the port; older clients fall back to the port.
- **Every managed attempt.** These settings, `SCCACHE_IDLE_TIMEOUT=0` and the store below are set for every managed attempt, whether or not sccache is installed or the integration adds it. They do nothing if sccache never runs.
  - **No other storage applies.** The adapter passes through only inherited settings that shape cache keys or logging (`SCCACHE_BASEDIRS`, `SCCACHE_DIRECT`, `SCCACHE_C_CUSTOM_CACHE_BUSTER`, `SCCACHE_RECACHE`, `SCCACHE_LOG`), and records them. It removes every other inherited `SCCACHE_*` variable before setting its own, and points `SCCACHE_CONF` to an empty configuration file the node writes. sccache merges file and environment settings and chooses other backends before WebDAV (V-T07), so this is what keeps a user's configuration file, or an inherited setting such as `SCCACHE_BUCKET`, from taking effect.
  - **User-configured wrappers.** A wrapper the user configured (Cargo `build.rustc-wrapper`, `RUSTC_WRAPPER`, a CMake tree configured with sccache, or a script that calls sccache) therefore starts the attempt's own server inside the container on first use (L-20). It uses the node's store, never the shared default server or the user's own storage. The attempt's recorded environment shows the replacement.
- **Started at launch, inside the container.** When the adapter detects that the attempt uses sccache, the server starts as a launch step ([04](04-execution.md) §3), while the node and its store are up. It detects use when the integration adds sccache, or a wrapper appears in the environment, the Cargo configuration or the CMake cache. Starting the server before the build also avoids two first compiles each starting one.
  - A server start reads the store and fails when the store is unreachable (L-21).
  - From sccache 0.18.0, the adapter sets `SCCACHE_SKIP_CACHE_CHECK=1`, so a server that has to start while the node is down still starts and compiles without the cache (V-T07).
  - With 0.17.0, which lacks that setting, compiles that need a new server fail until the node returns. A server that a user's wrapper starts lazily is in the same position.

  How the launch step runs on each platform:
  - **Windows:** the holder starts `sccache --start-server` in the attempt's jobs (root, then child) and waits for it before it resumes the root process.
    - It then checks that the process listening on the assigned port is in the attempt's job (`GetExtendedTcpTable`, `IsProcessInJob`).
    - If another process holds the port, it retries with another port, up to 5 times. If none works, the attempt fails at launch with `SPAWN_FAILED`, rather than have its compiles reach a server outside it.
  - **Linux:** `arcforges node exec-launch`, the unit's `ExecStart` for attempts with launch steps, starts it inside the unit's cgroup and then replaces itself with the command (`execve`), so no wrapper stays behind (A-T04).
- **Watching the port.** While the attempt runs, its holder (Windows) or the node (Linux) checks every second whether a process outside the attempt's container listens on the attempt's port.
  - **Attempts that use sccache** are stopped with `ENDPOINT_TAKEN`, because their compiles would reach that process. An attempt uses sccache when the adapter detected it at launch, or once an sccache process has appeared in its container. This also covers a server that an undetected wrapper starts later.
  - **Any other attempt** keeps running, and the collision is recorded (finding `ENDPOINT_COLLISION`).
  - **Remaining gaps.** A compile can reach a foreign listener that appears in the second between two checks, and a wrapper script that sets its own `SCCACHE_SERVER_PORT` is outside the watch (T-21).
- **On a miss**, the attempt's own server runs the compiler inside the attempt's job or unit. Its limits apply, its use is accounted to the attempt, and cancelling the attempt ends the server and the compile at once (L-20: within 0.1 s on Windows). Since 0.17.0 the server also aborts a compile whose client has gone (V-T07).
- **One store, served by the node.** Every attempt's server uses the node's compiler-cache store through `SCCACHE_WEBDAV_ENDPOINT=http://127.0.0.1:<port>/cache/<cache_id>/`, with a bearer token issued for the attempt (`SCCACHE_WEBDAV_TOKEN`).
  - **Only writer.** The node is the store's only writer: it writes entries atomically and keeps the quota by evicting the least recently used entries.
  - **Exact per attempt.** It counts the bytes each attempt writes, which is exact even while attempts share the cache ([07](07-records-diagnosis-memory.md) §1.5).
  - **Access.** It refuses requests without a valid token.
  - **Protocol.** It implements what sccache uses: `GET`, `PUT`, `PROPFIND` and `MKCOL` (L-21).
  - **Bounded answers.** It answers every request within 30 s, accepting or refusing it, because sccache waits for each write without a timeout of its own (V-T07). A hung node is restarted ([06](06-storage-workspaces.md) §5), so a wait cannot last.
  - **Ledger.** The store keeps its own ledger instead of being walked ([07](07-records-diagnosis-memory.md) §1.5):
    - the first `PUT` of a key counts its bytes for the writing attempt; a `PUT` of a key already present counts nothing;
    - an entry fetched from a peer for an attempt's `GET` counts as filled from that peer for the attempt;
    - evictions count as removed bytes.
  - **Online eviction.** The node evicts the store online, without the maintenance lease, because it is the only writer.
  - **A stable address.** The store keeps its port across node restarts, so running servers reach it again. The store's port also comes from that range, and on Windows the node binds it with `SO_EXCLUSIVEADDRUSE`, so no other process can bind it while the node holds it. If another process holds the port when the node restarts, the node takes a new one and stops the attempts that use sccache with `ENDPOINT_TAKEN`, because their servers would send reads and tokens to that process; other attempts keep running. The window while the node is down remains a stated risk (T-21).
  - **LAN.** With LAN sharing on, it also reads through to peers (§6).
- **If the store goes away** while a server runs (the node stops), compiles continue as misses and failed writes are counted as errors (L-21).
- **End of the attempt.** Before leftover termination, the attempt's end step (Windows holder; Linux `ExecStop`, [04](04-execution.md) §3):
  1. reads `sccache --show-stats --stats-format=json`, which gives the attempt's own counters;
  2. runs `sccache --stop-server`, which waits at most 10 s for requests in flight (V-T07).

  Leftover termination then ends anything still running.
- **Local state.** With only the store configured, sccache keeps no local cache, and its preprocessor cache (direct mode) is off (V-T07); `SCCACHE_DIR` points into the attempt's temporary directory for anything else. C/C++ projects that want a warm preprocessor cache use ccache.
- **Cost.** One server start per attempt that uses sccache, and no warm in-memory state between attempts. Cache entries are shared through the store.
- **Supported versions.** sccache 0.17.0 or later (verified with 0.17.0, L-20 and L-21; 0.18.0 reviewed, V-T07). The adapter adds sccache only from that version on, and records the version of any sccache it finds.
- **Exposure.** An attempt's server on a loopback port has no authentication. While the attempt runs, another local user could submit compile requests to it (T-21). On Linux, supported versions use the private socket instead.

**ccache** compiles in the process the build started; it has no compile server (V-T08).
- It would start the compiler outside the job only if the job allowed breakaway, which attempt jobs never do ([AD-0005](../decisions/AD-0005-resource-enforcement.md) Windows §2).
- Its local cache directory is shared through ccache's own locks.
- A per-attempt statistics log gives the attempt's own counters: `CCACHE_STATSLOG=<logs>/<attempt>/ccache-stats.log` (ccache 4.4 or later).
- Remote storage for LAN sharing goes through the helper endpoint that the node serves (§6), so no task starts a long-lived helper.

**.NET.** The Roslyn compiler server (VBCSCompiler) and the MSBuild server are shared per user and SDK by pipe name, and outlive the build (V-T09).
- Managed .NET builds therefore run without them: the adapter sets `MSBUILDDISABLENODEREUSE=1`, `DOTNET_CLI_USE_MSBUILD_SERVER=false` and `UseSharedCompilation=false` (§3.1). MSBuild worker nodes end with the build.
- Sharing warm compiler servers safely across attempts is accepted future work (roadmap RM-13). Policy `dotnet.shared_build_servers` is refused in release 1.

**MSVC.** The PDB server (`mspdbsrv`), which `cl` starts and other compiles reuse by endpoint name, is made private to the attempt with `_MSPDBSRV_ENDPOINT_=arcforges-<attempt>` (A-T05, F-T06).

**FASTBuild** runs its local workers as its own children (§3.8).

**Records.** Process records show the compiler processes under their attempt. The process label `SHARED_SERVICE` stays in the contract and is not used in release 1.

## 6. LAN cache sharing

1. The serving node exposes a **WebDAV-compatible subset** on its mTLS peer listener: `OPTIONS`, `PROPFIND` (depth 0/1), `GET`, `HEAD`, `PUT`, `DELETE` under `/cache/<cache_id>/`. Per-peer policy decides read and write access, with a quota enforced per peer (R-CACHE-007).
2. Tools cannot present client certificates (sccache uses a WebDAV client with basic/bearer authentication, V-T02), so the node connects to peers on their behalf over the mTLS channel.
   - sccache: attempts always use the node's own store (§5). With LAN sharing on, the store reads through to peers that allow reads, keeping fetched entries locally, and writes through to peers that allow writes. A per-attempt bearer token protects the loopback endpoint.
   - ccache: ccache 4.14 deprecates its built-in HTTP backend in favour of remote storage helpers (V-T03). The **node itself serves the helper protocol** on a per-user IPC endpoint and forwards to peers over the mTLS channel:
     - the endpoint is the named pipe `\\.\pipe\arcforges-<user SID hash>-ccache` on Windows (DACL: the user only), and `$XDG_RUNTIME_DIR/arcforges/ccache.sock` (mode `0600`) on Linux;
     - the setting is `remote_storage = crsh:<endpoint>`. Per the ccache manual, `crsh:` connects to a helper that is already running; ccache never starts it. While the node is down, ccache treats the remote storage as unavailable and keeps using its local cache;
     - no token is needed, because the endpoint admits only the user (A-T03);
     - ccache versions without helper support fall back to the built-in HTTP backend against the node's loopback endpoint (`http://127.0.0.1:<port>/peer/<peer_id>/cache/<cache_id>/` with `@bearer-token=`, plain HTTP to loopback only), which forwards to the peer;
     - the adapter records which mode is used, and F-T04 verifies the protocol and the syntax against the installed ccache.
3. Multi-level use: the node's store is the local level, so sccache needs no multi-level chain of its own.
4. Entries are opaque to ArcForges. The tools' integrity checks detect corruption, not a less-trusted producer: an entry written by a peer with write access passes them whatever it contains, which is why cache writes are off by default and granted per trusted peer ([11](11-security-privacy.md) §4, T-10). The node only enforces size limits (an entry ≤ 256 MiB) and quotas. (Corrected 2026-10-19; this item previously said "Integrity is the tool's responsibility".)
5. **Scope boundary (release 1, confirmed by the product owner, [AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) §4).** LAN sharing covers compiler caches (sccache WebDAV, ccache helper) and the transfer CAS used by placement. Accepted future work ([product definition](../product/product-definition.md) §7):
   - **dependency caches** (NuGet, npm, Cargo, pip; roadmap RM-02): each node keeps its own managed cache and downloads from the upstream registries; per-attempt package counts across nodes, and download sizes where the tools report them (§7, [07](07-records-diagnosis-memory.md) §1.5), show what sharing would save;
   - **FASTBuild remote workers** (roadmap RM-03): `-dist` use is observed and labelled, never managed (§3.8).

## 7. Effectiveness and duplicates

`CacheService.GetCacheReport` shows the following (R-CACHE-008):
- Hit and miss counts per attempt, from each attempt's own sccache statistics and ccache statistics log; per cache, their sums and the sccache store's ledger. `ccache --print-stats` reports the whole cache, so it serves only cache-wide totals.
- NuGet restore counters: packages installed versus reused, parsed from restore output, and http-cache growth per attempt.
- Per-attempt cache usage and downloads (`CacheUsage`, [07](07-records-diagnosis-memory.md) §1.5): what each attempt added to or used from each managed cache.
- Result cache `OBSERVE` mode: observations and would-be hits per period ([04](04-execution.md) §11).
- **Duplicate cache copies:** global-packages-like folders found by disk analysis outside the managed cache, such as `~/.nuget/packages` or per-task `NUGET_PACKAGES` folders seen in unmanaged processes' environments where readable. The report gives package-version overlap with the managed cache and the reclaimable bytes.
- **Per-task restores:** managed attempts whose caller overrode `NUGET_PACKAGES` with a unique folder. These raise finding `PER_TASK_RESTORE`.
