"""Test: Creates ERD with one entity and produces pdf/tex output."""

import os

from texonomy import Entity, ERDiagram

journal = Entity("Journal", ["name", "ISBN number", "title"])
journal.set_primary("ISBN number")

diag = ERDiagram(journal)

with open("entity.tex", "w") as er:
    er.write(diag.to_latex())

os.system("pdflatex entity.tex")
