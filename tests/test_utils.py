import pytest

from mal_tier_list_bbcode_gen import utils


@pytest.mark.parametrize(
    "input_list,output_list",
    [
        pytest.param(
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            id="ordered_no_dups"
        ),
        pytest.param(
            [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
            [1, 2, 3, 4, 5],
            id="ordered_dups"
        ),
        pytest.param(
            [2, 1, 3, 7],
            [2, 1, 3, 7],
            id="maintain_order_no_dups"
        ),
        pytest.param(
            [2, 1, 3, 7, 7, 3, 1, 2, 8],
            [2, 1, 3, 7, 8],
            id="maintain_order_dups"
        ),
    ],
)
def test_deduplicate_list(input_list, output_list):
    assert utils.deduplicate_list(input_list) == output_list


@pytest.mark.parametrize(
    "input_list,filter_set,expected_list",
    [
        pytest.param(
            [1, 2, 3, 4, 5],
            set(),
            [1, 2, 3, 4, 5],
            id="empty_set"
        ),
        pytest.param(
            [1, 2, 3, 4, 5],
            set([2, 4]),
            [1, 3, 5],
            id="two_elem_set"
        ),
        pytest.param(
            [],
            set(),
            [],
            id="all_empty"
        ),
        pytest.param(
            [2, 1, 3, 7],
            set([2, 1, 3, 7]),
            [],
            id="all_filtered"
        ),
    ],
)
def test_filter_list_by_set(input_list, filter_set, expected_list):
    filtered_list = utils.filter_list_by_set(input_list, filter_set)

    assert filtered_list == expected_list
