# Text-to-Video Generator

An AI-powered application that converts text descriptions into short videos using diffusion models.

## Quick Start

### Installation
```bash
git clone https://github.com/Sreeshanth25503/Text---Video-Generator.git
cd Text---Video-Generator
pip install -r requirements.txt
```

### Usage

**Web Interface (Easiest)**
```bash
python web_interface.py
```

**Basic Version**
```bash
python main.py
```

**Advanced Version**
```bash
python advanced_generator.py
```

**Run All Tests**
```bash
python run_all.py
```

## Features

- Text-to-Video Generation using DAMO ViLab model
- Three usage modes: Basic, Advanced, Web Interface
- Advanced controls: negative prompts, custom resolution, seed control
- GPU Support (CUDA) and CPU fallback
- Metadata saving and batch processing

## System Requirements

- Python 3.8+
- 8GB RAM minimum (16GB recommended)
- NVIDIA GPU with CUDA 11.8+ (optional but recommended)
- 7GB storage for model cache

## Performance

| Setting | Time | Quality |
|---------|------|---------|
| Fast (8 frames, 15 steps) | 30-45s | Good |
| Balanced (16 frames, 25 steps) | 1.5-2min | Excellent |
| High Quality (24 frames, 50 steps) | 5-7min | Very High |

## Example Usage

### Basic Generation
```python
from main import TextToVideoGenerator

generator = TextToVideoGenerator()
generator.generate_video(
    prompt="A cat playing with a yarn ball",
    num_frames=16,
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
generator = AdvancedTextToVideoGenerator()
prompts = ["A cat", "A sunset", "A robot dancing"]
videos = generator.batch_generate(prompts, output_folder="batch_videos")
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| prompt | Text description | Required |
| negative_prompt | What to avoid | None |
| num_frames | Video length | 8 |
| num_inference_steps | Quality iterations | 20 |
| guidance_scale | Prompt adherence | 7.5 |
| seed | Reproducibility | Random |

## Troubleshooting

**CUDA Out of Memory**
- Reduce num_frames (try 8)
- Reduce num_inference_steps (try 15)
- Use smaller resolution (256x256)

**Slow Generation**
- Use GPU instead of CPU
- Reduce quality settings

**Model Download Fails**
- First run downloads 7GB (requires stable internet)
- Model is cached for future use

**ImportError**
```bash
pip install -r requirements.txt
pip install --upgrade pip
```

## File Structure

```
Text---Video-Generator/
 main.py                 # Basic generator
 advanced_generator.py   # Advanced features
 web_interface.py        # Gradio web UI
 run_all.py             # Test suite
 requirements.txt        # Dependencies
 README.md              # This file
 LICENSE                # MIT License
 .github/               # GitHub templates
```

## Model Info

- **Model**: DAMO ViLab Text-to-Video MS 1.7B
- **Source**: Hugging Face Model Hub
- **Size**: ~7GB
- **Resolution**: 256x256 pixels
- **Length**: Up to 32 frames (~4 seconds)

## Common Prompts

**Nature**
- "A beautiful sunset over mountains, cinematic"
- "Ocean waves crashing on beach"
- "Forest with sunlight"

**Animals**
- "Cat playing with yarn, photorealistic"
- "Dog running in field"
- "Birds flying through clouds"

**Technology**
- "Robot dancing in futuristic city"
- "Holographic data visualization"
- "Space station orbiting Earth"

## Contributing

Contributions welcome! See [CONTRIBUTING.md](.github/CONTRIBUTING.md)

## Security

See [SECURITY.md](.github/SECURITY.md) for security concerns

## License

MIT License - See [LICENSE](LICENSE)

## Citation

```bibtex
@software{text_to_video_generator_2025,
  title = {Text-to-Video Generator},
  author = {Sreeshanth},
  year = {2025},
  url = {https://github.com/Sreeshanth25503/Text---Video-Generator}
}
```

## Support

- Report Bugs: [GitHub Issues](https://github.com/Sreeshanth25503/Text---Video-Generator/issues)
- Questions: [GitHub Discussions](https://github.com/Sreeshanth25503/Text---Video-Generator/discussions)

## Acknowledgments

- DAMO ViLab for text-to-video model
- Hugging Face for model hosting
- PyTorch and diffusers teams

---

**Made with  for the AI community**

Last Updated: December 2025
