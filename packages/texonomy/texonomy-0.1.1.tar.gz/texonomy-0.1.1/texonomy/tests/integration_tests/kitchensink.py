"""Test: Creates ERD with, well, everything."""

import os

from texonomy import Entity, ERDiagram, Relationship, Direction, MANY_TO_EXACTLY_ONE, EXACTLY_ONE_TO_MANY

journal = Entity("Journal", ["name", "ISBN number", "title", "pub freq", "subscription price"])
journal.set_primary("ISBN number")

diag = ERDiagram(journal)

editor = Entity("Editor-in-chief", ["name", "personal affiliation", "email"])
editor.set_primary("email")
diag.add_relationship(Relationship(journal, editor, "edited-by", MANY_TO_EXACTLY_ONE, Direction.RIGHT))

issue = Entity("Issue", ["issue-num"], True)
diag.add_relationship(
    Relationship(journal, issue, "issues", EXACTLY_ONE_TO_MANY, Direction.BELOW, ["publication-date"]), True
)

article = Entity("Article", ["doi-identifier", "title", "page range"])
diag.add_relationship(Relationship(issue, article, "contains", ((1, -1), (1, 1)), Direction.RIGHT))

author = Entity("Author", ["name", "author-id"])
author.set_primary("author-id")
diag.add_relationship(Relationship(article, author, "authored-by", ((1, -1), (0, -1)), Direction.BELOW))

contact_author = Entity("Contact author", ["contact email"])
diag.add_specialization(author, contact_author)

with open("kitchensink.tex", "w") as er:
    er.write(diag.to_latex())

os.system("pdflatex kitchensink.tex")
