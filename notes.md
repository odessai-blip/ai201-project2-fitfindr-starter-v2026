# Milestone 1 notes

Listing fields: id, title, description, category, style_tags, size,
condition, price, colors, brand, platform

Wardrobe item fields: id, name, category, colors, style_tags, notes

Empty wardrobe: {"items": []}

Gotchas:
- brand and notes can be null
- size format is inconsistent (W30 L30, S/M, XL (oversized), M)
- platform casing varies (thredUp)
- style_tags and colors are lists
