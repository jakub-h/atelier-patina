import argparse
import sys
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the thumbnail script."""
    parser = argparse.ArgumentParser(
        description="Create thumbnails for images in a directory."
    )
    parser.add_argument("images_dir", help="Directory containing images")
    parser.add_argument(
        "--size",
        type=int,
        nargs=2,
        default=[600, 800],
        metavar=("WIDTH", "HEIGHT"),
        help="Thumbnail size (default: 600x800)",
    )
    return parser.parse_args()


def create_thumbnail(
    image_path: Path, thumb_dir: Path, size: tuple[int, int] = (600, 800)
) -> None:
    """Create a thumbnail with center crop to maintain aspect ratio."""
    img = Image.open(image_path)

    # Calculate target aspect ratio
    target_ratio = size[0] / size[1]

    # Calculate dimensions for center crop
    img_ratio = img.width / img.height
    if img_ratio > target_ratio:
        # Image is wider than target ratio
        new_width = int(img.height * target_ratio)
        crop_left = (img.width - new_width) // 2
        crop_box = (crop_left, 0, crop_left + new_width, img.height)
    else:
        # Image is taller than target ratio
        new_height = int(img.width / target_ratio)
        crop_top = (img.height - new_height) // 2
        crop_box = (0, crop_top, img.width, crop_top + new_height)

    # Crop and resize
    img = img.crop(crop_box)
    img = img.resize(size, Image.Resampling.LANCZOS)

    thumb_path = thumb_dir / f"{image_path.stem}-thumb{image_path.suffix}"
    save_kwargs: dict = {"optimize": True}
    if image_path.suffix.lower() in (".jpg", ".jpeg"):
        save_kwargs["quality"] = 85
    img.save(thumb_path, **save_kwargs)


def main(args: argparse.Namespace) -> None:
    """Create thumbnails for all images in the given directory."""
    args = parse_args()
    images_dir = Path(args.images_dir)
    size = tuple(args.size)

    if not images_dir.exists():
        print(f"Error: Directory {images_dir} does not exist")
        sys.exit(1)

    # Create thumbnails subdirectory
    thumb_dir = images_dir / "thumbnails"
    thumb_dir.mkdir(exist_ok=True)

    # Process all images
    image_extensions = [".jpg", ".jpeg", ".png", ".PNG"]
    for ext in image_extensions:
        for image_path in images_dir.glob(f"*{ext}"):
            if image_path.parent != thumb_dir:  # Skip if image is in thumbnails dir
                print(f"Creating thumbnail for {image_path.name}")
                create_thumbnail(image_path, thumb_dir, size)


if __name__ == "__main__":
    args = parse_args()
    main(args)
