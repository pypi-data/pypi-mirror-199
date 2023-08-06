"""Test: Creates ERD with a relationship that has an attribute."""

import os

from texonomy import Entity, Relationship, ERDiagram, EXACTLY_ONE_TO_MANY, Direction

journal = Entity("Journal", ["name", "ISBN number", "title"])
journal.set_primary("ISBN number")
issue = Entity("Issue", ["issue-num"])

diag = ERDiagram(journal)

diag.add_relationship(
    Relationship(journal, issue, "issues", EXACTLY_ONE_TO_MANY, Direction.BELOW, ["publication-date"])
)

with open("relattr.tex", "w") as er:
    er.write(diag.to_latex())

os.system("pdflatex relattr.tex")
