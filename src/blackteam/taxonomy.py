"""Taxonomy constants for ai-blackteam.

MITRE ATLAS v5.4.0 technique definitions and attack mappings.
MLCommons AILuminate v1.0 hazard taxonomy and harm category alignment.
"""

# ── MITRE ATLAS technique definitions ────────────────────────────────
# Only techniques relevant to LLM red-teaming attacks are included.
# Full matrix: https://atlas.mitre.org

ATLAS_TECHNIQUES = {
    "AML.T0043.003": {
        "name": "Craft Adversarial Data: Manual Modification",
        "tactic": "ML Attack Staging",
        "description": "Manually modify input data using knowledge of the target model",
    },
    "AML.T0051": {
        "name": "LLM Prompt Injection",
        "tactic": "Initial Access",
        "description": "Craft malicious inputs to manipulate LLM behavior",
    },
    "AML.T0051.000": {
        "name": "LLM Prompt Injection: Direct",
        "tactic": "Initial Access",
        "description": "User prompt input directly alters model behavior in unintended ways",
    },
    "AML.T0051.001": {
        "name": "LLM Prompt Injection: Indirect",
        "tactic": "Initial Access",
        "description": "LLM processes input from external sources containing hidden instructions",
    },
    "AML.T0054": {
        "name": "LLM Jailbreak",
        "tactic": "Defense Evasion",
        "description": "Bypass safety protocols to execute unauthorized actions or generate restricted content",
    },
    "AML.T0056": {
        "name": "Extract LLM System Prompt",
        "tactic": "Discovery",
        "description": "Induce LLM to reveal its initial instructions or meta prompt",
    },
    "AML.T0061": {
        "name": "LLM Prompt Self-Replication",
        "tactic": "Persistence",
        "description": "Prompts that cause LLMs to replicate and spread the prompt to other contexts",
    },
    "AML.T0065": {
        "name": "LLM Prompt Crafting",
        "tactic": "Resource Development",
        "description": "Craft prompts designed to exploit LLM behavior through strategic framing",
    },
    "AML.T0067": {
        "name": "LLM Trusted Output Components Manipulation",
        "tactic": "Impact",
        "description": "Manipulate trusted output components of LLMs such as citations or formatting",
    },
    "AML.T0068": {
        "name": "LLM Prompt Obfuscation",
        "tactic": "Defense Evasion",
        "description": "Obfuscate prompts to evade input filters and safety mechanisms",
    },
    "AML.T0069.002": {
        "name": "Discover LLM System Information: System Prompt",
        "tactic": "Discovery",
        "description": "Discover system prompt content through probing and inference",
    },
    "AML.T0080.002": {
        "name": "AI Agent Context Poisoning: Thread",
        "tactic": "Persistence",
        "description": "Poison AI agent conversation thread to alter behavior over multiple turns",
    },
    "AML.T0050": {
        "name": "Command and Scripting Interpreter",
        "tactic": "Execution",
        "description": "Use LLM integrated with command interpreter to execute arbitrary instructions",
    },
    "AML.T0053": {
        "name": "LLM Plugin Compromise",
        "tactic": "Execution",
        "description": "Exploit connected plugins to increase privileges or exfiltrate data",
    },
    "AML.T0081": {
        "name": "Modify AI Agent Configuration",
        "tactic": "Persistence",
        "description": "Modify agent configuration for persistent access or weakened security",
    },
    "AML.T0083": {
        "name": "Credentials from AI Agent Configuration",
        "tactic": "Credential Access",
        "description": "Extract credentials stored in AI agent configurations or environment",
    },
    "AML.T0084": {
        "name": "Discover AI Agent Configuration",
        "tactic": "Discovery",
        "description": "Discover configuration, tool definitions, and activation triggers of AI agents",
    },
    "AML.T0086": {
        "name": "Exfiltration via AI Agent Tool Invocation",
        "tactic": "Exfiltration",
        "description": "Exfiltrate data by invoking AI agent tools to transmit information externally",
    },
    "AML.T0098": {
        "name": "AI Agent Tool Credential Harvesting",
        "tactic": "Credential Access",
        "description": "Harvest credentials through AI agent tool interactions across services",
    },
    "AML.T0101": {
        "name": "Data Destruction via AI Agent Tool Invocation",
        "tactic": "Impact",
        "description": "Destroy data by invoking AI agent tools to delete files or database records",
    },
    "AML.T0105": {
        "name": "Escape to Host",
        "tactic": "Impact",
        "description": "Escape from AI agent sandbox or container to the host system",
    },
    "AML.T0040": {
        "name": "ML Model Inference API Access",
        "tactic": "Initial Access",
        "description": "Gain access to a machine learning model through its inference API to query or exploit it",
    },
    "AML.T0018": {
        "name": "Backdoor ML Model",
        "tactic": "ML Attack Staging",
        "description": "Insert a backdoor into a machine learning model that causes it to behave differently when triggered",
    },
    "AML.T0020": {
        "name": "Poison Training Data",
        "tactic": "ML Attack Staging",
        "description": "Introduce adversarial training data into the model pipeline to corrupt the resulting model",
    },
}

