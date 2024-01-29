# Reddit-Scraper
Scrape your favorite subreddits and download the content for use in machine learning or mass backup applications. An example of such an application might be if you needed to train a machine vision system to detect guitars, you could bulk download from [r/guitars](https://www.reddit.com/r/guitars/) and have more guitar pictures than you could ever want. Then, you could pull a bunch of images from [r/drums](https://www.reddit.com/r/drums/) and you'd have a bunch of relevant negative images to use in your model.

## Features

- **Subreddit Specific Scraping:** Targets individual subreddits and extracts image links.
- **Automated Browser Navigation:** Uses headless Chrome to navigate pages and simulate user actions.
- **Download Management:** Images are downloaded and saved locally, with existing files in the target directory skipped to avoid duplicates.
- **Multiprocessing Support:** Leverages Python's multiprocessing capabilities to parallelize the scraping process, improving efficiency.

## Requirements

- Python 3.x
- `undetected_chromedriver` package
- `multiprocessing` package
- `re` (regular expressions) package
- Chrome browser installed on the system

## Setup and Configuration

Before running the script, ensure you have the required packages installed. You can install the necessary packages using pip:

shell

`pip install undetected_chromedriver`

Also, make sure that Chrome is installed on your system as the script utilizes Chrome for web scraping.

### Folder Structure

Create a directory where the images will be saved. The default path used in the script is `/media/sf_redDrive/reddit/`. If you wish to use a different path, update the `dest` variable accordingly.

### Subreddit List

Prepare a file named `toSearch` containing a list of subreddits you want to scrape. Each subreddit should be on a new line. Lines starting with `#` will be ignored, allowing for comments or temporary disabling of certain subreddits.

## Usage

To run the script, simply execute it with Python:

shell

`python reddit_scraper.py`

The script will perform the following steps:

1. Read the list of subreddits from the `toSearch` file.
2. Create a directory for each subreddit if it doesn't already exist.
3. Initialize multiprocessing with the specified number of cores.
4. Open browser instances for each subreddit and scrape image links.
5. Download images to the respective subreddit directories.
6. After scraping, all Chrome instances will be terminated.

## Notes

- The script uses headless Chrome to avoid opening actual browser windows.
- Images are saved using the title extracted from the subreddit post.
- Existing images are skipped to prevent downloading duplicates.
- The number of cores for multiprocessing is set by the `MAX_SEARCH_CPU_CORES` variable.

## Disclaimer

Ensure you have the right to scrape and download images from the specific subreddits. Respect the terms of service of Reddit and the privacy and copyright of image owners.
