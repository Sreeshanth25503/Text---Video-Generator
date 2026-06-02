# -*- coding: utf-8 -*-
"""
TEXT-TO-VIDEO GENERATOR - Web Interface
A clean, minimal Gradio app for generating videos from text using
the damo-vilab/text-to-video-ms-1.7b diffusion model.
"""

import gradio as gr
import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
import os
from datetime import datetime
import traceback
import time

# -- Output folder --
OUTPUT_DIR = "generated_videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -- Load model (once, at startup) --
print("\n" + "="*60)
print("  TEXT-TO-VIDEO GENERATOR  ")
print("="*60)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE  = torch.float16 if DEVICE == "cuda" else torch.float32

if DEVICE == "cuda":
    gpu_name = torch.cuda.get_device_name(0)
    gpu_mem  = torch.cuda.get_device_properties(0).total_memory / 1e9
    print(f"  GPU  : {gpu_name}  ({gpu_mem:.1f} GB VRAM)")
    print(f"  CUDA : {torch.version.cuda}")
else:
    print("  WARNING: No GPU detected. Running on CPU (very slow).")

print("  Loading model - please wait ...")

PIPE = DiffusionPipeline.from_pretrained(
    "damo-vilab/text-to-video-ms-1.7b",
    torch_dtype=DTYPE,
    variant="fp16" if DEVICE == "cuda" else None,
    cache_dir="./model_cache",
)
PIPE = PIPE.to(DEVICE)
PIPE.scheduler = DPMSolverMultistepScheduler.from_config(PIPE.scheduler.config)

if DEVICE == "cuda":
    PIPE.enable_model_cpu_offload()
    PIPE.vae.enable_slicing()

print("  Model ready!\n" + "="*60 + "\n")


# -- Generation function --
def generate_video(prompt, negative_prompt, num_frames, num_steps, guidance, seed):
    """Generate a video from the given prompt and return (status, video_path)."""

    if not prompt or not prompt.strip():
        return "[Error] Please enter a prompt.", None

    try:
        num_frames  = int(num_frames)
        num_steps   = int(num_steps)
        guidance    = float(guidance)
        seed_val    = int(seed) if seed and int(seed) > 0 else None

        if seed_val is not None:
            torch.manual_seed(seed_val)

        print(f"\n[GEN] Prompt: '{prompt[:70]}'")
        print(f"      Frames={num_frames}  Steps={num_steps}  Guidance={guidance}  Seed={seed_val}")

        t0 = time.time()

        with torch.inference_mode():
            output = PIPE(
                prompt=prompt,
                negative_prompt=negative_prompt if negative_prompt and negative_prompt.strip() else None,
                num_frames=num_frames,
                num_inference_steps=num_steps,
                guidance_scale=guidance,
                height=256,
                width=256,
            )

        frames = output.frames[0]
        gen_time = time.time() - t0

        timestamp    = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path  = os.path.join(OUTPUT_DIR, f"video_{timestamp}.mp4")
        export_to_video(frames, output_path, fps=8)

        file_mb   = os.path.getsize(output_path) / (1024 * 1024)
        duration  = num_frames / 8.0

        status = (
            "[OK] Video generated successfully!\n\n"
            f"File   : video_{timestamp}.mp4\n"
            f"Time   : {gen_time:.1f}s\n"
            f"Length : {duration:.1f}s  ({num_frames} frames @ 8 fps)\n"
            f"Size   : {file_mb:.2f} MB\n"
            f"Saved  : {os.path.abspath(output_path)}"
        )
        print(f"[OK] Done in {gen_time:.1f}s -> {output_path}")
        return status, os.path.abspath(output_path)

    except Exception as e:
        error_type = type(e).__name__
        oom = "out of memory" in str(e).lower() or "cuda" in str(e).lower()

        if oom:
            msg = (
                "[GPU Memory Error]\n\n"
                "Try:\n"
                "- Reduce Frames to 8\n"
                "- Reduce Steps to 15\n"
                "- Restart the app if needed"
            )
        else:
            msg = f"[Error: {error_type}]\n\n{str(e)[:200]}"

        print(f"[ERROR] {e}")
        print(traceback.format_exc())
        return msg, None


