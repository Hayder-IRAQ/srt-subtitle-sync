<div align="center">

# 🎬 SRT Subtitle Sync Tool

**Fix subtitle timing in seconds — single files or entire folders, with a clean modern GUI.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2%2B-green)](https://github.com/TomSchimansky/CustomTkinter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()

</div>

---

## 🔧 The Problem

You download a movie subtitle file and the text is always **0.5 seconds too early** or **2 seconds too late**. Every single line. Fixing them one by one is impossible.

**SRT Subtitle Sync Tool** shifts all timestamps in one click.

---

## ✨ Features

| Feature | Details |
|---|---|
| ⏱️ **Precise timing** | Adjust by any amount — e.g. `-0.5`, `+2`, `-1.3` seconds |
| 📁 **Batch processing** | Add individual files or scan an entire folder recursively |
| 🚀 **Quick buttons** | One-click presets: -2s, -1s, -0.5s, +0.5s, +1s, +2s |
| 💾 **Flexible output** | Save with custom suffix, to a different folder, or overwrite original |
| 🔒 **Safe by default** | Creates `_Synced` copies — never overwrites unless you choose to |
| 🌙 **Modern dark UI** | Built with CustomTkinter |
| 🔠 **Encoding support** | Handles UTF-8, UTF-8 BOM, and Latin-1 (older SRT files) |
| ⚡ **Non-blocking** | Processing runs in a background thread — UI stays responsive |

---

## 🚀 Quick Start

### 1. Install dependency
```bash
pip install customtkinter
```

### 2. Run
```bash
python main.py
```

### 3. Use
1. Click **Add Files** or **Add Folder** to select your `.srt` files
2. Enter the time offset (e.g. `-0.5` to shift subtitles 0.5 seconds earlier)
3. Choose output settings (suffix, folder, or overwrite)
4. Click **START SYNC** 🚀

---

## 📸 Screenshot

> _Coming soon_

---

## 📦 Requirements

| Package | Purpose |
|---|---|
| `customtkinter` | Modern dark-themed GUI |
| `tkinter` | Built into Python — no install needed |

Everything else (`re`, `threading`, `pathlib`, `datetime`) is Python standard library.

---

## ⚙️ How It Works

SRT timestamps look like this:
```
00:01:23,456 --> 00:01:25,789
```

The tool finds every timestamp with a regex pattern and shifts it by your specified offset using Python's `datetime` + `timedelta`. Negative times are clamped to `00:00:00,000` automatically.

---

## 🗂️ Project Structure

```
srt-subtitle-sync/
├── main.py          # Full application (single file)
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 💡 Example

Subtitles appear **1 second too late**:
- Enter `-1` in the time field
- Click START SYNC
- Done — all timestamps shifted back by 1 second

Subtitles appear **2.5 seconds too early**:
- Enter `+2.5`
- Click START SYNC

---

## 🤝 Contributing

Contributions welcome! Ideas:
- Support for `.ass` / `.vtt` subtitle formats
- Preview before saving
- Auto-detect offset from audio

Fork → feature branch → PR.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Hayder Odhafa / حيدر عذافة**
GitHub: [@Hayder-IRAQ](https://github.com/Hayder-IRAQ)

---

<div align="center">
Made with ❤️ — SRT Subtitle Sync Tool v1.0 © 2025 Hayder Odhafa
</div>
