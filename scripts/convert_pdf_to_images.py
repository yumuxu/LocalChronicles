import os
import sys
from pathlib import Path

# Try to import pdf2image, but provide a helpful error if it fails
try:
    from pdf2image import convert_from_path, pdfinfo_from_path
except ImportError:
    print("Error: The 'pdf2image' library is not installed.")
    print("Please install it using: pip install pdf2image")
    print("You also need to install 'poppler' and add it to your PATH.")
    sys.exit(1)

def convert_pdf(pdf_path, output_folder=None, dpi=300, fmt='png'):
    """
    Converts a PDF file to images.
    
    Args:
        pdf_path (str): Path to the PDF file.
        output_folder (str): Directory to save images. Defaults to PDF's directory.
        dpi (int): Resolution of the output images.
        fmt (str): Output format (png, jpeg, tiff, ppm).
    """
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"Error: File not found: {pdf_path}")
        return

    if output_folder is None:
        output_folder = pdf_file.parent / pdf_file.stem
    else:
        output_folder = Path(output_folder) / pdf_file.stem
        
    output_folder.mkdir(parents=True, exist_ok=True)

    print(f"Converting '{pdf_file.name}' to images at {dpi} DPI...")

    try:
        # Get PDF info to know total pages
        info = pdfinfo_from_path(str(pdf_file))
        max_pages = info["Pages"]
        print(f"Total pages to convert: {max_pages}")

        # Convert page by page to save memory and show progress
        for page_num in range(1, max_pages + 1):
            image_name = f"{pdf_file.stem}_page_{page_num}.{fmt}"
            output_path = output_folder / image_name

            if output_path.exists():
                print(f"[{page_num}/{max_pages}] Skipping page {page_num} (already exists)")
                continue

            print(f"[{page_num}/{max_pages}] Converting page {page_num}...")
            
            # Convert just this page
            images = convert_from_path(str(pdf_file), dpi=dpi, first_page=page_num, last_page=page_num)
            
            if images:
                image = images[0]
                image.save(output_path, fmt.upper())
                print(f"Saved: {output_path}")
            
        print("Conversion complete.")

    except Exception as e:
        print(f"Error during conversion: {e}")
        print("Ensure 'poppler' is installed and added to PATH.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_pdf_to_images.py <pdf_path> [output_folder] [dpi]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    
    output_folder = None
    if len(sys.argv) > 2:
        output_folder = sys.argv[2]
        
    dpi = 300
    if len(sys.argv) > 3:
        try:
            dpi = int(sys.argv[3])
        except ValueError:
            print("Warning: DPI must be an integer. Using default 300 DPI.")

    convert_pdf(pdf_path, output_folder, dpi)