# -- Gradio UI --
def build_ui():
    device_badge = (
        f"GPU: {torch.cuda.get_device_name(0)}" if DEVICE == "cuda"
        else "CPU only (no GPU detected - very slow)"
    )
    status_color = "#22c55e" if DEVICE == "cuda" else "#ef4444"

    _theme = gr.themes.Soft(
        primary_hue="violet",
        secondary_hue="purple",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
    )
    _css = """
    .gradio-container { max-width: 920px !important; margin: auto; }
    #app-header { text-align: center; padding: 1.5rem 0 1rem; }
    #app-header h1 { font-size: 1.9rem; font-weight: 800; margin-bottom: 0.3rem; }
    #app-header p  { color: #888; font-size: 0.93rem; }
    .device-badge {
        display: inline-block;
        padding: 0.25rem 0.8rem;
        border-radius: 99px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(139,92,246,0.1);
        color: #a78bfa;
        border: 1px solid rgba(139,92,246,0.25);
        margin-top: 0.6rem;
    }
    .generate-btn { font-size: 1rem !important; font-weight: 700 !important; }
    """

    with gr.Blocks(title="Text-to-Video Generator") as demo:

        # Header
        gr.HTML(f"""
        <div id="app-header">
          <h1>&#127916; Text-to-Video Generator</h1>
          <p>Type any description &mdash; AI will generate a short video from it</p>
          <span class="device-badge" style="color:{status_color}">
            &#x25CF; {device_badge}
          </span>
        </div>
        """)

        # Main layout
        with gr.Row(equal_height=False):
            # Left: inputs
            with gr.Column(scale=1):
                prompt = gr.Textbox(
                    label="Prompt",
                    placeholder="A golden retriever running on a sunny beach, cinematic",
                    lines=3,
                )
                negative = gr.Textbox(
                    label="Negative Prompt  (optional)",
                    placeholder="blurry, low quality, distorted, dark",
                    lines=2,
                )
                with gr.Row():
                    frames = gr.Slider(8, 24, value=8, step=8,
                                       label="Frames",
                                       info="8=1s | 16=2s | 24=3s")
                    steps  = gr.Slider(10, 35, value=20, step=5,
                                       label="Steps",
                                       info="More = better quality, slower")
                with gr.Row():
                    guidance = gr.Slider(1.0, 10.0, value=7.5, step=0.5,
                                         label="Guidance Scale",
                                         info="How closely to follow prompt")
                    seed = gr.Number(value=-1, label="Seed",
                                      precision=0, info="-1 = random")

                btn = gr.Button(
                    "Generate Video",
                    variant="primary",
                    elem_classes="generate-btn",
                )

            # Right: outputs
            with gr.Column(scale=1):
                status_box = gr.Textbox(
                    label="Status",
                    lines=8,
                    interactive=False,
                    placeholder="Click 'Generate Video' to start ...",
                )
                video_out = gr.Video(label="Generated Video", format="mp4")

        # Examples
        gr.Markdown("### Example Prompts")
        gr.Examples(
            examples=[
                ["A cat playing with a ball of yarn, photorealistic, bright lighting",
                 "blurry, low quality", 8, 20, 7.5, -1],
                ["Sunset over the ocean, golden hour, cinematic wide shot",
                 "blurry, dark, overexposed", 16, 25, 7.5, -1],
                ["A robot dancing in a neon-lit futuristic city",
                 "blurry, distorted", 8, 20, 7.5, -1],
                ["Flowers blooming in a garden, vivid colors, time-lapse",
                 "blurry, low quality, winter", 8, 20, 7.5, 42],
                ["Waves crashing on a rocky coastline, slow motion, dramatic",
                 "blurry, still, calm", 16, 25, 8.0, -1],
            ],
            inputs=[prompt, negative, frames, steps, guidance, seed],
            label=" ",
        )

        # Tips accordion
        with gr.Accordion("Tips and Troubleshooting", open=False):
            gr.Markdown("""
**For best results:**
- Be descriptive: include style, lighting, mood  
  *e.g. "A cat playing, photorealistic, bright lighting, high detail"*
- Use negative prompts to avoid common problems  
  *e.g. "blurry, low quality, distorted, dark"*
- Set a seed number to reproduce the same video

**If you get GPU out-of-memory errors:**
- Set Frames to 8
- Set Steps to 15
- Restart the app

**Expected generation times (RTX 3050 / 4 GB VRAM):**

| Frames | Steps | Estimated Time |
|--------|-------|----------------|
| 8 | 15 | 1-2 minutes |
| 16 | 25 | 3-5 minutes |
| 24 | 25 | 6-9 minutes |
            """)

        # Wire up button
        btn.click(
            fn=generate_video,
            inputs=[prompt, negative, frames, steps, guidance, seed],
            outputs=[status_box, video_out],
            show_progress="full",
        )

    return demo, _theme, _css


# -- Entry point --
if __name__ == "__main__":
    demo, _theme, _css = build_ui()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        share=False,
        theme=_theme,
        css=_css,
    )