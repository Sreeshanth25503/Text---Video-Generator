# 🎬 Text-to-Video Generator

A complete AI-powered application that converts text descriptions into short videos using diffusion models.

---

## 📚 What This Project Does

This project uses AI (specifically diffusion models) to generate videos from text. For example:
- Input: "A cat playing with a ball of yarn"
- Output: A 2-second video showing exactly that!

**How it works (simple explanation):**
1. You give the AI a text description
2. The AI "imagines" what that would look like frame by frame
3. The frames are combined into a video

---

## 🗂️ Project Structure

```
text-to-video-generator/
│
├── main.py                  # Basic video generator (start here!)
├── advanced_generator.py    # Advanced version with more features
├── web_interface.py         # Web UI for easy use (no coding needed)
├── requirements.txt         # List of packages to install
├── README.md               # This file - project documentation
│
├── generated_videos/       # Your generated videos go here
├── model_cache/            # Downloaded AI models stored here
└── gradio_outputs/         # Videos from web interface
```

---

## 🚀 Getting Started

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed.
- Check: Open terminal and type `python --version`
- Download from: https://www.python.org/downloads/

### Step 2: Install Required Packages
Open terminal in your project folder and run:
```bash
pip install -r requirements.txt
```

**This will install:**
- PyTorch (the AI brain)
- Diffusers (contains video generation models)
- Transformers (understands text)
- OpenCV (works with videos)
- And other helpful tools

⏰ **Note:** Installation may take 10-15 minutes depending on your internet speed.

### Step 3: Run Your First Video!

**Option A: Command Line (Basic)**
```bash
python main.py
```
This will generate example videos automatically.

**Option B: Web Interface (Easiest)**
```bash
pip install gradio  # If not already installed
python web_interface.py
```
Then open the URL shown in your browser and start generating!

---

## 💡 How to Use

### Basic Usage (main.py)

```python
from main import TextToVideoGenerator

# Create the generator
generator = TextToVideoGenerator()

# Generate a video
generator.generate_video(
    prompt="A dog running on the beach",
    num_frames=16,           # 16 frames = ~2 seconds
    num_inference_steps=25,  # Higher = better quality
    output_path="my_video.mp4"
)
```

### Advanced Usage (advanced_generator.py)

```python
from advanced_generator import AdvancedTextToVideoGenerator

generator = AdvancedTextToVideoGenerator()

# Generate with negative prompt (tell AI what to avoid)
generator.generate_video(
    prompt="A beautiful sunset over mountains",
    negative_prompt="blurry, low quality, distorted",
    num_frames=16,
    guidance_scale=9.0,  # How strictly to follow prompt
    seed=42,             # For reproducible results
    output_path="sunset.mp4"
)

# Generate multiple videos at once
prompts = [
    "A cat sleeping",
    "A car driving",
    "Birds flying"
]
generator.batch_generate(prompts, output_folder="my_videos")

# Compare different quality settings
generator.compare_settings(
    prompt="A rocket launching",
    output_folder="comparison"
)
```

### Web Interface Usage

1. Run: `python web_interface.py`
2. Open browser (automatically opens)
3. Fill in the form:
   - **Prompt**: What you want to see
   - **Negative Prompt**: What to avoid (optional)
   - **Settings**: Adjust quality and length
4. Click "Generate Video"
5. Wait 1-3 minutes
6. Download your video!

---

## 🎛️ Parameter Guide

### Essential Parameters

| Parameter | What It Does | Good Values | Effect |
|-----------|--------------|-------------|--------|
| **prompt** | Your text description | Any text | What appears in video |
| **negative_prompt** | What to avoid | "blurry, low quality" | Improves quality |
| **num_frames** | Video length | 8-32 | More = longer video |
| **num_inference_steps** | Quality iterations | 15-50 | More = better quality |
| **guidance_scale** | Follow prompt strength | 7-12 | Higher = more accurate |
| **seed** | Reproducibility | Any number | Same seed = same video |

### Understanding the Numbers

**num_frames:**
- 8 frames = ~1 second (very short)
- 16 frames = ~2 seconds (standard)
- 24 frames = ~3 seconds (longer)
- 32 frames = ~4 seconds (maximum)

**num_inference_steps:**
- 15 steps = Fast but lower quality
- 25 steps = Good balance (recommended)
- 50 steps = Best quality but slow

**guidance_scale:**
- 7.0 = More creative/loose interpretation
- 9.0 = Balanced (recommended)
- 12.0 = Very strict to prompt
- 15.0 = Maximum adherence

---

## 🎯 Example Prompts

### Good Prompts (Clear and Descriptive)
✅ "A cat playing with a ball of yarn, realistic style"
✅ "Sunset over the ocean, cinematic, golden hour"
✅ "A robot dancing in a futuristic city at night"
✅ "Flowers blooming in a garden, time-lapse style"
✅ "Waves crashing on a rocky beach, slow motion"

### Avoid Vague Prompts
❌ "Something cool"
❌ "A video"
❌ "Nice scenery"

### Tips for Better Results
1. **Be specific**: Include details like style, time of day, mood
2. **Add style keywords**: "cinematic", "realistic", "cartoon style"
3. **Use negative prompts**: Add "blurry, low quality, distorted"
4. **Keep it simple**: 1-2 sentences work best
5. **Mention motion**: "walking", "flying", "spinning" helps

