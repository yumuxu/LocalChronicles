
from mcp.server.fastmcp import FastMCP
import os
import sys
from pathlib import Path

# Add scripts folder to path to allow imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import existing modules
# We wrap these in try-except to avoid crashing if dependencies are missing during initial setup
try:
    import convert_pdf_to_images
    import ocr_folder
    from paddleocr import PaddleOCR
    import paddle
except ImportError as e:
    print(f"Warning: Dependencies missing: {e}")

# Initialize MCP Server
mcp = FastMCP("LocalChronicles OCR Server")

# Global OCR Engine (Lazy load)
_ocr_engine = None

def get_ocr_engine():
    global _ocr_engine
    if _ocr_engine is None:
        print("Initializing PaddleOCR Engine...")
        # Environment hacks from ocr_folder.py are already applied when importing ocr_folder
        # But we ensure they are set just in case
        os.environ['USERPROFILE'] = os.getcwd()
        os.environ["PADDLEOCR_HOME"] = os.path.join(os.getcwd(), ".paddleocr")
        os.environ["PADDLEX_HOME"] = os.path.join(os.getcwd(), ".paddlex")
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
        os.environ['FLAGS_use_mkldnn'] = '0'
        os.environ['FLAGS_allocator_strategy'] = 'auto_growth'
        
        paddle.set_device('cpu')
        _ocr_engine = PaddleOCR(use_angle_cls=True, lang="ch", enable_mkldnn=False)
        print("PaddleOCR Engine Initialized.")
    return _ocr_engine

@mcp.tool()
def pdf_to_images(pdf_path: str, output_folder: str = None, dpi: int = 300) -> str:
    """
    Convert a PDF file to images.
    
    Args:
        pdf_path: Path to the PDF file.
        output_folder: Directory to save images. Defaults to PDF's directory.
        dpi: Resolution of the output images. Default is 300.
    """
    try:
        convert_pdf_to_images.convert_pdf(pdf_path, output_folder, dpi)
        return f"Conversion completed for {pdf_path}"
    except Exception as e:
        return f"Error converting PDF: {str(e)}"

@mcp.tool()
def run_ocr_on_folder(image_folder: str) -> str:
    """
    Run OCR on all images in a folder using PaddleOCR.
    This is a blocking operation that processes images sequentially.
    Results are saved to 'folder_name_ocr_result.txt' in the folder.
    
    Args:
        image_folder: Path to the folder containing images.
    """
    try:
        engine = get_ocr_engine()
        ocr_folder.process_images(image_folder, engine)
        
        folder_path = Path(image_folder)
        result_file = folder_path / f"{folder_path.name}_ocr_result.txt"
        return f"OCR task completed. Results saved to {result_file}"
    except Exception as e:
        return f"Error running OCR: {str(e)}"

@mcp.tool()
def ocr_single_image(image_path: str) -> str:
    """
    Run OCR on a single image.
    
    Args:
        image_path: Path to the image file.
    """
    try:
        engine = get_ocr_engine()
        result = ocr_folder.ocr_image_paddle(image_path, engine)
        return result
    except Exception as e:
        return f"Error OCRing image: {str(e)}"

if __name__ == "__main__":
    mcp.run()
