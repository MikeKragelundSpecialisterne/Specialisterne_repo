import os 
import requests

class RequestHandler:
    _instance = None

    def __new__(cls, destination_folder):
        if cls._instance is None:
            cls._instance = super(RequestHandler, cls).__new__(cls)
            cls._instance.destination_folder = destination_folder
            cls._instance.success_list = []
        return cls._instance

    def download(self, url, destination_filename):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(os.path.join(self.destination_folder, destination_filename), 'wb') as file:
                    file.write(response.content)
                print(f"Download successful: {destination_filename}")
                return True
            else:
                print(f"Failed to download: {destination_filename}")
                return False
        except requests.RequestException as e:
            print(f"Error downloading {url}: {e}")
            return False

    def to_aws(self, success_list):
        # Placeholder for AWS uploading logic
        print("Uploading to AWS...")
        for filename in success_list:
            print(f"Uploaded {filename} to AWS")