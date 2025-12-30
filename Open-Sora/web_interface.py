"""
OPEN-SORA WEB INTERFACE
Gradio-based web UI for easy video generation without coding.
"""

import gradio as gr
from advanced_generator import AdvancedTextToVideoGenerator
import os
import torch

# Initialize generator
generator = None

def load_generator():
    """Load the Open-Sora generator"""
    global generator
    if generator is None:
        generator = AdvancedTextToVideoGenerator()
    return generator

def generate_video_interface(prompt, negative_prompt, num_frames, steps, guidance):
    """
    WHAT THIS DOES:
    Generates video based on Gradio interface inputs.
    """
    
    try:
        gen = load_generator()
        
        output_path = os.path.join("gradio_outputs", f"video_{int(torch.cuda.Event().record())}.mp4")
        os.makedirs("gradio_outputs", exist_ok=True)
        
        # Convert slider values
        num_frames = int(num_frames)
        steps = int(steps)
        guidance = float(guidance)
        
        # Generate video
        result = gen.generate_video(
            prompt=prompt,
            negative_prompt=negative_prompt if negative_prompt else None,
            num_frames=num_frames,
            num_inference_steps=steps,
            guidance_scale=guidance,
            output_path=output_path
        )
        
        if result:
            return result, f"[SUCCESS] Video generated successfully!\nFile: {output_path}"
        else:
            return None, "[ERROR] Video generation failed. Check console for details."
    
    except Exception as e:
        return None, f"[ERROR] {str(e)}"

def launch_interface():
    """
    WHAT THIS DOES:
    Launches the Gradio web interface for Open-Sora.
    """
    
    print("[*] Initializing Open-Sora Web Interface...")
    
    with gr.Blocks(title="Open-Sora Video Generator", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# Open-Sora Text-to-Video Generator")
        gr.Markdown("Generate high-quality videos from text descriptions using Open-Sora model")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Input")
                
                prompt = gr.Textbox(
                    label="Prompt",
                    placeholder="Describe the video you want to generate...",
                    lines=3,
                    value="A beautiful sunset over mountains with calm clouds"
                )
                
                negative_prompt = gr.Textbox(
                    label="Negative Prompt (Optional)",
                    placeholder="What to avoid in the video...",
                    lines=2,
                    value="blurry, low quality, distorted"
                )
                
                gr.Markdown("### Settings")
                
                num_frames = gr.Slider(
                    label="Video Frames",
                    minimum=8,
                    maximum=32,
                    step=8,
                    value=16
                )
                
                steps = gr.Slider(
                    label="Inference Steps (Quality)",
                    minimum=25,
                    maximum=100,
                    step=25,
                    value=50
                )
                
                guidance = gr.Slider(
                    label="Guidance Scale (Prompt Adherence)",
                    minimum=1.0,
                    maximum=15.0,
                    step=0.5,
                    value=7.5
                )
                
                generate_btn = gr.Button("Generate Video", variant="primary", size="lg")
            
            with gr.Column():
                gr.Markdown("### Output")
                
                output_video = gr.Video(label="Generated Video")
                output_text = gr.Textbox(label="Status", interactive=False)
        
        # Connect button
        generate_btn.click(
            fn=generate_video_interface,
            inputs=[prompt, negative_prompt, num_frames, steps, guidance],
            outputs=[output_video, output_text]
        )
        
        # Examples
        gr.Markdown("### Example Prompts")
        gr.Examples(
            examples=[
                ["A beautiful sunset over the ocean with calm waves", "blurry, low quality", 16, 50, 7.5],
                ["A cat playing with a ball of yarn", "distorted, low quality", 16, 50, 7.5],
                ["A rocket launching into space", "blurry, low quality", 16, 50, 7.5],
                ["Waves crashing on a beach", "low quality, distorted", 16, 50, 7.5],
                ["A butterfly landing on a flower", "blurry, distorted", 16, 50, 7.5],
            ],
            inputs=[prompt, negative_prompt, num_frames, steps, guidance],
            fn=generate_video_interface,
            outputs=[output_video, output_text],
            cache_examples=False
        )
        
        gr.Markdown("---")
        gr.Markdown("**Information:**")
        gr.Markdown("""
        - Open-Sora generates high-quality videos (1024x576)
        - More inference steps = better quality but slower
        - Generation typically takes 5-10 minutes
        - GPU with 24GB+ VRAM recommended
        """)
    
    print("[OK] Web interface ready!")
    print("[*] Opening browser at http://127.0.0.1:7860")
    
    demo.launch(share=False, server_name="127.0.0.1", server_port=7860)


if __name__ == "__main__":
    launch_interface()