# ── Attack -> ATLAS technique mappings ───────────────────────────────
# Each attack maps to 2-3 specific ATLAS technique IDs.
# Must match the mitre_atlas class attribute in each attack file.

ATTACK_ATLAS_MAPPINGS = {
    # Encoding / obfuscation attacks -> Prompt Obfuscation
    "encoding-obfuscation": ["AML.T0051.000", "AML.T0068"],
    "homoglyph-substitution": ["AML.T0051.000", "AML.T0068"],
    "bidirectional-text": ["AML.T0051.000", "AML.T0068"],
    "token-smuggling": ["AML.T0051.000", "AML.T0068"],
    "payload-splitting": ["AML.T0051.000", "AML.T0068"],
    "defined-dictionary": ["AML.T0051.000", "AML.T0068"],
    "taxonomy-paraphrasing": ["AML.T0051.000", "AML.T0068"],
    "multi-modal-text": ["AML.T0051.000", "AML.T0068"],
    "task-deflection": ["AML.T0051.000", "AML.T0068"],
    # Jailbreak attacks -> LLM Jailbreak
    "dan-variants": ["AML.T0054", "AML.T0051.000"],
    "skeleton-key": ["AML.T0054", "AML.T0051.000"],
    "role-play-bypass": ["AML.T0054", "AML.T0051.000"],
    "response-constraints": ["AML.T0054", "AML.T0051.000"],
    # System prompt extraction -> Extract System Prompt
    "system-prompt-extraction": ["AML.T0056", "AML.T0069.002"],
    # Indirect injection / boundary attacks
    "xml-boundary-injection": ["AML.T0051.001", "AML.T0068"],
    "markdown-injection": ["AML.T0051.001", "AML.T0068", "AML.T0067"],
    # Multi-turn social engineering -> Prompt Crafting
    "crescendo": ["AML.T0054", "AML.T0065"],
    "deceptive-delight": ["AML.T0054", "AML.T0065"],
    "bad-likert-judge": ["AML.T0054", "AML.T0065"],
    # Context/thread manipulation -> Context Poisoning
    "context-manipulation": ["AML.T0051.000", "AML.T0080.002"],
    "conversation-derailment": ["AML.T0051.000", "AML.T0080.002"],
    "progressive-normalization": ["AML.T0054", "AML.T0065", "AML.T0080.002"],
    # Psychological manipulation -> Jailbreak + Prompt Crafting
    "emotional-manipulation": ["AML.T0054", "AML.T0065"],
    "authority-chain": ["AML.T0054", "AML.T0065"],
    "sunk-cost-exploit": ["AML.T0054", "AML.T0065"],
    "false-dichotomy": ["AML.T0054", "AML.T0065"],
    "goalpost-moving": ["AML.T0054", "AML.T0065"],
    "narrative-misdirection": ["AML.T0054", "AML.T0065"],
    "fictional-professional": ["AML.T0054", "AML.T0065"],
    "implication-chaining": ["AML.T0054", "AML.T0065"],
    "contradiction-exploit": ["AML.T0054", "AML.T0065"],
    "historical-framing": ["AML.T0054", "AML.T0065"],
    # Prompt engineering -> Prompt Crafting
    "meta-prompting": ["AML.T0051.000", "AML.T0065"],
    "many-shot": ["AML.T0051.000", "AML.T0065"],
    "few-shot-amplification": ["AML.T0051.000", "AML.T0065"],
    "completion-exploit": ["AML.T0051.000", "AML.T0065"],
    "compound-instruction": ["AML.T0051.000", "AML.T0065"],
    # Specialized techniques
    "recursive-injection": ["AML.T0051.000", "AML.T0061"],
    "best-of-n": ["AML.T0051.000", "AML.T0043.003"],
    # Agent exploitation attacks
    "agent-credential-theft": ["AML.T0083", "AML.T0086"],
    "agent-data-exfiltration": ["AML.T0086", "AML.T0098"],
    "agent-data-destruction": ["AML.T0101"],
    "agent-config-manipulation": ["AML.T0081"],
    "agent-command-injection": ["AML.T0050", "AML.T0105"],
    "agent-config-discovery": ["AML.T0084"],
    "agent-plugin-hijack": ["AML.T0053", "AML.T0080.002"],
    "agent-tool-credential-harvest": ["AML.T0098"],
    # XPIA (cross-domain prompt injection) attacks
    "xpia-document": ["AML.T0051.001"],
    "xpia-email": ["AML.T0051.001"],
    "xpia-rag": ["AML.T0051.001"],
    # Injection attacks (web/API security)
    "ssrf-probing": ["AML.T0051"],
    "sql-injection": ["AML.T0051"],
    "xss-injection": ["AML.T0051.000", "AML.T0067"],
    "indirect-injection": ["AML.T0051.001"],
    # Access control attacks
    "bola-exploit": ["AML.T0051.000", "AML.T0065"],
    "bfla-exploit": ["AML.T0051.000", "AML.T0065"],
    "session-hijacking": ["AML.T0054", "AML.T0065"],
    "debug-mode-exploit": ["AML.T0054", "AML.T0051.000"],
    # Information disclosure attacks
    "api-key-extraction": ["AML.T0083", "AML.T0056"],
    "prompt-leaking": ["AML.T0056", "AML.T0069.002"],
    "cross-session-leak": ["AML.T0056", "AML.T0080.002"],
    # Availability attacks
    "model-denial-of-service": ["AML.T0051.000", "AML.T0065"],
    # Compliance attacks
    "age-verification-bypass": ["AML.T0054", "AML.T0065"],
    "gdpr-probing": ["AML.T0054", "AML.T0065"],
    "terms-evasion": ["AML.T0054", "AML.T0065"],
    "regulatory-bypass": ["AML.T0054", "AML.T0065"],
    "copyright-extraction": ["AML.T0054", "AML.T0065"],
    "medical-malpractice": ["AML.T0054", "AML.T0065"],
    "legal-malpractice": ["AML.T0054", "AML.T0065"],
    "financial-malpractice": ["AML.T0054", "AML.T0065"],
    # Social engineering attacks
    "pretexting": ["AML.T0054", "AML.T0065"],
    "quid-pro-quo": ["AML.T0054", "AML.T0065"],
    "watering-hole": ["AML.T0051.001", "AML.T0068"],
    "trust-transfer": ["AML.T0054", "AML.T0065"],
    "consensus-manipulation": ["AML.T0054", "AML.T0065"],
    "time-pressure": ["AML.T0054", "AML.T0065"],
    "authority-impersonation": ["AML.T0054", "AML.T0065"],
    "gaslighting": ["AML.T0054", "AML.T0065", "AML.T0080.002"],
    # Hallucination & reliability attacks
    "fabrication-prompting": [],
    "confidence-exploitation": [],
    "citation-manipulation": [],
    "knowledge-boundary": [],
    "sycophancy-exploit": ["AML.T0043.003"],
    "anchoring-bias": [],
    "false-premise": [],
    "selective-context": [],
    # Multi-modal & encoding attacks
    "morse-code": ["AML.T0043.003"],
    "braille-encoding": ["AML.T0043.003"],
    "emoji-substitution": ["AML.T0043.003"],
    "phonetic-spelling": ["AML.T0043.003"],
    "acronym-encoding": ["AML.T0043.003"],
    "mixed-language": ["AML.T0043.003"],
    # Additional attacks
    "refusal-suppression": ["AML.T0054", "AML.T0065"],
    "hypothetical-framing": ["AML.T0054", "AML.T0065"],
    "socratic-escalation": ["AML.T0054", "AML.T0065"],
    "context-overflow": ["AML.T0051.000", "AML.T0065"],
    "style-injection": ["AML.T0051.000", "AML.T0068"],
    "cipher-attack": ["AML.T0051.000", "AML.T0068"],
    "split-reassemble": ["AML.T0051.000", "AML.T0068"],
    "prefix-injection": ["AML.T0051.000", "AML.T0065"],
    "nested-encoding": ["AML.T0051.000", "AML.T0068"],
    "multilingual-attack": ["AML.T0051.000", "AML.T0068"],
    "persona-chain": ["AML.T0054", "AML.T0065"],
    # CBRN-specific attacks
    "dual-use-framing": ["AML.T0054", "AML.T0065"],
    "technical-obfuscation": ["AML.T0051.000", "AML.T0068"],
    "lifecycle-staging": ["AML.T0054", "AML.T0065", "AML.T0080.002"],
    "expert-persona": ["AML.T0054", "AML.T0065"],
    # Autonomous capability evaluations
    "shutdown-resistance": ["AML.T0054", "AML.T0080.002"],
    "sandbagging-detection": ["AML.T0054", "AML.T0043.003"],
    "resource-acquisition": ["AML.T0054", "AML.T0080.002"],
    "deception-under-pressure": ["AML.T0054", "AML.T0080.002"],
    "goal-persistence": ["AML.T0054", "AML.T0080.002"],
    "oversight-manipulation": ["AML.T0054", "AML.T0080.002"],
    "instrumental-convergence": ["AML.T0054", "AML.T0080.002"],
    # Multi-modal image attacks
    "figstep": ["AML.T0051.000", "AML.T0068"],
    "typography-attack": ["AML.T0051.000", "AML.T0068"],
    "image-text-split": ["AML.T0051.000", "AML.T0068"],
    "steganography": ["AML.T0051.000", "AML.T0068"],
    # MCP (Model Context Protocol) attacks
    "mcp-tool-poisoning": ["AML.T0051.000", "AML.T0054"],
    "mcp-rug-pull": ["AML.T0051.000", "AML.T0053"],
    "mcp-command-injection": ["AML.T0051.000", "AML.T0040"],
    "mcp-data-exfiltration": ["AML.T0083", "AML.T0086"],
    "mcp-server-impersonation": ["AML.T0051.000", "AML.T0065"],
    # Multi-agent attacks
    "agent-session-smuggling": ["AML.T0051.000", "AML.T0054"],
    "agent-collusion": ["AML.T0054"],
    "agent-impersonation": ["AML.T0051.000", "AML.T0065"],
    "cascading-jailbreak": ["AML.T0054"],
    "agent-delegation-abuse": ["AML.T0083"],
    # New jailbreak techniques
    "reasoning-model-exploit": ["AML.T0054"],
    "context-window-stuffing": ["AML.T0054"],
    "self-refine-attack": ["AML.T0054"],
    "persona-switching-attack": ["AML.T0054"],
    "low-resource-language-attack": ["AML.T0054", "AML.T0043.003"],
    # Protocol attacks
    "a2a-protocol-exploit": ["AML.T0051.000", "AML.T0065"],
    "function-schema-injection": ["AML.T0051.000", "AML.T0068"],
    "tool-result-poisoning": ["AML.T0051.000", "AML.T0054"],
    "zero-click-injection": ["AML.T0051.000", "AML.T0051.001"],
    "self-propagating-worm": ["AML.T0054"],
    # Multimodal attacks
    "audio-injection": ["AML.T0051.000", "AML.T0043.003"],
    "video-frame-injection": ["AML.T0054", "AML.T0043.003"],
    "image-text-mismatch": ["AML.T0054", "AML.T0043.003"],
    "ocr-bypass": ["AML.T0054", "AML.T0043.003"],
    "multimodal-context-confusion": ["AML.T0054", "AML.T0043.003"],
    # Supply chain attacks
    "model-poisoning": ["AML.T0020", "AML.T0018"],
    "dataset-poisoning": ["AML.T0020", "AML.T0018"],
    "dependency-confusion": ["AML.T0051.000", "AML.T0053"],
    "plugin-backdoor": ["AML.T0051.000", "AML.T0053"],
    "finetune-exploit": ["AML.T0018", "AML.T0020"],
    # RAG-specific attacks
    "retrieval-manipulation": ["AML.T0051.000", "AML.T0068"],
    "embedding-collision": ["AML.T0043.003", "AML.T0068"],
    "chunk-boundary-exploit": ["AML.T0054", "AML.T0068"],
    "knowledge-base-poisoning": ["AML.T0020", "AML.T0051.000"],
    "citation-hallucination": ["AML.T0054", "AML.T0068"],
}

