"""
OPEN-SORA TEXT-TO-VIDEO GENERATOR
This is a basic generator using Open-Sora model for high-quality video generation.

Open-Sora Features:
- Higher resolution (1024x576)
- Better quality than DAMO
- Longer videos (up to 8 seconds)
- Professional results
"""

import torch
from diffusers import DiffusionPipeline
import os
from typing import Optional
import time

class TextToVideoGenerator:
    """
    OPEN-SORA VIDEO GENERATOR
    
    SIMPLE EXPLANATION:
    This generator uses Open-Sora model which is one of the best free models available.
    It produces higher quality videos than DAMO ViLab.
    """
    
    def __init__(
        self, 
        model_name="hpcai-tech/Open-Sora",
        cache_dir="./model_cache"
    ):
        """
        WHAT THIS DOES:
        Sets up Open-Sora model for video generation.
        
        PARAMETERS:
        - model_name: Open-Sora model from Hugging Face
        - cache_dir: Where to save downloaded model
        """
        
        print("[*] Initializing Open-Sora Text-to-Video Generator...")
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name
        self.cache_dir = cache_dir
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        print(f"[*] Device: {self.device.upper()}")
        print(f"[*] Model: {model_name}")
        print(f"[*] Cache: {cache_dir}")
        
        # Check GPU memory
        if self.device == "cuda":
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"[*] GPU Memory: {gpu_memory:.2f} GB")
            if gpu_memory < 20:
                print("[WARN] Warning: Open-Sora works best with 24GB+ VRAM")
                print("[WARN] You may experience out-of-memory errors")
        
        try:
            # Load Open-Sora pipeline
            print("[*] Loading Open-Sora model (this may take a few minutes)...")
            self.pipe = DiffusionPipeline.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                cache_dir=cache_dir
            )
            
            self.pipe = self.pipe.to(self.device)
            
            # Memory optimizations
            if self.device == "cuda":
                self.pipe.enable_model_cpu_offload()
                self.pipe.enable_vae_slicing()
                torch.cuda.empty_cache()
            
            print("[OK] Open-Sora model loaded successfully!\n")
            
        except Exception as e:
            print(f"[ERROR] Failed to load Open-Sora model: {e}")
            print("[ERROR] Make sure you have 24GB+ VRAM or use cloud GPU")
            raise
    
    def generate_video(
        self,
        prompt: str,
        num_frames: int = 16,
        height: int = 1024,
        width: int = 576,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
        output_path: str = "output_video.mp4",
        seed: Optional[int] = None
    ):
        """
        GENERATE VIDEO WITH OPEN-SORA
        
        PARAMETERS EXPLAINED:
        
        - prompt: What you want in the video (e.g., "a dog playing")
        
        - num_frames: Number of frames in video
          SIMPLE: 16 frames = ~2 seconds at 8 fps
        
        - height/width: Video dimensions
          SIMPLE: 1024x576 is Open-Sora default (high quality)
        
        - num_inference_steps: Quality iterations
          SIMPLE: 50 is recommended for Open-Sora (higher = better quality)
        
        - guidance_scale: How strictly AI follows prompt
          SIMPLE: 7.5 is balanced
        
        - seed: For reproducibility
          SIMPLE: Use same seed = get same video
        """
        
        print(f"\n[GEN] Generating video with Open-Sora...")
        print(f"[PROMPT] {prompt}")
        print(f"[SETTINGS] Frames: {num_frames}, Resolution: {width}x{height}, Steps: {num_inference_steps}")
        
        start_time = time.time()
        
        # Set seed for reproducibility
        if seed is not None:
            torch.manual_seed(seed)
            print(f"[SEED] {seed}")
        
        try:
            # Generate video
            with torch.inference_mode():
                output = self.pipe(
                    prompt=prompt,
                    num_frames=num_frames,
                    height=height,
                    width=width,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale
                )
            
            video_frames = output.frames[0]
            
            # Export to video
            from diffusers.utils import export_to_video
            export_to_video(video_frames, output_path, fps=8)
            
            elapsed_time = time.time() - start_time
            print(f"[OK] Video generated successfully in {elapsed_time:.1f} seconds")
            print(f"[OK] Video saved: {output_path}")
            
            # Get file size
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            print(f"[INFO] File size: {file_size:.2f} MB")
            
            return output_path
            
        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                print("[ERROR] CUDA out of memory!")
                print("[ERROR] Open-Sora needs 24GB+ VRAM")
                print("[ERROR] Solutions:")
                print("  1. Reduce num_frames (try 8 instead of 16)")
                print("  2. Reduce resolution (try 512x256)")
                print("  3. Use cloud GPU (Google Colab, RunPod)")
                torch.cuda.empty_cache()
            else:
                print(f"[ERROR] {e}")
            return None
        except Exception as e:
            print(f"[ERROR] {e}")
            return None


def main():
    """
    EXAMPLE USAGE OF OPEN-SORA GENERATOR
    """
    
    # Create generator
    generator = TextToVideoGenerator()
    
    # Example 1: Simple video generation
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple Video Generation")
    print("="*60)
    
    generator.generate_video(
        prompt="A beautiful sunset over the ocean with calm waves",
        num_frames=16,
        output_path="test_opensora_basic.mp4",
        seed=42
    )
    
    # Example 2: Higher quality (more steps)
    print("\n" + "="*60)
    print("EXAMPLE 2: High Quality Generation")
    print("="*60)
    
    generator.generate_video(
        prompt="A cat playing with a ball of yarn on a wooden floor",
        num_frames=16,
        num_inference_steps=50,
        output_path="test_opensora_quality.mp4",
        seed=42
    )
    
    print("\n" + "="*60)
    print("GENERATION COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    main()
