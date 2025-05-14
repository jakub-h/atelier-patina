import argparse
from pathlib import Path

from bs4 import BeautifulSoup, Tag
from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fill gallery pages with images from corresponding directories"
    )
    parser.add_argument("gallery_dir", help="Directory containing gallery pages")
    parser.add_argument("images_dir", help="Directory containing image subdirectories")
    parser.add_argument("--item-name", "-i", default=None, help="Item name to process")
    return parser.parse_args()


def get_image_dimensions(image_path: Path) -> tuple[int, int]:
    """Get the dimensions of an image file"""
    with Image.open(image_path) as img:
        return img.size


def create_gallery_html(images_dir: Path, relative_path: str) -> BeautifulSoup:
    """Create HTML for gallery items using BeautifulSoup"""
    soup = BeautifulSoup("", "html.parser")

    for image_path in sorted(images_dir.iterdir()):
        if image_path.suffix not in [".jpg", ".jpeg", ".png", ".PNG"]:
            continue

        if "thumb" not in image_path.stem:  # Skip thumbnails
            # Find corresponding thumbnail
            thumb_path = (
                images_dir
                / "thumbnails"
                / f"{image_path.stem}-thumb{image_path.suffix}"
            )
            if not thumb_path.exists():
                continue

            width, height = get_image_dimensions(image_path)
            relative_image_path = f"../{relative_path}/{image_path.name}"
            relative_thumb_path = f"../{relative_path}/thumbnails/{thumb_path.name}"

            # Create elements using BeautifulSoup
            a_tag = soup.new_tag("a", href=relative_image_path)
            a_tag["data-pswp-width"] = str(width)
            a_tag["data-pswp-height"] = str(height)

            img_tag = soup.new_tag("img", src=relative_thumb_path, alt=image_path.stem)
            a_tag.append(img_tag)
            soup.append(a_tag)

    return soup


def main() -> None:
    args = parse_args()
    gallery_pages_dir = Path(args.gallery_dir)
    images_dir = Path(args.images_dir)

    if not all(p.exists() for p in [gallery_pages_dir, images_dir]):
        print("Error: One or more directories do not exist")
        exit(1)

    # Process each gallery page
    for page_path in gallery_pages_dir.glob("*.html"):
        # Extract item name from filename (e.g., 'zidle' from 'zidle.html')
        item_name = page_path.stem

        if args.item_name and item_name != args.item_name:
            continue

        # Find corresponding images directory
        item_images_dir = images_dir / item_name
        if not item_images_dir.exists():
            print(f"Warning: No image directory found for {item_name}")
            continue

        # Read the HTML file
        html_content = page_path.read_text(encoding="utf-8")

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the gallery div
        gallery_div = soup.find("div", {"class": "gallery", "id": "realizace-gallery"})
        if not gallery_div or not isinstance(gallery_div, Tag):
            print(f"Warning: Gallery div not found in {page_path}")
            continue

        # Generate new gallery HTML
        relative_path = f"images/gallery/{item_name}"
        new_gallery_soup = create_gallery_html(item_images_dir, relative_path)

        # Replace gallery content
        gallery_div.clear()
        gallery_div.extend(new_gallery_soup.contents)

        # Write updated content back to file
        page_path.write_text(soup.prettify(formatter="minimal"), encoding="utf-8")
        print(f"Updated gallery in {page_path}")


if __name__ == "__main__":
    main()
