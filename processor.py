import re

TIER_RATES = {
    "VIP": 150.0,
    "PREMIUM": 90.0,
    "GENERAL": 45.0,
}

# ASCII-only patterns (re.ASCII stops other Unicode digits from matching)
_PREFIX_RE = re.compile(r"[A-Za-z0-9]+", re.ASCII)
_DIGITS_RE = re.compile(r"[0-9]{1,6}", re.ASCII)  # also guards against huge numbers

MAX_ROW = 1000
MAX_AGE = 120


def decode_promo_voucher(voucher_code):
    if not isinstance(voucher_code, str):
        return "Invalid voucher: input must be text"
    parts = voucher_code.strip().split('-')
    if len(parts) != 2:
        return "Invalid voucher: expected format PREFIX-PERCENT (e.g. EARLY-20)"
    prefix, pct_str = parts[0].strip(), parts[1].strip()
    if not _PREFIX_RE.fullmatch(prefix):
        return "Invalid voucher: prefix must be letters/digits only"
    if not _DIGITS_RE.fullmatch(pct_str):
        return "Invalid voucher: percentage must be a whole number"
    percentage = int(pct_str)
    if not 0 <= percentage <= 100:
        return "Invalid voucher: percentage must be between 0 and 100"
    return f"Valid {prefix.upper()}: {percentage}% OFF"


def calculate_seat_tier_price(tier_spec):
    """Returns the price as a float, or None if the tier spec is invalid."""
    if not isinstance(tier_spec, str):
        return None
    parts = tier_spec.split('@')
    if len(parts) != 2:
        return None
    tier, row_str = parts[0].strip().upper(), parts[1].strip()
    if tier not in TIER_RATES:
        return None
    if not _DIGITS_RE.fullmatch(row_str):
        return None
    row = int(row_str)
    if row > MAX_ROW:
        return None
    return TIER_RATES[tier] + (row * 2.0)


def parse_attendee_badge(badge_csv):
    if not isinstance(badge_csv, str):
        return "Invalid badge: input must be text"
    tokens = badge_csv.split(',')
    if len(tokens) != 3:
        return "Invalid badge: expected format Name,Age,Seat"
    name, age_str, seat = (t.strip() for t in tokens)
    if not name:
        return "Invalid badge: name is empty"
    if not seat:
        return "Invalid badge: seat is empty"
    if not _DIGITS_RE.fullmatch(age_str):
        return "Invalid badge: age must be a whole number"
    age = int(age_str)
    if age > MAX_AGE:
        return "Invalid badge: age out of range"
    category = "Child" if age < 18 else "Adult"
    return f"{name} [{category}] - Seat {seat}"


def main():
    print("==== Running decode_promo_voucher ====")
    v_input = input("Enter voucher (e.g. EARLY-20): ")
    print("Voucher:", decode_promo_voucher(v_input))

    print("\n==== Running calculate_seat_tier_price ====")
    t_input = input("Enter tier spec (e.g. VIP@4): ")
    price = calculate_seat_tier_price(t_input)
    if price is None:
        print("Seat Price: Invalid tier spec (expected TIER@ROW, tier = VIP/PREMIUM/GENERAL)")
    else:
        print("Seat Price: $", price)

    print("\n==== Running parse_attendee_badge ====")
    b_input = input("Enter badge CSV (Name,Age,Seat): ")
    print("Badge:", parse_attendee_badge(b_input))


if __name__ == "__main__":
    main()