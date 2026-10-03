---
date:
  created: 2026-09-30
---

# 0.24.1 NSCANgClient leaves the Windows installer after antivirus detections

0.24.1 is a small follow-up to 0.24.0 with one change: the Windows installer
no longer ships `NSCANgClient`, because a few antivirus engines report its DLL
as malware and made the whole MSI look infected. The module is still in the
Windows zip, still signed, and is copied into place by hand.

This release is **only a workaround** for what are most likely false positives,
not a fix: the module's code is the same as in 0.24.0, and nothing else
changed. **If you use `NSCANgClient` on Windows, stay on (or install) the
0.24.0 build instead**, which still ships the module in the installer.

## ✨ Highlights

- ⚠️ **Only a workaround: `NSCANgClient` users should use 0.24.0.** 0.24.1
  changes nothing but the packaging of this one module. If you submit results
  over NSCA-NG from Windows, the 0.24.0 installer gives you the same module
  without the manual copy.

- 📦 **`NSCANgClient` is no longer in the Windows MSI.** Four antivirus engines
  on VirusTotal flag `NSCANgClient.dll` from 0.24.0 with generic
  machine-learning verdicts. Until the vendors have analysed it, the module
  ships in the Windows zip only. Linux and macOS packages are unchanged. (#1615)
- 🔒 **A security notice on what the detections do and do not mean.** The
  verdicts are likely false positives but unconfirmed, and the release's
  signature, attestation and checksums show the file was not altered after the
  build, not that the build itself was clean. The notice and FAQ 1.12 spell out
  both.
- 🪟 **The DLL stays signed in the zip.** The signing list is read from the
  installer sources, so leaving the module out of the MSI would have dropped it
  from signing too; it is now kept on the list explicitly.

## 🔍 Detailed changes

### 📦 Windows installer — `NSCANgClient` removed

The detections come from Avast and AVG (`Win64:Evo-gen [Trj]`), Avira and
WithSecure (`TR/W64.Evo`), Sophos (`Mal/Generic-S`) and Trellix (`Artemis`).
Microsoft Defender and the other engines report the file as clean. All four
are generic verdicts that score what a file looks like rather than signatures
for a known malware family, and a small, rarely seen DLL whose code is mostly a
TLS handshake over raw sockets is a shape they are known to over-fire on.

Because a flagged installer is enough for a download to be blocked, the
`NSCANgClient` component is taken out of the MSI until the vendors clear it. It
remains in the Windows zip, Authenticode-signed like every other binary of the
release and covered by the zip's `SHA256SUMS`. If a configured
`NSCANgClient = enabled` cannot find the module, the load-failure hint now says
to copy the DLL from the zip instead of pointing at an installer feature that no
longer exists.

If you use NSCA-NG from Windows, the simplest option is to stay on 0.24.0. To
run 0.24.1 and keep using it, copy `modules\NSCANgClient.dll` from the
zip of the **same version and platform** into the installation's `modules`
folder, after this upgrade and after every later one. The steps are on the
[NSCANgClient reference](https://nsclient.org/docs/reference/client/NSCANgClient/)
page.

### 🔒 Documentation — antivirus detections

- A new [security notice](https://nsclient.org/docs/security/notices/) describes the detections, what the release evidence
  (signature, Sigstore build provenance attestation, `SHA256SUMS`) rules out,
  and what it cannot rule out: a compromise before the signature.
- FAQ 1.12 now separates what those checks prove from what they cannot, and
  sends failed checks or signs of a real compromise to a private GitHub
  security advisory.
- The NSCA-NG scenario, the installing page and the installer options table
  point Windows users at the manual install.

## ⚠️ Upgrade notes

The full list is on the [upgrading page](https://nsclient.org/docs/setup/upgrading/).

- **Windows, `NSCANgClient` users: use 0.24.0 instead.** 0.24.1 is only a
  workaround for the antivirus detections and has nothing else in it, so
  staying on 0.24.0 keeps the module installed and managed by the MSI. If you
  upgrade anyway: an MSI upgrade removes the copy an earlier
  installer put there, and the service then logs that the module was not found.
  Copy `modules\NSCANgClient.dll` from the matching zip into the `modules`
  folder after upgrading, and again after every later upgrade: the installer
  does not own a file copied this way, so it never replaces it. Check the file
  first as FAQ 1.12 shows. Nothing to do if you do not use NSCA-NG on Windows,
  or on Linux and macOS.

## Download

[You can download the new version from GitHub](https://github.com/mickem/nscp/releases/0.24.1){ .md-button }

// Michael Medin
