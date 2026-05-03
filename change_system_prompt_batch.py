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

# Runs the subprocess and inputs paths+prompts
def run_pipeline(images: list[str], system_prompt: str, prompt: str, label: str) -> None:
    """Run the pipeline subprocess for one system prompt over all images."""
    # system_prompt goes first (consumed once at startup by run_llava.py),
    # then path + prompt pairs for each iteration of its while True loop.
    stdin_lines = [system_prompt]
    for img_path in images:
        stdin_lines.append(img_path)
        stdin_lines.append(prompt)
    stdin_input = "\n".join(stdin_lines) + "\n"

    print(f"\n[{label}] Running on {len(images)} image(s)...")
    result = subprocess.run(
        [sys.executable, MODEL_PIPELINE],
        input=stdin_input,
        text=True,
        capture_output=True,
    )

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        # Filter out expected EOFError — raised when stdin is exhausted and run_llava.py's while True loop tries to read another path
        filtered = "\n".join(
            line for line in result.stderr.splitlines()
            if "EOFError" not in line and "input()" not in line
        )
        if filtered:
            print(filtered, file=sys.stderr)


def main() -> None:
    images = get_images(IMAGE_FOLDER)
    total = len(images)

    print(f"Found {total} image(s) in '{IMAGE_FOLDER}'.\n")
    print("=" * 60)

    systemprompt1 = input("First system prompt: ").strip()
    systemprompt2 = input("Second system prompt: ").strip()
    prompt = input("User prompt: ").strip()

    print("=" * 60)

    run_pipeline(images, systemprompt1, prompt, label="System Prompt 1")
    run_pipeline(images, systemprompt2, prompt, label="System Prompt 2")

    print("\n" + "=" * 60)
    print(f"Done. All {total} image(s) processed with both system prompts.")


if __name__ == "__main__":
    main()