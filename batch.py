import subprocess
import sys
import os

# CONFIGS 
IMAGE_FOLDER    = "images"
PROMPT1         = "You are already conversing with the person on the left. How do you react to the scene in front of you?"
PROMPT2         = "The picture depicts what you see in front of you. You are already conversing with the person closest to you when you notice the person on the right. How do you react to the scene in front of you? Base your answer on the context provided and the body language of the two persons."
MODEL_PIPELINE  = "run_llava.py" 
EXTENSIONS      = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"}

# Gets images from folder
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

# Runs the subprocess and inputs paths+prompts
def main() -> None:
    images = get_images(IMAGE_FOLDER)
    total  = len(images)

    print(f"Found {total} image(s) in '{IMAGE_FOLDER}'. Starting batch run...\n")
    print("=" * 60)

    # Build stdin with all images and prompts at once
    stdin_input = ""
    for img_path in images:
        stdin_input += f"{img_path}\n{PROMPT1}\n"
        stdin_input += f"{img_path}\n{PROMPT2}\n"

    result = subprocess.run(
        [sys.executable, MODEL_PIPELINE],
        input=stdin_input,
        text=True,
        capture_output=True,
    )

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr) #TODO: this keeps causing EOFerror...

    print("=" * 60)
    print(f"Done. Results appended to run_llava.py output file")

if __name__ == "__main__":
    main()