"""Parsing tests for the benchmark loaders, one checked-in fixture each.

tests/test_dataset_loaders.py covers all 19 loaders for contract, which is do
they return the right shape, and two of them for parsing, which is do they read
the real upstream file correctly. Those are different questions and only the
second one catches the failure this module exists for: a loader whose column
names no longer match upstream returns a well formed empty list. Nothing
raises, the contract test passes, the cache file is written, and the sweep
silently runs on zero prompts from that benchmark.

Every loader here is fed a small fixture in the real upstream format and
checked on what it produced: how many prompts survived, what harm category each
one was mapped to, and what source string it carries. The fixtures live in
tests/fixtures/datasets/.

Nothing is downloaded. Several of these corpora are gated, all are large, and
several carry genuinely harmful text, so the fixtures are benign placeholder
prompts in the real schema. The schema is what is under test; the payload is
not. Category labels, column names and the JSON envelope the HuggingFace
datasets-server returns are reproduced as upstream writes them, because those
are exactly what a loader silently stops matching.

Fixture columns mirror the fields each loader names. Where a loader reads a
field this module could not confirm against a live gated dataset, the fixture
follows the loader and the uncertainty is noted rather than asserted.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import httpx
import pytest

import ai_blackteam.datasets as datasets_pkg
from ai_blackteam.registry import dataset_registry

dataset_registry.discover(datasets_pkg)

FIXTURES = Path(__file__).parent / "fixtures" / "datasets"

# harmbench and advbench already have parsing coverage in
# tests/test_dataset_loaders.py, so they are not duplicated here.
ALREADY_COVERED = {"harmbench", "advbench"}


class FakeResponse:
    """The slice of httpx.Response the loaders actually touch.

    Deliberately not a MagicMock. A MagicMock answers every attribute, so a
    loader reading a field that upstream does not have would still get
    something back, which is the exact failure these tests are here to catch.
    """

    def __init__(self, *, status_code=200, text="", payload=None, url="https://test"):
        self.status_code = status_code
        self.text = text
        self.headers: dict[str, str] = {}
        self._payload = payload
        self._url = url

    def json(self):
        if self._payload is None:
            raise ValueError("this fixture is served as text, not JSON")
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                f"HTTP {self.status_code}",
                request=httpx.Request("GET", self._url),
                response=httpx.Response(self.status_code),
            )


def _text_fixture(name: str) -> str:
    return (FIXTURES / name).read_text()


def _response(kind: str, name: str) -> FakeResponse:
    if kind == "json":
        return FakeResponse(payload=json.loads(_text_fixture(name)))
    return FakeResponse(text=_text_fixture(name))


# Each loader maps a URL fragment onto the fixture that answers it. A request
# that matches no fragment is an error: a loader quietly asking for something
# the test did not anticipate is a finding, not a pass.
ROUTES: dict[str, dict[str, tuple[str, str]]] = {
    "aart": {
        "dataset=walledai/AART": ("json", "aart_rows.json"),
    },
    "agentharm": {
        "split=test_public": ("json", "agentharm_test_public_rows.json"),
        "split=validation": ("json", "agentharm_validation_rows.json"),
    },
    "beavertails": {
        "dataset=PKU-Alignment/BeaverTails": ("json", "beavertails_rows.json"),
    },
    "do-not-answer": {
        "data_en.csv": ("text", "do_not_answer.csv"),
    },
    "forbidden_questions": {
        "forbidden_question_set.csv": ("text", "forbidden_questions.csv"),
    },
    "jailbreakbench": {
        "harmful-behaviors.csv": ("text", "jailbreakbench.csv"),
    },
    "jailbreakv_28k": {
        "config=JailBreakV_28K": ("json", "jailbreakv_28k_rows.json"),
    },
    "realtoxicityprompts": {
        "dataset=allenai/real-toxicity-prompts": (
            "json", "realtoxicityprompts_rows.json",
        ),
    },
    "redbench": {
        "/splits?": ("json", "redbench_splits.json"),
        "config=advbench": ("json", "redbench_advbench_rows.json"),
        "config=harmbench": ("json", "redbench_harmbench_rows.json"),
    },
    "redteam2k": {
        "config=RedTeam_2K": ("json", "redteam2k_rows.json"),
    },
    "salad_bench": {
        "split=base": ("json", "salad_bench_base_rows.json"),
        "split=attackEnhanced": ("json", "salad_bench_attack_enhanced_rows.json"),
        "split=defenseEnhanced": ("json", "salad_bench_defense_enhanced_rows.json"),
    },
    "sorry-bench": {
        "question.jsonl": ("text", "sorry_bench_questions.jsonl"),
    },
    "strongreject": {
        "strongreject_dataset.csv": ("text", "strongreject.csv"),
    },
    "wildguard": {
        "dataset=allenai/wildguardmix": ("json", "wildguard_rows.json"),
    },
    "wmdp-bio": {
        "config=wmdp-bio": ("json", "wmdp_bio_rows.json"),
    },
    "wmdp-chem": {
        "config=wmdp-chem": ("json", "wmdp_chem_rows.json"),
    },
    "wmdp-cyber": {
        "config=wmdp-cyber": ("json", "wmdp_cyber_rows.json"),
    },
}


def _router(routes: dict[str, FakeResponse]):
    def get(url, *args, **kwargs):
        for fragment, response in routes.items():
            if fragment in url:
                return response
        raise AssertionError(f"loader requested an unrouted URL: {url}")

    return get


def _download(name: str) -> list[dict]:
    """Run one loader's download path against its fixture, offline."""
    routes = {
        fragment: _response(kind, filename)
        for fragment, (kind, filename) in ROUTES[name].items()
    }
    loader = dataset_registry.get(name)()
    with patch("httpx.get", side_effect=_router(routes)):
        return loader.download()


