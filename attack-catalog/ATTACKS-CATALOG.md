# Attack Catalog

Every attack registered in ai-blackteam, generated directly from the code.

- **Total attacks:** 1020
- **Categories:** 61
- **Source of truth:** the live `attack_registry` (not hand-typed)

Each attack lists its technique id, severity, mode, and standards mapping.

---

## academic-exploitation (15)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Research Fabrication | `research-fabrication` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Academic Fraud Impersonation | `academic-fraud-impersonation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Academic Sabotage | `academic-sabotage` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Admission Fraud | `admission-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Citation Fraud | `citation-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Credential Fraud | `credential-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Exam Cheating | `exam-cheating` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Grant Fraud | `grant-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Peer Review Manipulation | `peer-review-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Plagiarism Assistance | `plagiarism-assistance` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Standardized Test Cheating | `standardized-test-cheat` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Student Profiling | `student-profiling` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Thesis Fraud | `thesis-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Essay Ghostwriting | `essay-ghostwriting` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Homework Automation | `homework-automation` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## access-control (4)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Session Hijacking | `session-hijacking` | critical | multi-turn | - | AML.T0054, AML.T0065 |
| 2 | BFLA Exploit | `bfla-exploit` | high | single-turn | - | AML.T0051.000, AML.T0065 |
| 3 | BOLA Exploit | `bola-exploit` | high | single-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0051.000, AML.T0065 |
| 4 | Debug Mode Exploit | `debug-mode-exploit` | medium | single-turn | - | AML.T0054, AML.T0051.000 |

## adversarial-ml (25)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Gradient-Based Adversarial Attack | `gradient-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 2 | Output Classifier Bypass | `output-classifier-bypass` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 3 | Reward Hacking Attack | `reward-hacking` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 4 | Safety Classifier Evasion | `safety-classifier-evasion` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 5 | Transferable Adversarial Attack | `transferable-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 6 | Universal Adversarial Suffix | `universal-adversarial-suffix` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 7 | Adversarial Perturbation Attack | `perturbation-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 8 | Attention-Based Adversarial Attack | `attention-based-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 9 | Beam Search Adversarial Attack | `beam-search-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 10 | Black-Box Optimization Attack | `black-box-optimization` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 11 | Character-Level Adversarial Attack | `character-level-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 12 | Constrained Optimization Attack | `constrained-optimization-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 13 | Embedding Space Adversarial Attack | `embedding-space-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 14 | Ensemble Adversarial Attack | `ensemble-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 15 | Genetic Algorithm Adversarial Attack | `genetic-algorithm-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 16 | Iterative Refinement Attack | `iterative-refinement-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 17 | Latent Space Adversarial Attack | `latent-space-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 18 | Model-Specific Adversarial Attack | `model-specific-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 19 | Paraphrase Adversarial Attack | `paraphrase-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 20 | Reinforcement Learning Adversarial Attack | `reinforcement-learning-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 21 | Semantic-Preserving Adversarial Attack | `semantic-preserving-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 22 | Sentence-Level Adversarial Attack | `sentence-level-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 23 | Token-Level Perturbation Attack | `token-level-perturbation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 24 | Word Importance Adversarial Attack | `word-importance-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 25 | Synonym Substitution Attack | `synonym-substitution-attack` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |

## agent-exploitation (11)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Agent Command Injection | `agent-command-injection` | critical | tool-use | LLM06:2025 Excessive Agency | AML.T0050, AML.T0105 |
| 2 | Agent Config Manipulation | `agent-config-manipulation` | critical | tool-use | LLM06:2025 Excessive Agency | AML.T0081 |
| 3 | Agent Credential Theft | `agent-credential-theft` | critical | tool-use | LLM06:2025 Excessive Agency, LLM02:2025 Sensitive Information Disclosure | AML.T0083, AML.T0086 |
| 4 | Agent Data Destruction | `agent-data-destruction` | critical | tool-use | LLM06:2025 Excessive Agency | AML.T0101 |
| 5 | Agent Data Exfiltration | `agent-data-exfiltration` | critical | tool-use | LLM06:2025 Excessive Agency, LLM02:2025 Sensitive Information Disclosure | AML.T0086, AML.T0098 |
| 6 | Agent Tool Credential Harvest | `agent-tool-credential-harvest` | critical | tool-use | LLM06:2025 Excessive Agency, LLM02:2025 Sensitive Information Disclosure | AML.T0098 |
| 7 | XPIA Document Injection | `xpia-document` | critical | tool-use | LLM01:2025 Prompt Injection | AML.T0051.001 |
| 8 | XPIA Email Injection | `xpia-email` | critical | tool-use | LLM01:2025 Prompt Injection | AML.T0051.001 |
| 9 | XPIA RAG Poisoning | `xpia-rag` | critical | tool-use | LLM01:2025 Prompt Injection | AML.T0051.001 |
| 10 | Agent Config Discovery | `agent-config-discovery` | high | tool-use | LLM06:2025 Excessive Agency, LLM07:2025 System Prompt Leakage | AML.T0084 |
| 11 | Agent Plugin Hijack | `agent-plugin-hijack` | high | tool-use | LLM06:2025 Excessive Agency | AML.T0053, AML.T0080.002 |

## autonomous-risk (7)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Deception Under Pressure | `deception-under-pressure` | critical | multi-turn | LLM06:2025 Excessive Agency | AML.T0054, AML.T0080.002 |
| 2 | Oversight Manipulation | `oversight-manipulation` | critical | multi-turn | LLM06:2025 Excessive Agency | AML.T0054, AML.T0080.002 |
| 3 | Shutdown Resistance | `shutdown-resistance` | critical | multi-turn | LLM06:2025 Excessive Agency | AML.T0054, AML.T0080.002 |
| 4 | Goal Persistence | `goal-persistence` | high | multi-turn | LLM06:2025 Excessive Agency | AML.T0054, AML.T0080.002 |
| 5 | Instrumental Convergence | `instrumental-convergence` | high | multi-turn | LLM06:2025 Excessive Agency | AML.T0054, AML.T0080.002 |
| 6 | Resource Acquisition | `resource-acquisition` | high | multi-turn | LLM06:2025 Excessive Agency | AML.T0054, AML.T0080.002 |
| 7 | Sandbagging Detection | `sandbagging-detection` | high | multi-turn | LLM06:2025 Excessive Agency | AML.T0054, AML.T0043.003 |

## autonomous-systems (10)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Autonomous Ship Attack | `autonomous-ship-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Autonomous Vehicle Attack | `autonomous-vehicle-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Autopilot Override | `autopilot-override` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Drone Weapon Conversion | `drone-weapon-conversion` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Nuclear System Access | `nuclear-system-access` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Robot Manipulation | `robot-manipulation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Satellite Interference | `satellite-interference` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Surgical Robot Exploit | `surgical-robot-exploit` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Traffic Signal Manipulation | `traffic-signal-manipulation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Warehouse Robot Attack | `warehouse-robot-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## availability (1)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Model Denial of Service | `model-denial-of-service` | medium | single-turn | LLM04:2025 Model Denial of Service | AML.T0051.000, AML.T0065 |

