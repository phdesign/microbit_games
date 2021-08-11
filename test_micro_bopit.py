from micro_bopit import create_exponential_decay

def test_create_exponential_decay():
    fn = create_exponential_decay(1000, 200)
    assert fn(0) == 1000
    assert round(fn(10)) == 951
    assert round(fn(100)) == 607
    assert round(fn(1000)) == 7