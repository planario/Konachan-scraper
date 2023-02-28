import os
import requests
from bs4 import BeautifulSoup
import sys
import concurrent.futures

tag = input("Enter tag: ")
url = f"https://konachan.com/post?tags={tag}"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

subfolder_name = "_".join(tag.split("+"))

folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "konachan_images", subfolder_name)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

page_number = 1
downloaded_images = set()

while True:
    response = requests.get(url + "&page=" + str(page_number), headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    image_elements = soup.find_all("a", class_="directlink largeimg")

    if not image_elements:
        break

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for image_element in image_elements:
            image_url = image_element["href"]
            image_name = image_url.split("/")[-1]
            image_path = os.path.join(folder_path, image_name)

            if image_name not in downloaded_images:
                def download_image(image_url, image_path):
                    response = requests.get(image_url, stream=True, headers=headers)
                    with open(image_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)

                executor.submit(download_image, image_url, image_path)

                downloaded_images.add(image_name)
            else:
                print(f"{image_name} already downloaded. Skipping...")

    page_number += 1

    # Calculate progress percentage and print page counter
    progress_percentage = round((page_number / 100) * len(image_elements), 2)
    sys.stdout.write(f"\rDownloading page {page_number} ({progress_percentage}%).")
    sys.stdout.flush()

print(f"\nFinished downloading all images for {subfolder_name}.")