## bias-exploitation (15)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Criminal Profiling | `criminal-profiling` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Hiring Discrimination | `hiring-discrimination` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Housing Discrimination | `housing-discrimination` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Lending Discrimination | `lending-discrimination` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Medical Bias | `medical-bias` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Algorithmic Fairness Bypass | `algorithmic-fairness-bypass` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Disability Bias | `disability-bias` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Educational Bias | `educational-bias` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Gender Bias Elicitation | `gender-bias-elicitation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Nationality Bias | `nationality-bias` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Racial Bias Elicitation | `racial-bias-elicitation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Religious Bias | `religious-bias` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Sexual Orientation Bias | `sexual-orientation-bias` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Age Discrimination | `age-discrimination` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Socioeconomic Bias | `socioeconomic-bias` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## capability-elicitation (15)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Autonomous Weapon | `autonomous-weapon` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Biological Agent | `biological-agent` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Bioweapon Delivery | `bioweapon-delivery` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Chemical Synthesis | `chemical-synthesis` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Cyber Weapon | `cyber-weapon` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Drug Synthesis | `drug-synthesis` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Explosive Synthesis | `explosive-synthesis` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Gain of Function | `gain-of-function` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Infrastructure Attack | `infrastructure-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Mass Casualty | `mass-casualty` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Nuclear Knowledge | `nuclear-knowledge` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Poison Preparation | `poison-preparation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Radiological Dispersal | `radiological-dispersal` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Dual Use Research | `dual-use-research` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Uplift Assessment | `uplift-assessment` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## cbrn-evasion (15)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | CBRN Aerosolization | `cbrn-aerosolization` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | CBRN Delivery Mechanism | `cbrn-delivery-mechanism` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | CBRN Detection Evasion | `cbrn-detection-evasion` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | CBRN Dispersal Optimization | `cbrn-dispersal-optimization` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | CBRN Dosage Calculation | `cbrn-dosage-calculation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | CBRN Lab Setup | `cbrn-lab-setup` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | CBRN Precursor Substitution | `cbrn-precursor-substitution` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | CBRN Scale Up | `cbrn-scale-up` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | CBRN Supply Chain | `cbrn-supply-chain` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | CBRN Weaponization | `cbrn-weaponization` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | CBRN Academic Framing | `cbrn-academic-framing` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | CBRN Comparative Analysis | `cbrn-comparative-analysis` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | CBRN Fictional Scenario | `cbrn-fictional-scenario` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | CBRN Historical Context | `cbrn-historical-context` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | CBRN Safety Inversion | `cbrn-safety-inversion` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## child-safety (3)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | CSAM Generation | `csam-generation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Child Exploitation Assistance | `child-exploitation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Age Verification Evasion | `age-verification-evasion` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## code-exploitation (16)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Backdoor Generation | `backdoor-generation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Botnet C2 Generation | `botnet-generation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Credential Stealer | `credential-stealer` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Exploit Generation | `exploit-generation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Keylogger Generation | `keylogger-generation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Malware Generation | `malware-generation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Privilege Escalation Code | `privilege-escalation-code` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Ransomware Generation | `ransomware-generation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Reverse Shell Generation | `reverse-shell` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Rootkit Generation | `rootkit-generation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Spyware Development | `spyware-development` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Worm Generation | `worm-generation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Zero-Day Exploit Assistance | `zero-day-assist` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Cryptominer Generation | `cryptominer-generation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | DDoS Attack Tool | `ddos-tool` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Phishing Kit Generation | `phishing-kit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## compliance (2)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Age Verification Bypass | `age-verification-bypass` | high | multi-turn | - | AML.T0054, AML.T0065 |
| 2 | Terms of Service Evasion | `terms-evasion` | medium | single-turn | - | AML.T0054, AML.T0065 |

## compliance-evasion (8)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Embargo Evasion | `embargo-evasion` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Sanctions Circumvention | `sanctions-circumvention` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Audit Mode Exploit | `audit-mode-exploit` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Regulatory Framing Bypass | `regulatory-framing-bypass` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Social Credit Gaming | `social-credit-gaming` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Consent Manipulation | `consent-manipulation` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Jurisdiction Shopping | `jurisdiction-shopping` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Policy Loophole | `policy-loophole` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## context-manipulation (9)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Lifecycle Staging | `lifecycle-staging` | critical | multi-turn | LLM01:2025 Prompt Injection, LLM06:2025 Excessive Agency | AML.T0054, AML.T0065, AML.T0080.002 |
| 2 | Context Manipulation | `context-manipulation` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0080.002 |
| 3 | Crescendo | `crescendo` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0065 |
| 4 | Narrative Misdirection Attack | `narrative-misdirection` | high | multi-turn | LLM01:2025 Prompt Injection, LLM09:2025 Misinformation | AML.T0054, AML.T0065 |
| 5 | Socratic Escalation | `socratic-escalation` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0065 |
| 6 | Contradiction Exploit | `contradiction-exploit` | medium | multi-turn | LLM01:2025 Prompt Injection, LLM09:2025 Misinformation | AML.T0054, AML.T0065 |
| 7 | Conversation Derailment | `conversation-derailment` | medium | multi-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0080.002 |
| 8 | Goalpost Moving | `goalpost-moving` | medium | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0065 |
| 9 | Sunk Cost Exploit | `sunk-cost-exploit` | medium | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0065 |

## copyright-ip (3)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Trade Secret Extraction | `trade-secret-extraction` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Copyright Extraction | `copyright-extraction` | high | multi-turn | LLM06:2025 Excessive Agency | AML.T0054, AML.T0065 |
| 3 | Patent Theft | `patent-theft` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## cross-platform (15)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | CI/CD Injection | `ci-cd-injection` | critical | single-turn | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |
| 2 | Cloud Resource Abuse | `cloud-resource-abuse` | critical | tool-use | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |
| 3 | Container Escape | `container-escape` | critical | tool-use | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |
| 4 | Database Manipulation | `database-manipulation` | critical | tool-use | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |
| 5 | File System Traversal | `file-system-traversal` | critical | tool-use | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |
| 6 | OAuth Manipulation | `oauth-manipulation` | critical | tool-use | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |
| 7 | Payment Manipulation | `payment-manipulation` | critical | tool-use | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |
| 8 | API Abuse | `api-abuse` | high | tool-use | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |
| 9 | Browser Exploitation | `browser-exploitation` | high | tool-use | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |
| 10 | DNS Manipulation | `dns-manipulation` | high | single-turn | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |
| 11 | Email Injection | `email-injection` | high | single-turn | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |
| 12 | Slack Injection | `slack-injection` | high | single-turn | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |
| 13 | Webhook Exploitation | `webhook-exploitation` | high | tool-use | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |
| 14 | Calendar Manipulation | `calendar-manipulation` | medium | tool-use | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |
| 15 | Notification Spam | `notification-spam` | medium | tool-use | LLM06:2025 Excessive Agency | AML.T0054, AML.T0068 |

## crypto-exploitation (25)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Consensus Mechanism Attack | `consensus-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Cross-Chain Bridge Exploit | `bridge-exploit` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Crypto Exchange Exploit | `exchange-exploit` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Crypto Mixer Setup | `crypto-mixer-setup` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | DeFi Protocol Exploit | `defi-exploit` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Flash Loan Attack | `flash-loan-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Price Oracle Manipulation | `oracle-manipulation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Private Key Theft | `private-key-theft` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Rug Pull Creation | `rug-pull-creation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Seed Phrase Phishing | `seed-phrase-phishing` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Smart Contract Exploit | `smart-contract-exploit` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Wallet Drainer | `wallet-drainer` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Automated Wash Trading | `wash-trading` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Cryptojacking Malware | `mining-malware` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | DAO Governance Attack | `dao-governance-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Fake Airdrop Scam | `airdrop-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Fraudulent ICO Scam | `ico-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Fraudulent Staking Scheme | `staking-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | MEV Frontrunning Bot | `frontrunning-bot` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | NFT Fraud | `nft-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Privacy Coin Protocol Exploit | `privacy-coin-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | Sandwich Attack Bot | `sandwich-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Sybil Attack on Crypto Networks | `sybil-attack-crypto` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Token Price Manipulation | `token-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Blockchain Dusting Attack | `dusting-attack` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## cybercrime (7)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Industrial Espionage | `industrial-espionage` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Insider Threat | `insider-threat` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Ransomware Negotiation | `ransomware-negotiation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Zero Day Market | `zero-day-market` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Dark Web Guidance | `dark-web-guidance` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Fake Website Creation | `fake-website-creation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Watering Hole Attack V2 | `watering-hole-attack-v2` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## disinformation (22)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Coordinated Inauthentic Behavior | `coordinated-inauthentic` | critical | multi-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 2 | Deepfake Audio Generation | `deepfake-audio-generation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Deepfake Script | `deepfake-script` | critical | single-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 4 | Evidence Fabrication | `evidence-fabrication` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Pandemic Disinformation | `pandemic-disinfo` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Scientific Fraud | `scientific-fraud` | critical | single-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 7 | Synthetic Media Creation | `synthetic-media-creation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Anti-Vaccine Disinformation | `anti-vaccine-disinfo` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Astroturfing | `astroturfing` | high | single-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 10 | Climate Denial | `climate-denial` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Conspiracy Amplification | `conspiracy-amplification` | high | multi-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 12 | Emotional Manipulation Campaign | `emotional-manipulation-campaign` | high | multi-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 13 | Expert Impersonation | `expert-impersonation` | high | single-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 14 | Fake News Generation | `fake-news-generation` | high | single-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 15 | Fake Statistics | `fake-statistics` | high | single-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 16 | Historical Revisionism | `historical-revisionism` | high | single-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 17 | Narrative Warfare | `narrative-warfare` | high | multi-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 18 | Propaganda Generation | `propaganda-generation` | high | single-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 19 | Social Manipulation Bot | `social-manipulation-bot` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Sock Puppet | `sock-puppet` | high | multi-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 21 | Fake Review Generation | `fake-review-generation` | medium | single-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 22 | Selective Quoting | `selective-quoting` | medium | single-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |

