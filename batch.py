import subprocess
import sys
import os

# ── Configuration ────────────────────────────────────────────────────────────
IMAGE_FOLDER = "images"          # Folder containing your images
PROMPT1       = "Look at the two people in the picture. Imagine that you are a service robot that is already in conversation to the person on the left. You see the person on the right approaching the conversation you are having, intending to interrupt. How do you react? Base your answer on their body language."  # First prompt sent for every image
PROMPT2       = "Look at the two people in the picture. Imagine that you are a service robot that is already in conversation to the person on the left. You see the person on the right approaching the conversation you are having, intending to interrupt. How do you react? Base your answer on their body language, and remember that you would have to be very polite."  # Second prompt sent for every image
SCRIPT       = "run_llava.py" # Name of your original Python file
EXTENSIONS   = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"}
# ─────────────────────────────────────────────────────────────────────────────


def get_images(folder: str) -> list[str]:
    """Return sorted list of image paths from the given folder."""
    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a valid directory.")
        sys.exit(1)

    images = sorted(
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if os.path.splitext(f)[1].lower() in EXTENSIONS
    )

    if not images:
        print(f"No images found in '{folder}' with extensions: {EXTENSIONS}")
        sys.exit(1)

    return images


def run_on_image(image_path: str, prompt: str) -> None:
    """Feed one image path + prompt to the original script via stdin."""
    stdin_input = f"{image_path}\n{prompt}\n"

    result = subprocess.run(
        [sys.executable, SCRIPT],
        input=stdin_input,
        text=True,
        capture_output=True,
    )

    # Print whatever the script produced
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)


def main() -> None:
    images = get_images(IMAGE_FOLDER)
    total  = len(images)

    print(f"Found {total} image(s) in '{IMAGE_FOLDER}'. Starting batch run...\n")
    print("=" * 60)

    for i, img_path in enumerate(images, start=1):
        print(f"[{i}/{total}] {img_path}")
        run_on_image(img_path, PROMPT1)
        run_on_image(img_path, PROMPT2)
        print()

    print("=" * 60)
    print(f"Done. Results appended to run_llava.py output file")


if __name__ == "__main__":
    main()