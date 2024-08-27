import requests
from bs4 import BeautifulSoup

class MP3Downloader:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.mp3_links_dict = {}

    def fetch_webpage(self):
        """
        Fetches the HTML content of the webpage.
        """
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')
        else:
            raise Exception(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    def extract_mp3_links(self, soup):
        """
        Extracts the titles and .mp3 links from the webpage.
        """
        title_elements = soup.find_all(class_="prch-title")

        for title_element in title_elements:
            # Get the title text and sanitize it for a valid filename
            mp3_title = title_element.get_text(strip=True).replace(' ', '_')

            # Find the closest .mp3 link after the title
            mp3_link = title_element.find_next('a', href=True)

            if mp3_link and mp3_link['href'].endswith('.mp3'):
                mp3_url = mp3_link['href']

                # Ensure the link is an absolute URL
                if not mp3_url.startswith('http'):
                    mp3_url = self.url.rsplit('/', 1)[0] + '/' + mp3_url

                # Store the title and mp3 URL in the dictionary
                self.mp3_links_dict[mp3_title] = mp3_url

    def download_mp3(self, title, mp3_url):
        """
        Downloads an mp3 file from a given URL and saves it with the provided title.
        Also prints the size of the file before downloading.
        """
        try:
            # Make a HEAD request to get the file size before downloading
            head_response = requests.head(mp3_url, headers=self.headers)
            if head_response.status_code == 200:
                # Get the Content-Length header
                content_length = head_response.headers.get('Content-Length')
                if content_length:
                    # Convert the file size to MB
                    file_size_mb = int(content_length) / (1024 * 1024)
                    print(f"Downloading '{title}' - File size: {file_size_mb:.2f} MB")
            else:
                print(f"Failed to retrieve file size for {mp3_url}. Status code: {head_response.status_code}")

            # Proceed to download the file
            mp3_response = requests.get(mp3_url, headers=self.headers)
            if mp3_response.status_code == 200:
                filename = f"{title}.mp3"
                with open(filename, 'wb') as f:
                    f.write(mp3_response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download the mp3 file from {mp3_url}. Status code: {mp3_response.status_code}")
        except Exception as e:
            print(f"An error occurred while downloading {mp3_url}: {e}")

    def download_all_mp3s(self):
        """
        Downloads all the mp3 files found on the webpage.
        """
        for title, mp3_url in self.mp3_links_dict.items():
            self.download_mp3(title, mp3_url)

    def get_total_mp3_size(self):
        """
        Gets the total size of all the mp3 files without downloading them.
        Prints the iterator and total size in GB at each iteration.
        """
        total_size = 0
        iterator = 0

        for title, mp3_url in self.mp3_links_dict.items():
            iterator += 1  # Increment the iterator for each loop

            try:
                # Make a HEAD request to get the file size
                head_response = requests.head(mp3_url, headers=self.headers)
                if head_response.status_code == 200:
                    # Get the Content-Length header
                    content_length = head_response.headers.get('Content-Length')
                    if content_length:
                        total_size += int(content_length)
                else:
                    print(f"Failed to retrieve HEAD info for {mp3_url}. Status code: {head_response.status_code}")
            except Exception as e:
                print(f"An error occurred while retrieving HEAD info for {mp3_url}: {e}")

            # Convert size to GB for readability and print the current state
            total_size_gb = total_size / (1024 * 1024 * 1024)
            print(f"Iteration {iterator}: Total size so far: {total_size_gb:.6f} GB")

        return total_size_gb  # Return total size in GB

    def run(self):
        """
        Runs the full mp3 downloading process.
        """
        try:
            # Step 1: Fetch the webpage
            soup = self.fetch_webpage()

            # Step 2: Extract mp3 links and titles
            self.extract_mp3_links(soup)

            # Step 3: Download all the mp3 files
            self.download_all_mp3s()

        except Exception as e:
            print(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    url = 'https://www.faithfulwordbaptist.org/page5.html'
    downloader = MP3Downloader(url)

    # Fetch the webpage and extract the mp3 links
    soup = downloader.fetch_webpage()
    downloader.extract_mp3_links(soup)

    # Calculate the total size of the mp3 files
    total_size_mb = downloader.get_total_mp3_size()
    print(f"Total size of all mp3 files: {total_size_mb:.2f} MB")

    # Run the downloader to download all mp3s
    # downloader.run()  # Uncomment this line to download all mp3s
