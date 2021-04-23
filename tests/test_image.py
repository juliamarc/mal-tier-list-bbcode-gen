import pytest

from mal_tier_list_bbcode_gen.image import Image, GoogleDriveSourceError


def test_source_direct_url():
    image_url = 'example.com/test.png'
    image = Image('direct URL', image_url)

    assert image.image_url == image_url


def test_source_google_drive_file_id():
    expected_url = ('https://drive.google.com/uc'
                    '?id=1olKc6TUJ1kPJa7cKWVp7dNZFwHb_0k8Z')
    image_url = '1olKc6TUJ1kPJa7cKWVp7dNZFwHb_0k8Z'
    image = Image('Google Drive', image_url)

    assert image.image_url == expected_url


def test_source_google_drive_share_link():
    expected_url = ('https://drive.google.com/uc'
                    '?id=1olKc6TUJ1kPJa7cKWVp7dNZFwHb_0k8Z')
    image_url = ('https://drive.google.com/file/d/'
                 '1olKc6TUJ1kPJa7cKWVp7dNZFwHb_0k8Z/view?usp=sharing')
    image = Image('Google Drive', image_url)

    assert image.image_url == expected_url


def test_source_google_no_file_id():
    image_url = ('https://drive.google.com/file/d/view?usp=sharing')
    with pytest.raises(GoogleDriveSourceError):
        Image('Google Drive', image_url)


def test_source_not_valid():
    with pytest.raises(KeyError, match=r".*is not a valid image source.*"):
        Image('not valid', 'example.com/test.png')


def test_get_bbcode():
    image_url = 'example.com/test.png'
    expected_bbcode = f'[img]{image_url}[/img]'
    image = Image('direct URL', image_url)

    assert image.get_bbcode() == expected_bbcode
