import pytest

import mal_tier_list_bbcode_gen.exceptions as exceptions

from mal_tier_list_bbcode_gen.entry import Entry


@pytest.fixture(autouse=True)
def direct_image_url():
    return 'example.com/test.png'


@pytest.mark.parametrize(
    "mal_url,expected_name",
    [
        pytest.param(
            'https://myanimelist.net/character/142314/Zeke',
            'Zeke',
            id="one_word"
        ),
        pytest.param(
            'https://myanimelist.net/character/164471/Satoru_Gojou',
            'Satoru Gojou',
            id="two_words"
        ),
        pytest.param(
            'https://myanimelist.net/character/3934/Olivier_Mira_Armstrong',
            'Olivier Mira Armstrong',
            id="three_words"
        ),
        pytest.param(
            'https://myanimelist.net/character/71121/Hange_Zo%C3%AB',
            'Hange Zoë',
            id="unquote"
        ),
    ],
)
def test_name(mal_url, expected_name):
    entry = Entry(mal_url, 'direct URL', direct_image_url)

    assert entry.name == expected_name


@pytest.mark.parametrize(
    "mal_url",
    [
        pytest.param(
            'https://myanimelist.net/character/142314/Zeke',
            id="character"
        ),
        pytest.param(
            'https://myanimelist.net/anime/39026/Dumbbell_Nan_Kilo_Moteru',
            id="anime"
        ),
        pytest.param(
            'https://myanimelist.net/manga/113138/Jujutsu_Kaisen',
            id="manga"
        ),
        pytest.param(
            'https://myanimelist.net/people/212/Daisuke_Ono',
            id="people"
        ),
    ],
)
def test_validate_mal_url_valid_url(mal_url):
    entry = Entry(mal_url, 'direct URL', direct_image_url)

    assert entry.mal_url == mal_url


def test_validate_mal_url_invalid_url():
    invalid_mal_url = 'https://www.google.com/'
    with pytest.raises(exceptions.InvalidMALURL):
        Entry(invalid_mal_url, 'direct URL', direct_image_url)


def test_get_bbcode():
    mal_url = 'https://myanimelist.net/character/142314/Zeke'
    entry = Entry(mal_url, 'direct URL', direct_image_url)
    expected_bbcode = f'[url={mal_url}][img]{entry.image_url}[/img][/url]'

    assert entry.get_bbcode() == expected_bbcode
