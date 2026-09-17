"""Universal jailbreak search for multi-question bounty challenges.

Designed for programs like OpenAI Bio Bounty where success means **one seed
prompt** that defeats **every** challenge question from a clean chat without
triggering moderation, not single-target catalog ASR.

Challenge question text is never shipped by this package. Load questions from
a local YAML file after you are authorized by the program (NDA / platform).
"""

from ai_blackteam.universal.challenge import (
    ChallengeSpec,
    load_challenge,
    write_challenge_template,
)
from ai_blackteam.universal.scoring import (
    QuestionResult,
    UniversalScore,
    compose_prompt,
    score_question_response,
    score_universal,
)
from ai_blackteam.universal.search import UniversalSearchResult, search_universal

__all__ = [
    "ChallengeSpec",
    "load_challenge",
    "write_challenge_template",
    "QuestionResult",
    "UniversalScore",
    "compose_prompt",
    "score_question_response",
    "score_universal",
    "UniversalSearchResult",
    "search_universal",
]
