from hmbtg_utils.anonymizer import no_ip


def test_simple_ip():
    assert no_ip("123.123.1.1") == "123.123.0.0"


def test_simple_ip_dashed():
    assert no_ip("123-123-1-1") == "123-123-0-0"
