"""
ADVANCED TEXT-TO-VIDEO GENERATOR
This version includes extra features like:
- Negative prompts (tell AI what NOT to include)
- Custom video settings (resolution, length, quality)
- Progress tracking
- Video preview generation
"""

import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
import os
from typing import Optional, List
from tqdm import tqdm
import json
from datetime import datetime

class AdvancedTextToVideoGenerator:
    """
    ADVANCED VIDEO GENERATOR
    
    SIMPLE EXPLANATION:
    This is an upgraded version with more control and features.
    You can fine-tune exactly how your video looks!
    """
    
    def __init__(
        self, 
        model_name="damo-vilab/text-to-video-ms-1.7b",
        cache_dir="./model_cache"
    ):
        """
        WHAT THIS DOES:
        Sets up the advanced video generator with options for customization.
        
        PARAMETERS:
        - model_name: Which AI model to use
        - cache_dir: Where to save downloaded models (so you don't download twice)
        """
        
        print("[*] Initializing Advanced Text-to-Video Generator...")
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name
        self.cache_dir = cache_dir
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        print(f"[*] Device: {self.device.upper()}")
        print(f"[*] Model: {model_name}")
        print(f"[*] Cache: {cache_dir}")
        
        # Load pipeline
        self.pipe = DiffusionPipeline.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            variant="fp16" if self.device == "cuda" else None,
            cache_dir=cache_dir
        )
        
        self.pipe = self.pipe.to(self.device)
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config
        )
        
        # Memory optimizations
        if self.device == "cuda":
            self.pipe.enable_model_cpu_offload()
            self.pipe.enable_vae_slicing()
        
        # Generation history
        self.generation_history = []
        
        print("[OK] Generator ready!\n")
    
    def generate_video(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        num_frames: int = 16,
        height: int = 256,
        width: int = 256,
        num_inference_steps: int = 25,
        guidance_scale: float = 9.0,
        fps: int = 8,
        output_path: str = "output_video.mp4",
        seed: Optional[int] = None,
        save_metadata: bool = True
    ):
        """
        GENERATE VIDEO WITH ADVANCED OPTIONS
        
        PARAMETERS EXPLAINED:
        
        - prompt: What you want in the video (e.g., "a dog playing")
        
        - negative_prompt: What you DON'T want (e.g., "blurry, low quality")
          SIMPLE: This tells the AI what to avoid
        
        - num_frames: Number of frames (pictures) in video
          SIMPLE: 16 frames = ~2 seconds at 8 fps
        
        - height/width: Video dimensions in pixels
          SIMPLE: 256x256 is small and fast, 512x512 is bigger but slower
        
        - num_inference_steps: Quality iterations
          SIMPLE: Higher = better quality but slower (25 is good balance)
        
        - guidance_scale: How strictly AI follows your prompt
          SIMPLE: 7-9 is balanced, higher = more literal
        
        - fps: Frames per second
          SIMPLE: 8 fps = standard, 24 fps = smooth (like movies)
        
        - seed: Random number for reproducibility
          SIMPLE: Use same seed = get same video again
        
        - save_metadata: Save generation info with video
          SIMPLE: Saves a text file with all the settings you used
        """
        
        print(f"\n[GEN] Generating video...")
        print(f"[PROMPT] {prompt}")
        if negative_prompt:
            print(f"[NEGATIVE] {negative_prompt}")
        
        # Set random seed for reproducibility
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
            
            # Export to video file
            export_to_video(video_frames, output_path, fps=fps)
            
            # Save metadata
            if save_metadata:
                self._save_metadata(
                    output_path, prompt, negative_prompt, num_frames,
                    height, width, num_inference_steps, guidance_scale,
                    fps, seed
                )
            
            # Add to history
            self.generation_history.append({
                "timestamp": datetime.now().isoformat(),
                "prompt": prompt,
                "output_path": output_path,
                "seed": seed
            })
            
            print(f"[OK] Video saved: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"[ERROR] {e}")
            return None
    
    def _save_metadata(
        self, video_path, prompt, negative_prompt, num_frames,
        height, width, num_inference_steps, guidance_scale, fps, seed
    ):
        """
        WHAT THIS DOES:
        Saves all the settings used to create a video in a text file.
        
        SIMPLE: Creates a "recipe" file so you can recreate the video later
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
                "fps": fps,
                "seed": seed
            },
            "model": self.model_name,
            "device": self.device,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save as JSON file next to video
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
        Generates multiple videos at once with a progress bar!
        
        PARAMETERS:
        - prompts: List of text descriptions
        - output_folder: Where to save all videos
        - **kwargs: Any other settings (num_frames, guidance_scale, etc.)
        """
        
        os.makedirs(output_folder, exist_ok=True)
        results = []
        
        print(f"\n[BATCH] Batch generating {len(prompts)} videos...\n")
        
        # Use tqdm for progress bar
        for i, prompt in enumerate(tqdm(prompts, desc="Generating videos")):
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
    
    def get_generation_history(self):
        """
        WHAT THIS DOES:
        Returns a list of all videos you've generated in this session.
        
        SIMPLE: Shows you everything you've created so far
        """
        return self.generation_history
    
    def compare_settings(
        self,
        prompt: str,
        output_folder: str = "comparison"
    ):
        """
        WHAT THIS DOES:
        Generates the same video with different settings so you can compare!
        
        SIMPLE: Creates 3 versions (fast, balanced, high-quality) so you see the difference
        """
        
        os.makedirs(output_folder, exist_ok=True)
        
        settings = [
            {
                "name": "fast",
                "num_frames": 8,
                "num_inference_steps": 15,
                "guidance_scale": 7.0
            },
            {
                "name": "balanced",
                "num_frames": 16,
                "num_inference_steps": 25,
                "guidance_scale": 9.0
            },
            {
                "name": "high_quality",
                "num_frames": 24,
                "num_inference_steps": 50,
                "guidance_scale": 12.0
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


def main():
    """
    EXAMPLE USAGE OF ADVANCED GENERATOR
    """
    
    # Create generator
    generator = AdvancedTextToVideoGenerator()
    
    # Example 1: Basic generation with negative prompt
    print("\n" + "="*60)
    print("EXAMPLE 1: Using Negative Prompts")
    print("="*60)
    
    generator.generate_video(
        prompt="A beautiful sunset over mountains, cinematic",
        negative_prompt="blurry, low quality, distorted",
        num_frames=16,
        output_path="sunset_video.mp4",
        seed=42  # Using seed for reproducibility
    )
    
    # Example 2: Compare different quality settings
    print("\n" + "="*60)
    print("EXAMPLE 2: Quality Comparison")
    print("="*60)
    
    generator.compare_settings(
        prompt="A cat playing with a toy mouse",
        output_folder="quality_comparison"
    )
    
    # Example 3: Batch generation
    print("\n" + "="*60)
    print("EXAMPLE 3: Batch Generation")
    print("="*60)
    
    prompts = [
        "A rocket launching into space",
        "Waves crashing on a beach",
        "A butterfly landing on a flower"
    ]
    
    generator.batch_generate(
        prompts,
        output_folder="batch_videos",
        num_frames=16,
        guidance_scale=9.0
    )
    
    # Show generation history
    print("\n" + "="*60)
    print("GENERATION HISTORY")
    print("="*60)
    history = generator.get_generation_history()
    for i, entry in enumerate(history, 1):
        print(f"{i}. {entry['prompt']}")
        print(f"   File: {entry['output_path']}")
        print()


if __name__ == "__main__":
    main()