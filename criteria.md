# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
My search is a plain keyword match, so some phrasings of a query won't overlap with any listing's title, tags, or description and will return nothing. That's a miss from the data and the matching, not a bug in the loop. The fit card also comes from a model call, which can occasionally fail or return something unusable. 5 of 5 would punish normal variation, so I set 4 of 5.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
This path never calls the model. If search_listings returns an empty list, my loop checks for it and stops, and that is plain code that behaves the same every time. A miss would mean the branch is broken, not that I got unlucky, so anything below 5 of 5 would be hiding a bug.

---

## 3. Something about state

3. Given a query that matches at least one listing, the id of the listing
   returned by search_listings is the same id that suggest_outfit and
   create_fit_card receive, in 5 of 5 tries.
   
**Why this target:**
The listing id is passed from one tool to the next by my own code, and no model decides it. Nothing random can change it between steps. If the id differs even once, the session is passing the wrong item, which is a bug that needs fixing, so I'm not leaving room for misses.


---

## 4. Something about the fit card

4. Given a query that matches at least one listing, the fit card is 2 to 4
   sentences and mentions the item, its price, and its platform, in 4 of 5
   tries, even though the wording differs between runs.
   



**Why this target:**
The fit card is written by a model, so the wording changes every run and it sometimes leaves out a detail such as the platform or the price, even when my code is correct. I can check what the card contains but not its exact words, so I allow one miss in five. I didn't go lower because the prompt should include all three details, and missing them often would mean my prompt is wrong.


---

## 5. Your choice



5. Given the query 'vintage graphic tee under $30', every listing returned
   by search_listings has a price of $30 or less, in 5 of 5 tries.
   


**Why this target:**
The price filter is a plain comparison (price <= max_price) in search_listings, and no model is involved. If a $38 listing ever shows up for 'under $30', the filter has a bug, so the target allows no misses.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
