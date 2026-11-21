import pytest
from cloud_storage_tier import process_storage_tenants, monitor_replication_latency


def test_single_active_hot_tenant():
    tenants = [
        {
            "account_active": True,
            "tier": "hot",
            "has_backup_vault": False,
            "buckets": [{"size_gb": 100, "corrupted": False, "egress_gb": 50}],
        }
    ]
    result = process_storage_tenants(tenants, 10.0)
    assert result == {"total_billed": 2.5, "status": "BILLED"}


def test_cool_tenant_with_backup_fee_and_egress_surcharge():
    tenants = [
        {
            "account_active": True,
            "tier": "cool",
            "has_backup_vault": True,
            "buckets": [{"size_gb": 40, "corrupted": False, "egress_gb": 150}],
        }
    ]
    result = process_storage_tenants(tenants, 12.5)
    assert result == {"total_billed": 12.5 + (40 * 0.015) + (150 - 100) * 0.08, "status": "BILLED"}


def test_archive_bucket_corruption_resets_charge_and_zero_usage():
    tenants = [
        {
            "account_active": True,
            "tier": "archive",
            "has_backup_vault": False,
            "buckets": [{"size_gb": 10, "corrupted": True, "egress_gb": 50}],
        }
    ]
    assert process_storage_tenants(tenants, 0) == {"total_billed": 0.0, "status": "ZERO_USAGE"}


def test_large_hot_bucket_uses_discount_and_ignores_invalid_bucket_sizes():
    tenants = [
        {
            "account_active": True,
            "tier": "hot",
            "has_backup_vault": False,
            "buckets": [
                {"size_gb": 600, "corrupted": False, "egress_gb": 20},
                {"size_gb": 0, "corrupted": False, "egress_gb": 50},
                {"size_gb": -1, "corrupted": False, "egress_gb": 25},
            ],
        }
    ]
    expected = 600 * 0.025 * 0.90
    assert process_storage_tenants(tenants, 10.0) == {"total_billed": round(expected, 2), "status": "BILLED"}


def test_unknown_tier_and_multiple_flagged_buckets_trigger_audit_flag():
    tenants = [
        {
            "account_active": True,
            "tier": "unknown",
            "has_backup_vault": False,
            "buckets": [{"size_gb": 25, "corrupted": False, "egress_gb": 10}],
        },
        {
            "account_active": True,
            "tier": "hot",
            "has_backup_vault": False,
            "buckets": [
                {"size_gb": 0, "corrupted": False, "egress_gb": 0},
                {"size_gb": -5, "corrupted": False, "egress_gb": 0},
                {"size_gb": 30, "corrupted": True, "egress_gb": 0},
                {"size_gb": 40, "corrupted": False, "egress_gb": 0},
                {"size_gb": 0, "corrupted": False, "egress_gb": 0},
                {"size_gb": 50, "corrupted": False, "egress_gb": 0},
                {"size_gb": 5, "corrupted": False, "egress_gb": 0},
            ],
        },
    ]
    expected = 40 * 0.025 + 50 * 0.025 + 5 * 0.025
    assert process_storage_tenants(tenants, 0) == {"total_billed": round(expected, 2), "status": "AUDIT_FLAGGED"}


def test_invalid_inputs_and_inactive_tenants_raise_or_skip():
    with pytest.raises(ValueError):
        process_storage_tenants("not-a-list", 10)
    with pytest.raises(ValueError):
        process_storage_tenants([], -1)

    tenants = [
        {"account_active": False, "tier": "hot", "buckets": [{"size_gb": 100, "corrupted": False, "egress_gb": 0}]},
        {"account_active": True, "tier": "hot", "has_backup_vault": False, "buckets": [{"size_gb": 10, "corrupted": False, "egress_gb": 0}]},
    ]
    assert process_storage_tenants(tenants, 0) == {"total_billed": 0.25, "status": "BILLED"}


def test_monitor_replication_latency_handles_empty_and_alert_cases():
    assert monitor_replication_latency([]) == "NO_DATA"
    assert monitor_replication_latency(None) == "NO_DATA"
    assert monitor_replication_latency([[100, 50, 150], [60, 80, 90]]) == "SYNCED"
    assert monitor_replication_latency([[100, 250, 260], [10, 20, 30]]) == "SYNC_LAG_ALERT"
    assert monitor_replication_latency([[100, 80, 150], [10, 210, 230]]) == "SYNC_LAG_ALERT"
    assert monitor_replication_latency([[100, 80, 150], [10, 20, 50]]) == "SYNCED"