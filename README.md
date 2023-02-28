# Konachan-scraper

This code will download all images from every page from a single tag you input from the website www.konachan.com

It is writen in Python and it use BeautifulSoup4.

to use just clone this repo, go to the folder with your terminal and run this to install the requirements:
pip install -r requirements.txt

then just run the script, it will request a tag for you to input and will start the download. It creates a folder for every tag you use it.
I've made it to download a single tag and just 5 images in parallel to avoid issues with performance to the website.

please note: Konachan is a booru project website, its tag are used like this in example "fairy_tail", dont use spaces to separate words, it will not work.
