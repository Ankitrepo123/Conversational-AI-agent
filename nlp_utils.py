import re
from datetime import timedelta
import dateparser
import spacy

nlp = spacy.load("en_core_web_sm", exclude=["tagger", "parser", "lemmatizer"])  # lighter

# Matches things like "3-5 PM", "14:00 - 16:30", etc.
RANGE_RE = re.compile(
    r"(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\s*[-–]\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)",
    re.I,
)

AFFIX_HOURS = {
    "morning": (9, 12),
    "afternoon": (15, 18),
    "evening": (18, 21),
}

def extract_range(text: str,tz: str = "Asia/Kolkata"):
    text_lower = text.lower()

    # 1️⃣  Turn “3-5 PM” into two separate phrases
    match = RANGE_RE.search(text_lower)
    manual_times = []
    if match:
        manual_times = [match.group(1), match.group(2)]

    # 2️⃣  Run spaCy only if we still need more entities
    doc = nlp(text) if len(manual_times) < 2 else []

    candidates = manual_times +([
        ent.text for ent in doc.ents if ent.label_ in {"DATE", "TIME"}
    ]if hasattr(doc, "ents")      
    else [])

    parsed: list[dateparser.datetime_parser.datetime] = []
    for token in candidates:
        dt = dateparser.parse(
            token,
            settings={
                "TIMEZONE": tz,
                "RETURN_AS_TIMEZONE_AWARE": True,
                "PREFER_DATES_FROM": "future",
            },
        )
        if dt:
            for word, (h_start, h_end) in AFFIX_HOURS.items():
                if word in token.lower():
                    dt = dt.replace(hour=h_start, minute=0)
                    parsed.append(dt)
                    dt_end = dt.replace(hour=h_end)
                    parsed.append(dt_end)
                    break
            else:
                parsed.append(dt)

    parsed = sorted(parsed)  

    return (
        parsed[0].isoformat() if len(parsed) > 0 else None,
        parsed[1].isoformat() if len(parsed) > 1 else None,
    )
