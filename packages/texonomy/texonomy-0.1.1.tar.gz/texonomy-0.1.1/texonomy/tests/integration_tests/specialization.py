"""Test: Creates ERD with a generalization/specialization relationship."""

import os

from texonomy import Entity, ERDiagram

author = Entity("Author", ["name", "author-id"])
author.set_primary("author-id")
contact_author = Entity("Contact author", ["contact email"])

diag = ERDiagram(author)

diag.add_specialization(author, contact_author)

with open("specialization.tex", "w") as er:
    er.write(diag.to_latex())

os.system("pdflatex specialization.tex")
