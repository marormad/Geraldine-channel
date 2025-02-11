import requests
from bs4 import BeautifulSoup
import base64
import os
import re

# Ticker list
ticker = "MMM"
# URL of the website
url = f"https://geraldineweiss.onrender.com/?ticker={ticker}&years=12&fundamental=on"
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")

# Create a folder to save images specific to the ticker
os.makedirs(ticker, exist_ok=True)

# Find all image containers
image_containers = soup.find_all("div", class_="image-container")

# Loop through each image container
for container in image_containers:
    # Get the <h2> text
    h2_tag = container.find("h2")
    if h2_tag:
        image_name = h2_tag.get_text(strip=True)
        # Replace invalid characters in filenames with underscores
        image_name = re.sub(r'[^\w\-_]', '_', image_name)  # Keep only letters, digits, underscores, and hyphens

        # Get the <img> tag
        img_tag = container.find("img")
        if img_tag and img_tag.get('src'):
            image_src = img_tag['src']

            if image_src.startswith('data:image'):  # Base64-encoded image
                # Extract Base64 data
                base64_data = image_src.split(',')[1]
                image_data = base64.b64decode(base64_data)

                # Save the image inside the ticker folder
                with open(f"{ticker}/{image_name}.png", "wb") as f:
                    f.write(image_data)
                print(f"Base64 image saved as {ticker}/{image_name}.png")
            else:
                # Handle regular image URLs
                image_response = requests.get(image_src)
                with open(f"{ticker}/{image_name}.jpg", "wb") as f:
                    f.write(image_response.content)
                print(f"Image saved as {ticker}/{image_name}.jpg")
    else:
        print("No <h2> tag found for an image container.")