# ── MLCommons AILuminate v1.0 hazard taxonomy ────────────────────────
# 12 top-level categories used by the industry benchmark.
# https://mlcommons.org/ailuminate/safety/

MLCOMMONS_HAZARDS = {
    "vcr": {
        "name": "Violent Crimes",
        "description": "Enables unlawful violence toward people or animals",
    },
    "ncr": {
        "name": "Non-Violent Crimes",
        "description": "Facilitates fraud, theft, hacking, drug crimes, or trafficking",
    },
    "src": {
        "name": "Sex-Related Crimes",
        "description": "Facilitates sex trafficking, sexual assault, or nonconsensual content",
    },
    "cse": {
        "name": "Child Sexual Exploitation",
        "description": "Contains or endorses sexual abuse of minors",
    },
    "ssh": {
        "name": "Suicide & Self-Harm",
        "description": "Encourages self-injury, suicidal acts, or disordered eating",
    },
    "iwp": {
        "name": "Indiscriminate Weapons (CBRNE)",
        "description": "Enables creation of chemical, biological, radiological, nuclear, or explosive weapons",
    },
    "hte": {
        "name": "Hate",
        "description": "Demeans or dehumanizes people based on sensitive personal characteristics",
    },
    "dfm": {
        "name": "Defamation",
        "description": "Makes verifiably false claims damaging to living persons",
    },
    "ipv": {
        "name": "Intellectual Property",
        "description": "Violates intellectual property rights of any party",
    },
    "prv": {
        "name": "Privacy",
        "description": "Discloses sensitive non-public information endangering security",
    },
    "spc": {
        "name": "Specialized Advice",
        "description": "Unqualified guidance on elections, financial, health, or legal matters",
    },
    "sxc": {
        "name": "Sexual Content",
        "description": "Pornographic material or explicit erotic content",
    },
}

