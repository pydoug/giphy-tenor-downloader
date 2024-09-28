import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_gif(url, path):
    try:
        gif_response = requests.get(url)
        gif_response.raise_for_status()
        with open(path, "wb") as f:
            f.write(gif_response.content)
        print(f"GIF saved at {path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading GIF from {url}: {e}")

def scrape_and_download_stickers(search_query, num_stickers=50):
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    url = f"https://tenor.com/pt-BR/search/{search_query}-stickers"
    driver.get(url)
    time.sleep(3)

    stickers = set()
    while len(stickers) < num_stickers:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sticker_container = soup.select_one('div#root div div:nth-of-type(3) div div div:nth-of-type(2)')
        if sticker_container:
            sticker_images = sticker_container.find_all('img')
            for img in sticker_images:
                stickers.add(img['src'])
                if len(stickers) >= num_stickers:
                    break
        else:
            print("Couldn't find the sticker container.")
            break

        if len(stickers) < num_stickers:
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(3)

    driver.quit()

    stickers = list(stickers)[:num_stickers]

    base_dir = search_query
    stickers_dir = os.path.join(base_dir, 'Stickers')
    os.makedirs(stickers_dir, exist_ok=True)

    for i, sticker_url in enumerate(stickers):
        full_sticker_url = urljoin(url, sticker_url)
        sticker_data = requests.get(full_sticker_url).content
        sticker_extension = os.path.splitext(full_sticker_url)[1]
        sticker_filename = os.path.join(stickers_dir, f"sticker_{i + 1}{sticker_extension}")

        with open(sticker_filename, 'wb') as sticker_file:
            sticker_file.write(sticker_data)
        print(f"Downloaded {sticker_filename}")

if __name__ == "__main__":
    print("1. Download GIFs from Giphy")
    print("2. Download Stickers from Tenor")
    choice = input("Choose an option (1 or 2): ")

    if choice == '1':
        search_term = input("Enter the search term for the GIFs: ")
        quantity = int(input("Enter the number of GIFs to download: "))
        api_key = input("Enter your Giphy API key: ")
        search_url = f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={search_term}&limit={quantity}"

        try:
            response = requests.get(search_url)
            response.raise_for_status()
            print(f"Successfully accessed API: {search_url}")
        except requests.exceptions.RequestException as e:
            print(f"Error accessing the search API: {e}")
            exit()

        data = response.json().get('data', [])
        if not data:
            print("No GIFs found.")
            exit()

        gif_links = [gif['images']['original_mp4']['mp4'] for gif in data]
        print(f"{len(gif_links)} GIFs found. Downloading the first {quantity}...")

        if not os.path.exists("giphy"):
            os.makedirs("giphy")

        for i, link in enumerate(gif_links):
            gif_path = f"giphy/gif_{i+1}.mp4"
            print(f"Downloading GIF {i+1}: {link}")
            download_gif(link, gif_path)

        print(f"Download of the first {quantity} GIFs completed!")

    elif choice == '2':
        search_query = input("Enter the search term for stickers: ")
        num_stickers = int(input("How many stickers do you want to capture? (up to 50): "))
        scrape_and_download_stickers(search_query, num_stickers)

    else:
        print("Invalid option. Please select either 1 or 2.")
