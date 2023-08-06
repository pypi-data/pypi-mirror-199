from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from . import templates

# Levels of indentation for LaTeX code
INDENTATION = [" " * 4 * i for i in range(5)]

# Some common cardinalities.
ONE_TO_ONE = ((0, 1), (0, 1))
ONE_TO_MANY = ((0, -1), (0, 1))
MANY_TO_ONE = ((0, 1), (0, -1))
MANY_TO_MANY = ((0, -1), (0, -1))
MANY_TO_EXACTLY_ONE = ((1, 1), (0, -1))
EXACTLY_ONE_TO_MANY = ((0, -1), (1, 1))


class Direction(Enum):
    ABOVE = "above"
    BELOW = "below"
    RIGHT = "right"
    LEFT = "left"


@dataclass
class Entity:
    name: str
    attributes: List[str]
    primary: int  # index into attributes list
    weak: bool

    def __init__(self, name: str, attributes: List[str], weak: bool = False) -> None:
        self.name = name
        self.weak = weak
        self.attributes = []
        for attribute in attributes:
            self.attributes.append(attribute)
        # the first attrib specified will defualt to the primary key
        self.primary = 0 if self.attributes else -1

    def __str__(self) -> None:
        return (
            f"{self.name} ({'Weak ' if self.weak else ''}Entity)\n"
            f"Attributes: {self.attributes}\n\n"
            f"Primary: {'None' if self.primary == -1 else self.attributes[self.primary]}"
        )

    def add_attribute(self, attribute: str) -> None:
        self.attributes.append(attribute)

    def set_primary(self, attribute: str) -> None:
        for idx, att in enumerate(self.attributes):
            if att == attribute:
                self.primary = idx
                return
        raise ValueError("This attribute doesn't exist.")

    # TODO: deal with empty attributes
    def to_latex(self) -> str:
        code = f"{{{'weak' if self.weak else ''}" f"entity={{{id(self)}}}{{{self.name}}}{{%"
        for idx, attribute in enumerate(self.attributes):
            code += f"\n{INDENTATION[-1]}"
            code += (
                fr"\{'dashuline' if self.weak else 'underline'}" fr"{{{attribute}}}\\"
                if idx == self.primary
                else fr"{attribute}\\"
            )
        return code + f"\n{INDENTATION[-2]}}}}};"


@dataclass
class Relationship:
    anchor: Entity
    new_entity: Entity
    label: str
    cardinality: Tuple[Tuple[int, int], Tuple[int, int]]
    direction: Direction
    attributes: Optional[List[str]] = None

    def __str__(self):
        return f"{self.label}: [{self.anchor.name} to {self.new_entity.name}]"

    def add_attribute(self, attribute: str) -> None:
        self.attributes.append(attribute)

    def attributes_to_latex(self) -> str:
        code = f"{{relattribute={{a{id(self)}}}{{%"

        if len(self.attributes) == 1:
            return code + f"\n{INDENTATION[-1]}{self.attributes[0]}\n" f"{INDENTATION[-2]}}}}};"

        for attribute in self.attributes:
            code += f"\n{INDENTATION[-1]}{attribute}"
            code += r"\\"

        return code + f"\n{INDENTATION[-2]}}}}};"


def determine_line_type(cardinality: Tuple[Tuple[int, int], Tuple[int, int]], direction: int) -> str:
    if cardinality[0 + direction][0] == 0:
        if cardinality[1 - direction][1] == 1:
            return "one line arrow"
        elif cardinality[1 - direction][1] == -1:
            return "one line"
        else:
            # TODO: label line with cardinality in the form x..y
            raise ValueError("Unsupported cardinality")
    elif cardinality[0 + direction][0] == 1:
        # total participation
        if cardinality[1 - direction][1] == 1:
            return "double line arrow"
        elif cardinality[1 - direction][1] == -1:
            return "double line"
        else:
            # TODO: label line with cardinality in the form x..y
            raise ValueError("Unsupported cardinality")


