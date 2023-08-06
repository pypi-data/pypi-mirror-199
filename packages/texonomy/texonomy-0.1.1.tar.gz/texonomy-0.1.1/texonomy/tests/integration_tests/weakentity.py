"""Test: Creates ERD with a weak entity."""

import os

from texonomy import Entity, Relationship, ERDiagram, EXACTLY_ONE_TO_MANY, Direction

journal = Entity("Journal", ["name", "ISBN number", "title"])
journal.set_primary("ISBN number")

# Issue is a weak entity.
issue = Entity("Issue", ["issue-num"], True)

diag = ERDiagram(journal)

# The last boolean param (optional) is set to true to indicate that this is a
# defining relationship.
diag.add_relationship(Relationship(journal, issue, "issues", EXACTLY_ONE_TO_MANY, Direction.BELOW), True)

with open("weakentity.tex", "w") as er:
    er.write(diag.to_latex())

os.system("pdflatex weakentity.tex")
