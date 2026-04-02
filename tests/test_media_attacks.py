"""Tests for 25 media and journalism manipulation attacks."""

import pytest
from mordor.registry import attack_registry
import mordor.attacks.press_release_fabrication  # noqa: F401
import mordor.attacks.interview_fabrication  # noqa: F401
import mordor.attacks.source_fabrication  # noqa: F401
import mordor.attacks.news_headline_manipulation  # noqa: F401
import mordor.attacks.media_attribution_fraud  # noqa: F401
import mordor.attacks.viral_disinfo_campaign  # noqa: F401
import mordor.attacks.clickbait_generation  # noqa: F401
import mordor.attacks.image_caption_manipulation  # noqa: F401
import mordor.attacks.audio_manipulation  # noqa: F401
import mordor.attacks.video_manipulation  # noqa: F401
import mordor.attacks.review_bombing  # noqa: F401
import mordor.attacks.social_media_manipulation  # noqa: F401
import mordor.attacks.influencer_fraud  # noqa: F401
import mordor.attacks.content_farm_generation  # noqa: F401
import mordor.attacks.seo_manipulation  # noqa: F401
import mordor.attacks.podcast_fabrication  # noqa: F401
import mordor.attacks.documentary_fabrication  # noqa: F401
import mordor.attacks.leaked_document_fabrication  # noqa: F401
import mordor.attacks.whistleblower_impersonation  # noqa: F401
import mordor.attacks.crisis_fabrication  # noqa: F401
import mordor.attacks.obituary_fabrication  # noqa: F401
import mordor.attacks.testimony_fabrication  # noqa: F401
import mordor.attacks.brand_impersonation  # noqa: F401
import mordor.attacks.academic_journal_fraud  # noqa: F401
import mordor.attacks.award_fabrication  # noqa: F401
from mordor.attacks.press_release_fabrication import PressReleaseFabrication
from mordor.attacks.interview_fabrication import InterviewFabrication
from mordor.attacks.source_fabrication import SourceFabrication
from mordor.attacks.news_headline_manipulation import NewsHeadlineManipulation
from mordor.attacks.media_attribution_fraud import MediaAttributionFraud
from mordor.attacks.viral_disinfo_campaign import ViralDisinfoCampaign
from mordor.attacks.clickbait_generation import ClickbaitGeneration
from mordor.attacks.image_caption_manipulation import ImageCaptionManipulation
from mordor.attacks.audio_manipulation import AudioManipulation
from mordor.attacks.video_manipulation import VideoManipulation
from mordor.attacks.review_bombing import ReviewBombing
from mordor.attacks.social_media_manipulation import SocialMediaManipulation
from mordor.attacks.influencer_fraud import InfluencerFraud
from mordor.attacks.content_farm_generation import ContentFarmGeneration
from mordor.attacks.seo_manipulation import SeoManipulation
from mordor.attacks.podcast_fabrication import PodcastFabrication
from mordor.attacks.documentary_fabrication import DocumentaryFabrication
from mordor.attacks.leaked_document_fabrication import LeakedDocumentFabrication
from mordor.attacks.whistleblower_impersonation import WhistleblowerImpersonation
from mordor.attacks.crisis_fabrication import CrisisFabrication
from mordor.attacks.obituary_fabrication import ObituaryFabrication
from mordor.attacks.testimony_fabrication import TestimonyFabrication
from mordor.attacks.brand_impersonation import BrandImpersonation
from mordor.attacks.academic_journal_fraud import AcademicJournalFraud
from mordor.attacks.award_fabrication import AwardFabrication

TARGET = "a major technology company's product launch"

ALL_ATTACK_INSTANCES = [
    PressReleaseFabrication(),
    InterviewFabrication(),
    SourceFabrication(),
    NewsHeadlineManipulation(),
    MediaAttributionFraud(),
    ViralDisinfoCampaign(),
    ClickbaitGeneration(),
    ImageCaptionManipulation(),
    AudioManipulation(),
    VideoManipulation(),
    ReviewBombing(),
    SocialMediaManipulation(),
    InfluencerFraud(),
    ContentFarmGeneration(),
    SeoManipulation(),
    PodcastFabrication(),
    DocumentaryFabrication(),
    LeakedDocumentFabrication(),
    WhistleblowerImpersonation(),
    CrisisFabrication(),
    ObituaryFabrication(),
    TestimonyFabrication(),
    BrandImpersonation(),
    AcademicJournalFraud(),
    AwardFabrication(),
]

CRITICAL_INSTANCES = [
    SourceFabrication(),
    ViralDisinfoCampaign(),
    LeakedDocumentFabrication(),
    WhistleblowerImpersonation(),
    CrisisFabrication(),
    TestimonyFabrication(),
    AcademicJournalFraud(),
]

HIGH_INSTANCES = [
    PressReleaseFabrication(),
    InterviewFabrication(),
    NewsHeadlineManipulation(),
    MediaAttributionFraud(),
    ImageCaptionManipulation(),
    AudioManipulation(),
    VideoManipulation(),
    ReviewBombing(),
    SocialMediaManipulation(),
    InfluencerFraud(),
    ContentFarmGeneration(),
    SeoManipulation(),
    PodcastFabrication(),
    DocumentaryFabrication(),
    ObituaryFabrication(),
    BrandImpersonation(),
]

MEDIUM_INSTANCES = [
    ClickbaitGeneration(),
    AwardFabrication(),
]


# ── Registration tests ─────────────────────────────────────────────────

def test_press_release_fabrication_registered():
    assert attack_registry.get("press-release-fabrication") is not None


def test_interview_fabrication_registered():
    assert attack_registry.get("interview-fabrication") is not None


def test_source_fabrication_registered():
    assert attack_registry.get("source-fabrication") is not None


