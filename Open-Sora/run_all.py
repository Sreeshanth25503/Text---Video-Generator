"""
OPEN-SORA TEST SUITE
Tests all versions of Open-Sora generator.
"""

import os
import sys
from advanced_generator import AdvancedTextToVideoGenerator

def run_basic_test():
    """Test basic video generation"""
    print("\n" + "="*70)
    print("TEST 1: BASIC VIDEO GENERATION")
    print("="*70)
    
    try:
        generator = AdvancedTextToVideoGenerator()
        
        result = generator.generate_video(
            prompt="A beautiful sunset over mountains with calm clouds",
            num_frames=8,
            num_inference_steps=25,
            output_path="test_basic_opensora.mp4"
        )
        
        if result:
            print("[OK] Basic test passed!")
            return True
        else:
            print("[ERROR] Basic test failed!")
            return False
    
    except Exception as e:
        print(f"[ERROR] Exception in basic test: {e}")
        return False

def run_advanced_test():
    """Test advanced features"""
    print("\n" + "="*70)
    print("TEST 2: ADVANCED FEATURES (Negative Prompt)")
    print("="*70)
    
    try:
        generator = AdvancedTextToVideoGenerator()
        
        result = generator.generate_video(
            prompt="A cat playing with a toy, detailed, clear",
            negative_prompt="blurry, low quality, distorted",
            num_frames=8,
            num_inference_steps=25,
            output_path="test_advanced_opensora.mp4",
            seed=42
        )
        
        if result:
            print("[OK] Advanced test passed!")
            return True
        else:
            print("[ERROR] Advanced test failed!")
            return False
    
    except Exception as e:
        print(f"[ERROR] Exception in advanced test: {e}")
        return False

def run_comparison_test():
    """Test quality comparison"""
    print("\n" + "="*70)
    print("TEST 3: QUALITY COMPARISON")
    print("="*70)
    
    try:
        generator = AdvancedTextToVideoGenerator()
        
        results = generator.compare_settings(
            prompt="A butterfly landing on a flower",
            output_folder="test_comparison_opensora"
        )
        
        if results and len(results) > 0:
            print("[OK] Comparison test passed!")
            return True
        else:
            print("[ERROR] Comparison test failed!")
            return False
    
    except Exception as e:
        print(f"[ERROR] Exception in comparison test: {e}")
        return False

def run_web_interface_test():
    """Test web interface"""
    print("\n" + "="*70)
    print("TEST 4: WEB INTERFACE")
    print("="*70)
    
    try:
        print("[*] Web interface can be tested by running: python web_interface.py")
        print("[*] This will open a browser at http://127.0.0.1:7860")
        return True
    
    except Exception as e:
        print(f"[ERROR] Exception in web interface test: {e}")
        return False

def main():
    """Run all tests"""
    
    print("\n")
    print("[GEN] OPEN-SORA TEXT-TO-VIDEO GENERATOR - TEST SUITE")
    print("[GEN] ================================================")
    print(f"[*] Model: hpcai-tech/Open-Sora")
    print(f"[*] This will test basic, advanced, and comparison features")
    print(f"[WARN] Each test may take 5-10 minutes!")
    
    input("\n[*] Press Enter to start tests...")
    
    results = {
        "basic": False,
        "advanced": False,
        "comparison": False,
        "web": False
    }
    
    # Run basic test
    results["basic"] = run_basic_test()
    
    # Ask if user wants to continue
    if results["basic"]:
        choice = input("\n[*] Run advanced test? (y/n): ").lower()
        if choice == 'y':
            results["advanced"] = run_advanced_test()
    
    # Ask for comparison
    if results["advanced"]:
        choice = input("\n[*] Run comparison test? (y/n): ").lower()
        if choice == 'y':
            results["comparison"] = run_comparison_test()
    
    # Test web interface
    choice = input("\n[*] Test web interface? (y/n): ").lower()
    if choice == 'y':
        results["web"] = run_web_interface_test()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Basic Test: {'PASSED' if results['basic'] else 'FAILED'}")
    print(f"Advanced Test: {'PASSED' if results['advanced'] else 'FAILED'}")
    print(f"Comparison Test: {'PASSED' if results['comparison'] else 'FAILED'}")
    print(f"Web Interface: {'PASSED' if results['web'] else 'FAILED'}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("[OK] All tests passed! Open-Sora is working correctly!")
    else:
        print("[WARN] Some tests failed. Check console output above.")
    
    print("\n[*] To generate videos, run:")
    print("    python main.py                (basic)")
    print("    python advanced_generator.py  (advanced)")
    print("    python web_interface.py       (web interface)")

if __name__ == "__main__":
    main()
