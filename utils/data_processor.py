def parse_transactions(raw_lines):
    """
    Parses raw sales lines into clean list of dictionaries
    """

    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
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

        # Clean product name (remove commas)
        product_name = product_name.replace(",", "")

        try:
            quantity = int(quantity.replace(",", ""))
            unit_price = float(unit_price.replace(",", ""))
        except ValueError:
            continue

        transaction = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        transactions.append(transaction)

    return transactions
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """

    valid_transactions = []
    invalid_count = 0

    regions = set()
    amounts = []

    # First pass: validation
    for tx in transactions:
        try:
            if (
                tx["Quantity"] <= 0
                or tx["UnitPrice"] <= 0
                or not tx["TransactionID"].startswith("T")
                or not tx["ProductID"].startswith("P")
                or not tx["CustomerID"].startswith("C")
                or not tx["Region"]
            ):
                invalid_count += 1
                continue

            amount = tx["Quantity"] * tx["UnitPrice"]
            tx["Amount"] = amount

            regions.add(tx["Region"])
            amounts.append(amount)

            valid_transactions.append(tx)

        except KeyError:
            invalid_count += 1

    # Display filter info
    print("Available regions:", sorted(regions))
    if amounts:
        print("Transaction amount range:", min(amounts), "to", max(amounts))

    filtered = valid_transactions

    # Region filter
    filtered_by_region = 0
    if region:
        before = len(filtered)
        filtered = [tx for tx in filtered if tx["Region"] == region]
        filtered_by_region = before - len(filtered)
        print("After region filter:", len(filtered))

    # Amount filters
    filtered_by_amount = 0
    if min_amount is not None:
        before = len(filtered)
        filtered = [tx for tx in filtered if tx["Amount"] >= min_amount]
        filtered_by_amount += before - len(filtered)

    if max_amount is not None:
        before = len(filtered)
        filtered = [tx for tx in filtered if tx["Amount"] <= max_amount]
        filtered_by_amount += before - len(filtered)

    if min_amount or max_amount:
        print("After amount filter:", len(filtered))

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(filtered)
    }

    return filtered, invalid_count, summary
