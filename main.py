from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)


def main():
    # Part 1: Read & clean
    raw_lines = read_sales_data("data/sales_data.txt")
    parsed = parse_transactions(raw_lines)
    valid_tx, _, _ = validate_and_filter(parsed)

    # Part 3: API integration
    api_products = fetch_all_products()
    product_mapping = create_product_mapping(api_products)

    enriched_transactions = enrich_sales_data(valid_tx, product_mapping)

    print("Total enriched transactions:", len(enriched_transactions))


if __name__ == "__main__":
    main()
