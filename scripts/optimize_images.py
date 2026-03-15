import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Re-encode gallery JPEGs at quality=85 to reduce file size."
    )
    parser.add_argument("gallery_dir", help="Root gallery directory (e.g. images/gallery)")
    return parser.parse_args()


def optimize_image(image_path: Path) -> None:
    original_size = image_path.stat().st_size

    img = ImageOps.exif_transpose(Image.open(image_path))

    # Write to a temp file first so we can compare sizes
    tmp_path = image_path.with_suffix(".tmp.jpg")
    img.save(tmp_path, format="JPEG", quality=85, optimize=True, progressive=True)

    new_size = tmp_path.stat().st_size

    if new_size < original_size:
        tmp_path.replace(image_path)
        saving_pct = (1 - new_size / original_size) * 100
        print(
            f"  {image_path.name}: {original_size // 1024}K → {new_size // 1024}K"
            f" (-{saving_pct:.0f}%)"
        )
    else:
        tmp_path.unlink()
        print(f"  {image_path.name}: skipped (already optimal, {original_size // 1024}K)")


def main() -> None:
    args = parse_args()
    gallery_dir = Path(args.gallery_dir)

    if not gallery_dir.exists():
        print(f"Error: {gallery_dir} does not exist")
        sys.exit(1)

    jpeg_extensions = {".jpg", ".jpeg"}
    images = [
        p
        for p in gallery_dir.rglob("*")
        if p.suffix.lower() in jpeg_extensions and "thumbnails" not in p.parts
    ]

    if not images:
        print("No JPEG images found.")
        return

    print(f"Optimizing {len(images)} images in {gallery_dir}...\n")
    for image_path in sorted(images):
        optimize_image(image_path)


if __name__ == "__main__":
    main()
