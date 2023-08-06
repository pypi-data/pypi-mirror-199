from texonomy import (
    determine_line_type,
    ONE_TO_ONE,
    ONE_TO_MANY,
    MANY_TO_ONE,
    MANY_TO_MANY,
    MANY_TO_EXACTLY_ONE,
    EXACTLY_ONE_TO_MANY,
)


def test_line_type() -> None:
    """
    Unit test for the determine_line_type() function.
    """
    assert determine_line_type(MANY_TO_MANY, 0) == "one line"
    assert determine_line_type(MANY_TO_MANY, 1) == "one line"

    assert determine_line_type(ONE_TO_MANY, 1) == "one line"
    assert determine_line_type(MANY_TO_ONE, 0) == "one line"

    assert determine_line_type(ONE_TO_ONE, 0) == "one line arrow"
    assert determine_line_type(ONE_TO_ONE, 1) == "one line arrow"

    assert determine_line_type(ONE_TO_MANY, 0) == "one line arrow"
    assert determine_line_type(MANY_TO_ONE, 1) == "one line arrow"

    assert determine_line_type(EXACTLY_ONE_TO_MANY, 0) == "one line arrow"
    assert determine_line_type(MANY_TO_EXACTLY_ONE, 1) == "one line arrow"

    assert determine_line_type(EXACTLY_ONE_TO_MANY, 1) == "double line"
    assert determine_line_type(MANY_TO_EXACTLY_ONE, 0) == "double line"
