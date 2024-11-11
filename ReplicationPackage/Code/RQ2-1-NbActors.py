# RQ2-1: Number of actors in a UML class diagram

import base64
import requests
import os
import openpyxl
from datetime import datetime
from PIL import Image

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set it as an environment variable.")

def get_image_files(directory):
    try:
        # Get all files in the specified directory
        files = os.listdir(directory)
        
        # Filter out files based on common image extensions
        image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.jfif','.tiff'))]
        
        return image_files  # Return the array of image filenames
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Initialize Excel workbook
output_file = "RQ2-1_nb_actor_gpt_4o_mini.xlsx"
wb = openpyxl.Workbook()
ws = wb.active
ws.append(["Image Name", "Response"])

# Specify the directory containing images
directory = "./gpt-4o-mini-UCD"
image_files_array = get_image_files(directory)

# Iterate through each image file in the directory
for file in image_files_array:
    image_path = os.path.join(directory, file)
    print(f"Processing: {image_path}")

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",  # specify your model here
        "temperature": 0.1,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a software engineer. Analyze the following image of a UML Use Case Diagram. How many actors are depicted? Respond with the number only."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    # Make a POST request to the API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Parse the response
    try:
        response_json = response.json()
        # Extract the content of the assistant's message
        content1 = response_json['choices'][0]['message']['content']
    except Exception as e:
        content1 = f"Error: {e}"

    # Append the image name and response to the Excel file
    ws.append([file, content1])

# Save the Excel file
wb.save(output_file)
print(f"Results saved to {output_file}")
