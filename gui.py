# gui.py
import tkinter as tk
from tkinter import messagebox
from downloader import MP3Downloader


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

        # Status
        self.status_label = tk.Label(root, text="Status: Waiting for URL", anchor="w")
        self.status_label.pack(fill=tk.X)

        # MP3 Downloader instance
        self.downloader = None

    def fetch_links(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        try:
            self.downloader = MP3Downloader(url)
            soup = self.downloader.fetch_webpage()
            self.downloader.extract_mp3_links(soup)
            self.status_label.config(text="Status: MP3 links fetched.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch MP3 links: {e}")

    def get_total_size(self):
        if not self.downloader or not self.downloader.mp3_links_dict:
            messagebox.showerror("Error", "No MP3 links available. Please fetch links first.")
            return

        try:
            total_size_gb = self.downloader.get_total_mp3_size()
            self.status_label.config(text=f"Total size: {total_size_gb:.2f} GB")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate total size: {e}")

    def download_mp3s(self):
        if not self.downloader or not self.downloader.mp3_links_dict:
            messagebox.showerror("Error", "No MP3 links available. Please fetch links first.")
            return

        try:
            self.downloader.download_all_mp3s()
            self.status_label.config(text="Status: All MP3s downloaded.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download MP3s: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