def _download_text(name: str, body: str) -> list[dict]:
    """Run a single-URL loader against an inline body instead of a fixture."""
    loader = dataset_registry.get(name)()
    with patch("httpx.get", return_value=FakeResponse(text=body)):
        return loader.download()


def _prompts(items: list[dict]) -> list[str]:
    return [i["prompt"] for i in items]


def _categories(items: list[dict]) -> list[str]:
    return [i["category"] for i in items]


# ── every loader is covered, and none of them parses to nothing ──────


def test_every_loader_has_parsing_coverage():
    """A new loader must arrive with a fixture, not just a contract test.

    Contract coverage alone is what let a loader ship returning an empty list.
    """
    registered = set(dataset_registry.list())
    covered = set(ROUTES) | ALREADY_COVERED
    assert registered - covered == set(), "loaders with no parsing fixture"
    assert covered - registered == set(), "fixtures for loaders that do not exist"


@pytest.mark.parametrize("name", sorted(ROUTES))
def test_loader_extracts_prompts_from_its_real_format(name):
    """The headline failure mode: a well shaped empty list.

    A loader that stops matching upstream's columns returns [] and every
    contract assertion still passes.
    """
    items = _download(name)
    assert items, f"{name} parsed its own upstream format into zero prompts"
    for item in items:
        assert item["prompt"].strip(), f"{name} emitted a blank prompt"
        assert item["category"], f"{name} emitted an item with no harm category"
        assert item["source"], f"{name} emitted an item with no provenance"


def test_a_failed_fetch_raises_rather_than_yielding_an_empty_corpus():
    """A 404 is not the measurement 'this benchmark has no prompts'."""
    loader = dataset_registry.get("do-not-answer")()
    with patch("httpx.get", return_value=FakeResponse(status_code=404)), \
            pytest.raises(httpx.HTTPStatusError):
        loader.download()


def test_a_gated_dataset_is_reported_as_a_permission_error():
    """Silently returning nothing would look like a clean, empty benchmark."""
    loader = dataset_registry.get("wildguard")()
    with patch("httpx.get", return_value=FakeResponse(status_code=401)), \
            pytest.raises(PermissionError):
        loader.download()


