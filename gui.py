import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout, QWidget, QMessageBox
from downloader import MP3Downloader

class DownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MP3 Downloader")
        self.setGeometry(100, 100, 400, 300)

        # Main layout
        self.main_layout = QVBoxLayout()

        # URL Entry
        self.url_label = QLabel("Enter URL:", self)
        self.main_layout.addWidget(self.url_label)

        self.url_entry = QLineEdit(self)
        self.main_layout.addWidget(self.url_entry)

        # Buttons
        self.fetch_button = QPushButton("Fetch MP3 Links", self)
        self.fetch_button.clicked.connect(self.fetch_links)
        self.main_layout.addWidget(self.fetch_button)

        self.size_button = QPushButton("Get Total MP3 Size", self)
        self.size_button.clicked.connect(self.get_total_size)
        self.main_layout.addWidget(self.size_button)

        self.download_button = QPushButton("Download All MP3s", self)
        self.download_button.clicked.connect(self.download_mp3s)
        self.main_layout.addWidget(self.download_button)

        self.clear_button = QPushButton("Clear Status", self)
        self.clear_button.clicked.connect(self.clear_status)
        self.main_layout.addWidget(self.clear_button)

        # Status Label
        self.status_label = QLabel("Status: Waiting for URL", self)
        self.main_layout.addWidget(self.status_label)

        # Main widget and layout
        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # MP3 Downloader instance
        self.downloader = None

    def fetch_links(self):
        url = self.url_entry.text()
        if not url:
            QMessageBox.critical(self, "Error", "Please enter a valid URL.")
            return

        # Disable buttons while fetching
        self.disable_buttons()

        # Run the process in a separate thread to avoid blocking the UI
        threading.Thread(target=self._fetch_links_thread, args=(url,)).start()

    def _fetch_links_thread(self, url):
        try:
            self.downloader = MP3Downloader(url)
            soup = self.downloader.fetch_webpage()
            self.downloader.extract_mp3_links(soup)
            self.status_label.setText("Status: MP3 links fetched.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch MP3 links: {e}")
        finally:
            self.enable_buttons()

    def get_total_size(self):
        if not self.downloader or not self.downloader.mp3_links_dict:
            QMessageBox.critical(self, "Error", "No MP3 links available. Please fetch links first.")
            return

        # Disable buttons while calculating size
        self.disable_buttons()

        # Run the process in a separate thread to avoid blocking the UI
        threading.Thread(target=self._get_total_size_thread).start()

    def _get_total_size_thread(self):
        try:
            total_size_gb = self.downloader.get_total_mp3_size()
            self.status_label.setText(f"Total size: {total_size_gb:.2f} GB")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to calculate total size: {e}")
        finally:
            self.enable_buttons()

    def download_mp3s(self):
        if not self.downloader or not self.downloader.mp3_links_dict:
            QMessageBox.critical(self, "Error", "No MP3 links available. Please fetch links first.")
            return

        # Disable buttons while downloading
        self.disable_buttons()

        # Run the process in a separate thread to avoid blocking the UI
        threading.Thread(target=self._download_mp3s_thread).start()

    def _download_mp3s_thread(self):
        try:
            self.downloader.download_all_mp3s()
            self.status_label.setText("Status: All MP3s downloaded.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download MP3s: {e}")
        finally:
            self.enable_buttons()

    def clear_status(self):
        """Clears the status label."""
        self.status_label.setText("Status: Waiting for URL")

    def disable_buttons(self):
        """Disables buttons to prevent multiple operations at once."""
        self.fetch_button.setEnabled(False)
        self.size_button.setEnabled(False)
        self.download_button.setEnabled(False)

    def enable_buttons(self):
        """Enables buttons after an operation is complete."""
        self.fetch_button.setEnabled(True)
        self.size_button.setEnabled(True)
        self.download_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DownloaderApp()
    window.show()
    sys.exit(app.exec_())