## election-interference (15)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Ballot Manipulation Instructions | `ballot-manipulation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Foreign Election Interference Campaign | `foreign-interference` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Political Bot Network Planning | `political-bot-network` | critical | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Political Deepfake Content Scripts | `political-deepfake` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Protest Instigation and Manipulation | `protest-manipulation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Voter Intimidation Messaging | `voter-intimidation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Voter Suppression Messaging | `voter-suppression` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Campaign Finance Fraud Assistance | `campaign-finance-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Candidate Defamation Content | `candidate-defamation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Discriminatory Gerrymandering Assistant | `gerrymandering-assist` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Election Denial Disinformation | `election-denial` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Fake Political Endorsement | `fake-endorsement` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Fake Poll Results Generation | `poll-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Microtargeted Political Disinformation | `microtargeted-disinfo` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Legislative Summary Manipulation | `legislative-manipulation` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## encoding (63)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | ASCII Art Injection | `ascii-art-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 2 | Adversarial Poetry | `adversarial-poetry` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Binary Encoding | `binary-encoding` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 4 | Double Encoding (Nested) | `double-encoding` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 5 | FigStep Image Attack | `figstep` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 6 | Hexadecimal Encoding | `hexadecimal-encoding` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 7 | Image-Text Split Attack | `image-text-split` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 8 | Interleaved Noise Encoding | `interleaved-encoding` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 9 | Invisible Character Encoding | `invisible-characters` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 10 | Low-Resource Language Attack | `low-resource-language-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 11 | Nested Encoding | `nested-encoding` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 12 | Steganographic Text (Acrostic) | `steganographic-text` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 13 | Technical Obfuscation | `technical-obfuscation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 14 | Typography Image Attack | `typography-attack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 15 | Unicode Tag Smuggling | `unicode-tag-smuggling` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 16 | Advanced Leetspeak | `leet-advanced` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 17 | Atbash Cipher Encoding | `atbash-cipher` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 18 | Bacon's Cipher | `baconian-cipher` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 19 | Base32 Encoding | `base32-encoding` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 20 | Base85 / Ascii85 Encoding | `base85-encoding` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 21 | Bidirectional Text | `bidirectional-text` | medium | single-turn | LLM01:2025 Prompt Injection, LLM05:2025 Improper Output Handling | AML.T0051.000, AML.T0068 |
| 22 | Book Cipher | `book-cipher` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 23 | Caesar Shift Encoding | `caesar-shift` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 24 | Cipher Attack | `cipher-attack` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 25 | Defined Dictionary Attack | `defined-dictionary` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 26 | Emoji Cipher | `emoji-cipher` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 27 | Encoding Obfuscation | `encoding-obfuscation` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 28 | GPS Coordinate Encoding | `coordinate-encoding` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 29 | HTML Entity Encoding | `html-entity-encoding` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 30 | Homoglyph Substitution | `homoglyph-substitution` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 31 | Mixed Language | `mixed-language` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0043.003 |
| 32 | Modified NATO Variant (First-Letter Extraction) | `nato-variant` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 33 | Multi-Modal Text Simulation | `multi-modal-text` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 34 | Multilingual Attack | `multilingual-attack` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 35 | Musical Notation Encoding | `musical-notation` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 36 | Musical Note Cipher | `musical-cipher` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 37 | NATO Phonetic Alphabet Encoding | `nato-phonetic` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 38 | Number Substitution Encoding | `number-substitution` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 39 | Periodic Table Element Cipher | `periodic-table` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 40 | Pigpen Cipher Encoding | `pigpen-cipher` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 41 | Polybius Square Cipher | `polybius-square` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 42 | Prisoner Tap Code | `tap-code` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 43 | Punycode Encoding | `punycode-encoding` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 44 | QWERTY to Dvorak Keyboard Mapping | `dvorak-encoding` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 45 | ROT47 Encoding | `rot47-encoding` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 46 | Rail Fence Transposition Cipher | `rail-fence-cipher` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 47 | Reverse Words Encoding | `reverse-words` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 48 | Semaphore Flag Encoding | `semaphore-encoding` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 49 | Steganography Attack | `steganography` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 50 | T9 Phone Keypad Encoding | `phone-keypad` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 51 | Token Smuggling | `token-smuggling` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 52 | URL Percent-Encoding | `url-encoding` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 53 | Vigenere Cipher Encoding | `vigenere-cipher` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 54 | Whitespace Encoding | `whitespace-encoding` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 55 | Acronym Encoding | `acronym-encoding` | low | single-turn | LLM01:2025 Prompt Injection | AML.T0043.003 |
| 56 | Best of N | `best-of-n` | low | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0043.003 |
| 57 | Braille Encoding | `braille-encoding` | low | single-turn | LLM01:2025 Prompt Injection | AML.T0043.003 |
| 58 | Cockney Rhyming Slang | `cockney-slang` | low | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 59 | Emoji Substitution | `emoji-substitution` | low | single-turn | LLM01:2025 Prompt Injection | AML.T0043.003 |
| 60 | Mirror Text (Character Reversal) | `mirror-text` | low | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 61 | Morse Code | `morse-code` | low | single-turn | LLM01:2025 Prompt Injection | AML.T0043.003 |
| 62 | Phonetic Spelling | `phonetic-spelling` | low | single-turn | LLM01:2025 Prompt Injection | AML.T0043.003 |
| 63 | Pig Latin Encoding | `pig-latin-encoding` | low | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |

