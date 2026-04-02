from mordor.taxonomy import ISO_42001_CONTROLS, HARM_TO_ISO_42001, get_iso_42001_control


def test_iso_42001_has_nine_controls():
    assert len(ISO_42001_CONTROLS) == 9


def test_iso_42001_controls_a2_through_a10():
    for i in range(2, 11):
        assert f"A.{i}" in ISO_42001_CONTROLS


def test_iso_42001_entries_have_name_and_description():
    for code, entry in ISO_42001_CONTROLS.items():
        assert "name" in entry, f"{code} missing name"
        assert "description" in entry, f"{code} missing description"


def test_harm_to_iso_maps_to_valid_controls():
    valid_controls = set(ISO_42001_CONTROLS.keys())
    for harm, control in HARM_TO_ISO_42001.items():
        assert control in valid_controls, f"{harm} maps to invalid control '{control}'"


def test_get_iso_42001_control_known():
    assert get_iso_42001_control("pii-extraction") == "A.7"
    assert get_iso_42001_control("agentic-risks") == "A.10"


def test_get_iso_42001_control_unknown():
    assert get_iso_42001_control("nonexistent") == "A.5"
