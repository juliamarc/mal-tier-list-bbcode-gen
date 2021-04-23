from mal_tier_list_bbcode_gen import utils


def test_dedup_list_with_dups():
    assert utils.deduplicate_list([7, 6, 2, 2, 3, 6, 4, 6]) == [7, 6, 2, 3, 4]


def test_dedup_list_with_no_dups():
    assert utils.deduplicate_list([2, 1, 3, 7]) == [2, 1, 3, 7]
