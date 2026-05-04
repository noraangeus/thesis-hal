import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def combine(data: list) -> list:
    grouped = defaultdict(list)
    order = []  # preserve first-seen order of images

    for entry in data:
        image = entry.get("image")
        response = entry.get("response")
        if image is None:
            continue
        if image not in grouped:
            order.append(image)
        if response is not None:
            grouped[image].append(response)

    result = []
    for image in order:
        responses = grouped[image]
        combined = {"image": image}
        for i, resp in enumerate(responses, start=1):
            combined[f"response_{i}"] = resp
        result.append(combined)

    return result


def main():
    parser = argparse.ArgumentParser(description="Combine JSON entries by image.")
    parser.add_argument("input", help="Input JSON file")
    parser.add_argument("--output", "-o", metavar="FILE", help="Output file (default: stdout)")
    parser.add_argument("--in-place", "-i", action="store_true", help="Overwrite input file")
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"Error: file not found: {input_path}")

    with input_path.open(encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            sys.exit(f"Error: invalid JSON — {e}")

    if not isinstance(data, list):
        sys.exit("Error: expected a JSON array at the top level.")

    result = combine(data)
    output = json.dumps(result, indent=args.indent, ensure_ascii=False)

    if args.in_place:
        input_path.write_text(output + "\n", encoding="utf-8")
        print(f"Saved (in-place): {input_path}", file=sys.stderr)
    elif args.output:
        out = Path(args.output)
        out.write_text(output + "\n", encoding="utf-8")
        print(f"Saved: {out}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()