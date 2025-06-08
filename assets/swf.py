# Sample Products (Indexed from 0 to 7)
products = [
    {"brand": "Samsung", "ram": "6GB"},
    {"brand": "Apple", "ram": "4GB"},
    {"brand": "Samsung", "ram": "6GB"},
    {"brand": "Xiaomi", "ram": "6GB"},
    {"brand": "Apple", "ram": "8GB"},
    {"brand": "Samsung", "ram": "4GB"},
    {"brand": "Samsung", "ram": "8GB"},
    {"brand": "OnePlus", "ram": "6GB"},
]

# Step 1: Build Inverted Index (attribute value → list of product IDs)
from collections import defaultdict

inverted_index = defaultdict(list)
for i, product in enumerate(products):
    for attr, value in product.items():
        key = f"{attr}:{value}"
        inverted_index[key].append(i)

# Step 2: Build Bitmaps from Inverted Index
def create_bitmap(product_count, id_list):
    bitmap = [0] * product_count
    for idx in id_list:
        bitmap[idx] = 1
    return bitmap

n = len(products)
bitmaps = {key: create_bitmap(n, ids) for key, ids in inverted_index.items()}

# Step 3: Filter Operation (AND logic)
def and_filter(bitmap1, bitmap2):
    return [b1 & b2 for b1, b2 in zip(bitmap1, bitmap2)]

# Example Query: Brand = Samsung AND RAM = 6GB
bm1 = bitmaps["brand:Samsung"]
bm2 = bitmaps["ram:6GB"]
result_bitmap = and_filter(bm1, bm2)

# Step 4: Retrieve matching product indices
matching_ids = [i for i, val in enumerate(result_bitmap) if val == 1]
print("Matching Product IDs:", matching_ids)
