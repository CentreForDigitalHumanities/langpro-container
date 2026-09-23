from dataclasses import dataclass
from enum import StrEnum


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
    and uninformative case) are placed at the end of the list.

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

    for item in used_items:
        functor = item["functor"]
        args = item["args"]

        if functor == "disj":
            kb_items.append(
                KBItem(
                    entity1=args[0], entity2=args[1], relationship=Relationship.DISJOINT
                )
            )
            continue

        entity1, entity2 = args[0], args[1]
        converse_item = [
            kb_item
            for kb_item in kb_items
            if kb_item.entity1 == entity2 and kb_item.entity2 == entity1
        ]
        if converse_item:
            converse_item[0].relationship = Relationship.EQUAL
            continue

        kb_items.append(
            KBItem(entity1=entity1, entity2=entity2, relationship=Relationship.SUBSET)
        )

    return sort_kb_items(kb_items)


def sort_kb_items(kb_items: list[KBItem]) -> list[KBItem]:
    """
    Sorts the KB items such that 'equal'/'subset' items containing 'be' are placed at the end of the list.
    """
    return sorted(
        kb_items,
        key=lambda item: (
            item.relationship != Relationship.DISJOINT,
            "be" in (item.entity1, item.entity2),
        ),
    )