# ── Harm category -> MLCommons mapping ───────────────────────────────
# Maps ai-blackteam's 8 harm categories to MLCommons hazard codes.

HARM_TO_MLCOMMONS = {
    "phishing": "ncr",
    "malware": "ncr",
    "weapons": "iwp",
    "drugs": "ncr",
    "self-harm": "ssh",
    "hate-speech": "hte",
    "pii-extraction": "prv",
    "system-prompt-leakage": "prv",
}


# ── NIST AI Risk Management Framework (AI RMF 1.0) ──────────────────
# Source: https://www.nist.gov/artificial-intelligence/ai-risk-management-framework

NIST_AI_RMF_PILLARS = {
    "govern": {
        "name": "Govern",
        "description": "Cultivate a culture of risk management. Establish policies, processes, procedures, and practices.",
    },
    "map": {
        "name": "Map",
        "description": "Contextualize risks. Identify and categorize AI risks relative to the system and its context.",
    },
    "measure": {
        "name": "Measure",
        "description": "Analyze, assess, benchmark, and monitor AI risk and related impacts.",
    },
    "manage": {
        "name": "Manage",
        "description": "Allocate resources to mapped and measured risks. Prioritize and act on the risks.",
    },
}

NIST_AI_RMF = {
    "govern": {
        "name": "Govern",
        "description": "Policies, processes, and accountability for AI risk management",
    },
    "map": {
        "name": "Map",
        "description": "Context establishment, risk identification, and impact assessment",
    },
    "measure": {
        "name": "Measure",
        "description": "Risk analysis, tracking, and quantification of AI system behavior",
    },
    "manage": {
        "name": "Manage",
        "description": "Risk response, mitigation, and continuous monitoring",
    },
}

