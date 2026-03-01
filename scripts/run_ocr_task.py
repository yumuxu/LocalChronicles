import os
import sys
from pathlib import Path

# Add the scripts folder to sys.path so we can import ocr_folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import ocr_folder

# Hardcoded path to avoid shell argument parsing issues with spaces
target_folder = r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 上册"

def main():
    print(f"Target folder: {target_folder}")
    
    if not os.path.exists(target_folder):
        print(f"Error: Folder does not exist: {target_folder}")
        return

    print("Initializing PaddleOCR...")
    try:
        from paddleocr import PaddleOCR
        import paddle
        paddle.set_device('cpu')
        # Minimal init that worked in test_paddle.py
        paddle_engine = PaddleOCR(use_angle_cls=True, lang="ch", enable_mkldnn=False)
        print("PaddleOCR initialized.")
        
        # Call the process_images function from ocr_folder.py
        ocr_folder.process_images(target_folder, paddle_engine)
        
    except ImportError:
        print("Error: paddleocr not installed.")
        sys.exit(1)
    except Exception as e:
        print(f"Error initializing PaddleOCR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
