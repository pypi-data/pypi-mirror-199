from texonomy import Entity, ERDiagram, Relationship, Direction, MANY_TO_EXACTLY_ONE, EXACTLY_ONE_TO_MANY


def test_add_entity() -> None:
    """
    Unit test for the ERDiagram's __init__() function.
    """
    journal = Entity("Journal", ["name", "ISBN number", "title"])
    journal.set_primary("ISBN number")

    # Add one entity
    diag = ERDiagram(journal)
    assert diag.entities == [journal]


def test_add_relationship() -> None:
    """
    Unit test for the add_relationship() function.
    """
    journal = Entity("Journal", ["name", "ISBN number", "title"])
    journal.set_primary("ISBN number")

    # Add one entity
    diag = ERDiagram(journal)
    assert diag.entities == [journal]

    editor = Entity("Editor-in-chief", ["name", "email"])
    editor.set_primary("email")

    # Try adding relationship with anchor entity not already in diagram.
    issue = Entity("Issue", ["issue-num"], True)
    try:
        diag.add_relationship(
            Relationship(editor, issue, "issues", EXACTLY_ONE_TO_MANY, Direction.BELOW, ["publication-date"]), True
        )
    except ValueError:
        assert diag.entities == [journal]

    diag.add_relationship(Relationship(journal, editor, "edited-by", MANY_TO_EXACTLY_ONE, Direction.RIGHT))
    assert diag.entities == [journal, editor]

    print(diag.to_latex())


if __name__ == "__main__":
    test_add_entity()
    print("-----------------------------------------------------------------")
    test_add_relationship()
    print("-----------------------------------------------------------------")
