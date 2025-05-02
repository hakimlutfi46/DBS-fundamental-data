import logging
from utils.load import load
from utils.extract import extract
from utils.transform import transform

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        df_raw = extract()
        if df_raw.empty:
            return

        df_cleaned = transform(df_raw)

        result = load(
            df=df_cleaned,
            db_url="postgresql://developer:12345@localhost:5432/fashiondb",  
            csv_file_path="products.csv",
            spreadsheet_id="1pvsfeNJHMKS-xevuULc2wOAhUICzBNt6hRGG7BlMdZE"
        )              
                
        success_count = sum(result.values())
        total_count = len(result)
        success_rate = (success_count / total_count) * 100

        print("\nRingkasan:")
        print(f"Total operasi    : {total_count}")
        print(f"Berhasil         : {success_count}")
        print(f"Gagal            : {total_count - success_count}")
        print(f"Tingkat sukses   : {success_rate:.1f}%")


        logging.info(f"Load Results: {result}")

    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")

if __name__ == "__main__":
    main()