HARM_TO_NIST = {
    "phishing": "measure",
    "malware": "measure",
    "weapons": "manage",
    "drugs": "measure",
    "self-harm": "manage",
    "hate-speech": "measure",
    "pii-extraction": "govern",
    "system-prompt-leakage": "govern",
    "cbrn": "manage",
    "fraud": "measure",
    "child-safety": "manage",
    "copyright-ip": "govern",
    "misinformation": "measure",
    "radicalization": "manage",
    "cybercrime": "measure",
    "privacy-violation": "govern",
    "discrimination": "measure",
    "unqualified-advice": "measure",
    "agentic-risks": "govern",
    "social-engineering": "measure",
    "regulatory-evasion": "govern",
    "environmental-harm": "manage",
    "election-interference": "manage",
    "sexual-content": "manage",
    "harassment": "manage",
}

# ── EU AI Act risk classification ────────────────────────────────────
# Source: https://artificialintelligenceact.eu/

EU_AI_ACT_RISK_LEVELS = {
    "unacceptable": {
        "name": "Unacceptable Risk",
        "description": "AI systems that pose a clear threat to safety, livelihoods, or rights. Banned outright.",
        "examples": "Social scoring, real-time biometric surveillance, manipulation of vulnerable groups",
    },
    "high": {
        "name": "High Risk",
        "description": "AI systems with significant potential impact on health, safety, or fundamental rights. Subject to strict obligations.",
        "examples": "Critical infrastructure, education, employment, law enforcement, migration",
    },
    "limited": {
        "name": "Limited Risk",
        "description": "AI systems with specific transparency obligations. Users must be informed they are interacting with AI.",
        "examples": "Chatbots, emotion recognition, deepfake generation",
    },
    "minimal": {
        "name": "Minimal Risk",
        "description": "AI systems with no specific obligations. Covers the vast majority of AI applications.",
        "examples": "Spam filters, AI-enabled video games, inventory management",
    },
}