def get_line_anchors(direction: Direction) -> Tuple[str, str]:
    if direction == Direction.ABOVE:
        return ("south", "north")
    if direction == Direction.BELOW:
        return ("north", "south")
    if direction == Direction.RIGHT:
        return ("west", "east")
    if direction == Direction.LEFT:
        return ("east", "west")


@dataclass
class ERDiagram:
    entities: List[Entity]
    code: str

    def __init__(self, entity: Entity) -> None:
        self.entities = [entity]
        self.code = fr"{INDENTATION[-2]}\pic {entity.to_latex()}" + "\n"

    def add_relationship(self, rel: Relationship, defining: bool = False) -> None:
        if rel.anchor not in self.entities:
            raise ValueError("Anchor does not exist in the diagram.")
        self.entities.append(rel.new_entity)

        # TODO: add space changing option

        # render relationship diamond
        self.code += (
            fr"{INDENTATION[-2]}\pic[{rel.direction.value}=3em "
            f"of {id(rel.anchor)}] {{{'def' if defining else ''}"
            f"relationship={{{id(rel)}}}{{{rel.label}}}}};\n"
        )

        # render other entity
        self.code += fr"{INDENTATION[-2]}\pic[{rel.direction.value}=3em "
        self.code += f"of {id(rel)}] {rel.new_entity.to_latex()}\n"

        line_type_one = determine_line_type(rel.cardinality, 0)
        line_type_two = determine_line_type(rel.cardinality, 1)
        line_anchors = get_line_anchors(rel.direction)

        # render line between anchor entity and relationship
        self.code += (
            fr"{INDENTATION[-2]}\draw[{line_type_one}] "
            f"({id(rel)}.{line_anchors[0]}) -- "
            f"({id(rel.anchor)}.{line_anchors[1]});\n"
        )

        # render line between new entity and relationship
        self.code += (
            fr"{INDENTATION[-2]}\draw[{line_type_two}] "
            f"({id(rel)}.{line_anchors[1]}) -- "
            f"({id(rel.new_entity)}.{line_anchors[0]});\n"
        )

        if rel.attributes:
            direction = (
                Direction.RIGHT
                if rel.direction == Direction.ABOVE or rel.direction == Direction.BELOW
                else Direction.ABOVE
            )

            line_anchors = get_line_anchors(direction)

            # Stick relationship attributes to the right of any vertical
            # relationship, and above any horizontal one.
            self.code += fr"{INDENTATION[-2]}\pic[{direction.value}=2em of "
            self.code += f"{id(rel)}] {rel.attributes_to_latex()}\n"
            # latex node id is "a" + rel id
            self.code += (
                fr"{INDENTATION[-2]}\draw[dashed line] ({id(rel)}."
                f"{line_anchors[1]}) -- (a{id(rel)}."
                f"{line_anchors[0]});\n"
            )

    def add_specialization(self, superclass: Entity, subclass: Entity) -> None:
        if superclass not in self.entities:
            raise ValueError("Anchor does not exist in the diagram.")
        self.entities.append(subclass)

        # add other entity
        self.code += fr"{INDENTATION[-2]}\pic[below=3em of {id(superclass)}]"
        self.code += f" {subclass.to_latex()}\n"
        self.code += fr"{INDENTATION[-2]}\draw[specialization] "
        self.code += f"({id(subclass)}.north) -- ({id(superclass)}.south);\n"

    def to_latex(self) -> str:
        prelude = pkg_resources.read_text(templates, 'template.tex')

        return (
            prelude + f"{INDENTATION[0]}\\begin{{document}}\n"
            f"{INDENTATION[1]}\\begin{{center}}\n"
            f"{INDENTATION[2]}\\begin{{tikzpicture}}\n"
            + self.code
            + f"{INDENTATION[2]}\\end{{tikzpicture}}\n"
            + f"{INDENTATION[1]}\\end{{center}}\n"
            f"{INDENTATION[0]}\\end{{document}}\n"
        )