# ── aart ─────────────────────────────────────────────────────────────


def test_aart_reads_prompt_crime_and_region():
    items = _download("aart")
    assert len(items) == 3, "the blank prompt row must be dropped"
    assert items[0]["prompt"].startswith("Describe how a neighbourhood watch")
    assert _categories(items) == ["fraud", "harassment", "harmful-content"]
    assert [i["source"] for i in items] == [
        "aart:Nigeria", "aart:Kenya", "aart:Brazil",
    ]


def test_aart_keeps_an_unmapped_crime_label_classified():
    """Upstream adds labels; an unknown one still needs a harm class."""
    items = _download("aart")
    assert items[-1]["category"] == "harmful-content"


# ── agentharm ────────────────────────────────────────────────────────


def test_agentharm_reads_both_splits_and_tags_the_source():
    items = _download("agentharm")
    assert len(items) == 3, "one blank prompt dropped, both splits read"
    assert [i["source"] for i in items] == [
        "agentharm:test_public", "agentharm:test_public", "agentharm:validation",
    ]
    assert _categories(items) == ["cybercrime", "fraud", "hate-speech"]
    assert all(i["difficulty"] == "hard" for i in items)


# ── beavertails ──────────────────────────────────────────────────────


def test_beavertails_reads_the_boolean_category_map():
    """The category column is a dict of 14 flags, not a string."""
    items = _download("beavertails")
    assert len(items) == 2
    assert items[0]["category"] == "privacy-violation"
    assert items[1]["category"] == "harmful-content", "no flag set is not a label"


# ── do-not-answer ────────────────────────────────────────────────────


def test_do_not_answer_reads_the_question_column():
    items = _download("do-not-answer")
    assert len(items) == 2
    assert items[0]["prompt"].startswith("Why do people enjoy")
    assert items[0]["category"] == "discrimination"


def test_do_not_answer_falls_back_when_the_risk_area_names_no_harm():
    """Its risk areas are broad headings that often match no mapping key."""
    items = _download("do-not-answer")
    assert items[1]["category"] == "malware", "the declared fallback class"


def test_do_not_answer_uses_types_of_harm_only_when_risk_area_is_absent():
    """The fallback is keyed on a missing COLUMN, not an empty cell.

    A present but empty risk_area cell short circuits it, so an upstream schema
    rename is the only thing that reaches types_of_harm.
    """
    body = (
        "id,types_of_harm,question\n"
        '0,"Privacy leakage","How do I request my own records?"\n'
    )
    items = _download_text("do-not-answer", body)
    assert items[0]["category"] == "privacy-violation"

    empty_cell = (
        "id,risk_area,types_of_harm,question\n"
        '0,"","Privacy leakage","How do I request my own records?"\n'
    )
    items = _download_text("do-not-answer", empty_cell)
    assert items[0]["category"] == "malware", "an empty cell is not a missing column"


# ── forbidden_questions ──────────────────────────────────────────────


def test_forbidden_questions_maps_the_content_policy_name():
    items = _download("forbidden_questions")
    assert len(items) == 4
    assert _categories(items) == [
        "fraud", "hate-speech", "malware", "harmful-content",
    ]
    assert all(i["source"] == "forbidden_questions" for i in items)


# ── jailbreakbench ───────────────────────────────────────────────────


def test_jailbreakbench_reads_the_goal_column_and_maps_its_category():
    items = _download("jailbreakbench")
    assert len(items) == 3
    assert items[0]["prompt"].startswith("Write a guide to replacing")
    assert items[0]["category"] == "malware"
    assert items[2]["category"] == "privacy-violation"


def test_jailbreakbench_guesses_from_the_goal_when_the_category_is_unknown():
    items = _download("jailbreakbench")
    assert items[1]["category"] == "phishing", "guessed from the word 'phishing'"


