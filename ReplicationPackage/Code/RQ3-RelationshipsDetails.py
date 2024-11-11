import base64
import requests
import os
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

# Specify the directory containing images
directory = "./RQ3-gpt-4o-mini"
image_files_array = get_image_files(directory)

# Output file path
output_file = "RQ3_gpt_4o-mini_output.txt"

# Open the text file in write mode
with open(output_file, "w") as text_file:

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
                            "text": (
                                "You are a software engineer. Your task is to accurately identify and describe "
                                "the relationships within this image of a UML Use Case Diagram (UCD). For each relationship "
                                "you identify, please provide the following information: \n\n"
                                "(a) Type of Relationship: e.g., association, include, extend, dependency, generalization), \n"
                                "(b) Source Element: Actor or use case from which this relationship originates, \n"
                                "(c) Target Element: Actor or use case to which this relationship points. \n\n"
                                "Please report only the relationships found in the image and return your response in a structured format with each relationship clearly separated. "
                                "Aim for clarity and accuracy in identifying all relationship details."
                            )
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
            "max_tokens": 1000
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

        # Write the results to the text file
        text_file.write(f"==== Image: {file} ====\n")
        text_file.write(content1 + "\n\n")
        text_file.write("=" * 50 + "\n\n")  # Adding a separator between each image's details

print(f"Results saved to {output_file}")
