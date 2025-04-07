import re


# Validate Israeli ID
def is_valid_id(id) -> bool:
    if not id.isdigit() or len(id) > 9 or len(id) < 5:
        return False
    id = id.zfill(9)
    total_sum = 0
    for idx, digit in enumerate(id):
        # Multiplying the digit times 1 or 2, depends if it's even or not.
        # Related to the Israeli id calculation formula.
        result = int(digit) * (idx % 2 + 1)
        if result > 9:
            result -= 9
        total_sum += result
    return total_sum % 10 == 0


# Validate Israeli phone number
def is_valid_phone(p) -> bool:
    return bool(re.match(r"^(?:\+972|0)\d{8,9}$", p))
