---
name: aso-cross-localization
description: App Store cross-localization ASO — expand one storefront's keyword footprint by loading keywords into the OTHER localizations that storefront also indexes (the US indexes English-US + 9 secondary locales). Covers the two indexing rules (each word counts once across all locales; phrases never combine across locales), Title>Subtitle>keyword-field ranking weight, keyword-first title ordering for unestablished brands, which secondary locales to add, and a char-count/duplicate validator. Use when planning App Store keywords or ASO, deciding which localizations to add, writing an app's Title/Subtitle/keyword fields, trying to raise impressions, or when the user mentions cross-localization, keyword indexing, secondary locales, or App Store Connect metadata.
---

# App Store cross-localization (ASO keyword expansion)

Expand one storefront's keyword footprint by loading keywords into the *other* localizations that storefront also indexes. A fully-used US set reaches ~1,600 chars of US-indexed keywords vs. 160 from English alone (the 9 secondary locales add ~1,440).

## The mechanic

A storefront indexes its **primary** localization **plus several secondary** ones. Any word placed in an indexed secondary locale ranks in that storefront — even if that locale's actual market never sees the listing.

**US storefront indexes 10 localizations:** English (US) + Arabic (SA), Simplified Chinese, Traditional Chinese (HK), French (FR), Korean, Portuguese (BR), Russian, Spanish (Mexico), Vietnamese. Full map, other storefronts, and a worked example: [REFERENCE.md](REFERENCE.md).

## Two hard rules — violate these and it silently does nothing

1. **Each word counts once** — across every field (Title/Subtitle/Keywords) AND every localization. Repeating a word anywhere is wasted budget. De-dup the *entire* bundle, not each locale.
2. **Phrases never combine across locales.** `sight` in en-US + `singing` in es-MX does **not** rank you for "sight singing" — only the two words separately. Every phrase must live complete inside one localization.

## Method

1. **Lock the primary** (e.g. en-US) — list every word it already uses.
2. **Pick secondary locales** the storefront indexes AND that serve ~zero-revenue markets for this app (an English listing there costs nothing). Pull revenue-by-territory first; never English-ify a locale that actually converts.
3. **Score candidates, then allocate by score** (see *Scoring* below) — no repeats across the bundle. Highest-KEI fresh phrases go in **Title, then Subtitle**; the rest in the keyword field.
4. **Stop when relevance drops.** The limit is *supply of relevant non-duplicate words*, not locale slots — a niche app usually exhausts good terms by **primary + 2 secondaries**. Adding junk terms to fill more slots brings vanity impressions and won't rank (low relevance).
5. **Validate** char counts + cross-locale duplicates with `scripts/validate_keywords.py` (`--demo` runs the NoteHunter example).
6. **Confirm indexing** — after release, track secondary-only terms on the *primary* storefront in a rank tracker. If they rank, the indexing is real; if not after ~2 weeks, revert that locale to its native market.

## Scoring candidates (KEI) — do this before allocating

Don't pick keywords by gut; score them and let the score drive placement.

- **Relevance-gate first.** Drop anything the app doesn't genuinely do. High popularity + low relevance = vanity impressions that never install (the "music games / kids" trap).
- **Three axes:** **Popularity** (Apple's search-volume index ~5–100), **Difficulty** (count + strength of ranking competitors), **Conversion** (does the term install/subscribe — use your own first-party data where you have it).
- **KEI = popularity ÷ difficulty** (some tools square popularity). High KEI = many searches, weak competition — the sweet spot for a small app.
- **Placement follows score:** highest KEI × relevance you can realistically rank for → **Title**; next tier → **Subtitle**; long tail + high-difficulty stretch terms → keyword field (cheap to attempt in a free secondary locale).
- **Where the numbers come from:** Apple Search Ads keyword popularity + your own **search-terms report** (first-party popularity AND conversion); third-party tools (AppFigures/Astro, AppTweak, MobileAction, Sensor Tower) for net-new terms; a rank tracker (Kranked) to confirm you moved.

## Writing the Title / Subtitle

- **Ranking weight: Title > Subtitle > Keyword field.** Load fresh keywords into the Title/Subtitle of added locales, not only the hidden keyword field.
- **Keyword-first, brand-second** when the brand isn't established: `Ear Training: NoteHunter`, not `NoteHunter: Ear Training`. Apple weights earlier title words more — don't spend prime position on an unsearched brand. In secondary locales, usually **drop the brand entirely** (it already ranks from the primary — repeating it violates Rule 1).
- **Never repeat the brand or any primary-locale word** in a secondary title.
- **Stay readable** — Apple guideline **2.3.7** rejects keyword-stuffed names. Two clean phrases that read like a real app name, never comma-salad.

## Executing in App Store Connect

- **Name + Subtitle** live on the **AppInfo** localization; **Keywords** on the **AppStoreVersion** localization. Adding a locale needs a minimally-complete listing (name, description, screenshots — reuse the primary's images).
- Automatable via the `appstoreconnect` MCP: `asc_post_app_info_localization`, `asc_post_app_store_version_localization`, and the matching `asc_patch_*` tools.
- Any Title/Subtitle/Keyword change ships with a **new app version submission**.

See [REFERENCE.md](REFERENCE.md) for the full locale tables, the NoteHunter worked example, and sources.
