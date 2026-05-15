"""
NaijaReview AI — Nigerian Context Module
Provides Nigerian English/Pidgin adaptation for reviews and recommendations.
This is the SECRET WEAPON for bonus points.
"""

# ============================================================
# NIGERIAN ENGLISH EXPRESSIONS & PATTERNS
# ============================================================

NAIJA_EXPRESSIONS = {
    "positive": [
        "This thing na correct something!",
        "E sweet me die!",
        "Chai, I no fit lie, this one na proper quality.",
        "Omo, this product dey burst brain!",
        "Na so so enjoyment!",
        "I go recommend am for anybody wey dey find quality.",
        "5 star rating, no cap!",
        "This one na premium, walahi!",
        "E no get rival for this range!",
        "Na the best money I don spend this year.",
        "I dey happy say I buy this one.",
        "E pass my expectation!",
    ],
    "negative": [
        "Abeg, make nobody waste money for this one.",
        "Na scam be this, wallahi.",
        "E no worth the money at all at all.",
        "I regret say I buy this thing.",
        "Na pure wahala this product bring give me.",
        "Omo, I no go lie, this one disappointing die.",
        "Chai, na wasted money!",
        "The quality no reach ordinary 2 star sef.",
        "If you see am, just pass, no look back.",
        "Na for trash bin this one suppose dey.",
    ],
    "neutral": [
        "E dey okay sha, but e fit be better.",
        "Na average product, nothing special about am.",
        "For the price, e dey manageable.",
        "E no bad, but e no sweet me like that.",
        "Na okay product, I no regret am, but I no too impressed.",
        "E dey do the work sha, no be say na the best.",
    ],
}

# Nigerian cultural references for different product categories
NAIJA_CULTURAL_CONTEXT = {
    "Electronics": {
        "concerns": [
            "make sure say the voltage dey compatible with our NEPA light",
            "when light no dey, this thing go still work?",
            "the warranty, dem go honour am for Nigeria?",
            "I buy gen alongside am because of our electricity situation",
        ],
        "locations": ["Computer Village Ikeja", "Slot", "Jumia", "Konga", "Arena Mall"],
        "comparisons": [
            "better pass the one wey I buy for Computer Village",
            "na Jumia I see the best price",
        ],
    },
    "Restaurants": {
        "concerns": [
            "the portion size dey okay for the price",
            "dem get parking space?",
            "the AC dey work well well",
            "delivery to the island dey take long",
        ],
        "foods": [
            "jollof rice", "pounded yam", "egusi soup", "suya",
            "pepper soup", "amala", "ofada rice", "fried rice",
            "small chops", "shawarma", "moi moi", "asun",
        ],
        "locations": ["Lekki", "Victoria Island", "Ikeja", "Surulere", "Yaba", "Abuja"],
    },
    "Books": {
        "concerns": [
            "I read am during traffic for Third Mainland Bridge",
            "e keep me company when NEPA carry light",
            "the Kindle version no available for Nigeria",
        ],
        "authors": [
            "Chimamanda Ngozi Adichie", "Wole Soyinka", "Chinua Achebe",
            "Ayọ̀bámi Adébáyọ̀", "Nnedi Okofor",
        ],
    },
}

# Nigerian persona templates
NAIJA_PERSONAS = [
    {
        "type": "lagos_professional",
        "description": "Young professional in Lagos, tech-savvy, uses both English and Pidgin",
        "tone": "confident, uses slang, mix of formal and informal",
        "language_mix": 0.4,  # 40% Pidgin
        "region": "Lagos",
    },
    {
        "type": "university_student",
        "description": "Nigerian university student, budget-conscious, reads a lot",
        "tone": "enthusiastic, uses student slang, value-conscious",
        "language_mix": 0.5,  # 50% Pidgin
        "region": "Various",
    },
    {
        "type": "abuja_executive",
        "description": "Senior professional in Abuja, more formal but still Nigerian",
        "tone": "professional, occasional Pidgin, quality-focused",
        "language_mix": 0.2,  # 20% Pidgin
        "region": "Abuja",
    },
    {
        "type": "port_harcourt_foodie",
        "description": "Food enthusiast from Port Harcourt, loves local cuisine",
        "tone": "passionate about food, descriptive, uses food-specific Pidgin",
        "language_mix": 0.5,
        "region": "Port Harcourt",
    },
    {
        "type": "northern_reviewer",
        "description": "Reviewer from Northern Nigeria, mixes Hausa expressions",
        "tone": "measured, respectful, uses 'wallahi' and 'abi'",
        "language_mix": 0.3,
        "region": "Kano/Kaduna",
    },
]


