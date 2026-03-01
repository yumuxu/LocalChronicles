import os
import sys

# Hack to fix PaddleOCR permission issue in sandbox
os.environ['USERPROFILE'] = os.getcwd()
os.environ["PADDLEOCR_HOME"] = os.path.join(os.getcwd(), ".paddleocr")
os.environ["PADDLEX_HOME"] = os.path.join(os.getcwd(), ".paddlex")

# Try to force CPU only and disable MKLDNN via env vars
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['FLAGS_allocator_strategy'] = 'auto_growth'

try:
    from paddleocr import PaddleOCR
    import paddle
    print(f"PaddlePaddle Version: {paddle.__version__}")
    
    print("Initializing PaddleOCR...")
    # Try minimal init, remove unknown args
    paddle.set_device('cpu')
    ocr = PaddleOCR(use_angle_cls=True, lang="ch", enable_mkldnn=False)
    
    print("PaddleOCR initialized successfully.")
    
    # Test with a dummy image if possible, or just exit
    print("Test passed.")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
