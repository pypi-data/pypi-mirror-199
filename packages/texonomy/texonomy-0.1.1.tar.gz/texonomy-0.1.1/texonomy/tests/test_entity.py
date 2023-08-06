from texonomy import Entity


def test_init() -> None:
    """
    Unit test for the Entity class' __init__ function.
    """
    student = Entity("Student", ["id", "name", "major", "grad_year"])
    assert student.attributes[student.primary] == "id"
    assert not student.weak
    print(student)

    contact = Entity("Contact", ["id", "name", "phone"], True)
    assert contact.weak
    print(contact)

    instructor = Entity("Instructor", [])
    assert instructor.primary == -1
    assert not instructor.weak
    print(instructor)


def test_primary() -> None:
    """
    Unit test for the Entity class' set_primary() function.
    """
    student = Entity("Student", ["name", "id", "major", "grad_year"])
    assert student.attributes[student.primary] == "name"

    # Setting the primary to an attribute.
    student.set_primary("id")
    assert student.attributes[student.primary] == "id"
    print(student)

    # Trying to set the primary to an attribute that doesn't exist.
    try:
        student.set_primary("gpa")
    except ValueError:
        assert student.attributes[student.primary] == "id"
    print(student)

    # Setting the primary to an added attribute.
    student.add_attribute("gpa")
    student.set_primary("gpa")
    assert student.attributes[student.primary] == "gpa"
    print(student)


if __name__ == "__main__":
    test_init()
    print("-----------------------------------------------------------------")
    test_primary()
    print("-----------------------------------------------------------------")
