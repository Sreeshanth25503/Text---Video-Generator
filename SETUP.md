# Quick Setup Guide

This guide helps you get the text-to-video generator running on your machine in minutes.

## ⚡ Quick Start (5 minutes)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/text-to-video-generator.git
cd text-to-video-generator
```

### Step 2: Install Python (if you don't have it)

- Download Python 3.8+ from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation
- Verify: `python --version`

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

⏰ **Time: 10-15 minutes** (downloads ~3 GB of packages + AI models)

### Step 4: Run Your First Video!

**Option A: Command Line (Fastest)**

```bash
python main.py
```

Generates a test video in ~10 seconds

**Option B: Advanced Features**

```bash
python advanced_generator.py
```

Generates video with custom settings and metadata

**Option C: Web Interface (Best)**

```bash
python web_interface.py
```

Opens browser at `http://127.0.0.1:7860` - use sliders to generate!

---

## 💻 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 8 GB minimum (16 GB recommended)
- **Storage**: 15 GB free (for models + videos)
- **GPU**: Optional but ~10x faster
  - NVIDIA GPU recommended (RTX 3050+)
  - CPU works but very slow (5-10 minutes per video)

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named..."

```bash
pip install -r requirements.txt
```

### "CUDA out of memory"

Edit main.py or run with smaller settings:

```python
num_frames=8  # Instead of 16
num_inference_steps=15  # Instead of 25
```

### "Model download is slow"

- First run downloads 7GB model (normal!)
- Subsequent runs use cached model (fast)
- Be patient on first generation

### "Generation takes too long"

- Using CPU? (Switch to GPU if possible)
- Too many frames? (Try 8 instead of 16)
- Too many steps? (Try 15 instead of 25)

---

## 📚 Project Structure

```
text-to-video-generator/
├── main.py                    # Basic version (start here!)
├── advanced_generator.py      # Advanced with more features
├── web_interface.py           # Web UI (no coding needed)
├── run_all.py                 # Test all 3 versions
├── requirements.txt           # Dependencies
├── readme.md                  # Full documentation
├── SETUP.md                   # This file
├── LICENSE                    # MIT license
├── generated_videos/          # Your videos go here
└── model_cache/               # Downloaded AI models
```

---

## 🚀 Usage Examples

### Example 1: Basic Generation

```bash
python main.py
```

### Example 2: Advanced with Custom Settings

```python
from advanced_generator import AdvancedTextToVideoGenerator

generator = AdvancedTextToVideoGenerator()
generator.generate_video(
    prompt="A cat playing with yarn",
    negative_prompt="blurry, low quality",
    num_frames=16,
    guidance_scale=9.0,
    output_path="my_video.mp4"
)
```

### Example 3: Batch Generation

```python
prompts = [
    "A rocket launching",
    "Ocean waves",
    "Butterfly on flower"
]
generator.batch_generate(prompts, output_folder="videos")
```

### Example 4: Web Interface

```bash
python web_interface.py
# Opens browser automatically at http://127.0.0.1:7860
```

---

## 📖 For Interviewers/Others

To run this project from GitHub:

1. **Clone it**

   ```bash
   git clone https://github.com/YOUR-USERNAME/text-to-video-generator.git
   cd text-to-video-generator
   ```

2. **Install requirements**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run it**
   ```bash
   python run_all.py
   ```
   Or run individual versions:
   - `python main.py` (quick test)
   - `python advanced_generator.py` (with features)
   - `python web_interface.py` (interactive UI)

---

## 🎯 Test Videos Generated

After running, you'll find videos in `generated_videos/` folder:

- `test_basic.mp4` - from main.py
- `test_advanced.mp4` - from advanced_generator.py
- `video_*.mp4` - from web_interface.py

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] Can run `python main.py` without errors
- [ ] Video file generated in `generated_videos/`
- [ ] Web interface launches with `python web_interface.py`

---

## 📞 Still Having Issues?

1. Check [readme.md](readme.md) for detailed documentation
2. Review [Troubleshooting](readme.md#troubleshooting) section
3. Check error messages carefully
4. Try with smaller settings (8 frames, 15 steps)

---

**Good luck! Have fun generating videos!** 🎬
