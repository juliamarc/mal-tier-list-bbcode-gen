import os

import pytest

from mal_tier_list_bbcode_gen.spreadsheetparser import (
    SpreadsheetParser, EntriesPerRowMissingError, EntriesPerRowNotANumberError)


@pytest.fixture
def epmty_ods_file_name():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'test_tiers_epmty.ods')


@pytest.fixture
def perfect_ods_file_name():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'test_tiers_perfect.ods')


@pytest.fixture
def settings_ods_file_name():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'test_tiers_settings.ods')


@pytest.fixture
def empty_ssp_with_mocked_parse_settings(mocker, epmty_ods_file_name):
    mocker.patch.object(SpreadsheetParser, '_parse_settings')
    return SpreadsheetParser(epmty_ods_file_name)


@pytest.fixture
def perfect_ssp_with_mocked_parse_settings(mocker, perfect_ods_file_name):
    mocker.patch.object(SpreadsheetParser, '_parse_settings')
    return SpreadsheetParser(perfect_ods_file_name)


@pytest.fixture
def settings_ssp_with_mocked_parse_settings(mocker, settings_ods_file_name):
    mocker.patch.object(SpreadsheetParser, '_parse_settings')
    return SpreadsheetParser(settings_ods_file_name)


def test_get_settings_sheet_exists(perfect_ssp_with_mocked_parse_settings):
    ssp = perfect_ssp_with_mocked_parse_settings
    settings_sheet = ssp._get_settings_sheet()

    assert settings_sheet.name == ssp.SETTINGS_SHEET_NAME


def test_get_settings_sheet_not_exists(empty_ssp_with_mocked_parse_settings):
    ssp = empty_ssp_with_mocked_parse_settings
    with pytest.raises(KeyError, match=r".*not found in spreadsheet*"):
        ssp._get_settings_sheet()


@pytest.mark.parametrize(
    "settings_sheet_name,expected_tier_names",
    [
        pytest.param(
            'S1', ['a', 'b', 'c', 'd', 'e'], id="normal"
        ),
        pytest.param(
            'S2', ['a', 'b', 'c', 'd', 'e'], id="skips"
        ),
        pytest.param(
            'S3', ['a', 'b', 'c', 'd', 'e'], id="duplicates"
        ),
        pytest.param(
            'S4', ['e', 'd', 'c', 'b', 'a'], id="reverse_alphabetical_order"
        ),
        pytest.param(
            'S5', ['2', '2.0', '2,0', '2,000', '2.000'], id="numbers"
        ),
        pytest.param(
            'S6', [], id="empty"
        ),
    ],
)
def test_parse_tier_order(
        mocker, settings_ssp_with_mocked_parse_settings,
        settings_sheet_name, expected_tier_names):
    mocker.patch.object(SpreadsheetParser, '_parse_settings')
    ssp = settings_ssp_with_mocked_parse_settings

    tier_names = ssp._parse_tier_order(
        ssp.spreadsheet.sheets[settings_sheet_name])

    assert tier_names == expected_tier_names


@pytest.mark.parametrize(
    "tier_names,sheets_names,expected_missing",
    [
        pytest.param(['a', 'b'], ['a', 'b'], set(),
                     id="same"),
        pytest.param(['a', 'b', 'c'], ['a', 'b'], set(['c']),
                     id="missing_sheet"),
        pytest.param(['a', 'b'], ['a', 'b', 'c'], set(),
                     id="unused_sheet"),
        pytest.param([], [], set(),
                     id="empty"),
    ],
)
def test_missing_tier_sheets(
        mocker, epmty_ods_file_name, tier_names, sheets_names,
        expected_missing):
    mocker.patch.object(SpreadsheetParser, '__init__', return_value=None)
    ss = mocker.patch.object(SpreadsheetParser, 'spreadsheet', create=True)
    ss.sheets.names.return_value = sheets_names

    ssp = SpreadsheetParser(epmty_ods_file_name)
    missing = ssp._check_for_missing_tier_sheets(tier_names)

    assert missing == expected_missing


def test_get_entries_per_row_setting_not_exists(
        settings_ssp_with_mocked_parse_settings):
    ssp = settings_ssp_with_mocked_parse_settings
    with pytest.raises(EntriesPerRowMissingError):
        ssp._get_entries_per_row_setting(ssp.spreadsheet.sheets['S6'])


@pytest.mark.parametrize(
    "settings_sheet_name,expected_entries_per_row",
    [
        pytest.param(
            'S2', 4, id="positive"
        ),
        pytest.param(
            'S3', 0, id="zero"
        ),
        pytest.param(
            'S5', 0, id="negative"
        ),
    ],
)
def test_get_entries_per_row_setting_number(
        settings_ssp_with_mocked_parse_settings, settings_sheet_name,
        expected_entries_per_row):
    ssp = settings_ssp_with_mocked_parse_settings
    entries_per_row = ssp._get_entries_per_row_setting(
        ssp.spreadsheet.sheets[settings_sheet_name])

    assert entries_per_row == expected_entries_per_row


def test_get_entries_per_row_setting_text(
        settings_ssp_with_mocked_parse_settings):
    ssp = settings_ssp_with_mocked_parse_settings
    with pytest.raises(EntriesPerRowNotANumberError):
        ssp._get_entries_per_row_setting(ssp.spreadsheet.sheets['S4'])


def test_parse_settings(mocker, perfect_ods_file_name):
    expected_settings = {
        'tier_names': ['tier S', 'tier A', 'tier B', 'tier C', 'tier D',
                       'tier E', 'tier F'],
        'entries_per_row': 4,
    }
    real_parse_settings = SpreadsheetParser._parse_settings
    mocker.patch.object(SpreadsheetParser, '_parse_settings')
    ssp = SpreadsheetParser(perfect_ods_file_name)
    ssp._parse_settings = real_parse_settings
    settings = ssp._parse_settings(ssp)

    assert settings == expected_settings
