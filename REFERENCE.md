# Cross-localization — reference

## US storefront: the 10 indexed localizations

Primary **English (U.S.)** plus 9 secondaries. The "market served" column is why you can fill a slot with English at no cost — pick the ones where the app earns ~nothing.

| Secondary locale | Serves storefront(s) | Safe to fill with English? |
|---|---|---|
| Spanish (Mexico) `es-MX` | Mexico + Spanish-default LatAm | Yes if LatAm ≈ $0 |
| Arabic (Saudi Arabia) `ar-SA` | MENA | Usually yes |
| Portuguese (Brazil) `pt-BR` | Brazil | Yes if BR ≈ $0 |
| Traditional Chinese (HK) `zh-Hant` | Hong Kong / Taiwan | Yes, unless demand-testing HK/TW |
| Russian `ru` | Russia + shows in others | Caution — Russia/Ukraine may convert |
| Vietnamese `vi` | Vietnam | Yes |
| Simplified Chinese `zh-Hans` | Mainland China | **No** if you run a real CN listing |
| French (France) `fr-FR` | France | **No** if you run a real FR listing |
| Korean `ko` | Korea | **No** if you run a real KR listing |

**Two traps:**
- **Spanish (Spain) `es-ES` is NOT the US secondary — Spanish (Mexico) `es-MX` is.** A Spain localization gives zero US bonus. Add es-MX specifically.
- A locale you're **already using for its home market** (e.g. a real French listing for France) is *also* US-indexed — but don't overwrite it with English; you'd sacrifice a real market's listing for a marginal US gain. Only English-ify **empty, ~zero-revenue** slots.
- Locales NOT in the US set (e.g. German, Japanese, Hungarian, Spanish-Spain) give **zero** US bonus — they only serve their own storefronts.

## Other storefronts

Every storefront has its own primary + secondary set following the same pattern (e.g. Canada indexes English-Canada + French-Canada; many storefronts carry **English (UK)** as a broad secondary). Some — notably the **UK and Australia** — index a **single** locale, so cross-localization buys nothing there. Verify a specific storefront's set against the sources below before planning it; only the US set is enumerated here because it's the highest-volume and best-documented.

## The two rules, with examples

**Rule 1 — each word once, everywhere.** If `pitch` is in your en-US keyword field, putting `pitch` again in es-MX earns nothing. De-dup across the *entire* bundle (all fields × all locales). This is why the real constraint is keyword *supply*, not the number of locale slots.

**Rule 2 — phrases stay within one locale.** To rank for the phrase "music dictation", both `music` and `dictation` must sit in the *same* localization. Words scattered across locales only rank individually. So place complete high-value phrases inside a single locale; never split them.

**Where the two rules collide (important).** To add a *new phrase* that shares a word with a locked locale, you must repeat that shared word — e.g. en-US already indexes `sight` (in "Sight Read"), but ranking the phrase "sight singing" in es-MX requires `sight` to appear again *in es-MX*. That repeat earns nothing for `sight` itself (Rule 1) but is the unavoidable **price of the phrase** (Rule 2), so it's justified. A repeat is only truly *wasted* when the repeated word forms no new phrase — e.g. the same standalone single-word keyword in two locales. `validate_keywords.py` lists every repeat; judge each by "does it build a distinct phrase here?"

## Worked example — NoteHunter (en-US + es-MX + Arabic)

**en-US** (the anchor — already live; every word here is off-limits elsewhere):
- Title: `NoteHunter: Ear Training App`
- Subtitle: `Sight Read, Intervals, Theory`
- Keywords: `relative pitch,perfect pitch,solfege,rhythm,music school,note reader,pitch trainer,melody,harmony`
- *(If the brand were NOT established, keyword-first would be better: `Ear Training: NoteHunter`.)*

**es-MX** (new — carries the strongest remaining phrases in Title/Subtitle):
- Title: `Sight Singing: Aural Skills`
- Subtitle: `Sheet Music, Chords & Scales`
- Keywords: `music dictation,treble clef,bass clef,musicianship,octave,key signature,note names,transcription`
- New US-indexed words: singing, aural, skills, sheet, chords, scales, dictation, treble, clef, bass, musicianship, octave, key, signature, note names, transcription

**Arabic (SA)** (new — mops up; note terms already turning generic → this is the natural stop):
- Title: `Music Lessons: Absolute Pitch`
- Subtitle: `Chord Recognition & Staff`
- Keywords: `metronome,conservatory,music college,music practice,note recognition,vocal,tuner,movable do`
- New words: lessons, absolute, chord, recognition, staff, metronome, conservatory, college, practice, vocal, tuner, movable do

A 4th locale would only hold guitar/karaoke/DJ filler — low relevance, vanity impressions. Primary + 2 secondaries exhausts a music-education niche.

## Locale selection by revenue (the gating step)

Before assigning any English keywords to a locale, confirm that locale's market earns ~nothing for the app (App Store Connect → Sales/Proceeds by territory, or a per-territory paywall/trial cut). An English listing shown to a market that *does* convert is a real cost. Rank the empty US-indexed slots by "least harm": markets with $0 revenue first.

## Char limits (Apple, glyph counts)

- Title ≤ 30 · Subtitle ≤ 30 · Keywords ≤ 100 (commas count; **no spaces after commas**).
- CJK and accented chars count as 1 glyph. Always re-verify in ASC's live counter — it's the authority.

## Sources

- [aso.dev — App Store cross-localization](https://aso.dev/metadata/cross-localization/) — US secondary-locale list + the two rules.
- [MobileAction — App Store cross-localization](https://www.mobileaction.co/blog/app-store-cross-localization/) — territory-level indexation.
