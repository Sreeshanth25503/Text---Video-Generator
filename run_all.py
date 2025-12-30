"""
Master script to run all three versions of the text-to-video generator
1. Basic version (main.py)
2. Advanced version (advanced_generator.py)
3. Web interface (web_interface.py)
"""

import sys
import os

def run_basic():
    """Run the basic version"""
    print("\n" + "="*70)
    print("[GEN] RUNNING BASIC TEXT-TO-VIDEO GENERATOR (main.py)")
    print("="*70)
    
    try:
        from main import TextToVideoGenerator
        
        generator = TextToVideoGenerator()
        
        # Generate a simple test video
        print("\n[*] Generating test video...")
        result = generator.generate_video(
            prompt="A simple animated pattern, abstract art style",
            num_frames=8,
            num_inference_steps=10,
            output_path="test_basic.mp4"
        )
        
        if result:
            print(f"[OK] Basic test completed! Video: {result}")
            return True
        else:
            print("[WARN] Basic generation failed")
            return False
            
    except Exception as e:
        print(f"[ERROR] Basic version error: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_advanced():
    """Run the advanced version"""
    print("\n" + "="*70)
    print("[GEN] RUNNING ADVANCED TEXT-TO-VIDEO GENERATOR (advanced_generator.py)")
    print("="*70)
    
    try:
        from advanced_generator import AdvancedTextToVideoGenerator
        
        generator = AdvancedTextToVideoGenerator()
        
        # Generate a test video with advanced features
        print("\n[*] Generating test video with advanced options...")
        result = generator.generate_video(
            prompt="A colorful gradient animation",
            negative_prompt="blurry, low quality",
            num_frames=8,
            height=256,
            width=256,
            num_inference_steps=10,
            guidance_scale=7.0,
            output_path="test_advanced.mp4",
            seed=42,
            save_metadata=True
        )
        
        if result:
            print(f"[OK] Advanced test completed! Video: {result}")
            return True
        else:
            print("[WARN] Advanced generation failed")
            return False
            
    except Exception as e:
        print(f"[ERROR] Advanced version error: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_web_interface():
    """Run the web interface"""
    print("\n" + "="*70)
    print("[WEB] RUNNING WEB INTERFACE (web_interface.py)")
    print("="*70)
    
    try:
        from web_interface import VideoGeneratorInterface
        
        print("\n[*] Launching web interface...")
        print("[*] The interface will open in your browser automatically")
        print("[*] Go to: http://127.0.0.1:7860")
        print("[*] When done, close the browser or press Ctrl+C to stop")
        print("\n")
        
        app = VideoGeneratorInterface()
        # This is a blocking call - the interface will run until user closes it
        app.launch_interface()
        return True
        
    except Exception as e:
        print(f"[ERROR] Web interface error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("[*] TEXT-TO-VIDEO GENERATOR - COMPLETE TEST SUITE")
    print("="*70)
    print("\nThis will run all three versions of the generator:")
    print("1. Basic version (main.py)")
    print("2. Advanced version (advanced_generator.py)")
    print("3. Web interface (web_interface.py)")
    
    results = {}
    
    # Run basic version
    print("\n" + "-"*70)
    print("STAGE 1: BASIC VERSION")
    print("-"*70)
    results['basic'] = run_basic()
    
    # Run advanced version
    print("\n" + "-"*70)
    print("STAGE 2: ADVANCED VERSION")
    print("-"*70)
    results['advanced'] = run_advanced()
    
    # Run web interface
    print("\n" + "-"*70)
    print("STAGE 3: WEB INTERFACE (OPTIONAL)")
    print("-"*70)
    user_choice = input("\nRun web interface? (y/n): ").strip().lower()
    if user_choice == 'y':
        results['web'] = run_web_interface()
    else:
        print("[SKIP] Skipping web interface")
        results['web'] = None
    
    # Summary
    print("\n" + "="*70)
    print("[SUMMARY] TEST RESULTS")
    print("="*70)
    print(f"Basic Version:    {'[OK] PASSED' if results['basic'] else '[ERROR] FAILED'}")
    print(f"Advanced Version: {'[OK] PASSED' if results['advanced'] else '[ERROR] FAILED'}")
    web_status = '[OK] PASSED' if results['web'] else ('[SKIP] SKIPPED' if results['web'] is None else '[ERROR] FAILED')
    print(f"Web Interface:    {web_status}")
    
    core_passed = results['basic'] and results['advanced']
    if core_passed:
        print("\n[SUCCESS] CORE TESTS PASSED! Project is fully functional!")
    else:
        print("\n[WARN] Some tests failed. Check errors above.")
    
    return 0 if core_passed else 1


if __name__ == "__main__":
    sys.exit(main())
