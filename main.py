import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
import os

class TextToVideoGenerator:
    """
    SIMPLE EXPLANATION:
    This is like a video-making machine. You tell it what you want to see,
    and it creates a video for you using AI.
    """
    
    def __init__(self, model_name="damo-vilab/text-to-video-ms-1.7b"):
        """
        WHAT __init__ DOES:
        This sets up the video generator when you first create it.
        It loads the AI model that will make videos.
        
        PARAMETERS:
        - model_name: The name of the AI model we're using (like choosing which artist will paint for you)
        """
        print("[*] Loading the AI model... This may take a few minutes!")
        
        # Check if we have a GPU (graphics card) available - makes things faster!
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[*] Using device: {self.device.upper()}")
        
        # Load the text-to-video pipeline
        # SIMPLE: This loads the AI "brain" that knows how to make videos
        self.pipe = DiffusionPipeline.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            variant="fp16" if self.device == "cuda" else None
        )
        
        # Move the model to GPU if available
        self.pipe = self.pipe.to(self.device)
        
        # Use a faster scheduler for quicker generation
        # SIMPLE: This is like choosing a faster painting technique
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config
        )
        
        # Enable memory optimizations
        # SIMPLE: This makes the AI use less computer memory
        if self.device == "cuda":
            self.pipe.enable_model_cpu_offload()
            self.pipe.enable_vae_slicing()
        
        print("[OK] Model loaded successfully!")
    
    def generate_video(
        self, 
        prompt, 
        num_frames=8,                    # Reduced for faster generation
        num_inference_steps=15,           # Reduced for speed (trade some quality)
        guidance_scale=7.5,
        output_path="output_video.mp4"
    ):
        """
        WHAT THIS FUNCTION DOES:
        This is the main function that creates your video from text!
        
        PARAMETERS EXPLAINED SIMPLY:
        - prompt: Your text description (e.g., "a dog running on beach")
        - num_frames: How many pictures to make (more = longer video, but slower)
        - num_inference_steps: How many times AI refines the video (more = better quality, but slower)
        - guidance_scale: How closely AI follows your text (higher = more accurate to text)
        - output_path: Where to save the video file
        
        RETURNS:
        - The path to your generated video file
        """
        
        print(f"\n[GEN] Generating video from prompt: '{prompt}'")
        print(f"[INFO] Settings: {num_frames} frames, {num_inference_steps} steps")
        
        try:
            # Generate the video frames
            # SIMPLE: This is where the AI actually creates your video!
            with torch.inference_mode():
                video_frames = self.pipe(
                    prompt=prompt,
                    num_frames=num_frames,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale
                ).frames
            
            # The output is a list of frames for each video
            # We take the first (and only) video
            video_frames = video_frames[0]
            
            # Export frames to video file
            # SIMPLE: This saves all the pictures as a video file
            export_to_video(video_frames, output_path, fps=8)
            
            print(f"[OK] Video saved successfully to: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"[ERROR] Error generating video: {e}")
            return None
    
    def generate_multiple_videos(self, prompts, output_folder="generated_videos"):
        """
        WHAT THIS DOES:
        Generates multiple videos from a list of text prompts.
        Useful when you want to create several videos at once!
        
        PARAMETERS:
        - prompts: A list of text descriptions
        - output_folder: Folder where all videos will be saved
        """
        
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        generated_videos = []
        
        for i, prompt in enumerate(prompts):
            output_path = os.path.join(output_folder, f"video_{i+1}.mp4")
            video_path = self.generate_video(prompt, output_path=output_path)
            
            if video_path:
                generated_videos.append(video_path)
        
        print(f"\n[SUCCESS] Generated {len(generated_videos)} videos!")
        return generated_videos


def main():
    """
    MAIN FUNCTION - This is where everything starts!
    This demonstrates how to use the TextToVideoGenerator.
    """
    
    # Create the video generator
    # SIMPLE: Turn on our video-making machine
    generator = TextToVideoGenerator()
    
    # Example 1: Generate a single video
    print("\n" + "="*50)
    print("EXAMPLE 1: Single Video Generation")
    print("="*50)
    
    prompt1 = "A cat playing with a ball of yarn, realistic style"
    generator.generate_video(
        prompt=prompt1,
        num_frames=16,  # Short video (16 frames)
        num_inference_steps=25,  # Good quality
        output_path="cat_video.mp4"
    )
    
    # Example 2: Generate multiple videos
    print("\n" + "="*50)
    print("EXAMPLE 2: Multiple Video Generation")
    print("="*50)
    
    prompts = [
        "A sunset over the ocean, cinematic",
        "A robot dancing in a futuristic city",
        "Flowers blooming in a garden, time-lapse style"
    ]
    
    generator.generate_multiple_videos(prompts)
    
    print("\n" + "="*50)
    print("🎊 ALL DONE! Check your videos!")
    print("="*50)


# This runs the main function when you execute the script
if __name__ == "__main__":
    main()