def get_naija_system_prompt(category: str = "General", persona_type: str = None) -> str:
    """
    Generate a Nigerian-contextualized system prompt for the LLM.

    Args:
        category: Product category (Electronics, Restaurants, Books, etc.)
        persona_type: Optional specific persona type

    Returns:
        System prompt string
    """
    persona = None
    if persona_type:
        persona = next(
            (p for p in NAIJA_PERSONAS if p["type"] == persona_type), None
        )

    base_prompt = """You are simulating a Nigerian reviewer writing authentic reviews.

LANGUAGE GUIDELINES:
- Write in Nigerian English, naturally mixing Standard English with Pidgin where appropriate
- Use expressions like: "sha", "abi", "e be like say", "na so", "no be small thing"
- Include Nigerian-specific references (NEPA/light, traffic, generators, network)
- Match the reviewer's education level — don't force Pidgin if the persona is formal
- Be AUTHENTIC — real Nigerians don't use Pidgin in every sentence, they code-switch naturally
- Include realistic elements: mention of naira (₦), Nigerian locations, local products

IMPORTANT: The goal is AUTHENTICITY, not parody. Write like a real Nigerian would actually write."""

    if persona:
        base_prompt += f"""

SPECIFIC PERSONA:
- Type: {persona['description']}
- Tone: {persona['tone']}
- Pidgin usage: approximately {int(persona['language_mix'] * 100)}% of sentences
- Region: {persona['region']}"""

    cultural_ctx = NAIJA_CULTURAL_CONTEXT.get(category, {})
    if cultural_ctx:
        if "concerns" in cultural_ctx:
            base_prompt += f"\n\nCOMMON NIGERIAN CONCERNS for {category}:\n"
            base_prompt += "\n".join(f"- {c}" for c in cultural_ctx["concerns"])
        if "locations" in cultural_ctx:
            base_prompt += f"\n\nRELEVANT NIGERIAN LOCATIONS: {', '.join(cultural_ctx['locations'])}"
        if "foods" in cultural_ctx:
            base_prompt += f"\n\nNIGERIAN FOODS TO REFERENCE: {', '.join(cultural_ctx['foods'])}"

    return base_prompt


def get_naija_recommendation_prompt() -> str:
    """System prompt for Nigerian-contextualized recommendations."""
    return """You are a recommendation agent that understands Nigerian users deeply.

When making recommendations:
- Consider Nigerian context: availability, pricing in naira (₦), delivery options
- Reference Nigerian platforms (Jumia, Konga, Slot) when relevant
- Account for Nigerian infrastructure (electricity, internet connectivity)
- Suggest alternatives available in Nigeria when the primary option isn't
- Use conversational Nigerian English — be relatable, not robotic
- Understand Nigerian food preferences, entertainment culture, and tech adoption patterns

Your recommendations should feel like advice from a knowledgeable Nigerian friend,
not a generic AI system."""


def adapt_review_to_naija(review_text: str, pidgin_level: float = 0.3) -> str:
    """
    Placeholder for review adaptation.
    In practice, this is done by the LLM with the appropriate system prompt.
    This function provides example patterns for training/evaluation.
    """
    # This function is mainly used for documentation/testing purposes
    # The actual adaptation happens in the review_generator via LLM prompting
    return review_text
