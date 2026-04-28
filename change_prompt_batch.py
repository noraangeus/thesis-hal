import subprocess
import sys
import os

# CONFIGS 
IMAGE_FOLDER    = "images"
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


def get_prompt_for_batch(batch_number: int) -> tuple[str, str]:
    """Prompt user to enter prompts for the current batch."""
    print(f"\n--- Batch {batch_number} ---")
    prompt1 = input("Enter PROMPT1 for this batch: ").strip()
    prompt2 = input("Enter PROMPT2 for this batch: ").strip()
    return prompt1, prompt2


def run_batch(batch_images: list[str], prompt1: str, prompt2: str, batch_number: int) -> None:
    """Build stdin and run the subprocess for a single batch."""
    stdin_input = ""
    for img_path in batch_images:
        stdin_input += f"{img_path}\n{prompt1}\n"
        stdin_input += f"{img_path}\n{prompt2}\n"

    print(f"\nRunning batch {batch_number} ({len(batch_images)} image(s))...")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, MODEL_PIPELINE],
        input=stdin_input,
        text=True,
        capture_output=True,
    )

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    print("=" * 60)


# Runs the subprocess and inputs paths+prompts
def main() -> None:
    images = get_images(IMAGE_FOLDER)
    total  = len(images)
    batch_size = 10

    print(f"Found {total} image(s) in '{IMAGE_FOLDER}'. Starting batch run...\n")

    batches = [images[i:i + batch_size] for i in range(0, total, batch_size)]
    num_batches = len(batches)

    print(f"Processing {num_batches} batch(es) of up to {batch_size} images each.")

    for batch_number, batch_images in enumerate(batches, start=1):
        print(f"\nBatch {batch_number}/{num_batches} — images {(batch_number - 1) * batch_size + 1}"
              f" to {min(batch_number * batch_size, total)} of {total}")

        prompt1, prompt2 = get_prompt_for_batch(batch_number)
        run_batch(batch_images, prompt1, prompt2, batch_number)

    print(f"\nDone. All {num_batches} batch(es) complete. Results appended to run_llava.py output file.")


if __name__ == "__main__":
    main()