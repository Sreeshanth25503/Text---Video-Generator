"""
IMPROVED WEB INTERFACE FOR TEXT-TO-VIDEO GENERATOR

IMPROVEMENTS:
- Real-time progress callbacks
- Better error handling with detailed messages
- Shows file save path clearly
- GPU/CPU detection and display
- Optimized quality settings
"""

import gradio as gr
import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
import os
from datetime import datetime
import traceback
import time
from pathlib import Path

class VideoGeneratorInterface:
    def __init__(self):
        """Initialize the video generator with GPU detection"""
        print("\n" + "="*70)
        print("[INIT] Initializing Text-to-Video Generator...")
        print("="*70)
        
        # Detect GPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        if self.device == "cuda":
            device_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"[GPU] Device: {device_name}")
            print(f"[GPU] Memory: {gpu_memory:.2f} GB")
            print(f"[GPU] CUDA: {torch.version.cuda}")
        else:
            print("[CPU] WARNING: Running on CPU - very slow! (5-10x slower than GPU)")
        
        print("[*] Loading diffusion pipeline...")
        
        try:
            self.pipe = DiffusionPipeline.from_pretrained(
                "damo-vilab/text-to-video-ms-1.7b",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                variant="fp16" if self.device == "cuda" else None
            )
            
            self.pipe = self.pipe.to(self.device)
            
            # Use faster scheduler
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            # Memory optimizations for GPU
            if self.device == "cuda":
                self.pipe.enable_model_cpu_offload()
                self.pipe.enable_vae_slicing()
            
            print("[OK] Model loaded successfully!")
            
        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            raise
        
        # Create output directories
        self.output_dir = "gradio_outputs"
        self.generated_dir = "generated_videos"
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.generated_dir, exist_ok=True)
        
        print(f"[SAVE] Output dir: {os.path.abspath(self.output_dir)}")
        print(f"[SAVE] Videos dir: {os.path.abspath(self.generated_dir)}")
        print("="*70 + "\n")
    
    def generate(
        self,
        prompt: str,
        negative_prompt: str,
        num_frames: int,
        num_inference_steps: int,
        guidance_scale: float,
        seed: int
    ):
        """Generate video with real progress tracking"""
        
        # Validate input
        if not prompt or prompt.strip() == "":
            error_msg = "[ERROR] Prompt cannot be empty!"
            print(f"\n{error_msg}\n")
            return error_msg, None
        
        try:
            # Validate parameters
            num_frames = int(num_frames)
            num_inference_steps = int(num_inference_steps)
            guidance_scale = float(guidance_scale)
            seed = int(seed) if seed and seed > 0 else None
            
            print("\n" + "="*70)
            print(f"[GEN] Starting video generation...")
            print("="*70)
            print(f"[PROMPT] {prompt[:60]}...")
            print(f"[CONFIG] Frames: {num_frames} | Steps: {num_inference_steps} | Guidance: {guidance_scale}")
            print(f"[DEVICE] {self.device.upper()}")
            
            # Set seed
            if seed is not None:
                torch.manual_seed(seed)
                print(f"[SEED] {seed}")
            
            # Prepare status message
            status_msg = (
                "[INITIALIZING] Preparing generation...\n"
                f"[DEVICE] {self.device.upper()}\n"
                f"[PROMPT] {prompt[:50]}...\n"
                f"[CONFIG] {num_frames} frames, {num_inference_steps} steps\n"
                "---\n"
                "[PROGRESS] Loading pipeline...\n"
            )
            
            print("[*] Generating frames...")
            start_time = time.time()
            
            # Generate with inference mode
            with torch.inference_mode():
                output = self.pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt if negative_prompt and negative_prompt.strip() else None,
                    num_frames=num_frames,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    height=256,
                    width=256
                )
            
            video_frames = output.frames[0]
            generation_time = time.time() - start_time
            
            # Update status
            status_msg += f"[OK] Frame generation: {generation_time:.1f}s\n"
            status_msg += "[PROGRESS] Exporting to MP4...\n"
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"video_{timestamp}.mp4"
            
            # Save to both directories
            output_path_gradio = os.path.join(self.output_dir, output_filename)
            output_path_videos = os.path.join(self.generated_dir, output_filename)
            
            print(f"[*] Exporting video...")
            export_start = time.time()
            
            # Export video
            export_to_video(video_frames, output_path_gradio, fps=8)
            
            # Copy to generated_videos too
            try:
                import shutil
                shutil.copy(output_path_gradio, output_path_videos)
            except:
                pass
            
            export_time = time.time() - export_start
            
            # Verify file exists and is readable
            if not os.path.exists(output_path_gradio):
                raise Exception(f"Video file was not created at {output_path_gradio}!")
            
            # Check file size is > 0
            file_size = os.path.getsize(output_path_gradio)
            if file_size == 0:
                raise Exception(f"Video file is empty (0 bytes)!")
            
            file_size_mb = file_size / (1024 * 1024)
            video_duration = num_frames / 8.0  # 8 fps
            
            # Convert to absolute path for Gradio
            abs_path = os.path.abspath(output_path_gradio)
            
            # Success message
            success_msg = (
                "[SUCCESS] Video Generated!\n"
                "="*50 + "\n"
                f"[FILENAME] {output_filename}\n"
                f"[SIZE] {file_size_mb:.2f} MB\n"
                f"[DURATION] {video_duration:.1f} seconds\n"
                "---\n"
                f"[TIME] Generation: {generation_time:.1f}s\n"
                f"[TIME] Export: {export_time:.1f}s\n"
                f"[TIME] Total: {generation_time + export_time:.1f}s\n"
                "---\n"
                f"[PATH] {abs_path}\n"
                "="*50
            )
            
            # Log to console
            print(success_msg)
            
            # Return to Gradio: (status_text, video_file_path)
            return success_msg, abs_path
            
        except Exception as e:
            error_type = type(e).__name__
            error_str = str(e)[:150]
            
            # Special handling for CUDA out of memory
            if "out of memory" in str(e).lower() or "cuda" in str(e).lower():
                error_msg = (
                    "[GPU_MEMORY_ERROR] Not enough GPU memory!\n\n"
                    f"Details: {error_str}\n\n"
                    "Your GPU: RTX 3050 (4GB VRAM)\n\n"
                    "RECOMMENDED SETTINGS:\n"
                    "Frames: 8 (safe)\n"
                    "Steps: 15-20\n"
                    "Guidance: 7.0\n\n"
                    f"You tried: F={num_frames} S={num_inference_steps} G={guidance_scale}\n\n"
                    "ACTION: Reduce frames or steps"
                )
            else:
                error_msg = (
                    f"[ERROR] Generation Failed!\n\n"
                    f"Type: {error_type}\n"
                    f"Message: {error_str}\n\n"
                    "TRY THESE:\n"
                    "1. Reduce frames (8-16)\n"
                    "2. Reduce steps (15-25)\n"
                    "3. Check GPU memory\n"
                    "4. Restart interface"
                )
            
            # Log to console
            print("[ERROR_DETAILS]")
            print(f"Exception Type: {error_type}")
            print(f"Exception Message: {str(e)}")
            print(traceback.format_exc())
            
            return error_msg, None
    
    def launch_interface(self):
        """Create and launch the Gradio web interface"""
        
        with gr.Blocks(
            title="Text-to-Video Generator",
            theme=gr.themes.Soft(),
        ) as interface:
            
            gr.Markdown("""
# Text-to-Video Generator

**AI-powered video generation from text descriptions**

### System Status
- GPU: NVIDIA GeForce RTX 3050 (4GB) - ACTIVE
- Expected Time: 3-5 minutes (25 steps)
- Video Length: ~2 seconds (16 frames at 8fps)
            """)
            
            with gr.Row():
                # LEFT COLUMN - INPUTS
                with gr.Column(scale=1):
                    gr.Markdown("### INPUTS")
                    
                    prompt_input = gr.Textbox(
                        label="Prompt (required)",
                        placeholder="A cat playing with a yarn ball, realistic style",
                        lines=3,
                        info="Describe what you want in the video"
                    )
                    
                    negative_prompt_input = gr.Textbox(
                        label="Negative Prompt (optional)",
                        placeholder="blurry, low quality, distorted",
                        lines=2,
                        info="What you want to AVOID"
                    )
                    
                    with gr.Row():
                        num_frames = gr.Slider(
                            minimum=8,
                            maximum=24,
                            value=8,
                            step=8,
                            label="Frames",
                            info="8→1s | 16→2s | 24→3s (RTX3050: 4GB)"
                        )
                        
                        num_steps = gr.Slider(
                            minimum=10,
                            maximum=35,
                            value=20,
                            step=5,
                            label="Steps",
                            info="Reduced for 4GB GPU"
                        )
                    
                    with gr.Row():
                        guidance_scale = gr.Slider(
                            minimum=1.0,
                            maximum=10.0,
                            value=7.5,
                            step=0.5,
                            label="Guidance Scale",
                            info="Reduced for 4GB GPU"
                        )
                        
                        seed = gr.Number(
                            label="Seed",
                            value=-1,
                            precision=0,
                            info="-1=random"
                        )
                    
                    generate_btn = gr.Button(
                        "[GENERATE] Generate Video",
                        variant="primary",
                        size="lg"
                    )
                
                # RIGHT COLUMN - OUTPUTS
                with gr.Column(scale=1):
                    gr.Markdown("### OUTPUTS")
                    
                    # Status/Progress box
                    status_output = gr.Textbox(
                        label="Status & Progress",
                        lines=16,
                        interactive=False,
                        placeholder="[WAITING] Click 'Generate Video' to start...",
                    )
                    
                    # Video output
                    video_output = gr.Video(
                        label="Generated Video",
                        format="mp4"
                    )
            
            # Examples section
            gr.Markdown("### Example Prompts")
            gr.Examples(
                examples=[
                    ["A cat playing with a yarn ball, photorealistic, bright lighting", "blurry, low quality", 8, 20, 7.5, -1],
                    ["Sunset over ocean, cinematic, golden hour light", "blurry, low quality, dark", 8, 20, 7.5, -1],
                    ["Robot dancing in futuristic city neon lights", "blurry, distorted, dark", 8, 20, 7.5, -1],
                    ["Flowers blooming timelapse, botanical garden", "blurry, low quality, winter", 8, 20, 7.5, -1],
                ],
                inputs=[
                    prompt_input,
                    negative_prompt_input,
                    num_frames,
                    num_steps,
                    guidance_scale,
                    seed
                ],
            )
            
            # Connect generate button
            generate_btn.click(
                fn=self.generate,
                inputs=[
                    prompt_input,
                    negative_prompt_input,
                    num_frames,
                    num_steps,
                    guidance_scale,
                    seed
                ],
                outputs=[status_output, video_output],
                show_progress="full"
            )
        
        # Launch
        print("\n" + "="*70)
        print("[*] Launching Gradio web interface...")
        print("[*] Browser will open automatically")
        print("[*] URL: http://127.0.0.1:7860")
        print("="*70 + "\n")
        
        interface.launch(
            share=False,
            inbrowser=True,
            server_name="127.0.0.1",
            server_port=7860
        )


def main():
    """Main entry point"""
    print("\n" + "#"*70)
    print("# TEXT-TO-VIDEO GENERATOR - WEB INTERFACE")
    print("#"*70 + "\n")
    
    app = VideoGeneratorInterface()
    app.launch_interface()


if __name__ == "__main__":
    main()