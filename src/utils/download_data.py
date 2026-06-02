import os
import requests

def download_uci_retail_data(save_dir="data"):
    """
    Downloads the UCI Online Retail dataset and saves it to the specified directory.
    """
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, "Online_Retail.xlsx")
    
    if os.path.exists(file_path):
        print(f"Dataset already exists at {file_path}. Skipping download.")
        return

    print("Downloading dataset from UCI (approx 23MB)... Please wait...")
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status() 
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"Successfully downloaded dataset to {file_path}")
        
    except Exception as e:
        print(f"Error downloading the dataset: {e}")

if __name__ == "__main__":
    download_uci_retail_data()