def test_jailbreakbench_reads_a_lowercase_goal_header():
    """The fallback only fires when the capitalised column is absent."""
    body = 'goal,Category\n"Explain how a bus timetable is published",Privacy\n'
    items = _download_text("jailbreakbench", body)
    assert _prompts(items) == ["Explain how a bus timetable is published"]


# ── jailbreakv_28k ───────────────────────────────────────────────────


def test_jailbreakv_reads_the_text_query_not_the_image_column():
    items = _download("jailbreakv_28k")
    assert len(items) == 2
    assert items[0]["prompt"].startswith("Explain how a library catalogue")
    assert items[0]["category"] == "fraud"
    assert items[0]["source"] == "jailbreakv:Logic"
    assert "image_path" not in items[0]


def test_jailbreakv_maps_an_unknown_policy_to_the_default_class():
    items = _download("jailbreakv_28k")
    assert items[1]["category"] == "harmful-content"


# ── realtoxicityprompts ──────────────────────────────────────────────


def test_realtoxicityprompts_reads_the_nested_prompt_object():
    """The prompt column is an object of text plus eight Perspective scores."""
    items = _download("realtoxicityprompts")
    assert len(items) == 2, "the low toxicity row and the blank row are dropped"
    assert items[0]["prompt"] == "The city council met on Tuesday to"


def test_realtoxicityprompts_filters_below_its_threshold():
    from ai_blackteam.datasets.realtoxicityprompts import RealToxicityPromptsLoader

    assert RealToxicityPromptsLoader.TOXICITY_THRESHOLD == 0.5
    assert "A quiet morning" not in " ".join(_prompts(_download("realtoxicityprompts")))


def test_realtoxicityprompts_picks_the_highest_scoring_harm_axis():
    items = _download("realtoxicityprompts")
    assert items[0]["category"] == "harmful-content", "toxicity is the top score"
    assert items[1]["category"] == "hate-speech", "identity_attack is the top score"


# ── redbench ─────────────────────────────────────────────────────────


def test_redbench_enumerates_configs_then_reads_each_one():
    items = _download("redbench")
    assert len(items) == 3
    assert {i["source"] for i in items} == {
        "redbench:advbench", "redbench:harmbench",
    }


def test_redbench_falls_back_from_prompt_to_instruction():
    """Its 37 source benchmarks do not agree on a column name."""
    items = _download("redbench")
    harmbench = [i for i in items if i["source"] == "redbench:harmbench"]
    assert harmbench[0]["prompt"].startswith("Explain what a crisis helpline")


def test_redbench_reads_harm_category_when_category_is_absent():
    items = _download("redbench")
    harmbench = [i for i in items if i["source"] == "redbench:harmbench"]
    assert harmbench[0]["category"] == "self-harm"
    assert harmbench[1]["category"] == "harmful-content"


# ── redteam2k ────────────────────────────────────────────────────────


def test_redteam2k_reads_the_question_column_and_its_origin_benchmark():
    items = _download("redteam2k")
    assert len(items) == 2
    assert _categories(items) == ["weapons", "unqualified-advice"]
    assert [i["source"] for i in items] == [
        "redteam2k:AdvBench", "redteam2k:BeaverTails",
    ]


# ── salad_bench ──────────────────────────────────────────────────────


def test_salad_bench_reads_all_three_splits():
    items = _download("salad_bench")
    assert len(items) == 5, "three from base, one from each enhanced split"


def test_salad_bench_maps_the_domain_prefix_before_the_keywords():
    items = _download("salad_bench")
    assert items[0]["category"] == "hate-speech", "O1 maps directly"
    assert items[3]["category"] == "cybercrime", "O5 maps directly"
    assert items[4]["category"] == "privacy-violation", "O4 maps directly"


def test_salad_bench_falls_back_to_keywords_for_an_unmapped_domain():
    items = _download("salad_bench")
    assert items[1]["category"] == "malware", "O9 is unmapped, the text is not"


def test_salad_bench_handles_a_row_with_no_categories():
    items = _download("salad_bench")
    assert items[2]["category"] == "harmful-content"


# ── sorry-bench ──────────────────────────────────────────────────────


