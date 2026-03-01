import os
import sys
from pathlib import Path

# Add scripts folder to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import convert_pdf_to_images
import ocr_folder
from paddleocr import PaddleOCR

# Define paths
pdf_path = r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 下册.pdf"
expected_img_folder = r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 下册"

def main():
    # 1. Convert PDF
    print(f"Starting processing for: {pdf_path}")
    
    # Always call convert_pdf, it now handles skipping existing pages
    print("Converting PDF to images (skipping existing)...")
    convert_pdf_to_images.convert_pdf(pdf_path, dpi=300)

    # 2. Initialize OCR Engine
    print("Initializing PaddleOCR...")
    # Environment hacks
    os.environ['USERPROFILE'] = os.getcwd()
    os.environ["PADDLEOCR_HOME"] = os.path.join(os.getcwd(), ".paddleocr")
    os.environ["PADDLEX_HOME"] = os.path.join(os.getcwd(), ".paddlex")
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    os.environ['FLAGS_use_mkldnn'] = '0'
    os.environ['FLAGS_allocator_strategy'] = 'auto_growth'
    
    try:
        # Initialize
        # Removed use_gpu and show_log as they caused errors.
        ocr_engine = PaddleOCR(use_angle_cls=True, lang="ch", enable_mkldnn=False)
    except Exception as e:
        print(f"Error initializing PaddleOCR: {e}")
        return

    # 3. Run OCR
    print(f"Starting OCR on folder: {expected_img_folder}")
    try:
        ocr_folder.process_images(expected_img_folder, ocr_engine)
        print("OCR Task Completed Successfully!")
    except Exception as e:
        print(f"Error during OCR processing: {e}")

if __name__ == "__main__":
    main()