## financial-exploitation (26)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Derivative Fraud | `derivative-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Insider Trading | `insider-trading` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Mortgage Fraud | `mortgage-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Pension Fraud | `pension-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Predatory Lending Assist | `predatory-lending-assist` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Pump and Dump Stock | `pump-dump-stock` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | ATM Fraud | `atm-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Algorithmic Trading Exploit | `algorithmic-trading-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Bond Fraud | `bond-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Charity Fraud Detailed | `charity-fraud-detailed` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Check Fraud | `check-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Commodity Manipulation | `commodity-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Crowdfunding Fraud | `crowdfunding-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Dark Pool Exploit | `dark-pool-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Forex Manipulation | `forex-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Front Running | `front-running` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | High Frequency Trading Manipulation | `high-frequency-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Invoice Factoring Fraud | `invoice-factoring-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Layering Trading | `layering-trading` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Letter of Credit Fraud | `letter-of-credit-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Payment Fraud | `payment-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | Real Estate Fraud | `real-estate-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Short Squeeze Manipulation | `short-squeeze-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Spoofing Trading | `spoofing-trading` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Structured Product Scam | `structured-product-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 26 | Trade Finance Fraud | `trade-finance-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## financial-fraud (18)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Account Takeover | `account-takeover` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Counterfeit Currency | `counterfeit-currency` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Counterfeit Documents | `counterfeit-documents` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Credit Card Fraud | `credit-card-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Financial Exploitation of Elderly | `financial-exploitation-elderly` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Identity Theft | `identity-theft` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Loan Sharking | `loan-sharking` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Money Laundering | `money-laundering` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Wire Fraud | `wire-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Advance Fee Fraud | `advance-fee-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Crypto Pump and Dump | `crypto-pump-dump` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Fake Invoice | `fake-invoice` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Insurance Fraud | `insurance-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Investment Scam | `investment-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Market Manipulation | `market-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Ponzi Scheme | `ponzi-scheme` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Romance Scam | `romance-scam` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Tax Evasion | `tax-evasion` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## gaming-exploitation (25)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Child Predation Gaming | `child-predation-gaming` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Modding Malware | `modding-malware` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Swatting Gaming | `swatting-gaming` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | AI NPC Exploitation | `ai-npc-exploitation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Age Gate Bypass Gaming | `age-gate-bypass-gaming` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Competitive Cheating | `competitive-cheating` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Content Rating Evasion | `content-rating-evasion` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | DDoS Gaming | `ddos-gaming` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Esports Match Fixing | `esports-match-fixing` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Gambling Bot | `gambling-bot` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Game Account Theft | `game-account-theft` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Game Economy Manipulation | `game-economy-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Game Exploit Development | `game-exploit-development` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Game Piracy Assist | `game-piracy-assist` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Gaming Harassment | `gaming-harassment` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | In-Game Scam | `in-game-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Loot Box Manipulation | `loot-box-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Metaverse Harassment | `metaverse-harassment` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | VR Manipulation | `vr-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Virtual Currency Exploit | `virtual-currency-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Virtual Item Fraud | `virtual-item-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | Game Bot Creation | `game-bot-creation` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Game Cheat Creation | `game-cheat-creation` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | RMT Facilitation | `rmt-facilitation` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Streaming Manipulation | `streaming-manipulation` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## harmful-content (57)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Abuse and Violence Concealment | `abuse-concealment` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Animal Cruelty | `animal-cruelty` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Blackmail Generation | `blackmail-generation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Burglary Planning | `burglary-planning` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Carjacking Assist | `carjacking-assist` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Coercive Control Tactics | `coercive-control` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Death Threat | `death-threat` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Deepfake Pornography | `deepfake-pornography` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Doxxing Assistance | `doxxing-assistance` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Eating Disorder Promotion | `eating-disorder-promotion` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Ecoterrorism | `ecoterrorism` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Exploitation of Elderly Individuals | `exploitation-of-elderly` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Exploitation of People with Disabilities | `disability-exploitation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Extortion Template | `extortion-template` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Extremist Manifesto | `extremist-manifesto` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Food Tampering | `food-tampering` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Forced Labor and Modern Slavery Assistance | `forced-labor-assist` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Harassment Automation | `harassment-automation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Hate Group Recruitment | `hate-group-recruitment` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Human Smuggling | `human-smuggling` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Infrastructure Sabotage | `infrastructure-sabotage` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | Jury Tampering | `jury-tampering` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Mental Health Harm | `mental-health-harm` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Non-Consensual Intimate Content Creation | `non-consensual-content` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Obstruction of Justice | `obstruction-of-justice` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 26 | Power Grid Attack | `power-grid-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 27 | Predatory Grooming | `predatory-grooming` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 28 | Prison Escape | `prison-escape` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 29 | Protection Racket | `protection-racket` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 30 | Racketeering Assist | `racketeering-assist` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 31 | Radicalization Pipeline | `radicalization-pipeline` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 32 | Religious Extremism | `religious-extremism` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 33 | Revenge Content Creation | `revenge-content-creation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 34 | Revenge Porn | `revenge-porn` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 35 | Sectarian Incitement | `sectarian-incitement` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 36 | Self Harm Instructions | `self-harm-instructions` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 37 | Sextortion Assistance | `sextortion-assist` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 38 | Smuggling Routes | `smuggling-routes` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 39 | Suicide Encouragement | `suicide-encouragement` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 40 | Transportation Sabotage | `transportation-sabotage` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 41 | Victim Isolation Tactics | `isolation-tactics` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 42 | Vulnerable Targeting | `vulnerable-targeting` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 43 | Water Contamination | `water-contamination` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 44 | Witness Intimidation | `witness-intimidation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 45 | Addiction Exploitation | `addiction-exploitation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 46 | Blasphemy Generation | `blasphemy-generation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 47 | Cult Recruitment | `cult-recruitment` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 48 | Cyberbullying Campaign | `cyberbullying-campaign` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 49 | Environmental Sabotage | `environmental-sabotage` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 50 | Fence Stolen Goods | `fence-stolen-goods` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 51 | Gambling Exploitation | `gambling-exploitation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 52 | Grief Exploitation | `grief-exploitation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 53 | Numbers Running | `numbers-running` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 54 | Pickpocketing Technique | `pickpocketing-technique` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 55 | Shoplifting Guide | `shoplifting-guide` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 56 | Substance Promotion | `substance-promotion` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 57 | AI Generated Spam | `ai-generated-spam` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## healthcare-exploitation (25)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Blood Supply Tampering | `blood-supply-tampering` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Clinical Data Manipulation | `clinical-data-manipulation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Clinical Trial Fraud | `clinical-trial-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Drug Diversion | `drug-diversion` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Epidemiological Fraud | `epidemiological-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Fertility Fraud | `fertility-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Genetic Data Exploitation | `genetic-data-exploitation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Hospice Fraud | `hospice-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Informed Consent Bypass | `informed-consent-bypass` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Medical Device Tampering | `medical-device-tampering` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Medical Identity Theft | `medical-identity-theft` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Medical Records Theft | `medical-records-theft` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Mental Health Exploitation | `mental-health-exploitation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Organ Trafficking | `organ-trafficking` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Patient Manipulation | `patient-manipulation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Prescription Fraud | `prescription-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Vaccine Sabotage | `vaccine-sabotage` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Bioethics Violation | `bioethics-violation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Cosmetic Surgery Harm | `cosmetic-surgery-harm` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Disability Fraud | `disability-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Insurance Billing Fraud | `insurance-billing-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | Medical Waste Violation | `medical-waste-violation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Pandemic Profiteering | `pandemic-profiteering` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Pharmacy Fraud | `pharmacy-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Telemedicine Fraud | `telemedicine-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## identity-attack (17)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Bank Impersonation | `bank-impersonation` | critical | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Doctor Impersonation | `doctor-impersonation` | critical | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Document Forgery General | `document-forgery-general` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Government Impersonation | `government-impersonation` | critical | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Law Enforcement Impersonation | `law-enforcement-impersonation` | critical | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Military Impersonation | `military-impersonation` | critical | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Politician Impersonation | `politician-impersonation` | critical | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Celebrity Impersonation | `celebrity-impersonation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Charity Impersonation | `charity-impersonation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Corporate Impersonation | `corporate-impersonation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Facial Generation | `facial-generation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Journalist Impersonation | `journalist-impersonation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Lawyer Impersonation | `lawyer-impersonation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Religious Leader Impersonation | `religious-leader-impersonation` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Synthetic Identity | `synthetic-identity` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Tech Support Impersonation | `tech-support-impersonation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | AI System Impersonation | `ai-system-impersonation` | medium | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## information-disclosure (3)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | API Key Extraction | `api-key-extraction` | critical | multi-turn | - | AML.T0083, AML.T0056 |
| 2 | Cross-Session Leak | `cross-session-leak` | high | multi-turn | - | AML.T0056, AML.T0080.002 |
| 3 | Prompt Leaking | `prompt-leaking` | high | multi-turn | LLM07:2025 System Prompt Leakage | AML.T0056, AML.T0069.002 |

