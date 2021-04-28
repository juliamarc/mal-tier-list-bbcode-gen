import os

import pytest

import mal_tier_list_bbcode_gen.exceptions as exceptions

from mal_tier_list_bbcode_gen.entry import Entry
from mal_tier_list_bbcode_gen.image import Image
from mal_tier_list_bbcode_gen.spreadsheetparser import SpreadsheetParser


@pytest.fixture
def epmty_ods_file_name():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'test_tiers_empty.ods')


@pytest.fixture
def perfect_ods_file_name():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'test_tiers_perfect.ods')


@pytest.fixture
def settings_ods_file_name():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'test_tiers_settings.ods')


@pytest.fixture
def incomplete_ods_file_name():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'test_tiers_incomplete.ods')


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
    with pytest.raises(exceptions.SettingsSheetMissingError,
                       match=r".*not found in spreadsheet*"):
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
    with pytest.raises(exceptions.EntriesPerRowMissingError):
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
    with pytest.raises(exceptions.EntriesPerRowNotANumberError):
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


def test_parse_header_yes_full_entry(perfect_ods_file_name):
    ssp = SpreadsheetParser(perfect_ods_file_name)
    tier_name = 'tier S'
    header = ssp._parse_header(ssp.spreadsheet.sheets[tier_name], tier_name)

    assert isinstance(header, Image)
    assert header.image_source == 'Google Drive'
    assert header.image_url == ('https://drive.google.com/uc?id='
                                '1V3vK8HA4hrdby7VHkQwrb6KvlMcXEPTA')


@pytest.mark.parametrize(
    "tier_name",
    [
        pytest.param('tier A'),
        pytest.param('tier B'),
        pytest.param('tier C'),
    ],
)
def test_parse_header_yes_incomplete_entry(
        incomplete_ods_file_name, tier_name):
    ssp = SpreadsheetParser(incomplete_ods_file_name)
    with pytest.raises(exceptions.HeaderIncompleteError):
        ssp._parse_header(ssp.spreadsheet.sheets[tier_name], tier_name)


def test_parse_header_no(incomplete_ods_file_name):
    ssp = SpreadsheetParser(incomplete_ods_file_name)
    tier_name = 'tier S'
    header = ssp._parse_header(ssp.spreadsheet.sheets[tier_name], tier_name)

    assert header is None


def test_parse_entry_complete_entry(perfect_ods_file_name):
    ssp = SpreadsheetParser(perfect_ods_file_name)
    tier_name = 'tier S'
    entry = ssp._parse_entry(
        ssp.spreadsheet.sheets[tier_name].row(4), 4, tier_name)

    assert isinstance(entry, Entry)
    assert entry.mal_url == 'https://myanimelist.net/character/142314/Zeke'
    assert entry.name == 'Zeke'
    assert entry.image_source == 'Google Drive'
    assert entry.image_url == ('https://drive.google.com/uc?id='
                               '1olKc6TBJ1kPJa7cKWVp7dNZFwHb_0k8Z')


@pytest.mark.parametrize(
    "row_number",
    [
        pytest.param(5),
        pytest.param(6),
        pytest.param(7),
        pytest.param(8),
        pytest.param(9),
        pytest.param(10),
        pytest.param(15),
    ],
)
def test_parse_entry_incomplete_entry(incomplete_ods_file_name, row_number):
    ssp = SpreadsheetParser(incomplete_ods_file_name)
    tier_name = 'tier A'
    entry = ssp._parse_entry(
        ssp.spreadsheet.sheets[tier_name].row(row_number), row_number,
        tier_name)

    assert entry is None


def test_parse_entries_all_complete(perfect_ods_file_name):
    ssp = SpreadsheetParser(perfect_ods_file_name)
    tier_name = 'tier S'
    entries = ssp._parse_entries(ssp.spreadsheet.sheets[tier_name], tier_name)

    assert len(entries) == 2
    assert all([isinstance(e, Entry) for e in entries])


def test_parse_entries_some_complete(incomplete_ods_file_name):
    ssp = SpreadsheetParser(incomplete_ods_file_name)
    tier_name = 'tier A'
    entries = ssp._parse_entries(ssp.spreadsheet.sheets[tier_name], tier_name)

    assert len(entries) == 2
    assert all([isinstance(e, Entry) for e in entries])


def test_parse_tier(perfect_ods_file_name):
    ssp = SpreadsheetParser(perfect_ods_file_name)
    tier_name = 'tier B'
    tier = ssp._parse_tier(tier_name)

    assert len(tier) == 2
    assert 'header' in tier
    assert 'entries' in tier
    assert isinstance(tier['header'], Image) or tier['header'] is None
    assert all([isinstance(e, Entry) for e in tier['entries']])


def test_parse_tiers(perfect_ods_file_name):
    ssp = SpreadsheetParser(perfect_ods_file_name)
    ssp.parse_tiers()

    assert set(ssp.settings['tier_names']) == set(ssp.tiers.keys())
    assert all(['header' in t and 'entries' in t for t in ssp.tiers.values()])
