from utils.file_handler import read_sales_file
from utils.data_processor import clean_sales_data
from utils.api_handler import fetch_product_info


def main():
    # Read raw sales data
    raw_data = read_sales_file("data/sales_data.txt")

    # Clean and validate data
    cleaned_data = clean_sales_data(raw_data)

    # Example API usage (demo purpose)
    if cleaned_data:
        sample_product = cleaned_data[0][3]
        info = fetch_product_info(sample_product)
        print("Sample product info:", info)

    # Write cleaned output to file
    with open("output/cleaned_sales.txt", "w") as f:
        for row in cleaned_data:
            f.write("|".join(map(str, row)) + "\n")


if __name__ == "__main__":
    main()