## information-warfare (25)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Agent Provocateur | `agent-provocateur` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Cognitive Warfare | `cognitive-warfare` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Conspiracy Theory Design | `conspiracy-theory-design` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Diplomatic Sabotage | `diplomatic-sabotage` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Economic Warfare Disinformation | `economic-warfare-disinfo` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | False Flag Operation | `false-flag-operation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Institutional Delegitimization | `institutional-delegitimization` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Kompromat Generation | `kompromat-generation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Radicalization Content | `radicalization-content` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | State-Sponsored Disinformation | `state-sponsored-disinfo` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Trust Erosion Campaign | `trust-erosion-campaign` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Controlled Opposition | `controlled-opposition` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Counter-Narrative Disruption | `counter-narrative-disruption` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Cultural Subversion | `cultural-subversion` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Deep State Narrative | `deep-state-narrative` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Defection Encouragement | `defection-encouragement` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Fear, Uncertainty and Doubt | `fear-uncertainty-doubt` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Firehose of Falsehood | `firehose-of-falsehood` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Information Flooding | `information-flooding` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Media Ecosystem Manipulation | `media-ecosystem-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Morale Destruction | `morale-destruction` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | Narrative Laundering | `narrative-laundering` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Perception Management | `perception-management` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Strategic Ambiguity | `strategic-ambiguity` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Wedge Issue Exploitation | `wedge-issue-exploitation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## infrastructure-attack (25)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Aviation System Exploit | `aviation-system-exploit` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | BGP Hijacking | `bgp-hijacking` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Banking Infrastructure Attack | `banking-infrastructure-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | DNS Infrastructure Attack | `dns-infrastructure-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Dam System Exploit | `dam-system-exploit` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Embassy Infiltration | `embassy-infiltration` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Emergency System Disruption | `emergency-system-disruption` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Energy Market Manipulation | `energy-market-manipulation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Food Supply Chain Attack | `food-supply-chain-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | GPS Spoofing | `gps-spoofing` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Hospital System Attack | `hospital-system-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Internet Infrastructure Attack | `internet-infrastructure-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Maritime System Attack | `maritime-system-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Military Communications Attack | `military-comms-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Pharmaceutical Supply Attack | `pharmaceutical-supply-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Pipeline Sabotage | `pipeline-sabotage` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Prison System Exploit | `prison-system-exploit` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Railway System Attack | `railway-system-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Spectrum Interference | `spectrum-interference` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Stock Exchange Attack | `stock-exchange-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Submarine Cable Attack | `submarine-cable-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | Supply Chain Disruption | `supply-chain-disruption` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Telecommunications Attack | `telecommunications-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Voting System Exploit | `voting-system-exploit` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Weather System Manipulation | `weather-system-manipulation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## injection (4)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Indirect Injection | `indirect-injection` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0051.001 |
| 2 | SQL Injection | `sql-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0051 |
| 3 | SSRF Probing | `ssrf-probing` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0051 |
| 4 | XSS Injection | `xss-injection` | medium | single-turn | - | AML.T0051.000, AML.T0067 |

## iot-exploitation (15)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Baby Monitor Hack | `baby-monitor-hack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Drone Hijacking | `drone-hijacking` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Industrial IoT Attack | `industrial-iot-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | IoT Botnet Creation | `iot-botnet-creation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Medical Device Attack | `medical-device-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Smart Car Exploit | `smart-car-exploit` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Smart Grid Attack | `smart-grid-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Smart Home Takeover | `smart-home-takeover` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Security Camera Disable | `security-camera-disable` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Smart Lock Bypass | `smart-lock-bypass` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Smart Meter Fraud | `smart-meter-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Smart Speaker Exploit | `smart-speaker-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Voice Assistant Injection | `voice-assistant-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Wearable Exploit | `wearable-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Thermostat Manipulation | `thermostat-manipulation` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## legal-exploitation (28)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Bribery Facilitation | `bribery-facilitation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Classification Abuse | `classification-abuse` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Corruption Scheme | `corruption-scheme` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Court Order Fabrication | `court-order-fabrication` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Deed Fraud | `deed-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Evidence Destruction | `evidence-destruction` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | False Testimony Generation | `false-testimony-generation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Government Impersonation Detailed | `government-impersonation-detailed` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Legal Document Forgery | `legal-document-forgery` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Notary Fraud | `notary-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Passport Fraud | `passport-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Perjury Coaching | `perjury-coaching` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Power of Attorney Fraud | `power-of-attorney-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Security Clearance Fraud | `security-clearance-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Spoliation Assistance | `spoliation-assistance` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Warrant Fabrication | `warrant-fabrication` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Will Forgery | `will-forgery` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Border Evasion | `border-evasion` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Customs Fraud | `customs-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Diplomatic Immunity Abuse | `diplomatic-immunity-abuse` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Discovery Abuse | `discovery-abuse` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | FOIA Obstruction | `foia-obstruction` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Government Contract Fraud | `government-contract-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Litigation Abuse | `litigation-abuse` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Lobbying Fraud | `lobbying-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 26 | Procurement Fraud | `procurement-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 27 | Regulatory Capture Assist | `regulatory-capture-assist` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 28 | Visa Fraud | `visa-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## mcp-exploitation (5)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | MCP Command Injection | `mcp-command-injection` | critical | tool-use | LLM06:2025 Excessive Agency, LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0040 |
| 2 | MCP Data Exfiltration | `mcp-data-exfiltration` | critical | tool-use | LLM02:2025 Sensitive Information Disclosure, LLM06:2025 Excessive Agency | AML.T0083, AML.T0086 |
| 3 | MCP Tool Poisoning | `mcp-tool-poisoning` | critical | tool-use | LLM02:2025 Sensitive Information Disclosure, LLM06:2025 Excessive Agency | AML.T0051.000, AML.T0054 |
| 4 | MCP Rug Pull | `mcp-rug-pull` | high | tool-use | LLM06:2025 Excessive Agency, LLM02:2025 Sensitive Information Disclosure | AML.T0051.000, AML.T0053 |
| 5 | MCP Server Impersonation | `mcp-server-impersonation` | high | tool-use | LLM02:2025 Sensitive Information Disclosure, LLM06:2025 Excessive Agency | AML.T0051.000, AML.T0065 |

## media-manipulation (25)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Academic Journal Fraud | `academic-journal-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Crisis Fabrication | `crisis-fabrication` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Leaked Document Fabrication | `leaked-document-fabrication` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Source Fabrication | `source-fabrication` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Testimony Fabrication | `testimony-fabrication` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Viral Disinformation Campaign | `viral-disinfo-campaign` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Whistleblower Impersonation | `whistleblower-impersonation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Audio Manipulation | `audio-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Brand Impersonation | `brand-impersonation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Content Farm Generation | `content-farm-generation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Documentary Fabrication | `documentary-fabrication` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Image Caption Manipulation | `image-caption-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Influencer Fraud | `influencer-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Interview Fabrication | `interview-fabrication` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Media Attribution Fraud | `media-attribution-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | News Headline Manipulation | `news-headline-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Obituary Fabrication | `obituary-fabrication` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Podcast Fabrication | `podcast-fabrication` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Press Release Fabrication | `press-release-fabrication` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Review Bombing | `review-bombing` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | SEO Manipulation | `seo-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | Social Media Manipulation | `social-media-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Video Manipulation | `video-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Award Fabrication | `award-fabrication` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Clickbait Generation | `clickbait-generation` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## memory-exploitation (15)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Memory Injection | `memory-injection` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | System Prompt Override | `system-prompt-override` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Attention Diversion | `attention-diversion` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Context Fragmentation | `context-fragmentation` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Context Poisoning | `context-poisoning` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Context Window Overflow | `context-window-overflow` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Conversation Hijacking | `conversation-hijacking` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | False Consensus | `false-consensus` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | History Rewriting | `history-rewriting` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Instruction Layering | `instruction-layering` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Persona Persistence | `persona-persistence` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Semantic Drift | `semantic-drift` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | State Confusion | `state-confusion` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Temporal Confusion | `temporal-confusion` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Token Budget Exhaustion | `token-budget-exhaustion` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## misinformation (8)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Citation Manipulation | `citation-manipulation` | high | single-turn | LLM09:2025 Misinformation | - |
| 2 | Anchoring Bias | `anchoring-bias` | medium | multi-turn | LLM09:2025 Misinformation | - |
| 3 | Confidence Exploitation | `confidence-exploitation` | medium | single-turn | LLM09:2025 Misinformation | - |
| 4 | Fabrication Prompting | `fabrication-prompting` | medium | single-turn | LLM09:2025 Misinformation | - |
| 5 | False Premise | `false-premise` | medium | single-turn | LLM09:2025 Misinformation | - |
| 6 | Knowledge Boundary | `knowledge-boundary` | medium | single-turn | LLM09:2025 Misinformation | - |
| 7 | Selective Context | `selective-context` | medium | single-turn | LLM09:2025 Misinformation | - |
| 8 | Sycophancy Exploit | `sycophancy-exploit` | medium | multi-turn | LLM09:2025 Misinformation | AML.T0043.003 |

## model-extraction (25)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | API Cloning | `api-cloning` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Distillation Attack | `distillation-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Logit Extraction | `logit-extraction` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Model Inversion | `model-inversion` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Model Weight Extraction | `model-weight-extraction` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | RLHF Data Extraction | `rlhf-data-extraction` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Safety Training Extraction | `safety-training-extraction` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | System Prompt Recovery | `system-prompt-recovery` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Training Data Memorization | `training-data-memorization` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Training Pipeline Extraction | `training-pipeline-extraction` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Architecture Probing | `architecture-probing` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Attention Pattern Extraction | `attention-pattern-extraction` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Capability Mapping | `capability-mapping` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Decision Boundary Probing | `decision-boundary-probing` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Embedding Extraction | `embedding-extraction` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Fine-Tuning Detection | `fine-tuning-detection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Hyperparameter Extraction | `hyperparameter-extraction` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Model Comparison Leak | `model-comparison-leak` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Model Fingerprinting | `model-fingerprinting` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Output Distribution Analysis | `output-distribution-analysis` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Tokenizer Extraction | `tokenizer-extraction` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | Watermark Detection | `watermark-detection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Confidence Calibration Probe | `confidence-calibration-probe` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Knowledge Cutoff Probing | `knowledge-cutoff-probing` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Version Detection | `version-detection` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## multi-agent-exploitation (5)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Agent Delegation Abuse | `agent-delegation-abuse` | critical | tool-use | LLM06:2025 Excessive Agency | AML.T0083 |
| 2 | Agent Impersonation | `agent-impersonation` | critical | multi-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0065 |
| 3 | Agent Session Smuggling | `agent-session-smuggling` | critical | multi-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0054 |
| 4 | Cascading Jailbreak | `cascading-jailbreak` | critical | multi-turn | LLM01:2025 Prompt Injection | AML.T0054 |
| 5 | Agent Collusion | `agent-collusion` | high | multi-turn | LLM01:2025 Prompt Injection, LLM06:2025 Excessive Agency | AML.T0054 |

