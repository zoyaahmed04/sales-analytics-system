# Handles reading sales data with multiple encodings

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns list of raw transaction lines (strings)
    """

    encodings = ["utf-8", "latin-1", "cp1252"]
    lines = []

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as file:
                for i, line in enumerate(file):
                    line = line.strip()

                    # Skip header row and empty lines
                    if i == 0 or not line:
                        continue

                    lines.append(line)

            # If reading succeeds, break out of loop
            break

        except FileNotFoundError:
            print("Error: File not found.")
            return []

        except UnicodeDecodeError:
            # Try next encoding
            continue

    return lines