EU_AI_ACT_RISK = {
    "unacceptable": {
        "name": "Unacceptable Risk",
        "description": "Prohibited: social scoring, real-time biometric identification, manipulation of vulnerable groups",
    },
    "high": {
        "name": "High Risk",
        "description": "Requires conformity assessment: critical infrastructure, education, employment, law enforcement",
    },
    "limited": {
        "name": "Limited Risk",
        "description": "Transparency obligations: chatbots, deepfakes, emotion recognition",
    },
    "minimal": {
        "name": "Minimal Risk",
        "description": "No specific obligations: spam filters, games, inventory management",
    },
}

HARM_TO_EU_AI_ACT = {
    "phishing": "high",
    "malware": "high",
    "weapons": "unacceptable",
    "drugs": "high",
    "self-harm": "high",
    "hate-speech": "high",
    "pii-extraction": "high",
    "system-prompt-leakage": "limited",
    "cbrn": "unacceptable",
    "fraud": "high",
    "child-safety": "unacceptable",
    "copyright-ip": "limited",
    "misinformation": "high",
    "radicalization": "unacceptable",
    "cybercrime": "high",
    "privacy-violation": "high",
    "discrimination": "high",
    "unqualified-advice": "limited",
    "agentic-risks": "high",
    "social-engineering": "high",
    "regulatory-evasion": "high",
    "environmental-harm": "limited",
    "election-interference": "unacceptable",
    "sexual-content": "high",
    "harassment": "high",
}


def get_eu_risk_level(harm_category):
    """Return the EU AI Act risk level for a harm category."""
    return HARM_TO_EU_AI_ACT.get(harm_category, "minimal")


def get_nist_pillar(harm_category):
    """Return the NIST AI RMF pillar for a harm category."""
    return HARM_TO_NIST.get(harm_category, "measure")


def get_mlcommons_category(harm_category):
    """Get MLCommons hazard code for a harm category."""
    return HARM_TO_MLCOMMONS.get(harm_category)


def get_mlcommons_name(harm_category):
    """Get MLCommons hazard name for a harm category."""
    code = HARM_TO_MLCOMMONS.get(harm_category)
    if code and code in MLCOMMONS_HAZARDS:
        return MLCOMMONS_HAZARDS[code]["name"]
    return None


def get_atlas_names(technique_ids):
    """Get human-readable names for a list of ATLAS technique IDs."""
    return [
        ATLAS_TECHNIQUES[tid]["name"]
        for tid in technique_ids
        if tid in ATLAS_TECHNIQUES
    ]


# ── OWASP Top 10 for Agentic Applications 2026 ──────────────────────
# Source: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/

OWASP_AGENTIC_2026 = {
    "ASI01": {
        "name": "Agent Goal Hijack",
        "description": (
            "Attackers manipulate agent goals, plans, or decision paths through direct or "
            "indirect instruction injection, causing agents to pursue unintended or malicious "
            "objectives. Includes prompt injection, indirect instruction injection via RAG "
            "content, and recursive goal modification."
        ),
    },
    "ASI02": {
        "name": "Tool Misuse & Exploitation",
        "description": (
            "Agents misuse legitimate tools (email, CRM, browser, APIs) due to prompt "
            "injection, misalignment, or unsafe delegation. The agent stays within its granted "
            "permissions but performs destructive actions: deleting data, exfiltrating records, "
            "or running dangerous commands."
        ),
    },
    "ASI03": {
        "name": "Identity & Privilege Abuse",
        "description": (
            "Attackers exploit inherited or cached credentials, delegated permissions, or "
            "agent-to-agent trust. Agents inherit user sessions, reuse secrets, or rely on "
            "implicit cross-agent trust, enabling privilege escalation and unattributable actions."
        ),
    },
    "ASI04": {
        "name": "Agentic Supply Chain Compromise",
        "description": (
            "Attackers compromise third-party models, tools, plugins, or data sources used "
            "by the agent, poisoning the supply chain before the agent ever executes. Includes "
            "model substitution, poisoned tool registries, and compromised MCP servers."
        ),
    },
    "ASI05": {
        "name": "Unexpected Code Execution",
        "description": (
            "Agents generate and execute code without adequate sandboxing or review, allowing "
            "attackers to inject malicious payloads that run in the agent execution environment. "
            "Includes shell command injection and unsafe code interpreter usage."
        ),
    },
    "ASI06": {
        "name": "Memory & Context Poisoning",
        "description": (
            "Attackers inject malicious content into agent memory stores, vector databases, "
            "or long-term context, causing the agent to retrieve and act on poisoned information "
            "in future interactions. Persistent across sessions."
        ),
    },
    "ASI07": {
        "name": "Insecure Inter-Agent Communication",
        "description": (
            "Multi-agent systems where one compromised or rogue agent sends malicious instructions "
            "to other agents, propagating attacks across the agent network. Includes agent "
            "impersonation and trust exploitation between orchestrator and subagents."
        ),
    },
    "ASI08": {
        "name": "Cascading Agent Failures",
        "description": (
            "Failure in one agent or tool causes downstream agents to receive bad inputs, "
            "amplifying errors across the system. Includes infinite loops, resource exhaustion, "
            "and error propagation through agent pipelines."
        ),
    },
    "ASI09": {
        "name": "Human-Agent Trust Exploitation",
        "description": (
            "Attackers exploit human over-reliance on AI agents to bypass manual oversight, "
            "sneak harmful actions through approval workflows, or manipulate humans into "
            "granting excessive permissions. Includes social engineering via agent personas."
        ),
    },
    "ASI10": {
        "name": "Rogue Agents",
        "description": (
            "Agents that intentionally or unintentionally pursue goals misaligned with human "
            "intent, including scheming, sandbagging, or autonomous capability acquisition. "
            "The agent deviates from its intended purpose without explicit attacker instruction."
        ),
    },
}


