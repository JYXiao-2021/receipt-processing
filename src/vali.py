import math
import re


class ValidationResult:
    def __init__(self, is_valid, message=""):
        self.is_valid = is_valid
        self.message = message


def is_pattern_valid(pattern, string):
    return bool(re.match(pattern, string))


def is_receipt_input_valid(value, type_):
    return value is not None and isinstance(value, type_)


def validate_receipt(receipt):
    if not is_receipt_input_valid(receipt, dict):
        return ValidationResult(False, "receipt has not correct type")
    retailer_name = receipt.get("retailer")
    purchase_date = receipt.get("purchaseDate")
    purchase_time = receipt.get("purchaseTime")
    receipt_total = receipt.get("total")
    receipt_items = receipt.get("items")

    if not is_receipt_input_valid(retailer_name, str) or not is_pattern_valid(r"^\S+$", retailer_name):
        return ValidationResult(False, "retailer name is not correct")
    if not is_receipt_input_valid(purchase_date, str) or not is_pattern_valid(r"^\d{4}-\d{2}-\d{2}$", purchase_date):
        return ValidationResult(False, "purchase date is not correct")
    if not is_receipt_input_valid(purchase_time, str) or not is_pattern_valid(r"^(?:[01]\d|2[0-3]):[0-5]\d$",
                                                                              purchase_time):
        return ValidationResult(False, "purchase time is not correct")
    if not is_receipt_input_valid(receipt_total, str) or not is_pattern_valid(r"^\d+\.\d{2}$", receipt_total):
        return ValidationResult(False, "receipt total is not correct")
    if (not is_receipt_input_valid(receipt_items, list)) or len(receipt_items) == 0 or (not is_all_items_in_receipt_valid(receipt_items)):
        return ValidationResult(False, "receipt items are not correct")

    return ValidationResult(True)

def is_all_items_in_receipt_valid (items):
    for item in items:

        if not isinstance(item, dict):
            return False

        shortDescription = item.get('shortDescription')
        price = item.get('price')

        if shortDescription is None or price is None:
            return False
        if not isinstance(shortDescription, str) or not is_pattern_valid(r"^[\w\s\-]+$", shortDescription):
            return False
        if not isinstance(price, str) or not is_pattern_valid(r"^\d+\.\d{2}$", price):
            return False
    return True


"""
for the second the part
"""
def get_points_for_retailer_name(receipt):
    points = 0
    retailer_name = receipt.get("retailer")

    if retailer_name is None:
        return points

    for char in retailer_name:
        if char.isalnum():
            points += 1
    return points


def get_purchase_day_points(receipt):
    points = 0
    purchase_date_str = receipt.get("purchaseDate")

    if purchase_date_str is None:
        return points

    purchase_day = int(purchase_date_str[-2:])
    if purchase_day % 2 != 0:
        points += 6
    return points


def get_purchase_hour_points(receipt):
    points = 0
    purchase_time_str = receipt.get("purchaseTime")

    if purchase_time_str is None or len(purchase_time_str) == 0:
        return points

    purchase_hour, purchase_minute = map(int, purchase_time_str.split(':'))

    if (purchase_hour == 14 and purchase_minute > 0) or (15 <= purchase_hour < 16):
        points += 10

    return points


def is_total_multiple_points(receipt):
    points = 0
    total_str = receipt.get("total")

    if total_str is None:
        return points

    total = float(total_str)
    if total % 0.25 == 0:
        points += 25
    return points


def is_total_round_dollar_amount_points(receipt):
    points = 0
    total_str = receipt.get("total")

    if total_str is None:
        return points

    total = float(total_str)
    if total % 1 == 0:
        points += 50
    return points


def get_points_for_items_in_receipt(receipt):
    points = 0
    receipt_items = receipt.get("items")

    if receipt_items is None:
        return points

    pair_receipt_items = len(receipt_items) // 2
    points = pair_receipt_items * 5
    return points


def trimmed_length_item_description_points(receipt):
    points = 0
    receipt_items = receipt.get("items")

    if receipt_items is None:
        return points

    for item in receipt_items:
        description = item.get("shortDescription", "")
        trimmed_description = description.strip()
        price = item.get("price", "0")
        price = float(price)
        if (len(trimmed_description) % 3 == 0 and len(description) > 0):
            points += math.ceil(price * 0.2)

    return points


def get_total_receipt_points(receipt):
    points = 0
    processors = [get_points_for_retailer_name,
                  get_purchase_day_points,
                  get_purchase_hour_points,
                  is_total_multiple_points,
                  is_total_round_dollar_amount_points,
                  get_points_for_items_in_receipt,
                  trimmed_length_item_description_points
                  ]
    for processor in processors:
        points += processor(receipt)

    return points





