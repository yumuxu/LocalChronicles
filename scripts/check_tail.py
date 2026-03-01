import os

file_path = r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 下册\八闽通志（修订本） 下册_ocr_result.txt"
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # Seek to end
        f.seek(0, 2)
        size = f.tell()
        # Read last 2000 bytes
        read_size = min(2000, size)
        f.seek(size - read_size)
        content = f.read()
        print(content)
else:
    print("File not found.")
