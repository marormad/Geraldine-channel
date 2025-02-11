import requests
from bs4 import BeautifulSoup
import base64
import os
import re
import time

# Ticker list
ticker_list = ["MCD", "MMM", "TFC", "MO", "JNJ", "VZ", "HRL", "O", "ADP", "A3M.MC", "RKT.L", "BRBY.L", "MDLZ", "HSY", "KO", "PEP", "NKE", "UPS", "LYB", "KHC", "ABBV", "CWT", "PG", "CL", "ABT", "WMT"]

# Loop to get and download the images from every ticker in the list
for ticker in ticker_list:

    # Check if the folder for the ticker already exists
    if os.path.exists(ticker):
        print(f"{ticker} already exists, skipping.")
        continue

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

                # Check if the src is a Base64-encoded image
                if image_src.startswith('data:image'):  # Base64-encoded image
                    # Extract Base64 data
                    base64_data = image_src.split(',')[1]
                    image_data = base64.b64decode(base64_data)

                    # Save the Base64 image
                    with open(f"{ticker}/{image_name}.png", "wb") as f:
                        f.write(image_data)
                    print(f"Base64 image saved as {ticker}/{image_name}.png")
                else:
                    try:
                        # Handle regular image URLs (check if it's a valid URL)
                        image_response = requests.get(image_src)
                        image_response.raise_for_status()  # This will raise an exception for invalid responses

                        with open(f"{ticker}/{image_name}.jpg", "wb") as f:
                            f.write(image_response.content)
                        print(f"Image saved as {ticker}/{image_name}.jpg")
                    except requests.exceptions.RequestException as e:
                        # Print the error message if the request fails
                        print(f"Error downloading image for {ticker}/{image_name}: {e}")
        else:
            print(f"No <h2> tag found for an image container in {ticker}.")
    
    # Wait for a while to be sure every images was successfully downloaded until continuing with next ticker
    time.sleep(30)
    print("30 seconds have passed, looking for next ticker...")

