# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Finds secondhand listings that match a keyword description, optionally filtered by size and price ceiling.
- **Inputs:** `description` (str), `size` (str or None), `max_price` (float or None). `max_price` is inclusive, so "under $30" means price <= 30. A size matches only if the lowercased size is a whole token of the listing's size, where tokens are split on spaces, "/" and parentheses. So "M" matches "M" and "S/M", but not "XL (oversized)" or "US 9".
- **Returns:** A list of listing dicts, best match first, at most config.SEARCH_RESULT_LIMIT. Each dict has id, title, description, category, style_tags (list), size, condition, price (float), colors (list), brand (str or None), platform (str). Score = number of description keywords found in title, description, style_tags, category, colors and brand. Ties go to the lower price. Zero-score listings are dropped.
- **When it has nothing:** Returns an empty list `[]`. Never None, never an exception, never a string.

### `suggest_outfit`

- **What it does:** Suggests one or two outfits that combine the listing with pieces from the user's wardrobe.
- **Inputs:** `new_item` (dict, one listing dict from search_listings), `wardrobe` (dict with an `items` key holding a list of wardrobe item dicts, each with id, name, category, colors, style_tags, notes; notes may be None)
- **Returns:** A non-empty str of outfit suggestions, naming specific wardrobe pieces by their `name` when the wardrobe has items.
- **When it has nothing:** If `wardrobe["items"]` is empty, returns a non-empty str of general styling advice for the item, with no wardrobe pieces named. Never returns "" and never raises.

### `create_fit_card`

- **What it does:** Writes a short social-post-style caption about the find.
- **Inputs:** `outfit` (str, the string returned by suggest_outfit), `new_item` (dict, the listing dict)
- **Returns:** A str of two to four sentences that mentions the item, its price and its platform once each, and names the vibe. It leaves out the brand when brand is None.
- **When it has nothing:** If `outfit` is empty or whitespace, returns a descriptive message str (for example "No outfit suggestion was provided, so there's nothing to write a caption about.") and does not call the model. Never raises.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**
If search_listings returns an empty list, put a "no matches" message in the session and stop. Otherwise take the first result, call suggest_outfit with it and the wardrobe, then pass that string and the same listing to create_fit_card.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print([(l['id'], l['price']) for l in search_listings('graphic tee', max_price=30)])"
[('lst_017', 15.0), ('lst_002', 18.0), ('lst_033', 19.0), ('lst_006', 24.0), ('lst_012', 20.0), ('lst_015', 26.0), ('lst_011', 27.0)]

$ python -c "from tools import search_listings; print(search_listings('designer ballgown', size='XXS', max_price=5))"
[]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
**Outfit 1: Casual Streetwear**
Pair the Vintage Levi's 501 Jeans with the White ribbed tank top and the Vintage black denim jacket (slightly cropped). Finish the look with the Chunky white sneakers, the Brown leather belt, and the Black crossbody bag.

**Outfit 2: Cozy & Edgy**
Style the Vintage Levi's 501 Jeans with the Oversized grey crewneck sweatshirt and the Black combat boots. Accessorize with the Brown leather belt for added definition and the Black crossbody bag for an effortless, everyday vibe.

$ python -c "from tools import suggest_outfit; from utils.data_loader import load_listings; print(suggest_outfit(load_listings()[0], {'items': []}))"
Vintage Levi's 501s are the ultimate streetwear staple. Here are two effortless ways to style them using pieces you likely already own:
(general advice, no wardrobe pieces named)
```

```
$ AI201_CACHE=0 python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Found my holy grail medium wash Vintage Levi's 501s on Depop for just $38 and I am never taking them off. They've got that perfect, lived-in 90s slouch that you just can't manufacture. Throwing them on with crisp white sneakers for the ultimate effortless weekend vibe.

$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('   ', load_listings()[0]))"
No outfit suggestion was provided, so there's nothing to write a caption about.
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* A draft of the Tool Inventory entries for my three tools, before I had looked at tools.py.
- *What came back:* Entries built on guesses. It used `query` as the first parameter of search_listings (the real name is `description`), and it made suggest_outfit and create_fit_card return dicts when the stubs say they return strings.
- *What I changed:* I pasted tools.py and the README, and the entries were redone to match the real signatures. I replaced my README bullets with the corrected versions and committed them.

**Moment 2**

- *What I asked for:* Code for all three tools, written against my Tool Inventory (inclusive price filter, whole-token size match, empty list on no match, general advice on an empty wardrobe).
- *What came back:* Working code, but its predicted test result for `search_listings('jacket', size='M')` was wrong. It said only lst_004 would match. My run returned lst_032 (M/L), lst_004 (M) and lst_022 (M).
- *What I changed:* I didn't change the code. I checked each returned listing against my own spec (all three have `m` as a whole token, and no shoes or `XL (oversized)` came back) and recorded the real output instead of the prediction. I also ran create_fit_card three times with `AI201_CACHE=0` to confirm the outputs differ, and tested the empty wardrobe and whitespace-outfit cases myself.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
