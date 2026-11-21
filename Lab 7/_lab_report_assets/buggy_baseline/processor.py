def parse_storage_quota(quota_str):
    """
    Parses storage quota string with unit suffix into Gigabytes (GB).
    Assumes format: '<digits><2-letter unit>' (e.g. '500MB', '20GB', '2TB').
    """
    cleaned = quota_str.strip().upper()
    val_str = cleaned[:-2]
    unit = cleaned[-2:]
    value = int(val_str)
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
    raw_str, comp_str = size_metric_str.split(':')
    raw_bytes = float(raw_str)
    comp_bytes = float(comp_str)
    ratio = raw_bytes / comp_bytes
    return round(ratio, 2)

def lookup_bandwidth_tier_rate(tier_descriptor):
    """
    Looks up rate per GB for egress traffic using the first 3 letters of the tier name.
    Assumes standard tier prefix with at least 3 letters.
    """
    prefix = tier_descriptor.strip().upper()[:3]
    tier_rates = {
        "HOT": 0.08,
        "COL": 0.05,
        "ARC": 0.02
    }
    return tier_rates[prefix]

def main():
    print("==== Running parse_storage_quota ====")
    q_input = input("Enter quota (e.g. 500MB, 10GB, 2TB): ")
    print(parse_storage_quota(q_input))

    print("\n==== Running compute_compression_ratio ====")
    c_input = input("Enter raw:compressed bytes (e.g. 1024:256): ")
    print("Compression Ratio:", compute_compression_ratio(c_input))

    print("\n==== Running lookup_bandwidth_tier_rate ====")
    t_input = input("Enter tier descriptor (e.g. HOT_TIER, COLD, ARCHIVE): ")
    print("Rate per GB: $", lookup_bandwidth_tier_rate(t_input))

if __name__ == "__main__":
    main()
