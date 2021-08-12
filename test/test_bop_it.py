from unittest.mock import patch
from bop_it import create_exponential_decay, volume_to_step, change_volume


def test_create_exponential_decay():
    fn = create_exponential_decay(1500, 200)
    assert fn(0) == 1500
    assert round(fn(10)) == 1427
    assert round(fn(100)) == 910
    assert round(fn(1000)) == 10


def test_volume_to_step():
    assert volume_to_step(255) == 5
    assert volume_to_step(128) == 3
    assert volume_to_step(127) == 2
    assert volume_to_step(1) == 0
    assert volume_to_step(0) == 0


@patch("bop_it.show_volume")
@patch("bop_it.set_volume")
def test_change_volume_should_reset_volume_when_max(mock_set_volume, mock_show_volume):
    new_volume = change_volume(255)

    mock_show_volume.assert_called_once_with(0)
    mock_set_volume.assert_called_once_with(0)
    assert new_volume == 0


@patch("bop_it.show_volume")
@patch("bop_it.set_volume")
def test_change_volume_should_increment_volume(mock_set_volume, mock_show_volume):
    new_volume = change_volume(128)

    mock_show_volume.assert_called_once_with(4)
    mock_set_volume.assert_called_once_with(204)
    assert new_volume == 204
