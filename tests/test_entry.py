from mal_tier_list_bbcode_gen.entry import Entry


def test_name_one_word():
    expected_name = 'Zeke'
    mal_url = 'https://myanimelist.net/character/142314/Zeke'
    image_url = 'example.com/test.png'
    entry = Entry(mal_url, 'direct URL', image_url)

    assert entry.name == expected_name
    assert str(entry) == expected_name


def test_name_two_words():
    expected_name = 'Satoru Gojou'
    mal_url = 'https://myanimelist.net/character/164471/Satoru_Gojou'
    image_url = 'example.com/test.png'
    entry = Entry(mal_url, 'direct URL', image_url)

    assert entry.name == expected_name
    assert str(entry) == expected_name


def test_name_three_words():
    expected_name = 'Olivier Mira Armstrong'
    mal_url = 'https://myanimelist.net/character/3934/Olivier_Mira_Armstrong'
    image_url = 'example.com/test.png'
    entry = Entry(mal_url, 'direct URL', image_url)

    assert entry.name == expected_name
    assert str(entry) == expected_name


def test_name_unquote():
    expected_name = 'Hange Zoë'
    mal_url = 'https://myanimelist.net/character/71121/Hange_Zo%C3%AB'
    image_url = 'example.com/test.png'
    entry = Entry(mal_url, 'direct URL', image_url)

    assert entry.name == expected_name
    assert str(entry) == expected_name


def test_get_bbcode():
    mal_url = 'https://myanimelist.net/character/142314/Zeke'
    entry = Entry(mal_url, 'direct URL', 'example.com/test.png')
    expected_bbcode = f'[url={mal_url}][img]{entry.image_url}[/img][/url]'

    assert entry.get_bbcode() == expected_bbcode
