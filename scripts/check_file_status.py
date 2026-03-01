import os
import glob

pdf_path = r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 下册.pdf"
img_folder = r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 下册"
parent_dir = r"f:\adsense\LocalChronicles\fujian"

print(f"Checking for PDF: {pdf_path}")
if os.path.exists(pdf_path):
    print("PDF Found!")
else:
    print("PDF NOT Found.")
    print("Files in parent directory:")
    try:
        files = os.listdir(parent_dir)
        for f in files:
            print(f"  - {f}")
    except Exception as e:
        print(f"Error listing directory: {e}")

print(f"\nChecking for Image Folder: {img_folder}")
if os.path.exists(img_folder):
    print("Image Folder Found!")
    images = glob.glob(os.path.join(img_folder, "*.png"))
    print(f"Found {len(images)} png images.")
else:
    print("Image Folder NOT Found.")
