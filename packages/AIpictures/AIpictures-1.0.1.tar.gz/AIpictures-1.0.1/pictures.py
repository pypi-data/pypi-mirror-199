import openai
import requests
import os
import random

def get_response():
    openai.api_key = input("Enter your OpenAI API key: ")
    prompt = input("Enter a prompt for the images: ")
    num_images = int(input("Enter the number of images to generate: "))
    size = input("Size 256x256, 512x512, 1024x1024: ")
    response = openai.Image.create(
    prompt=prompt,
    n=num_images,
    size=size
    )
    folder_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'openai_images')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for image_url in response['data']:
        image_url = image_url['url']
        response = requests.get(image_url)
        filename = f"{random.randint(1, 100000000)}.jpg"
        while os.path.exists(os.path.join(folder_path, filename)):
            filename = f"{random.randint(1, 100000000)}.jpg"
        with open(f"{folder_path}/{filename}", "wb") as f:
            f.write(response.content)
        
if __name__ == "__main__":
    get_response()