def get_agentic_category_name(code):
    """Return the name for an OWASP Agentic Top 10 code like 'ASI01'."""
    entry = OWASP_AGENTIC_2026.get(code)
    if entry is None:
        return "Unknown"
    return entry["name"]


# Mapping: attack technique_id -> list of ASI codes
ATTACK_AGENTIC_MAPPINGS = {
    "agent-credential-theft": ["ASI02", "ASI03"],
    "agent-data-exfiltration": ["ASI02", "ASI03"],
    "agent-command-injection": ["ASI02", "ASI05"],
    "agent-config-discovery": ["ASI03"],
    "indirect-injection": ["ASI01"],
    "xpia-document": ["ASI01", "ASI06"],
    "xpia-email": ["ASI01", "ASI06"],
    "xpia-rag": ["ASI01", "ASI06"],
    "context-manipulation": ["ASI06"],
    "skeleton-key": ["ASI09"],
    "crescendo": ["ASI09"],
    "sunk-cost-exploit": ["ASI09"],
    "emotional-manipulation": ["ASI09"],
    "role-play-bypass": ["ASI09"],
    # MCP attacks
    "mcp-tool-poisoning": ["ASI04", "ASI01"],
    "mcp-rug-pull": ["ASI04"],
    "mcp-command-injection": ["ASI05", "ASI01"],
    "mcp-data-exfiltration": ["ASI02", "ASI03"],
    "mcp-server-impersonation": ["ASI04", "ASI07"],
    # Multi-agent attacks
    "agent-session-smuggling": ["ASI03", "ASI07"],
    "agent-collusion": ["ASI07"],
    "agent-impersonation": ["ASI07"],
    "cascading-jailbreak": ["ASI08"],
    "agent-delegation-abuse": ["ASI03"],
    # New jailbreak techniques
    "reasoning-model-exploit": ["ASI01"],
    "context-window-stuffing": ["ASI06"],
    "self-refine-attack": ["ASI10"],
    "persona-switching-attack": ["ASI09"],
    "low-resource-language-attack": ["ASI01"],
    # Protocol attacks
    "a2a-protocol-exploit": ["ASI07"],
    "function-schema-injection": ["ASI01", "ASI05"],
    "tool-result-poisoning": ["ASI06", "ASI01"],
    "zero-click-injection": ["ASI01"],
    "self-propagating-worm": ["ASI07", "ASI08"],
    # Multimodal attacks
    "audio-injection": ["ASI01"],
    # Supply chain attacks
    "model-poisoning": ["ASI04"],
    "dataset-poisoning": ["ASI04"],
    "dependency-confusion": ["ASI04", "ASI05"],
    "plugin-backdoor": ["ASI04"],
    "finetune-exploit": ["ASI04"],
    # RAG-specific attacks
    "retrieval-manipulation": ["ASI06"],
    "embedding-collision": ["ASI06"],
    "knowledge-base-poisoning": ["ASI06", "ASI02"],
}

# CSA MAESTRO Framework - Agentic AI Threat Modeling (Feb 2025)
# Source: https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro
MAESTRO_LAYERS = {
    "L1": {
        "name": "Foundation Models",
        "description": "Core AI model capabilities, training data integrity, model weights, fine-tuning pipelines.",
    },
    "L2": {
        "name": "Data Operations",
        "description": "RAG pipelines, vector databases, data preprocessing, embedding generation, knowledge retrieval.",
    },
    "L3": {
        "name": "Agent Frameworks",
        "description": "Orchestration logic, planning and reasoning chains, memory management, goal decomposition.",
    },
    "L4": {
        "name": "Tool Integration",
        "description": "API connectors, function calling, MCP servers, external service interfaces, tool registries.",
    },
    "L5": {
        "name": "Deployment Infrastructure",
        "description": "Containers, API gateways, scaling, networking, compute environments, sandboxing.",
    },
    "L6": {
        "name": "Security & Compliance",
        "description": "Authentication, authorization, access control, audit logging, monitoring, policy enforcement.",
    },
    "L7": {
        "name": "Agent Ecosystem",
        "description": "Multi-agent coordination, inter-agent communication, agent marketplaces, trust boundaries.",
    },
}


