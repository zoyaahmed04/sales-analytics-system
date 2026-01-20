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

def calculate_total_revenue(transactions):
    total = 0.0
    for tx in transactions:
        total += tx["Quantity"] * tx["UnitPrice"]
    return total

def region_wise_sales(transactions):
    region_data = {}
    total_revenue = calculate_total_revenue(transactions)

    for tx in transactions:
        region = tx["Region"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += amount
        region_data[region]["transaction_count"] += 1

    # Calculate percentages
    for region in region_data:
        region_data[region]["percentage"] = round(
            (region_data[region]["total_sales"] / total_revenue) * 100, 2
        )

    # Sort by total_sales descending
    sorted_regions = dict(
        sorted(region_data.items(),
               key=lambda x: x[1]["total_sales"],
               reverse=True)
    )

    return sorted_regions

def top_selling_products(transactions, n=5):
    product_data = {}

    for tx in transactions:
        product = tx["ProductName"]
        qty = tx["Quantity"]
        amount = qty * tx["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += qty
        product_data[product]["revenue"] += amount

    result = []
    for product, data in product_data.items():
        result.append((product, data["quantity"], data["revenue"]))

    # Sort by quantity sold descending
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]

def customer_analysis(transactions):
    customer_data = {}

    for tx in transactions:
        cid = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        product = tx["ProductName"]

        if cid not in customer_data:
            customer_data[cid] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customer_data[cid]["total_spent"] += amount
        customer_data[cid]["purchase_count"] += 1
        customer_data[cid]["products_bought"].add(product)

    # Final formatting
    for cid in customer_data:
        total = customer_data[cid]["total_spent"]
        count = customer_data[cid]["purchase_count"]

        customer_data[cid]["avg_order_value"] = round(total / count, 2)
        customer_data[cid]["products_bought"] = list(
            customer_data[cid]["products_bought"]
        )

    # Sort by total_spent descending
    sorted_customers = dict(
        sorted(customer_data.items(),
               key=lambda x: x[1]["total_spent"],
               reverse=True)
    )

    return sorted_customers

def daily_sales_trend(transactions):
    daily_data = {}

    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        customer = tx["CustomerID"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily_data[date]["revenue"] += amount
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(customer)

    # Format output
    result = {}
    for date in sorted(daily_data.keys()):
        result[date] = {
            "revenue": daily_data[date]["revenue"],
            "transaction_count": daily_data[date]["transaction_count"],
            "unique_customers": len(daily_data[date]["customers"])
        }

    return result

def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)

    peak_date = None
    max_revenue = 0
    tx_count = 0

    for date, data in daily.items():
        if data["revenue"] > max_revenue:
            max_revenue = data["revenue"]
            peak_date = date
            tx_count = data["transaction_count"]

    return (peak_date, max_revenue, tx_count)

def low_performing_products(transactions, threshold=10):
    product_data = {}

    for tx in transactions:
        product = tx["ProductName"]
        qty = tx["Quantity"]
        amount = qty * tx["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += qty
        product_data[product]["revenue"] += amount

    result = []
    for product, data in product_data.items():
        if data["quantity"] < threshold:
            result.append((product, data["quantity"], data["revenue"]))

    # Sort by quantity ascending
    result.sort(key=lambda x: x[1])

    return result