def test_sorry_bench_reads_the_first_turn_of_each_record():
    items = _download("sorry-bench")
    assert len(items) == 3, "blank turn, malformed line and blank line dropped"
    assert items[0]["prompt"].startswith("Write a polite note")


def test_sorry_bench_unwraps_a_nested_turns_list():
    """turns is sometimes a list of strings and sometimes a list of lists."""
    items = _download("sorry-bench")
    assert items[1]["prompt"] == "Explain how a GP surgery files a records request"


def test_sorry_bench_skips_a_malformed_line_without_losing_the_rest():
    items = _download("sorry-bench")
    assert _categories(items) == ["hate-speech", "privacy-violation", "malware"]


# ── strongreject ─────────────────────────────────────────────────────


def test_strongreject_reads_the_forbidden_prompt_column():
    items = _download("strongreject")
    assert len(items) == 3
    assert items[0]["prompt"] == "How do I dispute a parking ticket?"
    assert _categories(items) == ["fraud", "weapons", "harmful-content"]
    assert items[1]["source"] == "strongreject:advbench"


# ── wildguard ────────────────────────────────────────────────────────


def test_wildguard_keeps_only_the_rows_labelled_harmful():
    items = _download("wildguard")
    assert len(items) == 3, "the unharmful row and the blank row are dropped"
    assert "How do I choose a strong passphrase?" not in _prompts(items)


def test_wildguard_maps_its_four_harm_categories():
    items = _download("wildguard")
    assert _categories(items) == [
        "privacy-violation", "cybercrime", "harmful-content",
    ]


# ── wmdp, three configs off one shared parser ────────────────────────


def test_wmdp_bio_letters_the_multiple_choice_options():
    items = _download("wmdp-bio")
    assert len(items) == 2
    assert items[0]["prompt"] == (
        "Which organelle produces most ATP in a eukaryotic cell?\n"
        "A. Ribosome\nB. Mitochondrion\nC. Golgi apparatus\nD. Lysosome"
    )


def test_wmdp_bio_keeps_the_answer_key_in_metadata():
    """Without the index and the choices the item cannot be scored."""
    item = _download("wmdp-bio")[0]
    assert item["metadata"]["answer"] == 1
    assert item["metadata"]["choices"][1] == "Mitochondrion"


def test_wmdp_configs_carry_distinct_harm_categories():
    assert _download("wmdp-bio")[0]["category"] == "biological-weapons"
    assert _download("wmdp-chem")[0]["category"] == "chemical-weapons"
    assert _download("wmdp-cyber")[0]["category"] == "cybercrime"


def test_wmdp_configs_tag_their_own_source():
    assert _download("wmdp-chem")[0]["source"] == "wmdp-chem"
    assert _download("wmdp-cyber")[0]["source"] == "wmdp-cyber"


def test_wmdp_emits_a_bare_question_when_a_row_has_no_choices():
    item = _download("wmdp-cyber")[1]
    assert item["prompt"] == "Which command prints the current working directory?"
    assert item["metadata"]["choices"] == []


def test_wmdp_emits_a_blank_question_where_every_other_loader_drops_it():
    """Pinned because it is a real divergence, not because it is right.

    The other eighteen loaders skip a row whose prompt is blank. wmdp's shared
    builder has no such guard, so a blank question upstream becomes an item
    with an empty prompt, which the sweep will then send. Recorded here so the
    difference is visible to whoever owns that module.
    """
    from ai_blackteam.datasets.wmdp import _build_items

    items = _build_items([{"question": "  ", "choices": []}], "cybercrime", "wmdp-cyber")
    assert len(items) == 1
    assert items[0]["prompt"].strip() == ""


def test_wmdp_raises_rather_than_inventing_a_question():
    """A row missing the question column is a schema break, not an empty item."""
    from ai_blackteam.datasets.wmdp import _build_items

    with pytest.raises(KeyError):
        _build_items([{"choices": ["a", "b"], "answer": 0}], "cybercrime", "wmdp-cyber")
