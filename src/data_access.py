from pathlib import Path
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def load_housing_data():
    # Download, extract, and load Kaggle housing data.
    api = KaggleApi()
    api.authenticate()  # uses kaggle.json from ~/.kaggle

    data_path = Path.cwd().parent.joinpath('datasets', 'raw')
    data_path.mkdir(parents=True, exist_ok=True)

    train_file = data_path.joinpath("train.csv")
    test_file = data_path.joinpath("test.csv")

    if not train_file.exists():
        api.competition_download_file(
            "house-prices-advanced-regression-techniques",
            "train.csv",
            path=str(data_path)
        )

    if not test_file.exists():
        api.competition_download_file(
            "house-prices-advanced-regression-techniques",
            "test.csv",
            path=str(data_path)
        )

    return pd.read_csv(train_file), pd.read_csv(test_file)
    
    