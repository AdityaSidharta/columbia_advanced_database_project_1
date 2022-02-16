def assert_params(client_key, engine_key, query, precision):
    assert isinstance(precision, float) and 0.0 <= precision <= 1.0
    assert len(query) and isinstance(query, str)
    assert len(client_key) and isinstance(client_key, str)
    assert len(engine_key) and isinstance(engine_key, str)
