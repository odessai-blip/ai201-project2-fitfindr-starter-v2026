"""
The three FitFindr tools.

    search_listings(description, size, max_price)  -> list[dict]
    suggest_outfit(new_item, wardrobe)             -> str
    create_fit_card(outfit, new_item)              -> str
"""

import re

import config
from generate import generate
from utils.data_loader import load_listings


STOPWORDS = {
    "a", "an", "the", "in", "on", "for", "under", "over", "below", "with",
    "and", "of", "to", "me", "i", "want", "need", "looking", "find", "size",
    "less", "than", "at", "most", "max", "or",
}


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _stem(token: str) -> str:
    # crude plural handling: "tees" -> "tee", "jeans" -> "jean"
    return token[:-1] if len(token) > 3 and token.endswith("s") else token


def _size_matches(wanted: str, listing_size: str) -> bool:
    # whole-token match: "m" matches "M" and "S/M", not "XL (oversized)" or "US 9"
    parts = [p for p in re.split(r"[\s/()]+", listing_size.lower()) if p]
    return wanted.strip().lower() in parts


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Return listing dicts matching the description, best match first.
    Filters: max_price (inclusive) and size (whole-token match).
    Returns [] when nothing matches. Never None, never raises.
    """
    keywords = [_stem(t) for t in _tokens(description) if t not in STOPWORDS]
    if not keywords:
        return []

    scored = []
    for listing in load_listings():
        if max_price is not None and listing["price"] > max_price:
            continue
        if size is not None and not _size_matches(size, listing["size"]):
            continue

        haystack = " ".join(
            [
                listing["title"],
                listing["description"],
                listing["category"],
                " ".join(listing["style_tags"]),
                " ".join(listing["colors"]),
                listing["brand"] or "",  # brand can be None
            ]
        )
        words = {_stem(t) for t in _tokens(haystack)}
        score = sum(1 for k in keywords if k in words)
        if score > 0:
            scored.append((score, listing["price"], listing))

    scored.sort(key=lambda s: (-s[0], s[1]))  # best score first, ties to lower price
    return [s[2] for s in scored][: config.SEARCH_RESULT_LIMIT]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Suggest one or two outfits using the listing and the user's wardrobe.
    Empty wardrobe -> general styling advice. Always returns a non-empty str.
    """
    item_line = (
        f"{new_item['title']} ({new_item['category']}, "
        f"colors: {', '.join(new_item['colors'])}, "
        f"style: {', '.join(new_item['style_tags'])})"
    )
    items = wardrobe.get("items", [])

    if not items:
        prompt = (
            f"A shopper is considering this secondhand piece: {item_line}.\n"
            "They haven't told us what they own. Give general styling advice: "
            "one or two outfit ideas using common wardrobe basics. "
            "Keep it under 120 words."
        )
    else:
        owned = "\n".join(
            f"- {w['name']} ({w['category']}, {', '.join(w['colors'])})"
            + (f" — {w['notes']}" if w.get("notes") else "")  # notes can be None
            for w in items
        )
        prompt = (
            f"A shopper is considering this secondhand piece: {item_line}.\n"
            f"Their wardrobe:\n{owned}\n\n"
            "Suggest one or two outfits that combine the new piece with items "
            "from their wardrobe. Name the wardrobe pieces exactly as listed. "
            "Keep it under 150 words."
        )

    result = generate(prompt)
    return result.strip() or "Try pairing this piece with simple basics in a neutral color."


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a 2-4 sentence social-post caption about the find.
    Empty/whitespace outfit -> descriptive message, no model call.
    """
    if not outfit or not outfit.strip():
        return "No outfit suggestion was provided, so there's nothing to write a caption about."

    brand = new_item.get("brand")
    brand_line = f"Brand: {brand}\n" if brand else ""  # brand is often None
    prompt = (
        "Write a 2 to 4 sentence social media caption about a thrift find. "
        "It should sound like a real post, not a product description. "
        "Mention the item, its price, and its platform once each, and be "
        "specific about the vibe.\n\n"
        f"Item: {new_item['title']}\n"
        f"{brand_line}"
        f"Price: ${new_item['price']:.0f}\n"
        f"Platform: {new_item['platform']}\n"
        f"Outfit idea: {outfit}"
    )
    return generate(prompt).strip()