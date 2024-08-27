# gui.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
import sys
from downloader import MP3Downloader
import threading

class TextRedirector:
    """
    Redirects output to a tkinter Text widget.
    """
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)  # Auto-scroll to the bottom

    def flush(self):
        pass  # Needed to be compliant with sys.stdout and sys.stderr


class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Downloader")

        # URL Entry
        self.url_label = tk.Label(root, text="Enter URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        # Buttons
        self.fetch_button = tk.Button(root, text="Fetch MP3 Links", command=self.fetch_links)
        self.fetch_button.pack()

        self.size_button = tk.Button(root, text="Get Total MP3 Size", command=self.get_total_size)
        self.size_button.pack()

        self.download_button = tk.Button(root, text="Download All MP3s", command=self.download_mp3s)
        self.download_button.pack()

        # Output Text Box
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=80)
        self.output_text.pack(padx=10, pady=10)

        # Status
        self.status_label = tk.Label(root, text="Status: Waiting for URL", anchor="w")
        self.status_label.pack(fill=tk.X)

        # Redirect stdout and stderr to the Text widget
        sys.stdout = TextRedirector(self.output_text)
        sys.stderr = TextRedirector(self.output_text)

        # MP3 Downloader instance
        self.downloader = None

    def fetch_links(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        # Run the process in a separate thread to avoid blocking the UI
        threading.Thread(target=self._fetch_links_thread, args=(url,)).start()

    def _fetch_links_thread(self, url):
        try:
            self.downloader = MP3Downloader(url)
            soup = self.downloader.fetch_webpage()
            self.downloader.extract_mp3_links(soup)
            self.status_label.config(text="Status: MP3 links fetched.")
            print("MP3 links fetched successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch MP3 links: {e}")
            print(f"Error: {e}")

    def get_total_size(self):
        if not self.downloader or not self.downloader.mp3_links_dict:
            messagebox.showerror("Error", "No MP3 links available. Please fetch links first.")
            return

        # Run the process in a separate thread to avoid blocking the UI
        threading.Thread(target=self._get_total_size_thread).start()

    def _get_total_size_thread(self):
        try:
            total_size_gb = self.downloader.get_total_mp3_size()
            self.status_label.config(text=f"Total size: {total_size_gb:.2f} GB")
            print(f"Total size of all MP3 files: {total_size_gb:.2f} GB")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate total size: {e}")
            print(f"Error: {e}")

    def download_mp3s(self):
        if not self.downloader or not self.downloader.mp3_links_dict:
            messagebox.showerror("Error", "No MP3 links available. Please fetch links first.")
            return

        # Run the process in a separate thread to avoid blocking the UI
        threading.Thread(target=self._download_mp3s_thread).start()

    def _download_mp3s_thread(self):
        try:
            self.downloader.download_all_mp3s()
            self.status_label.config(text="Status: All MP3s downloaded.")
            print("All MP3s downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download MP3s: {e}")
            print(f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
