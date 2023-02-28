import os
import requests
from bs4 import BeautifulSoup
import sys
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


tag = input("Enter tag: ")
url = f"https://konachan.com/post?tags={tag}"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

subfolder_name = "_".join(tag.split("+"))

folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "konachan_images", subfolder_name)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

page_number = 1
downloaded_images = set()


def download_image(image_url):
    image_name = image_url.split("/")[-1]
    image_path = os.path.join(folder_path, image_name)

    if image_name not in downloaded_images:
        with open(image_path, "wb") as f:
            f.write(requests.get(image_url).content)

        downloaded_images.add(image_name)
    else:
        print(f"{image_name} already downloaded. Skipping...")


with ThreadPoolExecutor(max_workers=5) as executor:
    while True:
        response = requests.get(url + "&page=" + str(page_number), headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        image_elements = soup.find_all("a", class_="directlink largeimg")

        if not image_elements:
            break

        image_urls = [image_element["href"] for image_element in image_elements]

        with tqdm(total=len(image_elements), desc=f"Downloading page {page_number}") as progress_bar:
            futures = []
            for image_url in image_urls:
                future = executor.submit(download_image, image_url)
                future.add_done_callback(lambda p: progress_bar.update())
                futures.append(future)
            for future in futures:
                future.result()

        page_number += 1

print(f"\nFinished downloading all images for {subfolder_name}.")
