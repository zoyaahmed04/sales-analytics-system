# Main entry point for the Sales Analytics System

from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    generate_sales_report
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)


def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # [1/10] Read data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # [2/10] Parse data
        print("\n[2/10] Parsing and cleaning data...")
        parsed_transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_transactions)} records")

        # [3/10] Display filter options
        regions = sorted(set(tx["Region"] for tx in parsed_transactions if tx["Region"]))
        amounts = [
            tx["Quantity"] * tx["UnitPrice"]
            for tx in parsed_transactions
            if tx["Quantity"] > 0 and tx["UnitPrice"] > 0
        ]

        print("\n[3/10] Filter Options Available:")
        print("Regions:", ", ".join(regions))
        if amounts:
            print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        choice = input("Do you want to filter data? (y/n): ").strip().lower()

        region_filter = None
        min_amount = None
        max_amount = None

        if choice == "y":
            region_filter = input("Enter region (or press Enter to skip): ").strip()
            min_input = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_input = input("Enter maximum amount (or press Enter to skip): ").strip()

            if min_input:
                min_amount = float(min_input)
            if max_input:
                max_amount = float(max_input)

        # [4/10] Validate transactions
        print("\n[4/10] Validating transactions...")
        valid_tx, invalid_count, summary = validate_and_filter(
            parsed_transactions,
            region=region_filter if region_filter else None,
            min_amount=min_amount,
            max_amount=max_amount
        )
        print(f"✓ Valid: {len(valid_tx)} | Invalid: {invalid_count}")

        # [5/10] Perform analyses
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_tx)
        region_wise_sales(valid_tx)
        top_selling_products(valid_tx)
        customer_analysis(valid_tx)
        daily_sales_trend(valid_tx)
        find_peak_sales_day(valid_tx)
        low_performing_products(valid_tx)
        print("✓ Analysis complete")

        # [6/10] Fetch API data
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)
        print(f"✓ Fetched {len(api_products)} products")

        # [7/10] Enrich sales data
        print("\n[7/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_tx, product_mapping)
        enriched_count = sum(1 for tx in enriched_transactions if tx.get("API_Match"))
        print(
            f"✓ Enriched {enriched_count}/{len(valid_tx)} transactions "
            f"({(enriched_count / len(valid_tx) * 100) if valid_tx else 0:.1f}%)"
        )

        # [8/10] Save enriched data
        print("\n[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt")

        # [9/10] Generate report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_tx, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt")

        # [10/10] Complete
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ An error occurred:")
        print(e)
        print("Please check input files or try again.")


if __name__ == "__main__":
    main()

