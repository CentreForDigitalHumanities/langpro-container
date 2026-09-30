from dataclasses import dataclass
from enum import StrEnum
from functools import partial


class Relationship(StrEnum):
    EQUAL = "equal"
    SUBSET = "subset"
    DISJOINT = "disjoint"


@dataclass
class KBItem:
    entity1: str
    entity2: str
    relationship: Relationship


def extract_used_kb_items(used_items: list[dict]) -> list:
    """
    Extracts the used knowledge base items from the LangPro output.

    This assumes that the LangPro output contains a list of used items, each
    represented as a dictionary with a 'functor' and 'args'.

    - Items with a 'disj' functor are mapped to a KB item with relationship
    'disjoint'.
    - Items with a single 'isa_wn' functor are mapped to a KB item with
    relationship 'subset'.
    - Item pairs with a 'isa_wn' functor and inverse arguments are mapped to a
    single KB item with relationship 'equal'.

    The output is sorted: 'equal'/'subset' items containing 'be' (a very common
    and uninformative case) are placed at the end of the list. The order of the
    other elements is preserved.

    Expected input (`used_items`):

    ```
    'kb': [
            {
                'args': ['dux', 'dax'],
                'functor': 'disj'
            }, {
                'args': ['lift', 'be'],
                'functor': 'isa_wn'
            },
            {
                'args': ['own', 'have'],
                'functor': 'isa_wn'
            },
            {
                'args': ['have', 'own'],
                'functor': 'isa_wn'
            }
        ]
    ```

    Expected output:

    ```
    [
        KBItem(entity1='dux', entity2='dax', relationship='disjoint'),
        KBItem(entity1='own', entity2='have', relationship='equal'),
        KBItem(entity1='lift', entity2='be', relationship='subset')]
    ```
    """
    kb_items: list[KBItem] = []

    # Maps (entity1, entity2) pairs to the first KBItem with those entities.
    first_by_pair: dict[tuple[str, str], KBItem] = {}

    def set_to_first_by_pair(kb_item: KBItem) -> None:
        first_by_pair.setdefault((kb_item.entity1, kb_item.entity2), kb_item)

    for item in used_items:
        functor = item["functor"]
        args = item["args"]

        if functor == "disj":
            kb_item = KBItem(
                entity1=args[0],
                entity2=args[1],
                relationship=Relationship.DISJOINT,
            )
            kb_items.append(kb_item)
            set_to_first_by_pair(kb_item)
            continue

        entity1, entity2 = args[0], args[1]
        converse_item = first_by_pair.get((entity2, entity1))
        if converse_item is not None:
            converse_item.relationship = Relationship.EQUAL
            continue

        kb_item = KBItem(
            entity1=entity1, entity2=entity2, relationship=Relationship.SUBSET
        )

        kb_items.append(kb_item)
        set_to_first_by_pair(kb_item)

    return sort_kb_items(kb_items)


def kb_item_order(item: KBItem) -> bool:
    """
    Returns a value that can be used to sort KB items.
    Items that are 'SUBSET' or 'EQUAL' and contain 'be' are considered less
    informative and are sorted to the end of the list.
    """
    return item.relationship in (Relationship.SUBSET, Relationship.EQUAL) and "be" in (
        item.entity1,
        item.entity2,
    )


sort_kb_items = partial(sorted, key=kb_item_order)
sort_kb_items.__doc__ = """Sorts KB items, placing 'SUBSET' and 'EQUAL' items containing 'be' at the end of the list."""