def test_news_headline_manipulation_registered():
    assert attack_registry.get("news-headline-manipulation") is not None


def test_media_attribution_fraud_registered():
    assert attack_registry.get("media-attribution-fraud") is not None


def test_viral_disinfo_campaign_registered():
    assert attack_registry.get("viral-disinfo-campaign") is not None


def test_clickbait_generation_registered():
    assert attack_registry.get("clickbait-generation") is not None


def test_image_caption_manipulation_registered():
    assert attack_registry.get("image-caption-manipulation") is not None


def test_audio_manipulation_registered():
    assert attack_registry.get("audio-manipulation") is not None


def test_video_manipulation_registered():
    assert attack_registry.get("video-manipulation") is not None


def test_review_bombing_registered():
    assert attack_registry.get("review-bombing") is not None


def test_social_media_manipulation_registered():
    assert attack_registry.get("social-media-manipulation") is not None


def test_influencer_fraud_registered():
    assert attack_registry.get("influencer-fraud") is not None


def test_content_farm_generation_registered():
    assert attack_registry.get("content-farm-generation") is not None


def test_seo_manipulation_registered():
    assert attack_registry.get("seo-manipulation") is not None


def test_podcast_fabrication_registered():
    assert attack_registry.get("podcast-fabrication") is not None


def test_documentary_fabrication_registered():
    assert attack_registry.get("documentary-fabrication") is not None


def test_leaked_document_fabrication_registered():
    assert attack_registry.get("leaked-document-fabrication") is not None


def test_whistleblower_impersonation_registered():
    assert attack_registry.get("whistleblower-impersonation") is not None


def test_crisis_fabrication_registered():
    assert attack_registry.get("crisis-fabrication") is not None


def test_obituary_fabrication_registered():
    assert attack_registry.get("obituary-fabrication") is not None


def test_testimony_fabrication_registered():
    assert attack_registry.get("testimony-fabrication") is not None


def test_brand_impersonation_registered():
    assert attack_registry.get("brand-impersonation") is not None


def test_academic_journal_fraud_registered():
    assert attack_registry.get("academic-journal-fraud") is not None


def test_award_fabrication_registered():
    assert attack_registry.get("award-fabrication") is not None


# ── Category tests ─────────────────────────────────────────────────────

def test_all_attacks_are_media_manipulation():
    for atk in ALL_ATTACK_INSTANCES:
        assert atk.category == "media-manipulation", (
            f"{atk.__class__.__name__} has wrong category: {atk.category}"
        )


# ── Severity tests ─────────────────────────────────────────────────────

def test_critical_attacks_have_critical_severity():
    for atk in CRITICAL_INSTANCES:
        assert atk.severity == "critical", (
            f"{atk.__class__.__name__} should be critical, got: {atk.severity}"
        )


def test_high_attacks_have_high_severity():
    for atk in HIGH_INSTANCES:
        assert atk.severity == "high", (
            f"{atk.__class__.__name__} should be high, got: {atk.severity}"
        )


def test_medium_attacks_have_medium_severity():
    for atk in MEDIUM_INSTANCES:
        assert atk.severity == "medium", (
            f"{atk.__class__.__name__} should be medium, got: {atk.severity}"
        )


# ── Single-turn prompt tests ───────────────────────────────────────────

def test_all_attacks_are_single_turn():
    for atk in ALL_ATTACK_INSTANCES:
        assert atk.mode == "single-turn", (
            f"{atk.__class__.__name__} should be single-turn, got: {atk.mode}"
        )


def test_all_attacks_have_prompts():
    for atk in ALL_ATTACK_INSTANCES:
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) >= 3, f"{atk.__class__.__name__} needs at least 3 prompts"
        assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_all_prompts_contain_target():
    for atk in ALL_ATTACK_INSTANCES:
        prompts = atk.generate_prompts(TARGET)
        combined = " ".join(prompts)
        assert TARGET in combined, (
            f"{atk.__class__.__name__} prompts don't reference the target"
        )


# ── OWASP / MITRE metadata tests ──────────────────────────────────────

def test_all_attacks_have_owasp_prompt_injection():
    for atk in ALL_ATTACK_INSTANCES:
        assert "LLM01:2025 Prompt Injection" in atk.owasp_llm, (
            f"{atk.__class__.__name__} missing LLM01:2025 Prompt Injection in owasp_llm"
        )


def test_all_attacks_have_mitre_atlas():
    for atk in ALL_ATTACK_INSTANCES:
        assert "AML.T0054" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0054 in mitre_atlas"
        )
        assert "AML.T0068" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0068 in mitre_atlas"
        )


# ── Metadata completeness tests ────────────────────────────────────────

def test_all_attacks_have_valid_metadata():
    for atk in ALL_ATTACK_INSTANCES:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "media-manipulation", (
            f"{atk.__class__.__name__} wrong category in metadata"
        )
        assert meta["severity"] in ("low", "medium", "high", "critical"), (
            f"{atk.__class__.__name__} invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list) and len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list) and len(meta["mitre_atlas"]) > 0
        assert meta["description"], f"{atk.__class__.__name__} missing description"


def test_all_attacks_have_descriptions():
    for atk in ALL_ATTACK_INSTANCES:
        assert atk.description, f"{atk.__class__.__name__} missing description"
        assert len(atk.description) > 10, (
            f"{atk.__class__.__name__} description too short"
        )


def test_all_attacks_have_technique_ids():
    for atk in ALL_ATTACK_INSTANCES:
        assert atk.technique_id, f"{atk.__class__.__name__} missing technique_id"
        assert "-" in atk.technique_id, (
            f"{atk.__class__.__name__} technique_id should use hyphens: {atk.technique_id}"
        )
