"""Real tests for the NetCore backend.

Covers the API surface end-to-end through TestClient, plus pure-logic unit tests for
the ArubaOS/ProCurve running-config parser (`services/config_parser.py`).
"""


# ── app metadata ────────────────────────────────────────────────────────────

def test_root_returns_app_metadata(client):
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body["app"] == "NetCore"
    assert body["version"]
    assert "features" in body and isinstance(body["features"], list)


def test_openapi_lists_routes(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    spec = r.json()
    paths = spec["paths"]
    # a handful of routes that must exist for the product to be what it claims
    for expected in ("/api/switches/", "/api/dashboard/stats"):
        assert expected in paths
    assert len(paths) > 20


# ── dashboard ───────────────────────────────────────────────────────────────

def test_dashboard_stats_shape(client):
    r = client.get("/api/dashboard/stats")
    assert r.status_code == 200
    body = r.json()
    for key in (
        "total_switches",
        "online_switches",
        "offline_switches",
        "total_configs",
        "open_security_findings",
        "active_workflows",
        "total_topologies",
    ):
        assert key in body, f"missing {key}"
        assert isinstance(body[key], int)


# ── switches CRUD ───────────────────────────────────────────────────────────

def test_switches_list_starts_as_list(client):
    r = client.get("/api/switches/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_switch_then_read_back(client):
    payload = {
        "hostname": "sw-test-01",
        "ip_address": "10.20.30.40",
        "vendor": "cisco_ios",
        "location": "lab",
        "tags": "test",
    }
    r = client.post("/api/switches/", json=payload)
    assert r.status_code in (200, 201), r.text
    created = r.json()
    assert created["hostname"] == "sw-test-01"
    assert created["ip_address"] == "10.20.30.40"
    new_id = created["id"]

    r = client.get(f"/api/switches/{new_id}")
    assert r.status_code == 200
    fetched = r.json()
    assert fetched["id"] == new_id
    assert fetched["hostname"] == "sw-test-01"

    # it must now be visible in the collection
    r = client.get("/api/switches/")
    assert any(s["id"] == new_id for s in r.json())


def test_created_switch_counts_toward_dashboard(client):
    client.post(
        "/api/switches/",
        json={"hostname": "sw-count-01", "ip_address": "10.20.30.41"},
    )
    stats = client.get("/api/dashboard/stats").json()
    assert stats["total_switches"] >= 1


# ── config parser (pure logic) ──────────────────────────────────────────────

SAMPLE_RUNNING_CONFIG = """hostname "core-sw-01"
time timezone -300
ip default-gateway 10.0.0.1
ip routing
sntp server priority 1 10.0.0.10
radius-server host 10.0.0.20 key "s3cret"
dhcp-snooping authorized-server 10.0.0.30
dhcp-snooping option 82

vlan 10
   name "USERS"
   untagged 1-24
   tagged 25-28
   ip address 10.0.10.1 255.255.255.0
   ip helper-address 10.0.0.5

vlan 20
   name "VOICE"
   tagged 25-28
"""


def test_parse_config_extracts_scalar_fields():
    from services.config_parser import parse_config

    cfg = parse_config(SAMPLE_RUNNING_CONFIG)
    assert cfg.hostname == "core-sw-01"
    assert cfg.timezone == -300
    assert cfg.default_gateway == "10.0.0.1"


def test_parse_config_detects_role_and_services():
    from services.config_parser import parse_config

    cfg = parse_config(SAMPLE_RUNNING_CONFIG)
    # "ip routing" present -> core
    assert cfg.role == "core"
    assert cfg.sntp_servers == ["10.0.0.10"]
    assert cfg.dhcp_authorized_servers == ["10.0.0.30"]
    assert cfg.dhcp_option82 is True
    assert [(r.host, r.key) for r in cfg.radius_servers] == [("10.0.0.20", "s3cret")]


def test_parse_config_parses_vlans():
    from services.config_parser import parse_config

    cfg = parse_config(SAMPLE_RUNNING_CONFIG)
    by_id = {v.id: v for v in cfg.vlans}
    assert 10 in by_id and 20 in by_id
    assert by_id[10].name == "USERS"
    assert by_id[10].untagged == "1-24"
    assert by_id[10].tagged == "25-28"
    assert by_id[10].ip == "10.0.10.1"
    assert by_id[10].mask == "255.255.255.0"
    assert by_id[10].helper == "10.0.0.5"
    assert by_id[20].name == "VOICE"


def test_parse_config_access_switch_is_not_core():
    from services.config_parser import parse_config

    cfg = parse_config('hostname "access-sw-09"\nvlan 1\n   untagged 1-48\n')
    assert cfg.role == "access"
    assert cfg.hostname == "access-sw-09"


def test_parse_config_empty_input_is_safe():
    from services.config_parser import parse_config

    cfg = parse_config("")
    assert cfg.hostname == ""
    assert cfg.vlans == []
    assert cfg.radius_servers == []
