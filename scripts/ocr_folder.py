import os
import sys
import base64
import json
import time
from pathlib import Path
import glob
import numpy as np
import cv2
import re

# Hack to fix PaddleOCR permission issue in sandbox
os.environ['USERPROFILE'] = os.getcwd()
os.environ["PADDLEOCR_HOME"] = os.path.join(os.getcwd(), ".paddleocr")
os.environ["PADDLEX_HOME"] = os.path.join(os.getcwd(), ".paddlex")

# Try to force CPU only and disable MKLDNN via env vars to avoid crash
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['FLAGS_allocator_strategy'] = 'auto_growth'

def ocr_image_paddle(image_path, ocr_engine):
    """
    Use PaddleOCR to OCR the image.
    """
    try:
        # Load using numpy+imdecode to handle Chinese paths
        with open(str(image_path), 'rb') as f:
            img_data = np.frombuffer(f.read(), dtype=np.uint8)
            img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)

        if img is None:
            return f"[Error: Failed to load image {image_path}]"

        h, w = img.shape[:2]
        
        # Resize to max side 1280 to prevent crashes on large images
        max_side = 1280
        scale = max_side / max(h, w)
        if scale < 1:
            new_w, new_h = int(w * scale), int(h * scale)
            img = cv2.resize(img, (new_w, new_h))
            # print(f"Resized {image_path.name} to {new_w}x{new_h}")

        # PaddleOCR v3+ (paddlex backend) returns a list of dicts
        # Removed 'cls' argument as it is not supported in predict()
        # Pass the numpy array directly
        result = ocr_engine.ocr(img)
            
        text_content = []
        if result:
            # Handle list of results (usually one per image)
            for res in result:
                if res is None:
                    continue
                    
                # Check for new dictionary format (v3+)
                if isinstance(res, dict) and 'rec_texts' in res:
                    text_content.extend(res['rec_texts'])
                # Check for old list format [[[[x,y],..], (text, score)], ...]
                elif isinstance(res, list):
                    for line in res:
                        if len(line) >= 2 and isinstance(line[1], tuple):
                            text_content.append(line[1][0])
                        elif len(line) >= 2 and isinstance(line[1], list):
                             text_content.append(line[1][0])
                
        return "\n".join(text_content)
    except Exception as e:
        return f"[OCR Error: {e}]"

def process_images(image_folder, ocr_engine=None):
    """
    Scan folder for images and OCR them.
    """
    folder = Path(image_folder)
    if not folder.exists():
        print(f"Error: Folder not found: {image_folder}")
        return

    # Find all images (png, jpg)
    images = list(folder.glob("*.png")) + list(folder.glob("*.jpg")) + list(folder.glob("*.jpeg"))
    
    if not images:
        print(f"No images found in {image_folder}")
        return

    # Sort images naturally by page number (1, 2, ... 10, 11 ...)
    def get_page_number(file_path):
        match = re.search(r'_page_(\d+)', file_path.name)
        if match:
            return int(match.group(1))
        return file_path.name
        
    images.sort(key=get_page_number)

    print(f"Found {len(images)} images to process. First 5: {[img.name for img in images[:5]]}")
    
    # Output file
    txt_output_path = folder / f"{folder.name}_ocr_result.txt"
    progress_file = folder / ".ocr_progress"
    
    processed_files = set()
    if progress_file.exists():
        with open(progress_file, 'r', encoding='utf-8') as f:
            processed_files = set(line.strip() for line in f)
        print(f"Found existing progress: {len(processed_files)} files already processed.")
    else:
        # Create/Clear output file if starting fresh
        with open(txt_output_path, 'w', encoding='utf-8') as f:
            f.write(f"OCR Results for folder: {folder.name}\n")
            f.write("=" * 50 + "\n\n")

    for i, image_path in enumerate(images):
        if image_path.name in processed_files:
            # Skip already processed
            continue
            
        print(f"[{i+1}/{len(images)}] Processing {image_path.name}...")
        
        try:
            ocr_text = ocr_image_paddle(image_path, ocr_engine)
            
            with open(txt_output_path, 'a', encoding='utf-8') as f:
                f.write(f"--- {image_path.name} ---\n\n")
                f.write(ocr_text)
                f.write("\n\n")
                
            # Mark as done
            with open(progress_file, 'a', encoding='utf-8') as f:
                f.write(f"{image_path.name}\n")
                
        except Exception as e:
            print(f"Error processing {image_path.name}: {e}")
            # Don't mark as done so we can retry

    print(f"All done! Results saved to: {txt_output_path}")
    # Optional: remove progress file if fully complete
    if len(processed_files) + 1 >= len(images): # Approximate check
        # os.remove(progress_file)
        pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ocr_folder.py <image_folder>")
        sys.exit(1)

    image_folder = sys.argv[1]

    print("Initializing PaddleOCR...")
    try:
        from paddleocr import PaddleOCR
        import paddle
        paddle.set_device('cpu')
        # Minimal init that worked in test_paddle.py
        paddle_engine = PaddleOCR(use_angle_cls=True, lang="ch", enable_mkldnn=False)
        print("PaddleOCR initialized.")
        
        process_images(image_folder, paddle_engine)
        
    except ImportError:
        print("Error: paddleocr not installed.")
        sys.exit(1)
    except Exception as e:
        print(f"Error initializing PaddleOCR: {e}")
        sys.exit(1)
