import os
import sys
import numpy as np

# Hack to fix PaddleOCR permission issue in sandbox
os.environ['USERPROFILE'] = os.getcwd()
os.environ["PADDLEOCR_HOME"] = os.path.join(os.getcwd(), ".paddleocr")
os.environ["PADDLEX_HOME"] = os.path.join(os.getcwd(), ".paddlex")

# Force CPU
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['FLAGS_allocator_strategy'] = 'auto_growth'

try:
    from paddleocr import PaddleOCR
    import paddle
    import cv2
    
    paddle.set_device('cpu')
    print("PaddlePaddle version:", paddle.__version__)
    
    # Create a dummy image
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img[:] = 255
    cv2.putText(img, 'Hello', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.imwrite("test_img.png", img)
    print("Dummy image created.")

    # 1. Test Full Pipeline without CLS with REAL IMAGE
    print("\n--- Test 1: Full Pipeline (No CLS) with REAL IMAGE ---")
    ocr_full = PaddleOCR(use_angle_cls=False, lang="ch", enable_mkldnn=False)
    
    real_img_path = r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 上册\八闽通志（修订本） 上册_page_1.png"
    if not os.path.exists(real_img_path):
        print(f"Error: Real image not found: {real_img_path}")
        # Fallback to test_img
        res = ocr_full.ocr("test_img.png")
    else:
        print(f"Testing with: {real_img_path}")
        
        # Load using numpy+imdecode to handle Chinese paths
        # This is the key fix!
        try:
            with open(real_img_path, 'rb') as f:
                img_data = np.frombuffer(f.read(), dtype=np.uint8)
                img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
        except Exception as e:
            print(f"Failed to load image via numpy: {e}")
            img = None

        if img is None:
            print("Failed to load image even with numpy trick")
        else:
            h, w = img.shape[:2]
            print(f"Original size: {w}x{h}")
            
            # Force Resize to test stability
            # Try to resize to max side 1280
            scale = 1280 / max(h, w)
            if scale < 1:
                new_w, new_h = int(w * scale), int(h * scale)
                img = cv2.resize(img, (new_w, new_h))
                print(f"Manually resized to: {new_w}x{new_h}")
            
            # We can now pass the numpy array directly to PaddleOCR
            res = ocr_full.ocr(img)
        
    print("Full (No CLS) Result Count:", len(res[0]) if res else 0)

    # 2. Test Full Pipeline with CLS
    # print("\n--- Test 2: Full Pipeline (With CLS) ---")
    # ocr_cls = PaddleOCR(use_angle_cls=True, lang="ch", enable_mkldnn=False)
    # res = ocr_cls.ocr("test_img.png") # Removed cls arg
    # print("Full (With CLS) Result:", res)

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
