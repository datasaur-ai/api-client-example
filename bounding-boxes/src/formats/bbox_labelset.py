LABELSET_KEYS = {"classes", "name", "autoLabelProvider"}
CLASS_KEYS = {"name", "captionAllowed", "captionRequired", "color", "questions"}
QUESTION_KEYS = {"id", "label", "required", "type", "config"}
DROPDOWN_KEYS = {"defaultValue", "multiple", "options"}
TEXT_KEYS = {"defaultValue", "multiline", "multiple"}


def validate_bbox_labelset(bbox_labelset: dict):
    assertKeys(bbox_labelset, LABELSET_KEYS, "top-level object")
    assert "classes" in bbox_labelset, "classes required"

    for index, labelclass in enumerate(bbox_labelset["classes"]):
        assertKeys(labelclass, CLASS_KEYS, f"labelclass {index}")
        assert "name" in labelclass, "name required"

        for question in labelclass["questions"]:
            assertExact(
                question,
                QUESTION_KEYS,
                f"question of label {labelclass['name']}",
            )

            if question["type"] == "DROPDOWN":
                assertDropdownQuestion(question)

            if question["type"] == "TEXT":
                assertKeys(
                    question["config"],
                    TEXT_KEYS,
                    f"config of question {question['label']}",
                )


def assertDropdownQuestion(question: dict):
    assertExact(
        question["config"],
        DROPDOWN_KEYS,
        f"config of question {question['label']}",
    )
    assert isinstance(question["config"]["options"], list)

    for opt in question["config"]["options"]:
        assertKeys(
            opt,
            {"id", "label", "parentId"},
            f"options of question {question['label']}",
        )


def assertKeys(dict: dict, valid_keys: set, identifier: str | None = None):
    """
    Ensure that dict keys are subset of valid_keys
    """
    keys = set(dict.keys())
    assert keys.issubset(
        valid_keys
    ), f"Invalid keys detected in {identifier}: {keys.difference(valid_keys)}"


def assertExact(dict: dict, valid_keys: set, identifier: str | None = None):
    """
    Ensure that dict keys are exactly equal to valid_keys
    """
    keys = set(dict.keys())
    assert (
        keys == valid_keys
    ), f"Invalid keys detected in {identifier}: {keys.difference(valid_keys) or valid_keys.difference(keys)}"
