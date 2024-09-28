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
from moviepy.editor import VideoFileClip

def scrape_and_download_gifs(search_query, num_gifs):
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    url = f"https://tenor.com/pt-BR/search/{search_query}-gifs"
    driver.get(url)

    gifs = set()
    while len(gifs) < num_gifs:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2) 

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        gif_container = soup.select_one('div#root div div:nth-of-type(3) div div div:nth-of-type(4)')
        if gif_container:
            gif_images = gif_container.find_all('img')
            for img in gif_images:
                gifs.add(img['src'])
                if len(gifs) >= num_gifs:
                    break

    driver.quit()

    gifs = list(gifs)[:num_gifs] 
    
    base_dir = search_query
    gifs_dir = os.path.join(base_dir, 'Gifs')
    mp4_dir = os.path.join(base_dir, 'Mp4')

    os.makedirs(gifs_dir, exist_ok=True)
    os.makedirs(mp4_dir, exist_ok=True)

    # Baixa cada GIF e converte para MP4
    for i, gif_url in enumerate(gifs):
        full_gif_url = urljoin(url, gif_url)
        gif_data = requests.get(full_gif_url).content
        
        gif_filename = os.path.join(gifs_dir, f"gif_{i + 1}.gif")
        mp4_filename = os.path.join(mp4_dir, f"gif_{i + 1}.mp4")
        
        # Salva o GIF
        with open(gif_filename, 'wb') as gif_file:
            gif_file.write(gif_data)
        print(f"Downloaded {gif_filename}")
        
        # Converte o GIF para MP4
        try:
            clip = VideoFileClip(gif_filename)
            clip.write_videofile(mp4_filename, codec='libx264')
            print(f"Converted {gif_filename} to {mp4_filename}")
        except Exception as e:
            print(f"Failed to convert {gif_filename} to MP4: {e}")


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
    print("1. Download GIFs from Tenor")
    print("2. Download Stickers from Tenor")
    choice = input("Choose an option (1 or 2): ")

    if choice == '1':
        search_query = input("Enter the search term for the GIFs: ")
        num_gifs = int(input("How many GIFs do you want to capture? "))
        scrape_and_download_gifs(search_query, num_gifs)

    elif choice == '2':
        search_query = input("Enter the search term for stickers: ")
        num_stickers = int(input("How many stickers do you want to capture? (up to 50): "))
        scrape_and_download_stickers(search_query, num_stickers)

    else:
        print("Invalid option. Please select either 1 or 2.")
