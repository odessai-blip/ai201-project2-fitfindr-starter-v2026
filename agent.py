"""
The FitFindr planning loop.

    python agent.py          runs both example paths below
"""

import re

import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable


# -- session state -----------------------------------------------------------

def new_session(query: str, wardrobe: dict) -> dict:
    """A fresh session for one user interaction. Single source of truth for a run."""
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one chosen -> goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# -- query parsing (regex) ---------------------------------------------------

_PRICE_RE = re.compile(
    r"(?:under|below|less than|max|up to)?\s*\$\s*(\d+(?:\.\d+)?)", re.IGNORECASE
)
_SIZE_RE = re.compile(r"\b(?:in\s+)?size\s+([A-Za-z0-9/]+)", re.IGNORECASE)


def parse_query(query: str) -> dict:
    """Split a plain-language query into description, size and max_price."""
    max_price = None
    size = None
    text = query

    price_match = _PRICE_RE.search(text)
    if price_match:
        max_price = float(price_match.group(1))
        text = _PRICE_RE.sub(" ", text)

    size_match = _SIZE_RE.search(text)
    if size_match:
        size = size_match.group(1)
        text = _SIZE_RE.sub(" ", text)

    description = " ".join(text.split())
    return {"description": description, "size": size, "max_price": max_price}


def _empty_search_message(parsed: dict) -> str:
    """
    Message shown when search finds nothing. It echoes what was searched,
    then names the specific things the user can loosen.
    """
    description = parsed.get("description") or "that search"
    size = parsed.get("size")
    max_price = parsed.get("max_price")

    searched = f"'{description}'"
    if size:
        searched += f" in size {size}"
    if max_price is not None:
        searched += f" under ${max_price:.0f}"

    tips = []
    if max_price is not None:
        tips.append("raise your price limit")
    if size:
        tips.append("try a different size or leave the size out")
    tips.append(
        "use fewer or simpler keywords, like 'jacket' or 'tee' "
        "instead of a long description"
    )

    return f"No listings matched {searched}. Try one of these: " + "; ".join(tips) + "."


# -- planning loop -----------------------------------------------------------

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Branch rule: if search_listings returns an empty list, put a message in
    session["error"] and return. Otherwise take the first result, call
    suggest_outfit with it and the wardrobe, then pass that string and the
    same item to create_fit_card.
    """
    session = new_session(query, wardrobe)
    iterations = 0

    # 1. parse
    session["parsed"] = parse_query(session["query"])

    # 2. search
    iterations += 1
    trace.check_iterations(iterations)
    parsed = session["parsed"]
    session["search_results"] = search_listings(
        parsed["description"],
        size=parsed["size"],
        max_price=parsed["max_price"],
    )

    # 3. THE BRANCH: nothing came back -> stop before suggest_outfit
    if not session["search_results"]:
        session["error"] = _empty_search_message(session["parsed"])
        return session

    # 4. choose the first result, then read it back out of the session
    session["selected_item"] = session["search_results"][0]

    # 5. suggest_outfit, reading from the session
    iterations += 1
    trace.check_iterations(iterations)
    session["outfit_suggestion"] = suggest_outfit(
        session["selected_item"], session["wardrobe"]
    )

    # 6. create_fit_card, reading from the session
    iterations += 1
    trace.check_iterations(iterations)
    session["fit_card"] = create_fit_card(
        session["outfit_suggestion"], session["selected_item"]
    )

    return session


# -- running it directly -----------------------------------------------------

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} -- it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} -- ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
