import os

progress_file = r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 上册\.ocr_progress"

if os.path.exists(progress_file):
    with open(progress_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print("Last 10 processed files:")
        for line in lines[-10:]:
            print(line.strip())
        print(f"Total processed: {len(lines)}")
else:
    print("Progress file not found.")
