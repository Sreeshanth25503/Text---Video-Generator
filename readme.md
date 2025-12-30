# Text-to-Video Generator

An AI-powered application that converts text descriptions into short videos using diffusion models.

## Features

- **Text-to-Video Generation** - Create videos from text prompts
- **Three Usage Modes**:
  - Basic version (simple API)
  - Advanced version (full control over parameters)
  - Web interface (Gradio UI - no coding needed)
- **Advanced Controls**:
  - Negative prompts (specify what NOT to include)
  - Custom resolution, frame count, and quality settings
  - Seed control for reproducible results
  - Metadata saving for generation tracking
- **GPU Support** - CUDA acceleration for faster generation
- **CPU Fallback** - Works on CPU (slower but compatible)

## Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Sreeshanth25503/Text---Video-Generator.git
cd Text---Video-Generator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Usage

#### Option 1: Web Interface (Easiest)
```bash
python web_interface.py
```
- Opens automatically in your browser at http://127.0.0.1:7860
- No coding required - just type your prompt!

#### Option 2: Basic Version
```bash
python main.py
```
- Simple API for quick video generation
- Perfect for beginners

#### Option 3: Advanced Version
```bash
python advanced_generator.py
```
- Full control over all parameters
- Batch generation support
- Quality comparison features

#### Option 4: Run All Tests
```bash
python run_all.py
```
- Tests all three versions automatically
- Generates sample videos

## Example Usage

### Basic Generation
```python
from main import TextToVideoGenerator

generator = TextToVideoGenerator()
generator.generate_video(
    prompt="A cat playing with a yarn ball",
    num_frames=16,
    num_inference_steps=25,
    output_path="my_video.mp4"
)
```

### Advanced Generation
```python
from advanced_generator import AdvancedTextToVideoGenerator

generator = AdvancedTextToVideoGenerator()
generator.generate_video(
    prompt="A sunset over mountains, cinematic",
    negative_prompt="blurry, low quality",
    num_frames=16,
    guidance_scale=7.5,
    seed=42,
    output_path="sunset.mp4"
)
```

### Batch Generation
```python
from advanced_generator import AdvancedTextToVideoGenerator

generator = AdvancedTextToVideoGenerator()

prompts = [
    "A cat playing with a yarn ball",
    "A sunset over mountains",
    "A robot dancing in a city"
]

videos = generator.batch_generate(
    prompts,
    output_folder="batch_videos",
    num_frames=16,
    guidance_scale=7.5
)
```

### Compare Quality Settings
```python
from advanced_generator import AdvancedTextToVideoGenerator

generator = AdvancedTextToVideoGenerator()

results = generator.compare_settings(
    prompt="A beautiful sunset",
    output_folder="comparison"
)
```

## Parameters Explained

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `prompt` | What you want in the video | Required | Text |
| `negative_prompt` | What to avoid | None | Text |
| `num_frames` | Number of frames (video length) | 8 | 8-24 |
| `num_inference_steps` | Quality iterations | 20 | 10-50 |
| `guidance_scale` | How strictly to follow prompt | 7.5 | 1.0-10.0 |
| `height` / `width` | Video resolution in pixels | 256 | 256-512 |
| `seed` | For reproducible results | Random | Integer |
| `fps` | Frames per second | 8 | 8-24 |

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **GPU**: NVIDIA GPU with CUDA 11.8+ (4GB VRAM minimum)
- **CPU**: Works without GPU but ~5-10x slower
- **Storage**: 7GB for model cache + space for generated videos

## Performance Benchmarks

| Setting | Time | Quality | GPU Memory |
|---------|------|---------|-----------|
| Fast (8 frames, 15 steps) | 30-45s | Good | 2-3GB |
| Balanced (16 frames, 25 steps) | 1.5-2min | Excellent | 3-4GB |
| High Quality (24 frames, 50 steps) | 5-7min | Very High | 4GB+ |

## File Structure

```
Text---Video-Generator/
├── main.py                 # Basic generator
├── advanced_generator.py   # Advanced features
├── web_interface.py        # Gradio web UI
├── run_all.py             # Test suite
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── .gitignore             # Git configuration
└── .github/               # GitHub templates
    ├── CONTRIBUTING.md
    ├── SECURITY.md
    └── ISSUE_TEMPLATE/
        └── bug_report.md
```

## Troubleshooting

### Issue: "CUDA Out of Memory" Error
**Solution:**
- Reduce `num_frames` (try 8 instead of 16)
- Reduce `num_inference_steps` (try 15 instead of 25)
- Use `height=256, width=256` instead of larger values
- Close other GPU-consuming applications

