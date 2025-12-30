# Open-Sora Text-to-Video Generator

High-quality video generation using the Open-Sora model.

## About Open-Sora

Open-Sora is one of the best free, open-source text-to-video models available:

- **Quality**: Excellent (much better than DAMO ViLab)
- **Resolution**: 1024x576 (high resolution)
- **Video Length**: Up to 8 seconds
- **GPU Memory**: 24GB+ recommended
- **Speed**: 5-10 minutes per video
- **License**: Open source (free to use)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Tests

```bash
python run_all.py
```

### 3. Generate Videos

**Basic Version:**

```bash
python main.py
```

**Advanced Version:**

```bash
python advanced_generator.py
```

**Web Interface:**

```bash
python web_interface.py
```

## Usage Examples

### Basic Generation

```python
from main import TextToVideoGenerator

generator = TextToVideoGenerator()
generator.generate_video(
    prompt="A beautiful sunset over mountains",
    num_frames=16,
    output_path="sunset.mp4"
)
```

### Advanced Generation with Negative Prompt

```python
from advanced_generator import AdvancedTextToVideoGenerator

generator = AdvancedTextToVideoGenerator()
generator.generate_video(
    prompt="A cat playing with a ball, detailed, clear",
    negative_prompt="blurry, low quality, distorted",
    num_frames=16,
    num_inference_steps=50,
    guidance_scale=7.5,
    seed=42,
    output_path="cat_video.mp4"
)
```

### Batch Generation

```python
generator = AdvancedTextToVideoGenerator()

prompts = [
    "A rocket launching into space",
    "Ocean waves at sunset",
    "Butterfly on a flower"
]

videos = generator.batch_generate(
    prompts,
    output_folder="batch_videos",
    num_frames=16
)
```

### Quality Comparison

```python
generator = AdvancedTextToVideoGenerator()

results = generator.compare_settings(
    prompt="A beautiful sunset",
    output_folder="comparison"
)
```

## Parameters

| Parameter           | Description        | Default  | Recommended           |
| ------------------- | ------------------ | -------- | --------------------- |
| prompt              | Video description  | Required | 1-2 sentences         |
| negative_prompt     | What to avoid      | None     | "blurry, low quality" |
| num_frames          | Video length       | 16       | 8-24                  |
| height              | Video height       | 1024     | 512-1024              |
| width               | Video width        | 576      | 256-576               |
| num_inference_steps | Quality iterations | 50       | 25-75                 |
| guidance_scale      | Prompt adherence   | 7.5      | 7.0-8.0               |
| seed                | Reproducibility    | None     | Any integer           |

## System Requirements

- **GPU Memory**: 24GB+ (RTX 4090, A100, etc.)
- **RAM**: 16GB minimum
- **Storage**: 30GB for model + videos
- **Python**: 3.8+
- **CUDA**: 11.8+ (for GPU)

## Performance

| Setting                            | Time      | GPU Memory | Quality     |
| ---------------------------------- | --------- | ---------- | ----------- |
| Fast (8 frames, 25 steps)          | 3-4 min   | 20GB       | Good        |
| Balanced (16 frames, 50 steps)     | 5-7 min   | 24GB       | Excellent   |
| High Quality (24 frames, 75 steps) | 10-15 min | 24GB+      | Outstanding |

## Troubleshooting

### CUDA Out of Memory

**Solution:**

```python
generator.generate_video(
    prompt="...",
    num_frames=8,           # Reduce frames
    num_inference_steps=25, # Reduce steps
    height=512,             # Reduce resolution
    width=256
)
```

### Model Download Issues

- First run downloads ~15GB
- Requires stable internet
- Model is cached for future use

### On 4GB GPU (RTX 3050)?

Open-Sora won't work locally. Use:

- **Google Colab** (Free 15GB GPU)
- **RunPod** ($0.44/hour)
- **AWS** ($0.50+/hour)

## Cloud GPU Options

### Google Colab (Free)

```python
# Upload this folder to Colab
# Run: !python main.py
```

### RunPod ($0.44/hour)

1. Go to runpod.io
2. Rent 24GB GPU
3. Upload this folder
4. Run python main.py

### AWS/Google Cloud

1. Launch GPU instance
2. Upload code
3. Run generation

## File Structure

```
Open-Sora/
├── main.py                    # Basic generator
├── advanced_generator.py      # Advanced features
├── web_interface.py           # Gradio web UI
├── run_all.py                # Test suite
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Model Information

- **Model Name**: hpcai-tech/Open-Sora
- **Source**: Hugging Face Model Hub
- **Size**: ~15GB
- **License**: Open source
- **Resolution**: 1024x576 (best free quality)
- **Repository**: https://github.com/hpcaitech/Open-Sora

## Common Prompts

**Nature**

- "A beautiful sunset over mountains with calm clouds"
- "Ocean waves crashing on a beach at golden hour"
- "Forest with sunlight filtering through trees"

**Animals**

- "A cat playing with a toy, detailed and clear"
- "A dog running through a field, cinematic"
- "Birds flying through clouds, slow motion"

**Technology**

- "A rocket launching into space with stars"
- "Holographic data visualization in blue"
- "Robot dancing in futuristic city"

## Performance Tips

1. **Start with fewer frames** (8 instead of 16)
2. **Use descriptive prompts** (include style, lighting, mood)
3. **Add negative prompts** (helps quality significantly)
4. **Increase steps for quality** (but takes longer)
5. **Save prompts that work** (for reuse)

## Limitations

- Generates short videos (up to 8 seconds)
- Requires 24GB+ VRAM
- Slow generation (5-10 minutes)
- Can't generate specific people
- Quality depends on prompt clarity

## License

This implementation is provided as-is for educational purposes.
Open-Sora model is under its own license from HPCAI-Tech.

## Support

For issues:

1. Check console output for error messages
2. Review troubleshooting section
3. Check Open-Sora GitHub: https://github.com/hpcaitech/Open-Sora
4. Check Hugging Face: https://huggingface.co/hpcai-tech/Open-Sora

---

**Generated with Open-Sora** 🚀

Last Updated: December 2025
