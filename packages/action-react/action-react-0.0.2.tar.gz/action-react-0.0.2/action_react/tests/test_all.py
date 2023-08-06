from action_react.main import check_message, get_target_channel, read_configs
from datetime import datetime
from pytest import mark
from telethon.tl.types import PeerChannel
from unittest.mock import patch


@mark.parametrize(
    'message', ["Taipei H: 7/26 -> 3/16", "Vancouver H: 7/26 -> 7/16", "Halifax J: 7/26 -> 3/16", "test string"]
)
@mark.parametrize('target_date', [datetime(2023, 6, 1).date()])
@mark.parametrize('cities', [["falifax", "vancouver"]])
@mark.parametrize('output', [(False, None)])
def test_check_message_failure(message, target_date, cities, output):
    assert check_message(message, target_date, cities) == output


@mark.parametrize('message', ["Halifax H: 7/26 -> 3/6"])
@mark.parametrize('target_date', [datetime(2023, 6, 1).date()])
@mark.parametrize('cities', [["halifax", "vancouver"]])
@mark.parametrize('output', [(True, (datetime(2023, 3, 6).date(), "Halifax"))])
def test_check_message(message, target_date, cities, output):
    assert check_message(message, target_date, cities) == output


@mark.parametrize('message', ["Halifax H: 7/26 -> 2024/3/6"])
@mark.parametrize('target_date', [datetime(2024, 6, 1).date()])
@mark.parametrize('cities', [["halifax", "vancouver"]])
@mark.parametrize('output', [(True, (datetime(2024, 3, 6).date(), "Halifax"))])
def test_check_message_with_year(message, target_date, cities, output):
    assert check_message(message, target_date, cities) == output


@patch('builtins.input', return_value='test_url')
def test_get_target_channel_with_url(input):
    assert get_target_channel() == 'test_url'


@patch('builtins.input', return_value='12345')
def test_get_target_channel_with_entity_id(input):
    channel = get_target_channel()
    assert type(channel) is PeerChannel
    assert channel.channel_id == 12345


def test_read_configs():
    assert read_configs("./action_react/tests/fixtures/config.ini") == (
        "test_api_id",
        "test_api_hash",
        "test_phone",
        "test_username",
        datetime(2023, 6, 1).date(),
        ["city_1", "city_2"],
    )
