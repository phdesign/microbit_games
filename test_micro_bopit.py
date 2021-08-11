from micro_bopit import create_exponential_decay

def test_create_exponential_decay():
    fn = create_exponential_decay(1500, 200)
    assert fn(0) == 1500
    assert round(fn(10)) == 1427
    assert round(fn(100)) == 910
    assert round(fn(1000)) == 10