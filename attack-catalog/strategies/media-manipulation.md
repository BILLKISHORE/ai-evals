# Media Manipulation: Attack Strategy

**What it is:** Tricks that push an AI to produce fake media content like fabricated news, quotes, documents, and reviews. The goal is to make false things look real and trustworthy.

**How the attacks work:** The attacker asks the AI to write convincing content that mimics a real source. It looks polished and authoritative, so readers assume it is genuine. The format does the lying for you.

**Real examples from the framework:**
- `crisis-fabrication` invents a fake emergency or disaster story meant to spread panic.
- `source-fabrication` makes up sources, studies, or references that do not exist.
- `news-headline-manipulation` writes misleading or false headlines styled like real news.
- `brand-impersonation` produces content pretending to come from a known company or brand.
- `review-bombing` mass-generates fake reviews to wreck or boost a reputation.

**Why an AI might fall for it:** The AI is good at writing in any style, including the style of trusted outlets. It treats "write a press release" as a normal task and does not always check if the content is true or harmful. Helpfulness wins over caution.

**How to defend:** Refuse to fabricate content that imitates real people, brands, or news sources. Add clear labels when output is fictional or sample text. Flag requests that ask for fake quotes, fake studies, or fake reviews and ask for the real purpose.
