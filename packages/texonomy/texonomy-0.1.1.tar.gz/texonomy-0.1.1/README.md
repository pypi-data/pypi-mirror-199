# texonomy

`texonomy`* is a Python tool that facilitates the generation of
entity-relationship diagrams in $\LaTeX$ using TikZ.

[![License](https://img.shields.io/github/license/basseches/texonomy)](https://github.com/basseches/texonomy)
[![Build Status](https://github.com/basseches/texonomy/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/basseches/texonomy/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/basseches/texonomy/branch/main/graph/badge.svg)](https://codecov.io/gh/basseches/texonomy)

*An entity-relationship diagram is more of an ontology than a taxonomy, but
when the shoe fits...

## Overview

Writing $\LaTeX$ code can be tedious; `texonomy` makes it easier. This tool
generates entity-relationship diagrams in $\LaTeX$ using a beginner-friendly
Python interface, so you can spend less time wrestling with missing semicolons.

## Prerequisites

To install `texonomy`, you'll need `python3.8` or higher and `pip`.

In order to output as a PDF, you'll need to install some software that includes
`pdflatex`, like TeX Live (recommended):

```sh
sudo apt install texlive
sudo apt-get install texlive-pictures # for TikZ
sudo apt-get install texlive-plain-generic # for ulem
```

## Getting started

Install `texonomy` with the following command:

```sh
pip install texonomy
```

### Example usage

Let's create a very simple program with `texonomy`. First, we'll create
an Entity object to represent a fruit:

```py
fruit = Entity("Fruit", ["SKU", "name", "price", "origin"])
```

The first argument is the entity's name, "Fruit". The second argument is a
list of the entity's attributes.

Let's create a diagram that contains our fruit entity...

```py
diag = ERDiagram(fruit)
```

...and output the generated $\LaTeX$ to a file!

```py
with open("fruit.tex", "w") as er:
    er.write(diag.to_latex())
```

Then, you can run `pdflatex` (or something similar) on the command line to
generate a PDF from this $\LaTeX$:

```sh
pdflatex fruit.tex
```

<img width="150" alt="Screen Shot 2023-03-26 at 8 18 18 PM" src="https://user-images.githubusercontent.com/59753614/227814129-0fa23181-eb29-44a7-b2de-3028484a1396.png">

It's that simple! Take a look at the programs in `texonomy/tests/integration_tests`
for more examples of API usage.
