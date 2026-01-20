from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, validate_and_filter


def main():
    raw_lines = read_sales_data("data/sales_data.txt")
    transactions = parse_transactions(raw_lines)

    valid_tx, invalid_count, summary = validate_and_filter(
        transactions,
        region=None,
        min_amount=None,
        max_amount=None
    )

    print("Summary:", summary)

    # Write cleaned data
    with open("output/cleaned_sales.txt", "w") as f:
        for tx in valid_tx:
            f.write(str(tx) + "\n")


if __name__ == "__main__":
    main()
