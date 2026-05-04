from transformers import pipeline
from PIL import Image
import datetime
import requests
import json

# Load once
pipe = pipeline("image-text-to-text", model="llava-hf/llava-v1.6-mistral-7b-hf")
#system_prompt = input("System prompt: ")

while True:
    path = input("Image path or URL: ")
    prompt = input("Prompt: ")
    #system_prompt = "Always act as if the attached image is your own vision. Respond accordingly."

    try:
        if path.startswith("http"):
            response = requests.get(path, timeout=10)
            response.raise_for_status()
            image = path  # URL is valid, pass it
        else:
            image = Image.open(path)

        messages = [
            # {"role": "system", "content":
            #  [{"type": "text", "text": system_prompt}]},
            {"role": "user", "content":
             [{"type": "image", "url": image},
            {"type": "text", "text": prompt}
        ]}]

        result = pipe(text=messages, max_new_tokens=500)
        output = result[0]["generated_text"][-1]["content"]
        print(output)

        # Write to a JSON file to save "chat history"
        log_entry = {
            # Makes sure timestamp is Swedish (UTC+2)
            "timestamp": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).strftime('%Y%m%d_%H%M%S'),
            "image": path,
            #"system prompt": system_prompt,
            "prompt": prompt,
            "response": output
        }

        try:
            with open("datasetv11.json", "r") as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []

        logs.append(log_entry)

        with open("datasetv11.json", "w") as f:
            json.dump(logs, f, indent=2)

    # Handle file path issues without crashing
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