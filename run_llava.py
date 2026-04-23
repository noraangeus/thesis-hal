from transformers import pipeline
from PIL import Image
import datetime
import requests
import json

# Load once
pipe = pipeline("image-text-to-text", model="llava-hf/llava-v1.6-mistral-7b-hf")

while True:
    path = input("Image path or URL: ")
    prompt = input("Prompt: ")

    try:
        if path.startswith("http"):
            response = requests.get(path, timeout=10)
            response.raise_for_status()
            image = path  # URL is valid, pass it directly
        else:
            image = Image.open(path)

        messages = [
            {"role": "user", "content":
             [{"type": "image", "url": image},
            {"type": "text", "text": prompt}
        ]}]

        result = pipe(text=messages, max_new_tokens=200)
        output = result[0]["generated_text"][-1]["content"]
        print(output)

        # Write to a JSON file to save "chat history"
        log_entry = {
            "timestamp": datetime.datetime.now().strftime('%Y%m%d_%H%M%S'),
            "image": path,
            "prompt": prompt,
            "response": output
        }

        try:
            with open("results.json", "r") as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []

        logs.append(log_entry)

        with open("results.json", "w") as f:
            json.dump(logs, f, indent=2)

    except requests.exceptions.MissingSchema:
        print("Invalid URL format. Make sure it starts with http:// or https://")
    except requests.exceptions.ConnectionError:
        print("Could not connect. Check your internet connection or the URL.")
    except requests.exceptions.HTTPError as e:
        print(f"URL returned an error: {e}")
    except requests.exceptions.Timeout:
        print("Request timed out. Try again or use a different URL.")
    except FileNotFoundError:
        print(f"No file found at: {path}")
    except Exception as e:
        print(f"Something went wrong: {e}")

    print()

# from transformers import AutoProcessor, AutoModelForImageTextToText

# processor = AutoProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
# model = AutoModelForImageTextToText.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
# messages = [
#     {
#         "role": "user",
#         "content": [
#             {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
#             {"type": "text", "text": "What animal is on the candy?"}
#         ]
#     },
# ]
# inputs = processor.apply_chat_template(
# 	messages,
# 	add_generation_prompt=True,
# 	tokenize=True,
# 	return_dict=True,
# 	return_tensors="pt",
# ).to(model.device)

# outputs = model.generate(**inputs, max_new_tokens=40)
# print(processor.decode(outputs[0][inputs["input_ids"].shape[-1]:]))