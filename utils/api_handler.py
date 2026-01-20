import requests


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print("API fetch successful. Products fetched:", len(products))

        cleaned_products = []
        for p in products:
            cleaned_products.append({
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "price": p.get("price"),
                "rating": p.get("rating")
            })

        return cleaned_products

    except Exception as e:
        print("API fetch failed:", e)
        return []

def create_product_mapping(api_products):
    """
    Creates mapping of product ID to product info
    """

    mapping = {}

    for product in api_products:
        pid = product.get("id")
        if pid is not None:
            mapping[pid] = {
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "rating": product.get("rating")
            }

    return mapping

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transactions with API product data
    """

    enriched = []

    for tx in transactions:
        tx_copy = tx.copy()

        # Extract numeric ID from ProductID (P101 -> 101)
        try:
            numeric_id = int("".join(filter(str.isdigit, tx["ProductID"])))
        except:
            numeric_id = None

        if numeric_id in product_mapping:
            api_data = product_mapping[numeric_id]
            tx_copy["API_Category"] = api_data.get("category")
            tx_copy["API_Brand"] = api_data.get("brand")
            tx_copy["API_Rating"] = api_data.get("rating")
            tx_copy["API_Match"] = True
        else:
            tx_copy["API_Category"] = None
            tx_copy["API_Brand"] = None
            tx_copy["API_Rating"] = None
            tx_copy["API_Match"] = False

        enriched.append(tx_copy)

    # Save to file
    output_file = "data/enriched_sales_data.txt"

    if enriched:
        headers = enriched[0].keys()
        with open(output_file, "w") as f:
            f.write("|".join(headers) + "\n")
            for tx in enriched:
                row = [str(tx[h]) for h in headers]
                f.write("|".join(row) + "\n")

    print("Enriched sales data saved to", output_file)

    return enriched
