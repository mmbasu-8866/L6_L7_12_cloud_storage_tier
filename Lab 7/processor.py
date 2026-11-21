import math
import re


def parse_storage_quota(quota_str):
    """
    Parses storage quota string with unit suffix into Gigabytes (GB).
    Assumes format: '<digits><2-letter unit>' (e.g. '500MB', '20GB', '2TB').
    """
    if not isinstance(quota_str, str):
        raise TypeError("Quota must be a string")

    cleaned = quota_str.strip().upper()
    if not re.fullmatch(r"\d+(?:\.\d+)?(?:MB|GB|TB)", cleaned):
        raise ValueError("Invalid quota format")

    val_str = cleaned[:-2]
    unit = cleaned[-2:]
    value = float(val_str)
    if not math.isfinite(value) or value < 0:
        raise ValueError("Quota value must be finite and non-negative")

    multipliers = {
        "MB": 0.001,
        "GB": 1.0,
        "TB": 1000.0
    }
    gb_total = value * multipliers[unit]
    return f"Quota: {gb_total:.2f} GB"


def compute_compression_ratio(size_metric_str):
    """
    Computes compression ratio: raw_bytes / compressed_bytes.
    Assumes format: 'raw_bytes:compressed_bytes' (e.g. '1024:256').
    """
    if not isinstance(size_metric_str, str):
        raise TypeError("Size metric must be a string")

    parts = size_metric_str.strip().split(':')
    if len(parts) != 2:
        raise ValueError("Invalid size metric format")

    try:
        raw_bytes = float(parts[0])
        comp_bytes = float(parts[1])
    except (TypeError, ValueError) as exc:
        raise ValueError("Size values must be numeric") from exc

    if not math.isfinite(raw_bytes) or not math.isfinite(comp_bytes):
        raise ValueError("Size values must be finite")
    if raw_bytes < 0 or comp_bytes <= 0:
        raise ValueError("Raw bytes must be non-negative and compressed bytes must be positive")

    ratio = raw_bytes / comp_bytes
    return round(ratio, 2)


def lookup_bandwidth_tier_rate(tier_descriptor):
    """
    Looks up rate per GB for egress traffic using the first 3 letters of the tier name.
    Assumes standard tier prefix with at least 3 letters.
    """
    if not isinstance(tier_descriptor, str):
        raise TypeError("Tier descriptor must be a string")

    prefix = tier_descriptor.strip().upper()[:3]
    if len(prefix) < 3:
        raise ValueError("Tier descriptor must contain at least 3 letters")

    tier_rates = {
        "HOT": 0.08,
        "COL": 0.05,
        "ARC": 0.02
    }
    if prefix not in tier_rates:
        raise ValueError("Unknown storage tier")
    return tier_rates[prefix]


def main():
    print("==== Running parse_storage_quota ====")
    q_input = input("Enter quota (e.g. 500MB, 10GB, 2TB): ")
    try:
        print(parse_storage_quota(q_input))
    except (TypeError, ValueError) as exc:
        print(f"Invalid input: {exc}")

    print("\n==== Running compute_compression_ratio ====")
    c_input = input("Enter raw:compressed bytes (e.g. 1024:256): ")
    try:
        print("Compression Ratio:", compute_compression_ratio(c_input))
    except (TypeError, ValueError) as exc:
        print(f"Invalid input: {exc}")

    print("\n==== Running lookup_bandwidth_tier_rate ====")
    t_input = input("Enter tier descriptor (e.g. HOT_TIER, COLD, ARCHIVE): ")
    try:
        print("Rate per GB: $", lookup_bandwidth_tier_rate(t_input))
    except (TypeError, ValueError) as exc:
        print(f"Invalid input: {exc}")

if __name__ == "__main__":
    main()