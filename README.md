# 🎬 Text-to-Video Generator

> AI-powered video generation from text descriptions using the **DAMO ViLab diffusion model**.

[![Live Demo](https://img.shields.io/badge/🤗%20Live%20Demo-HuggingFace%20Spaces-yellow)](https://huggingface.co/spaces/Sreeshanth25503/text-to-video-generator)
[![Showcase](https://img.shields.io/badge/🌐%20Showcase-GitHub%20Pages-blue)](https://sreeshanth25503.github.io/Text---Video-Generator/)
[![GitHub](https://img.shields.io/badge/⭐%20GitHub-Source%20Code-black)](https://github.com/Sreeshanth25503/Text---Video-Generator)
[![License](https://img.shields.io/badge/License-MIT-green)](#)

---

## 🚀 Quick Start

```bash
git clone https://github.com/Sreeshanth25503/Text---Video-Generator.git
cd Text---Video-Generator
pip install -r requirements.txt
python web_interface.py        # open http://127.0.0.1:7860
```

> ⚠️ First run downloads the AI model (~7 GB). Subsequent runs use local cache.

---

## 📁 Project Files

### Core Scripts

- **`main.py`** — Basic generator
  - Contains `TextToVideoGenerator` class
  - Two methods: `generate_video()` (single) and `generate_multiple_videos()` (batch)
  - Detects GPU/CPU automatically; applies memory optimisations on CUDA

- **`advanced_generator.py`** — Advanced generator with full control
  - `AdvancedTextToVideoGenerator` class extends the basic version
  - Extra features: negative prompts, custom resolution (height/width), seed control, metadata saving
  - `batch_generate()` with `tqdm` progress bar
  - `compare_settings()` — generates fast / balanced / high-quality versions of the same prompt
  - Saves a `.json` recipe file alongside each video

- **`web_interface.py`** — Gradio browser UI
  - Loads model once at startup (module-level, faster)
  - Clean two-column layout: inputs on left, video output on right
  - Sliders for frames, steps, guidance scale; seed input; example prompts
  - Saves all generated videos to `generated_videos/`
  - Shows generation time, file size, and save path in status box

- **`run_all.py`** — Master test/launcher script
  - Runs basic and advanced generators in sequence as a test suite
  - Asks interactively whether to launch the web interface
  - Prints a pass/fail summary at the end

- **`app.py`** — HuggingFace Spaces entry point
  - Thin wrapper that calls `build_ui()` from `web_interface.py`
  - Used when the project is deployed to HuggingFace Spaces

### Config & Docs

- **`requirements.txt`** — All Python dependencies (torch, diffusers, gradio, etc.)
- **`.gitignore`** — Excludes `model_cache/`, generated videos, `__pycache__`, etc.
- **`LICENSE`** — MIT License
- **`README_SPACES.md`** — HuggingFace Spaces metadata + short description

### Showcase

- **`docs/index.html`** — GitHub Pages showcase site
  - Dark theme landing page with feature cards, tech stack, and "Try Live Demo" button
  - No build step needed — pure HTML/CSS

### Auto-created at runtime *(not in git)*

- **`generated_videos/`** — MP4 output files
- **`model_cache/`** — Downloaded AI model weights (~7 GB)

---

## ⚙️ Parameters

| Parameter | What it controls | Default |
|-----------|-----------------|---------|
| `prompt` | Video description | required |
| `negative_prompt` | What to avoid | none |
| `num_frames` | Frames ÷ 8 fps = video length | 8 |
| `num_inference_steps` | Quality (more = better, slower) | 20 |
| `guidance_scale` | How strictly prompt is followed | 7.5 |
| `seed` | Reproducibility (-1 = random) | -1 |

---

## ⚡ Performance (RTX 3050 · 4 GB VRAM)

| Frames | Steps | Time | Quality |
|--------|-------|------|---------|
| 8 | 15 | ~1–2 min | Good |
| 16 | 25 | ~3–5 min | Excellent |
| 24 | 25 | ~6–9 min | High |

---

## 🛠️ Troubleshooting

- **GPU out of memory** → set Frames = 8, Steps = 15
- **Slow generation** → verify CUDA is detected (look for 🟢 badge in UI)
- **Import errors** → `pip install -r requirements.txt --upgrade`

---

## 📡 Live Demo & Showcase

| Link | What it is |
|------|-----------|
| [🤗 HuggingFace Spaces](https://huggingface.co/spaces/Sreeshanth25503/text-to-video-generator) | Working live demo (free GPU) |
| [🌐 GitHub Pages](https://sreeshanth25503.github.io/Text---Video-Generator/) | Project showcase site |

---

## 🏗️ Tech Stack

`PyTorch 2.5` · `Diffusers 0.36` · `Gradio 6` · `CUDA 12.1` · `Transformers` · `imageio-ffmpeg` · `HuggingFace Hub`

**Model:** [`damo-vilab/text-to-video-ms-1.7b`](https://huggingface.co/damo-vilab/text-to-video-ms-1.7b) — 1.7B parameter text-to-video diffusion model by DAMO Academy (Alibaba Group)

---

## 📜 License

MIT — see [LICENSE](LICENSE)

**Author:** [Sreeshanth](https://github.com/Sreeshanth25503) · Last updated: June 2026
