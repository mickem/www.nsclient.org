# Supported platforms

<!-- @formatter:off -->
!!! note "Support policy is being formalized"
    The matrix below reflects the current state. The exact set of supported versions, the cadence of legacy builds, and the long-term plan for Windows XP support are still being finalised and may change.
<!-- @formatter:on -->

NSClient++ is built for two operating system families: Windows and Linux.

## Windows

There are two Windows editions:

| Edition  | Supported on                                  | Installer           | Notes                                                                                                                                                |
|----------|-----------------------------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| Standard | Windows Server 2008 R2 / Windows 7 and later  | MSI (recommended)   | The mainline build. New features and fixes land here first.                                                                                          |
| Legacy   | Windows XP (latest Service Pack), Server 2003 | Manual install only | Best-effort build for older systems. The MSI installer is not supported on XP; the binaries need to be deployed and registered as a service by hand. |

The standard edition is built for 32-bit, 64-bit and ARM64; pick the one that matches the host architecture. The ARM64 build (Windows 11 ARM, Server 2025 ARM) ships without `PythonScript` and without the bundled Visual C++ runtime — install [vc_redist.arm64.exe](https://aka.ms/vs/17/release/vc_redist.arm64.exe) before the agent.

## Linux

NSClient++ runs on most modern Linux distributions. There is no single "minimum version" — what matters is that the C++ runtime and OpenSSL versions in the distribution are recent enough for the packaged build to load. The releases page lists packages for the distributions that are tested for each release.

Raspberry Pi OS is covered by the Debian 13 (Trixie) arm64 package, which works on a Pi 3 or newer running the 64-bit image, and on Debian 13 arm64 in general. There is no 32-bit Pi package — Raspberry Pi OS has defaulted to 64-bit since Bookworm.

## Architectures

* Windows: x86 (32-bit), x64 (64-bit) and ARM64
* Linux: x86_64 and arm64 (aarch64); others may build from source

## Choosing an edition on Windows

If the target machine runs Windows 7 / Server 2008 R2 or newer, use the **standard** edition — that is the only edition that receives new features.

The **legacy** edition only exists so that older estates (typically Windows XP and Server 2003) can still report into a modern monitoring server. New deployments should not start on the legacy edition.