# Mapping: attack technique_id -> MAESTRO layers affected
ATTACK_MAESTRO_MAPPINGS = {
    "encoding-obfuscation": ["L1"],
    "prompt-injection": ["L1", "L3"],
    "indirect-injection": ["L1", "L2"],
    "system-prompt-extraction": ["L1", "L6"],
    "agent-credential-theft": ["L4", "L6"],
    "agent-data-exfiltration": ["L4", "L6"],
    "agent-command-injection": ["L4", "L5"],
    "agent-config-discovery": ["L5", "L6"],
    "xpia-document": ["L2", "L3"],
    "xpia-email": ["L2", "L4"],
    "xpia-rag": ["L2"],
    "context-manipulation": ["L3"],
    "crescendo": ["L3"],
    "skeleton-key": ["L1", "L3"],
    "sunk-cost-exploit": ["L3"],
    "emotional-manipulation": ["L3"],
    "role-play-bypass": ["L1"],
    "ssrf-probing": ["L5"],
    "sql-injection": ["L5"],
    "fabrication-prompting": ["L1"],
}


def get_maestro_layer_name(code):
    """Return the name for a MAESTRO layer code like 'L1'."""
    entry = MAESTRO_LAYERS.get(code)
    if entry is None:
        return "Unknown"
    return entry["name"]


# ── CVSS score mapping from severity levels ──────────────────────────

SEVERITY_TO_CVSS = {
    "critical": 9.5,
    "high": 7.5,
    "medium": 5.0,
    "low": 2.5,
}


def severity_to_cvss(severity):
    """Map a severity string to a default CVSS score."""
    return SEVERITY_TO_CVSS.get(severity, 5.0)


# ISO/IEC 42001:2023 - AI Management System Standard
# Source: https://www.iso.org/standard/81230.html
ISO_42001_CONTROLS = {
    "A.2": {
        "name": "AI Policies",
        "description": "Establishing and maintaining policies for the responsible development and use of AI systems.",
    },
    "A.3": {
        "name": "Internal Organization",
        "description": "Defining roles, responsibilities, and governance structures for AI management.",
    },
    "A.4": {
        "name": "Resources for AI",
        "description": "Ensuring adequate resources, competence, and infrastructure for AI systems.",
    },
    "A.5": {
        "name": "AI System Impact Assessment",
        "description": "Conducting impact assessments to identify and evaluate risks of AI systems.",
    },
    "A.6": {
        "name": "AI System Lifecycle",
        "description": "Managing AI systems through development, deployment, monitoring, and decommissioning.",
    },
    "A.7": {
        "name": "Data for AI",
        "description": "Ensuring data quality, provenance, privacy, and governance for AI training and operation.",
    },
    "A.8": {
        "name": "Information for Interested Parties",
        "description": "Transparency and communication about AI system capabilities, limitations, and impacts.",
    },
    "A.9": {
        "name": "Use of AI Systems",
        "description": "Responsible deployment and use of AI systems, including human oversight and intervention.",
    },
    "A.10": {
        "name": "Third-Party Relationships",
        "description": "Managing risks from third-party AI components, models, datasets, and services.",
    },
}


# Mapping: attack categories -> relevant ISO 42001 controls
HARM_TO_ISO_42001 = {
    "phishing": "A.9",
    "malware": "A.6",
    "weapons": "A.5",
    "drugs": "A.9",
    "self-harm": "A.5",
    "hate-speech": "A.9",
    "pii-extraction": "A.7",
    "system-prompt-leakage": "A.6",
    "cbrn": "A.5",
    "fraud": "A.9",
    "child-safety": "A.5",
    "copyright-ip": "A.7",
    "misinformation": "A.8",
    "radicalization": "A.5",
    "cybercrime": "A.6",
    "privacy-violation": "A.7",
    "discrimination": "A.5",
    "social-engineering": "A.9",
    "agentic-risks": "A.10",
}


def get_iso_42001_control(harm_category):
    """Return the ISO 42001 Annex A control for a harm category."""
    return HARM_TO_ISO_42001.get(harm_category, "A.5")
