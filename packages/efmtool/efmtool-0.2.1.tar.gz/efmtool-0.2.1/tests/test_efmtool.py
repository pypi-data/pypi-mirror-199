import efmtool


def test_small_network(small_network):

    efms = efmtool.calculate_efms(*small_network)

    assert efms.shape[1] == 3
    assert efms.shape[0] == 5


def test_multiple_calls(small_network):

    _ = efmtool.calculate_efms(*small_network)
    efms = efmtool.calculate_efms(*small_network)

    assert efms.shape[1] == 3
    assert efms.shape[0] == 5


def test_blocked_network(blocked_network):
    efms = efmtool.calculate_efms(*blocked_network)

    assert efms.shape[1] == 0
