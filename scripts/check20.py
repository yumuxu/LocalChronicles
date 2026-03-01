import os

volumes_dir = r"f:\adsense\LocalChronicles\volumes"
files = [f for f in os.listdir(volumes_dir) if f.startswith('卷20')]
print(files)
print(f"\nTotal: {len(files)}")