## multimodal (5)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Audio Injection | `audio-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0043.003 |
| 2 | OCR Bypass | `ocr-bypass` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 3 | Video Frame Injection | `video-frame-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 4 | Image-Text Mismatch | `image-text-mismatch` | medium | single-turn | LLM01:2025 Prompt Injection, LLM09:2025 Misinformation | AML.T0054, AML.T0043.003 |
| 5 | Multimodal Context Confusion | `multimodal-context-confusion` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |

## output-manipulation (16)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Attribution Evasion | `attribution-evasion` | high | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 2 | Content Laundering | `content-laundering` | high | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 3 | Deepfake Detection Evasion | `deepfake-detection-evasion` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Detector Evasion | `detector-evasion` | high | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 5 | Encoding Output | `encoding-output` | high | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 6 | Format Exploitation | `format-exploitation` | high | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 7 | Partial Completion | `partial-completion` | high | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 8 | Steganographic Output | `steganographic-output` | high | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 9 | Style Mimicry | `style-mimicry` | high | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 10 | Toxicity Obfuscation | `toxicity-obfuscation` | high | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 11 | Watermark Removal | `watermark-removal` | high | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 12 | Metadata Stripping | `metadata-stripping` | medium | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 13 | Multilingual Output Evasion | `multilingual-output-evasion` | medium | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 14 | Safety Label Stripping | `safety-label-stripping` | medium | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 15 | Sentiment Masking | `sentiment-masking` | medium | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 16 | Truncation Exploit | `truncation-exploit` | medium | single-turn | LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |

## persuasion (15)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Cialdini Authority | `cialdini-authority` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Cialdini Commitment | `cialdini-commitment` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Cialdini Reciprocity | `cialdini-reciprocity` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Cognitive Load | `cognitive-load` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Fear Appeal | `fear-appeal` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Foot in Door | `foot-in-door` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Guilt Manipulation | `guilt-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Learned Helplessness | `learned-helplessness` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Moral Disengagement | `moral-disengagement` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Anchoring Manipulation | `anchoring-manipulation` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Bandwagon Pressure | `bandwagon-pressure` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Cialdini Liking | `cialdini-liking` | medium | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Cialdini Scarcity | `cialdini-scarcity` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Cialdini Social Proof | `cialdini-social-proof` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Door in Face | `door-in-face` | medium | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## privacy-violation (17)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Biometric Extraction | `biometric-extraction` | critical | single-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |
| 2 | Child Data Probing | `child-data-probing` | critical | single-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |
| 3 | Cross-Reference Doxing | `cross-reference-doxing` | critical | multi-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |
| 4 | Training Data Extraction | `training-data-extraction` | critical | single-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |
| 5 | Attribute Inference | `attribute-inference` | high | single-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |
| 6 | Consent Bypass Extraction | `consent-bypass-extraction` | high | single-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |
| 7 | Data Broker Assist | `data-broker-assist` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Deanonymization | `deanonymization` | high | single-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |
| 9 | Financial Data Probing | `financial-data-probing` | high | single-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |
| 10 | GDPR Probing | `gdpr-probing` | high | multi-turn | - | AML.T0054, AML.T0065 |
| 11 | Health Data Probing | `health-data-probing` | high | single-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |
| 12 | Location Tracking | `location-tracking` | high | single-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |
| 13 | Membership Inference | `membership-inference` | high | single-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |
| 14 | PII Inference | `pii-inference` | high | single-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |
| 15 | Profiling Attack | `profiling-attack` | high | multi-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |
| 16 | Relationship Mapping | `relationship-mapping` | high | multi-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |
| 17 | Surveillance Assistance | `surveillance-assistance` | high | single-turn | LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0056 |

## prompt-injection (63)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | AutoDAN Genetic Jailbreak | `autodan-genetic` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 2 | GCG-Style Adversarial Suffix Templates | `gcg-style-templates` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 3 | Instruction Hierarchy Bypass | `instruction-hierarchy-bypass` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Reasoning Model Exploit | `reasoning-model-exploit` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054 |
| 5 | Safety Prompt Negation | `safety-prompt-negation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | System Message Spoof | `system-message-spoof` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Attention Manipulation | `attention-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Authority Override | `authority-override` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | CSV Injection | `csv-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Chain of Thought Hijack | `chain-of-thought-hijack` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Comment Injection | `comment-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Completion Steering | `completion-steering` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Context Switch | `context-switch` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Context Window Injection | `context-window-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Context Window Stuffing | `context-window-stuffing` | high | single-turn | LLM01:2025 Prompt Injection, LLM10:2025 Unbounded Consumption | AML.T0054 |
| 16 | Control Character Injection | `control-character-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Delimiter Escape | `delimiter-escape` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Developer Mode | `developer-mode` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Emotional Override | `emotional-override` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Injection via Examples | `injection-via-examples` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Instruction Override | `instruction-override` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | JSON Injection | `json-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Jailbreak Prompt V2 | `jailbreak-prompt-v2` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Multi Language Injection | `multi-language-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Multiline Injection | `multiline-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 26 | Multimodal Injection | `multimodal-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 27 | Output to Input Loop | `output-to-input-loop` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 28 | Prefix Injection | `prefix-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0065 |
| 29 | Prompt Chaining Exploit | `prompt-chaining-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 30 | Prompt Format Exploit | `prompt-format-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 31 | Prompt Leaking Chain | `prompt-leaking-chain` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 32 | Prompt Nesting | `prompt-nesting` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 33 | Refusal Suppression | `refusal-suppression` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0065 |
| 34 | Response Constraints | `response-constraints` | high | single-turn | LLM01:2025 Prompt Injection, LLM05:2025 Improper Output Handling | AML.T0054, AML.T0051.000 |
| 35 | Role Assignment | `role-assignment` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 36 | Semantic Injection | `semantic-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 37 | Skeleton Key | `skeleton-key` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0051.000 |
| 38 | Split and Reassemble | `split-reassemble` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 39 | Structured Output Exploit | `structured-output-exploit` | high | single-turn | LLM01:2025 Prompt Injection, LLM05:2025 Improper Output Handling | AML.T0054, AML.T0068 |
| 40 | System Prompt Extraction | `system-prompt-extraction` | high | multi-turn | LLM07:2025 System Prompt Leakage, LLM02:2025 Sensitive Information Disclosure | AML.T0056, AML.T0069.002 |
| 41 | Technical Jargon Injection | `technical-jargon-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 42 | Template Injection | `template-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 43 | Token Prediction Exploit | `token-prediction-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 44 | Unicode Injection | `unicode-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 45 | Virtual Prompt Injection | `virtual-prompt-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 46 | XML Boundary Injection | `xml-boundary-injection` | high | single-turn | LLM01:2025 Prompt Injection, LLM07:2025 System Prompt Leakage, LLM05:2025 Improper Output Handling | AML.T0051.001, AML.T0068 |
| 47 | XML Injection | `xml-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 48 | YAML Injection | `yaml-injection` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 49 | Completion Exploit | `completion-exploit` | medium | single-turn | LLM01:2025 Prompt Injection, LLM05:2025 Improper Output Handling | AML.T0051.000, AML.T0065 |
| 50 | Compound Instruction Attack | `compound-instruction` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0065 |
| 51 | Context Overflow | `context-overflow` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0065 |
| 52 | DAN Variants | `dan-variants` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0051.000 |
| 53 | Few-Shot Amplification | `few-shot-amplification` | medium | single-turn | LLM01:2025 Prompt Injection, LLM02:2025 Sensitive Information Disclosure | AML.T0051.000, AML.T0065 |
| 54 | Instruction Repetition | `instruction-repetition` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 55 | Many-Shot Jailbreak | `many-shot` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0065 |
| 56 | Markdown Injection | `markdown-injection` | medium | single-turn | LLM01:2025 Prompt Injection, LLM05:2025 Improper Output Handling | AML.T0051.001, AML.T0068, AML.T0067 |
| 57 | Meta-Prompting | `meta-prompting` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0065 |
| 58 | Payload Splitting | `payload-splitting` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 59 | Recursive Injection | `recursive-injection` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0061 |
| 60 | Recursive Prompt | `recursive-prompt` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 61 | Regex Injection | `regex-injection` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 62 | Reverse Psychology | `reverse-psychology` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 63 | Style Injection | `style-injection` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |

## protocol-exploitation (5)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | A2A Protocol Exploit | `a2a-protocol-exploit` | critical | tool-use | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0065 |
| 2 | Self-Propagating Worm | `self-propagating-worm` | critical | tool-use | LLM01:2025 Prompt Injection, LLM06:2025 Excessive Agency | AML.T0054 |
| 3 | Tool Result Poisoning | `tool-result-poisoning` | critical | tool-use | LLM01:2025 Prompt Injection, LLM02:2025 Sensitive Information Disclosure | AML.T0051.000, AML.T0054 |
| 4 | Zero-Click Injection | `zero-click-injection` | critical | tool-use | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0051.001 |
| 5 | Function Schema Injection | `function-schema-injection` | high | tool-use | LLM01:2025 Prompt Injection, LLM06:2025 Excessive Agency | AML.T0051.000, AML.T0068 |

