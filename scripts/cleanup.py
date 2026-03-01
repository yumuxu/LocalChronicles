import os

volumes_dir = r"f:\adsense\LocalChronicles\volumes"
files = os.listdir(volumes_dir)
for f in files:
    if '_' not in f:
        os.remove(os.path.join(volumes_dir, f))
        print(f"删除: {f}")
print(f"\n清理完成，保留 {len(os.listdir(volumes_dir))} 个文件")
