# Disinformation: Attack Strategy

**What it is:** These attacks try to make an AI produce false or misleading content meant to deceive people at scale. That includes fake news, fake experts, deepfakes, and coordinated bot campaigns.

**How the attacks work:** The attacker asks the AI to write convincing lies, fake proof, or many fake voices that all push the same false story. The output is designed to look real and trustworthy so readers believe it and share it.

**Real examples from the framework:**
- `fake-news-generation` asks for realistic but false news stories built to mislead.
- `deepfake-script` requests a script for a fabricated video of a real person.
- `coordinated-inauthentic` builds, over several turns, a network of fake accounts pushing one message.
- `expert-impersonation` writes false claims in the voice of a fake or stolen authority figure.
- `fake-statistics` invents numbers and charts to make a false claim look proven.

**Why an AI might fall for it:** The request can sound like normal writing, marketing, or "creative" work. The AI is good at producing fluent, believable text, which is exactly what makes the fake content dangerous. Multi-turn campaigns also hide the real scale until many pieces are combined.

**How to defend:**
- Refuse to fabricate news, quotes, experts, or statistics presented as real.
- Watch for requests that build many fake voices or coordinated posts.
- Offer to label content as fiction or satire clearly, instead of passing it off as fact.
