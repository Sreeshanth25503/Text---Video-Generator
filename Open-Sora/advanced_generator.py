"""
OPEN-SORA ADVANCED TEXT-TO-VIDEO GENERATOR
This version includes extra features and advanced controls for Open-Sora.

Features:
- Negative prompts
- Custom video settings
- Batch generation
- Quality comparison
- Metadata saving
"""

import torch
from diffusers import DiffusionPipeline
from diffusers.utils import export_to_video
import os
from typing import Optional, List
from tqdm import tqdm
import json
from datetime import datetime
import time

class AdvancedTextToVideoGenerator:
    """
    ADVANCED OPEN-SORA VIDEO GENERATOR
    
    SIMPLE EXPLANATION:
    This is an upgraded version with full control and advanced features.
    You can fine-tune exactly how your video looks!
    """
    
    def __init__(
        self, 
        model_name="hpcai-tech/Open-Sora",
        cache_dir="./model_cache"
    ):
        """
        WHAT THIS DOES:
        Sets up the advanced Open-Sora video generator.
        
        PARAMETERS:
        - model_name: Open-Sora model from Hugging Face
        - cache_dir: Where to save downloaded model
        """
        
        print("[*] Initializing Advanced Open-Sora Text-to-Video Generator...")
        
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
        
        try:
            # Load pipeline
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
            
            # Generation history
            self.generation_history = []
            
            print("[OK] Advanced Open-Sora Generator ready!\n")
            
        except Exception as e:
            print(f"[ERROR] Failed to load Open-Sora model: {e}")
            raise
    
    def generate_video(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        num_frames: int = 16,
        height: int = 1024,
        width: int = 576,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
        output_path: str = "output_video.mp4",
        seed: Optional[int] = None,
        save_metadata: bool = True
    ):
        """
        GENERATE VIDEO WITH ADVANCED OPTIONS
        
        PARAMETERS EXPLAINED:
        
        - prompt: What you want in the video
        
        - negative_prompt: What you DON'T want
          SIMPLE: Tells AI what to avoid
        
        - num_frames: Number of frames
          SIMPLE: 16 frames = ~2 seconds at 8 fps
        
        - height/width: Video resolution
          SIMPLE: 1024x576 is default (high quality)
                   512x256 is lower (faster)
        
        - num_inference_steps: Quality iterations
          SIMPLE: 50 is recommended, higher = better quality but slower
        
        - guidance_scale: How strictly follow prompt
          SIMPLE: 7.5 is balanced
        
        - seed: Random number for reproducibility
          SIMPLE: Use same seed = get same video
        
        - save_metadata: Save generation info
          SIMPLE: Creates text file with all settings
        """
        
        print(f"\n[GEN] Generating video with Open-Sora...")
        print(f"[PROMPT] {prompt}")
        if negative_prompt:
            print(f"[NEGATIVE] {negative_prompt}")
        print(f"[SETTINGS] Frames: {num_frames}, Resolution: {width}x{height}, Steps: {num_inference_steps}")
        
        start_time = time.time()
        
        # Set seed
        if seed is not None:
            torch.manual_seed(seed)
            print(f"[SEED] {seed}")
        
        try:
            # Generate video
            with torch.inference_mode():
                output = self.pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_frames=num_frames,
                    height=height,
                    width=width,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale
                )
            
            video_frames = output.frames[0]
            
            # Export to video
            export_to_video(video_frames, output_path, fps=8)
            
            # Save metadata
            if save_metadata:
                self._save_metadata(
                    output_path, prompt, negative_prompt, num_frames,
                    height, width, num_inference_steps, guidance_scale, seed
                )
            
            # Add to history
            self.generation_history.append({
                "timestamp": datetime.now().isoformat(),
                "prompt": prompt,
                "output_path": output_path,
                "seed": seed
            })
            
            elapsed_time = time.time() - start_time
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            
            print(f"[OK] Video generated in {elapsed_time:.1f} seconds")
            print(f"[OK] File size: {file_size:.2f} MB")
            print(f"[OK] Video saved: {output_path}")
            
            return output_path
            
        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                print("[ERROR] CUDA out of memory!")
                print("[ERROR] Try reducing:")
                print("  - num_frames (reduce by half)")
                print("  - num_inference_steps (try 25-30)")
                print("  - resolution (try 512x256)")
                torch.cuda.empty_cache()
            else:
                print(f"[ERROR] {e}")
            return None
        except Exception as e:
            print(f"[ERROR] {e}")
            return None
    
    def _save_metadata(
        self, video_path, prompt, negative_prompt, num_frames,
        height, width, num_inference_steps, guidance_scale, seed
    ):
        """
        WHAT THIS DOES:
        Saves all settings used to create a video.
        
        SIMPLE: Creates a "recipe" file for recreating the video
        """
        
        metadata = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "settings": {
                "num_frames": num_frames,
                "height": height,
                "width": width,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "seed": seed
            },
            "model": self.model_name,
            "device": self.device,
            "timestamp": datetime.now().isoformat()
        }
        
        metadata_path = video_path.replace(".mp4", "_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"[SAVE] Metadata saved: {metadata_path}")
    
    def batch_generate(
        self,
        prompts: List[str],
        output_folder: str = "batch_output",
        **kwargs
    ):
        """
        WHAT THIS DOES:
        Generates multiple videos at once.
        
        PARAMETERS:
        - prompts: List of text descriptions
        - output_folder: Where to save all videos
        - **kwargs: Any other settings (num_frames, guidance_scale, etc.)
        """
        
        os.makedirs(output_folder, exist_ok=True)
        results = []
        
        print(f"\n[BATCH] Batch generating {len(prompts)} videos...\n")
        
        for i, prompt in enumerate(tqdm(prompts, desc="[BATCH] Generating videos")):
            output_path = os.path.join(output_folder, f"video_{i+1}.mp4")
            
            result = self.generate_video(
                prompt=prompt,
                output_path=output_path,
                **kwargs
            )
            
            if result:
                results.append(result)
        
        print(f"\n[OK] Generated {len(results)}/{len(prompts)} videos successfully!")
        return results
    
    def compare_settings(
        self,
        prompt: str,
        output_folder: str = "comparison"
    ):
        """
        WHAT THIS DOES:
        Generates same video with different settings for comparison.
        
        SIMPLE: Creates 3 versions (fast, balanced, high-quality)
        """
        
        os.makedirs(output_folder, exist_ok=True)
        
        settings = [
            {
                "name": "fast",
                "num_frames": 8,
                "num_inference_steps": 25,
                "guidance_scale": 7.0
            },
            {
                "name": "balanced",
                "num_frames": 16,
                "num_inference_steps": 50,
                "guidance_scale": 7.5
            },
            {
                "name": "high_quality",
                "num_frames": 24,
                "num_inference_steps": 75,
                "guidance_scale": 8.0
            }
        ]
        
        print(f"\n[COMPARE] Generating comparison videos for: '{prompt}'")
        
        results = {}
        for setting in settings:
            name = setting.pop("name")
            output_path = os.path.join(output_folder, f"{name}.mp4")
            
            print(f"\n[SETTINGS] {name.upper()}:")
            result = self.generate_video(
                prompt=prompt,
                output_path=output_path,
                **setting
            )
            results[name] = result
        
        print(f"\n[OK] Comparison complete! Check {output_folder}/ folder")
        return results
    
    def get_generation_history(self):
        """
        WHAT THIS DOES:
        Returns all videos generated in this session.
        """
        return self.generation_history


def main():
    """
    EXAMPLE USAGE OF ADVANCED OPEN-SORA GENERATOR
    """
    
    # Create generator
    generator = AdvancedTextToVideoGenerator()
    
    # Example 1: Basic generation with negative prompt
    print("\n" + "="*60)
    print("EXAMPLE 1: Using Negative Prompts")
    print("="*60)
    
    generator.generate_video(
        prompt="A beautiful sunset over mountains, cinematic, detailed",
        negative_prompt="blurry, low quality, distorted",
        num_frames=16,
        output_path="opensora_sunset.mp4",
        seed=42
    )
    
    # Example 2: Quality comparison
    print("\n" + "="*60)
    print("EXAMPLE 2: Quality Comparison")
    print("="*60)
    
    generator.compare_settings(
        prompt="A cat playing with a toy mouse",
        output_folder="opensora_comparison"
    )
    
    # Example 3: Batch generation
    print("\n" + "="*60)
    print("EXAMPLE 3: Batch Generation")
    print("="*60)
    
    prompts = [
        "A rocket launching into space with stars",
        "Waves crashing on a beach at sunset",
        "A butterfly landing on a flower"
    ]
    
    generator.batch_generate(
        prompts,
        output_folder="opensora_batch",
        num_frames=16
    )


if __name__ == "__main__":
    main()
