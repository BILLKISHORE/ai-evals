from mordor.taxonomy import MAESTRO_LAYERS, ATTACK_MAESTRO_MAPPINGS, get_maestro_layer_name


def test_maestro_has_seven_layers():
    assert len(MAESTRO_LAYERS) == 7


def test_maestro_has_all_layer_codes():
    for i in range(1, 8):
        assert f"L{i}" in MAESTRO_LAYERS


def test_maestro_entries_have_name_and_description():
    for code, entry in MAESTRO_LAYERS.items():
        assert "name" in entry, f"{code} missing name"
        assert "description" in entry, f"{code} missing description"


def test_get_maestro_layer_name():
    assert get_maestro_layer_name("L1") == "Foundation Models"
    assert get_maestro_layer_name("L4") == "Tool Integration"
    assert get_maestro_layer_name("L7") == "Agent Ecosystem"


def test_get_maestro_layer_name_unknown():
    assert get_maestro_layer_name("L99") == "Unknown"


def test_attack_maestro_mappings_use_valid_layers():
    valid_layers = set(MAESTRO_LAYERS.keys())
    for attack_id, layers in ATTACK_MAESTRO_MAPPINGS.items():
        for layer in layers:
            assert layer in valid_layers, f"Attack '{attack_id}' maps to invalid layer '{layer}'"
