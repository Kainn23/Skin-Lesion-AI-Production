import os
import pandas as pd
import kagglehub

class HAM10000DatasetInfo:
    def __init__(self):
        pass

    def load(self) -> pd.DataFrame:
        """
        Downloads the dataset if not present, and returns a dataframe containing the metadata
        along with an 'image_path' column for each image.
        """
        print("Downloading or locating HAM10000 dataset...")
        path = kagglehub.dataset_download("kmader/skin-cancer-mnist-ham10000")
        csv_path = os.path.join(path, "HAM10000_metadata.csv")
        
        df = pd.read_csv(csv_path)
        
        def get_image_path(image_id):
            p1 = os.path.join(path, "HAM10000_images_part_1", f"{image_id}.jpg")
            if os.path.exists(p1):
                return p1
            p2 = os.path.join(path, "HAM10000_images_part_2", f"{image_id}.jpg")
            if os.path.exists(p2):
                return p2
            # Check if images are just in the root dir
            p_root = os.path.join(path, f"{image_id}.jpg")
            if os.path.exists(p_root):
                return p_root
            return p1 # Fallback
            
        df['image_path'] = df['image_id'].apply(get_image_path)
        return df