### Issue: Slow Video Generation
**Solution:**
- If on CPU, consider using a GPU-enabled machine
- Reduce quality settings for faster results
- Use smaller frame counts for faster generation

### Issue: Model Download Fails
**Solution:**
- First run downloads ~7GB model (requires patience and stable internet)
- Model is cached in `model_cache` folder
- Subsequent runs will be much faster
- Check your internet connection

### Issue: ImportError - Module Not Found
**Solution:**
```bash
# Make sure all requirements are installed
pip install -r requirements.txt

# If still failing, try upgrading pip
pip install --upgrade pip
```

## Model Information

- **Model Name**: DAMO ViLab Text-to-Video MS 1.7B
- **Source**: Hugging Face Model Hub
- **Download Size**: ~7GB
- **License**: Model-specific (see Hugging Face card)
- **Citation**: DAMO ViLab team

## API Reference

### TextToVideoGenerator

```python
from main import TextToVideoGenerator

generator = TextToVideoGenerator(model_name="damo-vilab/text-to-video-ms-1.7b")

result = generator.generate_video(
    prompt="Your text prompt",
    num_frames=8,
    num_inference_steps=15,
    guidance_scale=7.5,
    output_path="output.mp4"
)

# Generate multiple videos
prompts = ["Video 1", "Video 2", "Video 3"]
videos = generator.generate_multiple_videos(
    prompts,
    output_folder="generated_videos"
)
```

### AdvancedTextToVideoGenerator

```python
from advanced_generator import AdvancedTextToVideoGenerator

generator = AdvancedTextToVideoGenerator(
    model_name="damo-vilab/text-to-video-ms-1.7b",
    cache_dir="./model_cache"
)

# Single video with all options
result = generator.generate_video(
    prompt="Your text prompt",
    negative_prompt="What to avoid",
    num_frames=16,
    height=256,
    width=256,
    num_inference_steps=25,
    guidance_scale=9.0,
    fps=8,
    output_path="output.mp4",
    seed=42,
    save_metadata=True
)

# Batch generation
results = generator.batch_generate(
    prompts=["Video 1", "Video 2"],
    output_folder="batch_videos",
    num_frames=16
)

# Compare quality settings
comparison = generator.compare_settings(
    prompt="Your text prompt",
    output_folder="comparison"
)

# Get generation history
history = generator.get_generation_history()
```

### VideoGeneratorInterface (Web)

```bash
python web_interface.py
# Opens web interface in browser at http://127.0.0.1:7860
```

Features:
- Text input for prompts
- Negative prompt support
- Slider controls for all parameters
- Real-time status updates
- Video preview in browser
- Automatic seed randomization option

## Common Prompts

Here are some effective prompts to try:

**Nature & Landscapes**
- "A beautiful sunset over mountains, cinematic lighting"
- "Ocean waves crashing on a beach, sunny day"
- "Forest with green trees and sunlight filtering through"

**Animals**
- "A cat playing with a yarn ball, photorealistic"
- "A dog running through a field, golden hour lighting"
- "Birds flying through clouds, cinematic view"

**Abstract & Art**
- "Colorful gradient animation, smooth transitions"
- "Abstract geometric shapes moving, neon colors"
- "Liquid flowing and morphing, trippy visual effects"

**Technology**
- "Robot dancing in futuristic city with neon lights"
- "Holographic data visualization, blue and purple"
- "Space station orbiting Earth, stars in background"

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](.github/CONTRIBUTING.md) for detailed guidelines on how to contribute.

## Security

For security concerns and responsible disclosure, please see [SECURITY.md](.github/SECURITY.md)

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Citation

If you use this project in your research or work, please cite:

```bibtex
@software{text_to_video_generator_2025,
  title = {Text-to-Video Generator},
  author = {Sreeshanth},
  year = {2025},
  url = {https://github.com/Sreeshanth25503/Text---Video-Generator}
}
```

## Support & Feedback

- **Report Bugs**: Open an issue on [GitHub Issues](https://github.com/Sreeshanth25503/Text---Video-Generator/issues)
- **Ask Questions**: Use [GitHub Discussions](https://github.com/Sreeshanth25503/Text---Video-Generator/discussions)
- **Request Features**: Create a feature request issue

## Acknowledgments

- **DAMO ViLab** for the excellent text-to-video diffusion model
- **Hugging Face** for model hosting and the diffusers library
- **PyTorch Team** for the deep learning framework
- **Gradio Team** for the web interface framework

## Disclaimer

This project is for educational and research purposes. Generated videos should be used responsibly and in compliance with applicable laws and regulations. Users are responsible for ensuring their use of generated content does not violate any rights or policies.

---

**Made with ❤️ for the AI community**

Last Updated: December 2025
