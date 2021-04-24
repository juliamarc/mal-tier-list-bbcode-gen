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
def test_dedup_list(input_list, output_list):
    assert utils.deduplicate_list(input_list) == output_list
