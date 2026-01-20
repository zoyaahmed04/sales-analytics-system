def clean_sales_data(raw_records):
    valid_records = []
    invalid_count = 0

    for index, record in enumerate(raw_records):
        # Skip header row
        if index == 0:
            continue

        parts = record.split("|")

        # Must have exactly 8 fields
        if len(parts) != 8:
            invalid_count += 1
            continue

        (
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ) = parts

        # Validation rules
        if not customer_id or not region:
            invalid_count += 1
            continue

        if not transaction_id.startswith("T"):
            invalid_count += 1
            continue

        # Clean product name (remove commas)
        product_name = product_name.replace(",", "")

        try:
            quantity = int(quantity.replace(",", ""))
            unit_price = float(unit_price.replace(",", ""))
        except:
            invalid_count += 1
            continue

        if quantity <= 0 or unit_price <= 0:
            invalid_count += 1
            continue

        valid_records.append([
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ])

    print("Total records parsed:", len(raw_records) - 1)
    print("Invalid records removed:", invalid_count)
    print("Valid records after cleaning:", len(valid_records))

    return valid_records

