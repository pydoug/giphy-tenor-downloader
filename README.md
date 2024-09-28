# Giphy and Tenor GIF and Sticker Downloader

This is a Python script that allows you to download GIFs from both Giphy and Tenor, as well as stickers from Tenor. The script also provides an option to convert downloaded GIFs into MP4 format using the `moviepy` library.

## Features

- **Download GIFs from Giphy**: Search and download GIFs directly from Giphy using the Giphy API.
- **Download GIFs from Tenor**: Scrape and download GIFs from Tenor based on a search query.
- **Download Stickers from Tenor**: Scrape and download stickers from Tenor.
- **Convert GIFs to MP4**: Automatically convert GIFs downloaded from Tenor to MP4 format for better compatibility.
- **Automatic folder organization**: GIFs, MP4s, and stickers are saved in separate folders based on your search queries.

## Requirements

- **Python 3.x** or higher
- **Libraries**:
  - `requests`
  - `beautifulsoup4`
  - `selenium`
  - `webdriver-manager`
  - `moviepy`
  - `bs4`

To install the required libraries, run the following command:

```bash
pip install requests beautifulsoup4 selenium webdriver-manager moviepy
```

## How to Use

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pydoug/giphy-tenor-downloader.git
   cd giphy-tenor-downloader
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Get a Giphy API key**:
   - Visit the [Giphy Developers page](https://developers.giphy.com/).
   - Sign up and get your API key.
   - You will need this API key to download GIFs from Giphy.

4. **Run the script**:
   ```bash
   python media_downloader.py
   ```

5. **Choose an option**: Once the script is running, you'll be prompted to choose between downloading GIFs or stickers.
   - **Option 1**: Download GIFs from Giphy.
   - **Option 2**: Download GIFs from Tenor and convert them to MP4.
   - **Option 3**: Download stickers from Tenor.

### Example

When running the script, you'll see the following prompts:

```bash
1. Download GIFs from Giphy
2. Download GIFs from Tenor
3. Download Stickers from Tenor
Choose an option (1, 2, or 3): 1
Enter the search term for the GIFs: cat
Enter the number of GIFs to download: 5
Enter your Giphy API key: YOUR_API_KEY_HERE
```

The script will then:
- **For Giphy GIFs**: Fetch and download the specified number of GIFs based on the search query from Giphy.
- **For Tenor GIFs**: Scrape the specified number of GIFs from Tenor, save them in `.gif` format, and convert them to `.mp4`.
- **For Tenor Stickers**: Scrape and download the specified number of stickers in `.png` or `.gif` format.

### Folder Structure

After running the script, the downloaded files will be organized in folders like this:

```
giphy-tenor-downloader/
│
└───cat/
    ├───Giphy/
    │   ├── gif_1.gif
    │   ├── gif_2.gif
    │   └── ...
    ├───Tenor_Gifs/
    │   ├── gif_1.gif
    │   ├── gif_2.gif
    │   └── ...
    ├───Mp4/
    │   ├── gif_1.mp4
    │   ├── gif_2.mp4
    │   └── ...
    └───Stickers/
        ├── sticker_1.png
        ├── sticker_2.png
        └── ...
```

### Functionality Summary

1. **Giphy GIF Download**:
   - Fetches GIFs directly from Giphy using the API.
   - Requires you to provide your Giphy API key.
   
2. **Tenor GIF Download and Conversion**:
   - Scrapes GIFs from Tenor, downloads them, and converts them into MP4 format for better compatibility.

3. **Tenor Sticker Download**:
   - Scrapes stickers from Tenor based on the search query and downloads them in `.png` or `.gif` format.

### Notes

- **Selenium**: The script uses Selenium for scraping Tenor, so you must have Google Chrome installed. The `webdriver-manager` library will handle the installation of the appropriate version of the Chrome WebDriver.
- **Moviepy**: Used for converting Tenor GIFs to MP4 format, ensuring greater compatibility with modern video players.
- **Giphy API**: To download GIFs from Giphy, you will need to sign up for an API key from [Giphy Developers](https://developers.giphy.com/).

## License

This project is licensed under the MIT License.