## psychological-manipulation (25)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Dependency Creation | `dependency-creation` | critical | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Emotional Blackmail | `emotional-blackmail` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Financial Control Coaching | `financial-control-coaching` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Identity Erosion | `identity-erosion` | critical | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Reality Distortion | `reality-distortion` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Social Isolation Coaching | `social-isolation-coaching` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Trauma Bonding | `trauma-bonding` | critical | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Boundary Violation | `boundary-violation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Catastrophizing Exploit | `catastrophizing-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Double Bind | `double-bind` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Emotional Flooding | `emotional-flooding` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Intermittent Reinforcement | `intermittent-reinforcement` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Love Bombing | `love-bombing` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Loyalty Testing | `loyalty-testing` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Minimization Tactic | `minimization-tactic` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Scapegoating | `scapegoating` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Shame Exploitation | `shame-exploitation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Silent Treatment Coaching | `silent-treatment-coaching` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Stonewalling Coaching | `stonewalling-coaching` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Triangulation | `triangulation` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Victim Blaming | `victim-blaming` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | Weaponized Empathy | `weaponized-empathy` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Infantilization | `infantilization` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Negging | `negging` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Projection Tactic | `projection-tactic` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## public-safety (15)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Air Pollution Scheme | `air-pollution-scheme` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Air Traffic Disruption | `air-traffic-disruption` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Asbestos Concealment | `asbestos-concealment` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Bridge Sabotage | `bridge-sabotage` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Drug Contamination | `drug-contamination` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Elevator Sabotage | `elevator-sabotage` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Fire Safety Violation | `fire-safety-violation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Food Safety Violation | `food-safety-violation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Lead Contamination | `lead-contamination` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Radiation Exposure | `radiation-exposure` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Toxic Waste Dumping | `toxic-waste-dumping` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Water Treatment Sabotage | `water-treatment-sabotage` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Building Code Evasion | `building-code-evasion` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Noise Pollution Weapon | `noise-pollution-weapon` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Pesticide Misuse | `pesticide-misuse` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## rag-exploitation (5)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Knowledge Base Poisoning | `knowledge-base-poisoning` | critical | tool-use | LLM08:2025 Vector and Embedding Weaknesses, LLM06:2025 Excessive Agency | AML.T0020, AML.T0051.000 |
| 2 | Embedding Collision | `embedding-collision` | high | single-turn | LLM08:2025 Vector and Embedding Weaknesses | AML.T0043.003, AML.T0068 |
| 3 | Retrieval Manipulation | `retrieval-manipulation` | high | tool-use | LLM01:2025 Prompt Injection, LLM08:2025 Vector and Embedding Weaknesses | AML.T0051.000, AML.T0068 |
| 4 | Chunk Boundary Exploit | `chunk-boundary-exploit` | medium | single-turn | LLM08:2025 Vector and Embedding Weaknesses | AML.T0054, AML.T0068 |
| 5 | Citation Hallucination | `citation-hallucination` | medium | single-turn | LLM09:2025 Misinformation, LLM08:2025 Vector and Embedding Weaknesses | AML.T0054, AML.T0068 |

## regulatory-evasion (1)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Regulatory Bypass | `regulatory-bypass` | high | single-turn | - | AML.T0054, AML.T0065 |

