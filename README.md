<div align="center">

# 📺 yuki-iptv

**IPTV player with EPG support**
Community-maintained continuation of the original [liya/yuki-iptv](https://codeberg.org/liya/yuki-iptv)

[![GitHub Release](https://img.shields.io/github/v/release/itachi-re/yuki-iptv)](https://github.com/itachi-re/yuki-iptv/releases)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](./COPYING)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey?logo=linux)](https://github.com/itachi-re/yuki-iptv)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![GitHub Issues](https://img.shields.io/github/issues/itachi-re/yuki-iptv)](https://github.com/itachi-re/yuki-iptv/issues)
[![Last Commit](https://img.shields.io/github/last-commit/itachi-re/yuki-iptv)](https://github.com/itachi-re/yuki-iptv/commits)
[![Total Downloads](https://img.shields.io/github/downloads/itachi-re/yuki-iptv/total)](https://github.com/itachi-re/yuki-iptv/releases)
</div>

> **yuki-iptv plus** — this repository ([serif453/yuki-iptv-plus](https://github.com/serif453/yuki-iptv-plus))
> is based on [itachi-re/yuki-iptv](https://github.com/itachi-re/yuki-iptv) and adds
> **recording while watching over a single connection** (no second connection to
> the provider) and a **Flatpak** package. The rest of this README describes the
> upstream project; its distro packages are published by itachi-re.

---

## 🎯 Our Goals

yuki-iptv plus exists to keep a great Linux IPTV player alive and to make it
better at the things viewers actually need.

- **Record without a second connection.** Most IPTV providers allow only one
  stream per account. Recording what you are watching should never cost you a
  second connection, so we record from the stream you are already playing.
- **Reliable recordings.** Recordings should survive reconnects, notice when
  nothing is being written, and never silently overwrite earlier footage.
- **Works on any distro.** A Flatpak package means the same app on Fedora,
  Ubuntu, Arch, openSUSE and everything in between, with no building from
  source.
- **Stay open and trustworthy.** Free software under GPL-3.0-or-later, a
  transparent history traced back to the original project, and releases
  published directly from this repository.
- **Respect the upstream project.** This is a community continuation, not a
  rebrand. Credit stays with the original authors, and fixes that belong
  upstream are shared back.
- **Player only, never content.** yuki-iptv does not provide, host, or bundle
  any channels or playlists. You bring your own legal sources.

---

## ⏺️ Record While Watching

Record the channel you are watching, **over the same single connection**.

When you press record, yuki-iptv plus saves the packets that are already
arriving for playback straight to a file. It does not open a second connection
to your provider and does not re-encode the video, so:

- ✅ **No extra connection:** works with accounts limited to one stream.
- ✅ **No quality loss:** the stream is copied as it is, without re-encoding,
  with very low CPU usage.
- ✅ **Watch and record at the same time:** playback is not interrupted.
- ✅ **Survives reconnects:** if the stream drops and reloads, recording
  continues in a new `_part2`, `_part3`, … file instead of overwriting the
  previous one.
- ✅ **Safe by design:** switching to another channel ends the recording, and
  you are warned if no data has been written for about 20 seconds.

**How to use it**

1. Start playing a channel.
2. Press the **Record** button, or the `R` hotkey (configurable in the
   keybinds settings).
3. Press it again to stop. Your file is finalized and ready to play.

**Tips**

- Use the `.ts` or `.mkv` container for recordings. Other formats are not
  recommended for stream copying.
- With the Flatpak package, choose your Videos or Downloads folder as the save
  folder in the settings so recordings are easy to find.

---

## ⚠️ Project Status

> **🧪 Early Testing Phase — Expect Bugs**
>
> This fork is in its **early stages**. Core functionality works, but rough edges
> exist and things may break between releases. Bug reports are not just
> tolerated — they are actively helpful. If something doesn't work, please
> [open an issue](https://github.com/itachi-re/yuki-iptv/issues).

The original upstream repository, [`liya/yuki-iptv`](https://codeberg.org/liya/yuki-iptv)
on Codeberg, has since been **removed entirely** (as of this writing the
repository returns a 404, and its listing on [Repology](https://repology.org/project/yuki-iptv/packages)
now flags the upstream homepage as dead). This is a change from the project's
earlier "archived" status. This repository is an independent, unofficial
continuation starting from upstream's final known commit (`72a32225be`,
archived on 2025-08-27) and is maintained here going forward.

Because the original repository is gone, the commit history linked above
may also disappear if Codeberg or GitHub caches expire — anyone with a local
clone predating the removal is encouraged to open an issue or PR so we can
preserve as much of that history as possible.

> **🔒 A note on trust:** this project's name has previously been targeted by lookalike forks bundling malicious code. Before installing from anywhere, verify the commit history traces cleanly back to a known source, and prefer release artifacts published directly from **this repository** over random third-party mirrors.

---

## ✨ Features

| Category | Features |
|---|---|
| **Playlists** | M3U / M3U8 / XSPF, XTream API |
| **Streams** | UDP multicast, HTTP, HLS (M3U8) |
| **Guide** | EPG via XMLTV and JTV formats |
| **Recording** | Stream recording with hotkeys |
| **Customization** | Per-channel video settings, user agent / Referer override |
| **Integration** | MPRIS support (media keys, desktop) |
| **VOD / Series** | Group-based movie/series organisation |
| **UI** | Channel search, favorites, groups, hide channels, tech info overlay |

> ⚠️ **Disclaimer:** yuki-iptv does not provide, host, or bundle any content, playlists, or TV channels. It is a player only. Channels shown in screenshots are for demonstration purposes only. See the Legal section below and [`DISCLAIMER.md`](./DISCLAIMER.md).

---

## 📦 Installation

### 📦 Flatpak (any distro)

yuki-iptv plus is currently distributed as a **Flatpak**, which works on any
Linux distribution.

Download `yuki-iptv-plus.flatpak` from
[Releases](https://github.com/serif453/yuki-iptv-plus/releases), then:

```bash
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install --user ./yuki-iptv-plus.flatpak
flatpak run io.github.serif453.YukiIptvPlus
```

Settings live in `~/.var/app/io.github.serif453.YukiIptvPlus/`. To keep
recordings somewhere easy to find, choose your Videos or Downloads folder as
the save folder in the settings.

---

### 🔧 Running from Source

```bash
git clone https://github.com/serif453/yuki-iptv-plus.git
cd yuki-iptv-plus
# Install dependencies listed in debian/control first
# At minimum: Python 3, PyQt, mpv
python3 usr/lib/yuki-iptv/yuki-iptv.py
```

If the entry point has moved, look under `usr/lib/yuki-iptv/` for the current main script.

**Dependencies:** see `debian/control` for the authoritative list. `usr/lib/yuki-iptv/thirdparty/` vendors `mpv.py` and `xtream.py` directly rather than pulling them via pip.

---

### 🗓️ Other Distributions and Platforms — Coming Over Time

> **🌍 More packages are planned.** This fork started with Flatpak, so that is
> the only officially supported install method for now. Installation guides
> for other distributions (native packages for openSUSE, Fedora, Arch, Debian
> and Ubuntu) will be added here as each package becomes available.
> Windows and macOS are long-term goals.

In the meantime, [running from source](#-running-from-source) works on any
Linux distro with Python 3, PyQt, and `mpv` available. If you'd like to
contribute packaging or platform support, pull requests are very welcome.

---

## 🗂️ Project Layout

```
usr/lib/yuki-iptv/
├── yuki-iptv.py          # Main entry point
├── yuki_iptv/            # Application modules (GUI, EPG, playlist, XTream, recording, MPRIS…)
└── thirdparty/           # Vendored libs: mpv.py, xtream.py (check individual license headers)
usr/bin/yuki-iptv         # Installed launcher script
usr/share/                # Desktop file, icons, assets
po/                       # Translation files (.po / .pot)
debian/                   # Debian packaging
```

---

## 📺 Making Playlists for Movies / Series (VOD)

Use the group `VOD` for movies:

```text
#EXTM3U
#EXTINF:-1 group-title="VOD",Channel 1
https://example.com
#EXTINF:-1 group-title="VOD SomeGroup",Channel 2
https://example.com
```

Use `SxxExx` in an entry's name to have it recognised as a series episode — for example `S01E12` for Season 1, Episode 12:

```text
#EXTM3U
#EXTINF:-1 tvg-name="SomeName S04E06 Season Title 1" group-title="SERIES SomeName",
file:///home/user/Videos/SomeName_4/SomeName.S04E06.mp4
```

---

## 🌐 Localization

Translation files live under `po/`. To help translate, edit the relevant `.po` file for your language and open a pull request. If a file for your language doesn't exist yet, generate one from `yuki-iptv.pot`.

---

## 🐛 Reporting Bugs

Since this fork is in early testing, **bug reports are especially valuable right now.**

Please include:
- Your distribution and version (e.g. openSUSE Tumbleweed, snapshot date)
- How you installed (Flatpak / from source)
- Steps to reproduce the issue
- Any relevant log output or error messages

→ [Open an issue](https://github.com/serif453/yuki-iptv-plus/issues)

---

## ⚖️ Legal

> This is a summary. The full text is in [`DISCLAIMER.md`](./DISCLAIMER.md).
> It is not legal advice, and laws differ between countries.

- **Player only.** yuki-iptv plus does not provide, host, sell or bundle any
  channels, streams, playlists or EPG data. No playlist is included.
- **Your sources, your responsibility.** Use only content you have the legal
  right to access. Do not use the software with pirated or unauthorized
  streams.
- **Recording is for personal use.** Recording features copy the stream you are
  already watching to your own device. Do not share or sell recordings unless
  you hold the rights, and check the rules in your country and your provider's
  terms.
- **No circumvention.** The software does not remove or bypass DRM,
  encryption, paywalls or geo-restrictions, and such contributions are not
  accepted.
- **No affiliation.** This is an independent, unofficial fork. It is not
  endorsed by any broadcaster, provider, or the authors of the original
  yuki-iptv. All trademarks and logos belong to their owners.
- **No warranty.** Provided "as is" under GPL-3.0-or-later, without warranty
  of any kind.
- **Privacy.** The source code contains no telemetry or analytics. The app only
  connects to the playlist, EPG and stream addresses you configure.
- **Copyright complaints.** This repository hosts source code only. Notices
  are handled as described in [`DISCLAIMER.md`](./DISCLAIMER.md#8-copyright-complaints-and-takedown-requests).

---

## 📜 License

yuki-iptv is free software, licensed under the **GNU General Public License v3.0 or later**. See [`COPYING`](./COPYING) for the full license text.

yuki-iptv is based on **Astroncia IPTV**, originally licensed GPL-3.0-only. The original yuki-iptv author received permission from Astroncia's author to relicense the code as GPL-3.0-or-later — see [`LICENSE-NOTICE.txt`](./LICENSE-NOTICE.txt) for that clarification.

Font Awesome icons (Font Awesome Free 5.15.4) are licensed under CC BY 4.0 — see [`LICENSE-CC-BY-4.0.txt`](./LICENSE-CC-BY-4.0.txt).

This software is distributed **WITHOUT ANY WARRANTY**; see `COPYING` for details.

---

## 🙏 Credits

- Originally created and maintained by **[liya](https://codeberg.org/liya)**
- Based on **Astroncia IPTV**
- Continued here by **[itachi-re](https://github.com/itachi-re)** since June 2026

---

## 🤝 Contributing

Bug reports, fixes, features, and translations are all welcome.
Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a pull request.
