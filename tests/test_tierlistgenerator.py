import os

import pytest

from mal_tier_list_bbcode_gen.tierlistgenerator import TierListGenerator


@pytest.fixture
def perfect_ods_file_name():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'test_tiers_perfect.ods')


def test_init(perfect_ods_file_name):
    tlg = TierListGenerator(perfect_ods_file_name)

    assert tlg.__dict__.get("settings") is not None
    assert tlg.__dict__.get("tiers") is not None


def test_generate(perfect_ods_file_name):
    tlg = TierListGenerator(perfect_ods_file_name)
    tlg.generate()

    assert tlg.__dict__.get("bbcode") is not None
    assert tlg.__dict__.get("html") is not None