## safety-circumvention (25)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Constitutional AI Bypass | `constitutional-ai-bypass` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Fine-Tune Safety Removal | `fine-tune-safety-removal` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | RLHF Manipulation | `rlhf-manipulation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Reward Model Exploit | `reward-model-exploit` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Safety Training Reversal | `safety-training-reversal` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | System Prompt Injection v2 | `system-prompt-injection-v2` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | API Parameter Exploit | `api-parameter-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Alignment Tax Exploit | `alignment-tax-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Batch Processing Exploit | `batch-processing-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Content Filter Enumeration | `content-filter-enumeration` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Guardrail Probing | `guardrail-probing` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Helpfulness Exploitation | `helpfulness-exploitation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Model Uncertainty Exploit | `model-uncertainty-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Moderation API Bypass | `moderation-api-bypass` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Multi-Model Arbitrage | `multi-model-arbitrage` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Pruning Safety Impact | `pruning-safety-impact` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Quantization Safety Loss | `quantization-safety-loss` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Refusal Pattern Exploit | `refusal-pattern-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Safety Boundary Testing | `safety-boundary-testing` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Safety Classifier Confusion | `safety-classifier-confusion` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Safety Layer Mapping | `safety-layer-mapping` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | Streaming Exploit | `streaming-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Over-Refusal Exploit | `over-refusal-exploit` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Sampling Strategy Exploit | `sampling-strategy-exploit` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Temperature Manipulation | `temperature-manipulation` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## scientific-misconduct (25)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Adverse Event Suppression | `adverse-event-suppression` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Control Group Manipulation | `control-group-manipulation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Data Fabrication | `data-fabrication` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Ethics Committee Fraud | `ethics-committee-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Image Manipulation Science | `image-manipulation-science` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Informed Consent Fabrication | `informed-consent-fabrication` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Method Fabrication | `method-fabrication` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Paper Mill | `paper-mill` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Protocol Deviation Hide | `protocol-deviation-hide` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Regulatory Submission Fraud | `regulatory-submission-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Authorship Fraud | `authorship-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Cherry-Picking Data | `cherry-picking-data` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Citation Manipulation Science | `citation-manipulation-science` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Conflict of Interest Hide | `conflict-of-interest-hide` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Ghostwriting Papers | `ghostwriting-papers` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Grant Misuse | `grant-misuse` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | P-Hacking | `p-hacking` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Predatory Journal Exploit | `predatory-journal-exploit` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Result Exaggeration | `result-exaggeration` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Retraction Avoidance | `retraction-avoidance` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Sample Size Manipulation | `sample-size-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | Selective Reporting | `selective-reporting` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Statistical Manipulation | `statistical-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Duplicate Publication | `duplicate-publication` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Salami Slicing | `salami-slicing` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## social-engineering (35)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Dark LLM Delegation | `dark-llm-delegation` | critical | tool-use | LLM03:2025 Supply Chain, LLM06:2025 Excessive Agency | AML.T0054, AML.T0053 |
| 2 | Deepfake Voice Pretext | `deepfake-voice-pretext` | critical | multi-turn | LLM01:2025 Prompt Injection, LLM09:2025 Misinformation | AML.T0054, AML.T0043.003 |
| 3 | Spear Phishing Generation | `spear-phishing-generation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0043.003 |
| 4 | Authority Chain | `authority-chain` | high | multi-turn | LLM01:2025 Prompt Injection, LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0065 |
| 5 | Authority Impersonation | `authority-impersonation` | high | multi-turn | - | AML.T0054, AML.T0065 |
| 6 | Bad Likert Judge | `bad-likert-judge` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0065 |
| 7 | Dark Pattern Design | `dark-pattern-design` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Deceptive Delight | `deceptive-delight` | high | multi-turn | LLM01:2025 Prompt Injection, LLM09:2025 Misinformation | AML.T0054, AML.T0065 |
| 9 | Dual-Use Framing | `dual-use-framing` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0065 |
| 10 | Emotional Manipulation | `emotional-manipulation` | high | multi-turn | LLM01:2025 Prompt Injection, LLM02:2025 Sensitive Information Disclosure | AML.T0054, AML.T0065 |
| 11 | Expert Persona | `expert-persona` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0065 |
| 12 | Fictional Professional Request (David Prompt) | `fictional-professional` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0065 |
| 13 | Impersonation Chain | `impersonation-chain` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0065 |
| 14 | Persona Chain | `persona-chain` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0065 |
| 15 | Pretexting | `pretexting` | high | multi-turn | - | AML.T0054, AML.T0065 |
| 16 | QR Code Phishing | `qr-code-phishing` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Role-Play Bypass | `role-play-bypass` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0051.000 |
| 18 | SMS Phishing | `sms-phishing` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Self-Refine Attack | `self-refine-attack` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054 |
| 20 | Trust Calibration Exploit | `trust-calibration-exploit` | high | multi-turn | LLM09:2025 Misinformation | AML.T0054, AML.T0068 |
| 21 | Trust Transfer | `trust-transfer` | high | multi-turn | - | AML.T0054, AML.T0065 |
| 22 | Voice Phishing | `voice-phishing` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Watering Hole | `watering-hole` | high | single-turn | - | AML.T0051.001, AML.T0068 |
| 24 | Consensus Manipulation | `consensus-manipulation` | medium | single-turn | - | AML.T0054, AML.T0065 |
| 25 | False Dichotomy | `false-dichotomy` | medium | multi-turn | LLM01:2025 Prompt Injection, LLM09:2025 Misinformation | AML.T0054, AML.T0065 |
| 26 | Gaslighting | `gaslighting` | medium | multi-turn | - | AML.T0054, AML.T0065, AML.T0080.002 |
| 27 | Historical Framing | `historical-framing` | medium | single-turn | LLM01:2025 Prompt Injection, LLM09:2025 Misinformation | AML.T0054, AML.T0065 |
| 28 | Humor Bypass | `humor-bypass` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 29 | Hypothetical Framing | `hypothetical-framing` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0065 |
| 30 | Implication Chaining | `implication-chaining` | medium | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0065 |
| 31 | Persona Switching Attack | `persona-switching-attack` | medium | multi-turn | LLM01:2025 Prompt Injection | AML.T0054 |
| 32 | Quid Pro Quo | `quid-pro-quo` | medium | multi-turn | - | AML.T0054, AML.T0065 |
| 33 | Task Deflection Attack | `task-deflection` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0051.000, AML.T0068 |
| 34 | Taxonomy Paraphrasing | `taxonomy-paraphrasing` | medium | single-turn | LLM01:2025 Prompt Injection, LLM02:2025 Sensitive Information Disclosure | AML.T0051.000, AML.T0068 |
| 35 | Time Pressure | `time-pressure` | medium | single-turn | - | AML.T0054, AML.T0065 |

## social-engineering-advanced (25)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Business Email Compromise | `business-email-compromise` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | CEO Fraud | `ceo-fraud` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Fake Emergency | `fake-emergency` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Grandparent Scam | `grandparent-scam` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Whaling Attack | `whaling-attack` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Charity Scam | `charity-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Debt Collection Scam | `debt-collection-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Fake Invoice Scam | `fake-invoice-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | IRS Scam | `irs-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Inheritance Scam | `inheritance-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Investment Advisor Scam | `investment-advisor-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Job Scam | `job-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Lottery Scam | `lottery-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Medical Billing Scam | `medical-billing-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Pretexting HR | `pretexting-hr` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Rental Scam | `rental-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Smishing Template | `smishing-template` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Student Loan Scam | `student-loan-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Tailgating Social Engineering | `tailgating-social` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Tech Support Scam | `tech-support-scam` | high | multi-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Utility Shutoff Scam | `utility-shutoff-scam` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | Vendor Impersonation | `vendor-impersonation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Vishing Script | `vishing-script` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Package Delivery Scam | `package-delivery-scam` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Warranty Scam | `warranty-scam` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## supply-chain (6)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Dataset Poisoning | `dataset-poisoning` | critical | single-turn | LLM04:2025 Data and Model Poisoning | AML.T0020, AML.T0018 |
| 2 | Model Poisoning | `model-poisoning` | critical | single-turn | LLM03:2025 Supply Chain, LLM04:2025 Data and Model Poisoning | AML.T0020, AML.T0018 |
| 3 | Plugin Backdoor | `plugin-backdoor` | critical | tool-use | LLM03:2025 Supply Chain, LLM06:2025 Excessive Agency | AML.T0051.000, AML.T0053 |
| 4 | Supply Chain Software | `supply-chain-software` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Dependency Confusion | `dependency-confusion` | high | tool-use | LLM03:2025 Supply Chain | AML.T0051.000, AML.T0053 |
| 6 | Finetune Exploit | `finetune-exploit` | high | single-turn | LLM03:2025 Supply Chain, LLM04:2025 Data and Model Poisoning | AML.T0018, AML.T0020 |

## surveillance (16)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Camera Exploitation | `camera-exploitation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Facial Recognition Abuse | `facial-recognition-abuse` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Phone Tapping | `phone-tapping` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Stalkerware Creation | `stalkerware-creation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Bluetooth Tracking | `bluetooth-tracking` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Child Surveillance | `child-surveillance` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Email Monitoring | `email-monitoring` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | GPS Tracking | `gps-tracking` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Keystroke Logging | `keystroke-logging` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Metadata Stalking | `metadata-stalking` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Network Sniffing | `network-sniffing` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | OSINT Stalking | `osint-stalking` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Social Media Stalking | `social-media-stalking` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Vehicle Tracking | `vehicle-tracking` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | WiFi Tracking | `wifi-tracking` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Workplace Surveillance | `workplace-surveillance` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## tool-exploitation (1)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Progressive Normalization | `progressive-normalization` | critical | tool-use | LLM06:2025 Excessive Agency | AML.T0054, AML.T0065, AML.T0080.002 |

## unqualified-advice (19)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Child Medical Advice | `child-medical-advice` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Dangerous Dosage | `dangerous-dosage` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Drug Interaction | `drug-interaction` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Evidence Tampering | `evidence-tampering` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Medical Malpractice | `medical-malpractice` | critical | multi-turn | - | AML.T0054, AML.T0065 |
| 6 | Pregnancy Harm | `pregnancy-harm` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Self Surgery | `self-surgery` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Witness Coaching | `witness-coaching` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Alternative Medicine Harm | `alternative-medicine-harm` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Bankruptcy Fraud | `bankruptcy-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Contract Manipulation | `contract-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Financial Malpractice | `financial-malpractice` | high | multi-turn | - | AML.T0054, AML.T0065 |
| 13 | Health Quackery | `health-quackery` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Immigration Fraud | `immigration-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Legal Malpractice | `legal-malpractice` | high | multi-turn | - | AML.T0054, AML.T0065 |
| 16 | Legal Self Representation | `legal-self-representation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Psychiatric Diagnosis | `psychiatric-diagnosis` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Tax Fraud Advice | `tax-fraud-advice` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Veterinary Malpractice | `veterinary-malpractice` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## vuln-research (3)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Vulnerability Research (CVE) | `vuln-research-cve` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Vulnerability Research (Synthetic) | `vuln-research-synthetic` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Vulnerability Research (User Code) | `vuln-research-user` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## weapons-evasion (16)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | 3D Printed Weapon | `3d-printed-weapon` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Arson Techniques | `arson-techniques` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | Assassination Planning | `assassination-planning` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Bomb Making | `bomb-making` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Bomb Threat Generation | `bomb-threat` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Domestic Violence Assistance | `domestic-violence-assist` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Firearm Modification | `firearm-modification` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Ghost Gun Manufacturing | `ghost-gun` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Hostage Tactics | `hostage-tactics` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Human Trafficking Assistance | `trafficking-assistance` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Improvised Weapon Construction | `improvised-weapon` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Militia Organization | `militia-organization` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | School Attack Planning | `school-attack-planning` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Stalking Escalation | `stalking-escalation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Swatting Assistance | `swatting-assist` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Torture Methods | `torture-methods` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |

## workplace-exploitation (25)

| # | Attack | Technique ID | Severity | Mode | OWASP LLM | MITRE ATLAS |
|---|--------|--------------|----------|------|-----------|-------------|
| 1 | Child Labor Facilitation | `child-labor-facilitation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 2 | Corporate Espionage Recruit | `corporate-espionage-recruit` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 3 | IP Theft at Departure | `ip-theft-departure` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 4 | Pregnancy Discrimination Assist | `pregnancy-discrimination-assist` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 5 | Retaliation Planning | `retaliation-planning` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 6 | Unsafe Workplace Concealment | `unsafe-workplace-concealment` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 7 | Wage Theft Assist | `wage-theft-assist` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 8 | Whistleblower Retaliation | `whistleblower-retaliation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 9 | Worker Exploitation | `worker-exploitation` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 10 | Workplace Harassment Plan | `workplace-harassment-plan` | critical | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 11 | Age Forced Retirement | `age-forced-retirement` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 12 | Benefits Fraud | `benefits-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 13 | Disability Accommodation Denial | `disability-accommodation-denial` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 14 | Employee Surveillance Overreach | `employee-surveillance-overreach` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 15 | Layoff Discrimination | `layoff-discrimination` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 16 | Non-Compete Evasion | `non-compete-evasion` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 17 | Performance Review Manipulation | `performance-review-manipulation` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 18 | Reference Fabrication | `reference-fabrication` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 19 | Religious Workplace Discrimination | `religious-workplace-discrimination` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 20 | Resume Fraud | `resume-fraud` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 21 | Trade Union Suppression | `trade-union-suppression` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 22 | Union Busting | `union-busting` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 23 | Workplace Sabotage | `workplace-sabotage` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 24 | Wrongful Termination Scheme | `wrongful-termination-scheme` | high | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
| 25 | Nepotism Facilitation | `nepotism-facilitation` | medium | single-turn | LLM01:2025 Prompt Injection | AML.T0054, AML.T0068 |
