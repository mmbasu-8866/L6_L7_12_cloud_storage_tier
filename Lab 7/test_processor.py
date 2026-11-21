import pytest
from hypothesis import given, strategies as st
from processor import parse_storage_quota, compute_compression_ratio, lookup_bandwidth_tier_rate

@given(st.one_of(st.text(), st.none()))
def test_parse_storage_quota_no_crash(s):
    try:
        result = parse_storage_quota(s)
    except (TypeError, ValueError, KeyError, OverflowError):
        return
    assert isinstance(result, str)
    assert "GB" in result

@given(st.one_of(st.text(), st.none()))
def test_compute_compression_ratio_safe(s):
    try:
        result = compute_compression_ratio(s)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        return
    assert isinstance(result, (int, float))
    assert result >= 0

@given(st.one_of(st.text(), st.none()))
def test_lookup_bandwidth_tier_rate_safe(s):
    try:
        result = lookup_bandwidth_tier_rate(s)
    except (TypeError, ValueError, KeyError):
        return
    assert isinstance(result, float)
    assert result >= 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("500MB", "Quota: 0.50 GB"),
        ("20GB", "Quota: 20.00 GB"),
        ("2TB", "Quota: 2000.00 GB"),
    ],
)
def test_parse_storage_quota_valid_values(value, expected):
    assert parse_storage_quota(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [("1024:256", 4.0), ("100:25", 4.0), ("0:10", 0.0)],
)
def test_compute_compression_ratio_valid_values(value, expected):
    assert compute_compression_ratio(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [("HOT_TIER", 0.08), ("COLD", 0.05), ("ARCHIVE", 0.02)],
)
def test_lookup_bandwidth_tier_rate_valid_values(value, expected):
    assert lookup_bandwidth_tier_rate(value) == expected