---

## ⚙️ Technical Details

### What Are Diffusion Models?

**Simple Explanation:**
Imagine an artist who:
1. Starts with random noise (like TV static)
2. Gradually removes the noise while adding details
3. Continues until a clear image/video emerges

That's how diffusion models work! They "denoise" random pixels into meaningful content guided by your text.

### The AI Pipeline

```
Your Text → Text Encoder → Diffusion Model → Video Frames → MP4 File
```

1. **Text Encoder**: Understands your prompt
2. **Diffusion Model**: Creates frames from noise
3. **VAE Decoder**: Converts AI data to viewable images
4. **Video Export**: Combines frames into MP4

### Model Information

**Default Model:** `damo-vilab/text-to-video-ms-1.7b`
- Size: ~7 GB
- Resolution: 256x256 pixels
- Length: Up to 32 frames (~4 seconds)
- Quality: Good for demonstrations and testing

---

## 🔧 Troubleshooting

### "CUDA out of memory"
**Problem:** Your GPU doesn't have enough memory
**Solution:**
```python
# Reduce these values:
num_frames=8          # Instead of 16
height=256, width=256 # Don't go higher
```

### "Model download is slow"
**Problem:** Large model files (7GB)
**Solution:** Be patient! First download takes time. It's saved for next use.

### "Generated video is blurry"
**Solutions:**
1. Increase `num_inference_steps` to 50
2. Add negative prompt: "blurry, low quality"
3. Increase `guidance_scale` to 11-12

### "Generation takes too long"
**Speed it up:**
```python
num_frames=8           # Fewer frames
num_inference_steps=15 # Fewer steps
# Trade quality for speed
```

### "ModuleNotFoundError"
**Problem:** Missing package
**Solution:**
```bash
pip install -r requirements.txt
# Or install specific package:
pip install diffusers torch
```

---

## 🖥️ System Requirements

### Minimum Requirements
- **CPU:** Modern multi-core processor
- **RAM:** 8 GB
- **Storage:** 15 GB free space
- **GPU:** Optional but recommended
- **OS:** Windows, macOS, or Linux

### Recommended for Best Performance
- **CPU:** Intel i7/AMD Ryzen 7 or better
- **RAM:** 16 GB or more
- **GPU:** NVIDIA GPU with 8GB+ VRAM (RTX 3070, 4060, etc.)
- **Storage:** 20 GB free space (SSD preferred)

### Performance Expectations

**With GPU (NVIDIA RTX 3070):**
- 16 frames, 25 steps: ~30 seconds

**Without GPU (CPU only):**
- 16 frames, 25 steps: ~5-10 minutes

---

## 📖 Learning Resources

### Understanding the Code

Each Python file has extensive comments explaining:
- What each function does
- What each parameter means
- Why we make certain choices

**Start here:**
1. Open `main.py`
2. Read the comments (text after `#`)
3. Run the code
4. Experiment with parameters

### Key Concepts to Learn

1. **PyTorch**: The math library that powers AI
2. **Diffusers**: Library with pre-trained models
3. **Transformers**: Helps AI understand text
4. **Tensors**: Multi-dimensional arrays (like matrices)

### Further Reading
- [Diffusers Documentation](https://huggingface.co/docs/diffusers)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [Stable Diffusion Guide](https://stable-diffusion-art.com/)

---

## 🎓 Project Ideas to Try

### Beginner
1. Generate videos from 10 different prompts
2. Compare fast vs slow generation settings
3. Try different styles (realistic, cartoon, cinematic)

### Intermediate
1. Create a video series with similar prompts
2. Build a custom prompt generator
3. Add video post-processing (filters, effects)

### Advanced
1. Fine-tune model on custom dataset
2. Create longer videos by stitching frames
3. Add audio generation
4. Build a full web application with database

---

## 📝 Notes and Tips

### Best Practices
- Start with default settings
- Use negative prompts for quality
- Save successful prompts for reuse
- Generate multiple versions and pick the best

### Common Mistakes to Avoid
❌ Setting num_frames too high (slow + memory issues)
❌ Forgetting negative prompts
❌ Using vague descriptions
❌ Not setting a seed for reproducibility

### Saving Time
- Use `seed` parameter to recreate good results
- Save metadata files (turned on by default)
- Start with low settings to test prompts
- Use batch generation for multiple videos

---

## 🤝 Contributing & Feedback

This is a learning project! Feel free to:
- Experiment and modify the code
- Add new features
- Share your generated videos
- Document what you learn

---

## 📜 License

This project uses open-source models and libraries:
- Model: DAMO-VILAB (Apache 2.0)
- Code: Educational use

---

## 🆘 Getting Help

If you're stuck:
1. Read error messages carefully
2. Check the Troubleshooting section above
3. Review the code comments
4. Try simpler settings first
5. Search the error on Google

---

## 🎉 Have Fun!

The best way to learn is by experimenting. Try different prompts, play with settings, and see what you can create!

**Remember:** Your first videos might not be perfect, and that's okay! Even professional AI researchers iterate many times to get good results.

Happy generating! 🎬✨