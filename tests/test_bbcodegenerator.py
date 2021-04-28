import os

import pytest

from mal_tier_list_bbcode_gen.bbcodegenerator import BBCodeGenerator
from mal_tier_list_bbcode_gen.entry import Entry
from mal_tier_list_bbcode_gen.image import Image


@pytest.mark.parametrize(
    "header,expected_bbcode",
    [
        pytest.param(
            Image('direct URL', 'example.com'),
            '[img]example.com[/img]\n',
            id='header_exists'),
        pytest.param(
            None,
            '',
            id='header_is_none'),
    ],
)
def test_generate_bbcode_for_header(header, expected_bbcode):
    bbcg = BBCodeGenerator({}, {})
    bbcode = bbcg._generate_bbcode_for_header(header)

    assert bbcode == expected_bbcode


@pytest.mark.parametrize(
    "entries_per_row,no_entries,expected_ends",
    [
        pytest.param(0, 0, ['\n']),
        pytest.param(0, 1, ['\n']),
        pytest.param(1, 2, ['\n', '\n']),
        pytest.param(2, 2, ['', '\n']),
        pytest.param(0, 5, ['', '', '', '', '\n']),
        pytest.param(4, 8, ['', '', '', '\n', '', '', '', '\n']),
        pytest.param(3, 8, ['', '', '\n', '', '', '\n', '', '\n']),
        pytest.param(2, 9, ['', '\n', '', '\n', '', '\n', '', '\n', '\n']),
        pytest.param(10, 5, ['', '', '', '', '\n']),
    ],
)
def test_calculate_newline_after(entries_per_row, no_entries, expected_ends):
    bbcg = BBCodeGenerator({'entries_per_row': entries_per_row}, {})
    ends = bbcg._calculate_newline_after(no_entries)

    assert ends == expected_ends


@pytest.mark.parametrize(
    "entries_per_row,tier,expected_bbcode",
    [
        pytest.param(0, {
            'header': Image('direct URL', 'example.com'),
            'entries': [
                Entry(
                    'https://myanimelist.net/character/370/Ayame_Souma',
                    'direct URL',
                    'example.com'),
                Entry(
                    'https://myanimelist.net/character/2160/Hei',
                    'direct URL',
                    'example2.com'),
                ],
            },
            ('[img]example.com[/img]\n'
             '[url=https://myanimelist.net/character/370/Ayame_Souma]'
             '[img]example.com[/img][/url]'
             '[url=https://myanimelist.net/character/2160/Hei]'
             '[img]example2.com[/img][/url]\n')
        ),
        pytest.param(1, {
            'header': None,
            'entries': [
                Entry(
                    'https://myanimelist.net/character/370/Ayame_Souma',
                    'direct URL',
                    'example.com'),
                Entry(
                    'https://myanimelist.net/character/2160/Hei',
                    'direct URL',
                    'example2.com'),
                ],
            },
            ('[url=https://myanimelist.net/character/370/Ayame_Souma]'
             '[img]example.com[/img][/url]\n'
             '[url=https://myanimelist.net/character/2160/Hei]'
             '[img]example2.com[/img][/url]\n')
        ),
        pytest.param(0, {
            'header': Image('direct URL', 'example.com'),
            'entries': [],
            },
            '[img]example.com[/img]\n'
        ),
        pytest.param(0, {
            'header': None,
            'entries': [],
            },
            ''
        ),
    ],
)
def test_generate_bbcode_for_tier(entries_per_row, tier, expected_bbcode):
    bbcg = BBCodeGenerator({'entries_per_row': entries_per_row}, {})
    bbcode = bbcg._generate_bbcode_for_tier(tier)

    assert bbcode == expected_bbcode


def test_generate_bbcode():
    bbcg = BBCodeGenerator(
        {'entries_per_row': 2}, {
            'tier S': {
                'header': None,
                'entries': [
                    Entry(
                        'https://myanimelist.net/character/370/Ayame_Souma',
                        'direct URL',
                        'example1.com'),
                    Entry(
                        'https://myanimelist.net/character/2455/Orochimaru',
                        'direct URL',
                        'example2.com'),
                ]
            },
            'tier A': {
                'header': Image('direct URL', 'example.com'),
                'entries': [
                    Entry(
                        'https://myanimelist.net/character/91959/Sakamoto',
                        'direct URL',
                        'example3.com'),
                    Entry(
                        'https://myanimelist.net/character/45627/Levi',
                        'direct URL',
                        'example4.com'),
                    Entry(
                        'https://myanimelist.net/character/164481/Mahito',
                        'direct URL',
                        'example5.com'),
                ]
            },
        },
    )
    expected_bbcode = (
        '[url=https://myanimelist.net/character/370/Ayame_Souma]'
        '[img]example1.com[/img][/url]'
        '[url=https://myanimelist.net/character/2455/Orochimaru]'
        '[img]example2.com[/img][/url]\n'
        '[img]example.com[/img]\n'
        '[url=https://myanimelist.net/character/91959/Sakamoto]'
        '[img]example3.com[/img][/url]'
        '[url=https://myanimelist.net/character/45627/Levi]'
        '[img]example4.com[/img][/url]\n'
        '[url=https://myanimelist.net/character/164481/Mahito]'
        '[img]example5.com[/img][/url]\n'
    )

    bbcg.generate_bbcode()

    assert bbcg.bbcode == expected_bbcode


def test_generate_html():
    bbcg = BBCodeGenerator(
        {'entries_per_row': 2}, {
            'tier S': {
                'header': None,
                'entries': [
                    Entry(
                        'https://myanimelist.net/character/370/Ayame_Souma',
                        'direct URL',
                        'example1.com'),
                    Entry(
                        'https://myanimelist.net/character/2455/Orochimaru',
                        'direct URL',
                        'example2.com'),
                ]
            },
            'tier A': {
                'header': Image('direct URL', 'example.com'),
                'entries': [
                    Entry(
                        'https://myanimelist.net/character/91959/Sakamoto',
                        'direct URL',
                        'example3.com'),
                    Entry(
                        'https://myanimelist.net/character/45627/Levi',
                        'direct URL',
                        'example4.com'),
                    Entry(
                        'https://myanimelist.net/character/164481/Mahito',
                        'direct URL',
                        'example5.com'),
                ]
            },
        },
    )
    test_html_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  'test_preview.html')
    with open(test_html_file, 'r') as f:
        expected_html = f.read()

    bbcg.generate_bbcode()
    bbcg.generate_html()

    assert bbcg.html == expected_html
