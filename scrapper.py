import requests
import bs4
import base64

# First get the request
url = "https://geraldineweiss.onrender.com/?ticker=JNJ&years=12&fundamental=on"
res = requests.get(url)
# Create a soup from request
soup = bs4.BeautifulSoup(res.text,"lxml")

# Grab one image
image_container = soup.find("div", class_="image-container")
if image_container:
    img_tag = image_container.find("img")
    if img_tag and img_tag.get('src'):
        image_src = img_tag['src']

        # It seems we're dealing with Base64-encoded images
        if image_src.startswith('data:image'):
            # Extract Base64 data
            base64_data = image_src.split(',')[1]
            image_data = base64.b64decode(base64_data)
        
        # Download image        
            with open ("downloaded_image.jpg","wb") as f:
                f.write(image_data)
            print("Base64 image successfully downloaded.")
        else:
            # Handle regular image URLs (in case they exist)
            image_response = requests.get(image_src)
            with open("downloaded_image.jpg", "wb") as f:
                f.write(image_response.content)
            print("Image successfully downloaded and saved as downloaded_image.jpg")
else:
    print("No .image-container or image found.")