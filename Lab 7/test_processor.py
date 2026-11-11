from hypothesis import given, strategies as st
from processor import decode_promo_voucher, calculate_seat_tier_price, parse_attendee_badge


@given(st.text() | st.none())
def test_decode_promo_voucher_no_crash(s):
    try:
        result = decode_promo_voucher(s)
    except Exception as e:
        assert False, f"decode_promo_voucher crashed with: {e!r} on input {s!r}"
    assert isinstance(result, str)


@given(st.text() | st.none())
def test_calculate_seat_tier_price_safe(s):
    try:
        result = calculate_seat_tier_price(s)
    except Exception as e:
        assert False, f"calculate_seat_tier_price crashed with: {e!r} on input {s!r}"
    # valid input -> non-negative float, invalid input -> None
    assert result is None or (isinstance(result, float) and result >= 0)


@given(st.text() | st.none())
def test_parse_attendee_badge_safe(s):
    try:
        result = parse_attendee_badge(s)
    except Exception as e:
        assert False, f"parse_attendee_badge crashed with: {e!r} on input {s!r}"
    assert isinstance(result, str)