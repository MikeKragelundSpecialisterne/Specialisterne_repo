from Downloader import Downloader
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import os 
import polars as pl

WORKERS = 10
FILES = 100
    
class FileHandler:
    def __init__(self, file_path_gri, destination_folder, output_folder):
        self.file_path_gri = file_path_gri
        self.downloader = Downloader(destination_folder)
        self.success_list = []
        self.output_folder = output_folder
    
    def start_download(self):
    # Reading URLs from the GRI Excel file
        #df = pd.read_excel(self.file_path_gri)
        df = pl.read_excel(self.file_path_gri, columns=["BRnum", "Pdf_URL", "Report Html Address"])
    
        print(df.head())  # Debug: Print the first few rows to ensure data is being read correctly
        urls = []
        count = 0
        for row in df.rows(named=True):
            if count == FILES:
                break
            primary_url = row['Pdf_URL']
            secondary_url = row['Report Html Address']
            filename = f"{row['BRnum']}.pdf"
            count += 1
            if primary_url:
                urls.append((primary_url, filename))
            else: 
                urls.append((secondary_url, filename))
        
        log_list = []
        with ThreadPoolExecutor(max_workers=WORKERS) as executor:  
            future_to_url = {executor.submit(self.downloader.download, url, filename): (url, filename) for url, filename in urls}
            
            for future in as_completed(future_to_url):
                url, filename = future_to_url[future]
                try:
                    success = future.result()
                    log_list.append({"BRNum": filename.split('.')[0], "Download_Status": 'Downloadet' if success else 'Ikke downloadet'})
                except Exception as exc:
                    print(f"Error downloading {url}: {exc}")
                    log_list.append({"BRNum": filename.split('.')[0], "Download_Status": 'Ikke downloadet'})

        self.write_downloaded_files(log_list)
        
    def write_downloaded_files(self, log_list):
        # Sort the log list by BRNum before writing to Excel
        sorted_log_list = sorted(log_list, key=lambda x: x["BRNum"])
        output_path = os.path.join(self.output_folder, "downloaded_files.xlsx")
        df = pd.DataFrame(sorted_log_list)
        df.to_excel(output_path, index=False)
        print(f"List of downloaded files written to {output_path}")