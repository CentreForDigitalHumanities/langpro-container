import pytest

from .extract_used_kb_items import (
    KBItem,
    Relationship,
    extract_used_kb_items,
    sort_kb_items,
)

test_input_output_pairs = [
    ([], []),
    (
        [{"functor": "disj", "args": ["dux", "dax"]}],
        [KBItem(entity1="dux", entity2="dax", relationship=Relationship.DISJOINT)],
    ),
    (
        [{"functor": "isa_wn", "args": ["lift", "be"]}],
        [KBItem(entity1="lift", entity2="be", relationship=Relationship.SUBSET)],
    ),
    (
        [
            {"functor": "isa_wn", "args": ["own", "have"]},
            {"functor": "isa_wn", "args": ["have", "own"]},
        ],
        [KBItem(entity1="own", entity2="have", relationship=Relationship.EQUAL)],
    ),
    (
        [
            {"functor": "disj", "args": ["dux", "dax"]},
            {"functor": "isa_wn", "args": ["lift", "be"]},
            {"functor": "isa_wn", "args": ["own", "have"]},
            {"functor": "isa_wn", "args": ["have", "own"]},
        ],
        [
            KBItem(entity1="dux", entity2="dax", relationship=Relationship.DISJOINT),
            KBItem(entity1="own", entity2="have", relationship=Relationship.EQUAL),
            KBItem(entity1="lift", entity2="be", relationship=Relationship.SUBSET),
        ],
    ),
]


@pytest.mark.parametrize("used_items, expected", test_input_output_pairs)
def test_extract_used_kb_items(used_items, expected):
    assert extract_used_kb_items(used_items) == expected


def test_sort_kb_items():
    items = [
        KBItem(entity1="human", entity2="be", relationship=Relationship.SUBSET),
        KBItem(entity1="cat", entity2="feline", relationship=Relationship.SUBSET),
        KBItem(entity1="dog", entity2="cat", relationship=Relationship.DISJOINT),
        KBItem(entity1="be", entity2="exist", relationship=Relationship.EQUAL),
        KBItem(entity1="fox", entity2="vulpine", relationship=Relationship.EQUAL),
        KBItem(entity1="sun", entity2="moon", relationship=Relationship.DISJOINT),
    ]

    sorted_items = sort_kb_items(items)

    expected = [
        KBItem(entity1="dog", entity2="cat", relationship=Relationship.DISJOINT),
        KBItem(entity1="sun", entity2="moon", relationship=Relationship.DISJOINT),
        KBItem(entity1="cat", entity2="feline", relationship=Relationship.SUBSET),
        KBItem(entity1="fox", entity2="vulpine", relationship=Relationship.EQUAL),
        KBItem(entity1="human", entity2="be", relationship=Relationship.SUBSET),
        KBItem(entity1="be", entity2="exist", relationship=Relationship.EQUAL),
    ]

    assert sorted_items == expected
