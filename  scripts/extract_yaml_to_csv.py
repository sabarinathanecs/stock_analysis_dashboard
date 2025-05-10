import os
import yaml
import pandas as pd

RAW_DATA_DIR = os.path.join('..', 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join('..', 'data', 'processed')

def extract_all_symbols():
    all_data = {}
    for month_folder in os.listdir(RAW_DATA_DIR):
        month_path = os.path.join(RAW_DATA_DIR, month_folder)
        if not os.path.isdir(month_path):
            continue
        for day_file in os.listdir(month_path):
            if not day_file.endswith('.yaml'):
                continue
            with open(os.path.join(month_path, day_file), 'r') as f:
                day_data = yaml.safe_load(f)
                for symbol, values in day_data.items():
                    if symbol not in all_data:
                        all_data[symbol] = []
                    values['date'] = day_file.replace('.yaml', '')
                    all_data[symbol].append(values)
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    for symbol, records in all_data.items():
        df = pd.DataFrame(records)
        df.to_csv(os.path.join(PROCESSED_DATA_DIR, f"{symbol}.csv"), index=False)

if __name__ == "__main__":
    extract_all_symbols()

