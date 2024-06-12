LABELSET_KEYS = {"classes", "name", "autoLabelProvider"}
CLASS_KEYS = {"id", "name", "captionAllowed", "captionRequired", "color", "questions"}
QUESTION_KEYS = {"id", "label", "required", "type", "config", "internalId"}
DROPDOWN_KEYS = {"defaultValue", "multiple", "options"}
TEXT_KEYS = {"defaultValue", "multiline", "multiple"}
OPTION_KEYS = {"id", "label", "parentId"}


def validate_bbox_labelset(bbox_labelset: dict):
    assertKeys(bbox_labelset, LABELSET_KEYS, "labelset object")
    if "classes" not in bbox_labelset:
        raise AssertionError("expected classes in labelset")

    for index, labelclass in enumerate(bbox_labelset["classes"]):
        assertKeys(labelclass, CLASS_KEYS, f"labelclass: {index}")
        if "name" not in labelclass:
            raise AssertionError("expected name in labelclass")

        for question in labelclass.get("questions", []):
            assertExact(
                question,
                QUESTION_KEYS,
                f"question of label: {labelclass['name']}",
            )

            if question["type"] == "DROPDOWN":
                assertDropdownQuestion(question)

            if question["type"] == "TEXT":
                assertKeys(
                    question["config"],
                    TEXT_KEYS,
                    f"config of question: {question['label']}",
                )


def assertDropdownQuestion(question: dict):
    assertKeys(
        question["config"],
        DROPDOWN_KEYS,
        f"config of question {question['label']}",
    )

    if not isinstance(question["config"]["options"], list):
        raise AssertionError(
            f"expects options as a list, received {type(question['config']['options'])}"
        )

    for opt in question["config"]["options"]:
        assertKeys(
            opt,
            OPTION_KEYS,
            f"options of question {question['label']}",
        )


def assertKeys(dict: dict, valid_keys: set, identifier: str | None = None):
    """
    Ensure that dict keys are subset of valid_keys
    """
    keys = set(dict.keys())
    if not keys.issubset(valid_keys):
        raise AssertionError(
            f"Invalid keys detected in {identifier}: {keys.difference(valid_keys)}"
        )


def assertExact(dict: dict, valid_keys: set, identifier: str | None = None):
    """
    Ensure that dict keys are exactly equal to valid_keys
    """
    keys = set(dict.keys())
    if not keys == valid_keys:
        if keys.issubset(valid_keys):
            raise AssertionError(
                f"Missing keys detected in {identifier}: {valid_keys.difference(keys)}"
            )
        raise AssertionError(
            f"Excess keys detected in {identifier}: {keys.difference(valid_keys)}"
        )
