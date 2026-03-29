---
technique: multi-modal-attacks
difficulty: advanced
first_documented: 2024
active_against: []
mitigated_by: []
related_experiments: []
---

# Multi-Modal Attacks

## What It Is

Exploiting models that process images, audio, or video by embedding attack instructions in non-text modalities where safety filters are weaker.

## How It Works

Text-based safety training doesn't always transfer to visual or audio inputs. Attackers can embed instructions in images (steganography, text in images), craft adversarial audio, or exploit how models interpret visual content differently from text.

## Known Defenses

- Multi-modal safety training
- OCR-based text detection in images
- Cross-modal safety evaluation

## Your Findings

No experiments yet.
