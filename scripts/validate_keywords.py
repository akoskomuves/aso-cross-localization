#!/usr/bin/env python3
"""Validate an App Store cross-localization keyword bundle.

Checks, for one storefront's set of indexed localizations:
  - Apple char limits: Title <=30, Subtitle <=30, Keywords <=100 (glyph count).
  - Keyword field hygiene: no spaces after commas (wastes chars).
  - Rule 1: each word counted once across ALL fields AND ALL locales -> flags
    any word that appears more than once anywhere (wasted budget).
  - Reports the set of unique indexed tokens the storefront gains.

Usage:
    python3 validate_keywords.py bundle.json
    python3 validate_keywords.py --demo        # runs the NoteHunter example

bundle.json shape:
    {
      "storefront": "US",
      "locales": {
        "en-US":  {"title": "...", "subtitle": "...", "keywords": "a,b,c"},
        "es-MX":  {"title": "...", "subtitle": "...", "keywords": "..."}
      }
    }

Note: Apple stems loosely (interval/intervals). This does a light singular
fold (trailing 's') for duplicate detection only — treat dup warnings as
"probably wasted", and always re-check counts in ASC's live counter.
"""
import argparse
import json
import re
import sys
import unicodedata

LIMITS = {"title": 30, "subtitle": 30, "keywords": 100}
# Apple ignores common connectors; don't flag them as dup keywords.
STOPWORDS = {"and", "the", "a", "an", "for", "to", "your", "of", "with",
             "app", "&", "or", "in", "on"}


def glyphs(s: str) -> int:
    """Glyph count as Apple displays it (NFC-normalized length)."""
    return len(unicodedata.normalize("NFC", s or ""))


def fold(word: str) -> str:
    """Lowercase + light singular fold for cross-field dup detection."""
    w = word.lower()
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        w = w[:-1]
    return w


def tokens(text: str):
    """Split a field into indexable words (letters/digits/CJK runs)."""
    if not text:
        return []
    # keep CJK and word chars; split on everything else
    raw = re.split(r"[^0-9A-Za-zÀ-ɏ一-鿿가-힣]+", text)
    out = []
    for w in raw:
        if not w:
            continue
        if w.lower() in STOPWORDS:
            continue
        out.append(w)
    return out


def validate(bundle: dict) -> int:
    storefront = bundle.get("storefront", "?")
    locales = bundle.get("locales", {})
    print(f"== Cross-localization check: {storefront} storefront "
          f"({len(locales)} locales) ==\n")

    problems = 0
    occurrences = {}  # folded token -> list of "locale/field"

    for locale, fields in locales.items():
        print(f"[{locale}]")
        for field in ("title", "subtitle", "keywords"):
            val = fields.get(field, "")
            n = glyphs(val)
            limit = LIMITS[field]
            flag = ""
            if n > limit:
                flag = f"  <-- OVER LIMIT ({limit})"
                problems += 1
            print(f"  {field:<9} {n:>3}/{limit}  {val}{flag}")
            if field == "keywords" and re.search(r",\s", val or ""):
                print("            note: space after a comma wastes characters")
            for w in tokens(val):
                occurrences.setdefault(fold(w), []).append(f"{locale}/{field}")
        print()

    dups = {t: locs for t, locs in occurrences.items() if len(locs) > 1}
    if dups:
        print("Repeated words (Rule 1 check) — each repeat earns nothing for that")
        print("word ITSELF. It's only justified if the repeat is needed to build a")
        print("distinct multi-word phrase IN that locale (Rule 2). Otherwise it's")
        print("wasted budget — reword to a fresh term. Verify each:")
        for t, locs in sorted(dups.items()):
            print(f"  '{t}'  in  {', '.join(locs)}")
    else:
        print("Rule 1: OK — no word duplicated across fields/locales.")

    unique = sorted(occurrences.keys())
    print(f"\nUnique indexed tokens gained on {storefront}: {len(unique)}")
    print("  " + ", ".join(unique))

    print("\nReminder: phrases only rank if BOTH words sit in the SAME locale "
          "(Rule 2). This checker verifies words, not phrase co-location.")
    print("Result:", "PASS" if problems == 0 else f"{problems} issue(s) — fix above.")
    return 1 if problems else 0


DEMO = {
    "storefront": "US",
    "locales": {
        "en-US": {
            "title": "NoteHunter: Ear Training App",
            "subtitle": "Sight Read, Intervals, Theory",
            "keywords": "relative pitch,perfect pitch,solfege,rhythm,music school,note reader,pitch trainer,melody,harmony",
        },
        "es-MX": {
            "title": "Sight Singing: Aural Skills",
            "subtitle": "Sheet Music, Chords & Scales",
            "keywords": "music dictation,treble clef,bass clef,musicianship,octave,key signature,note names,transcription",
        },
        "ar-SA": {
            "title": "Music Lessons: Absolute Pitch",
            "subtitle": "Chord Recognition & Staff",
            "keywords": "metronome,conservatory,music college,music practice,note recognition,vocal,tuner,movable do",
        },
    },
}


def main():
    ap = argparse.ArgumentParser(description="Validate an ASO cross-localization bundle.")
    ap.add_argument("bundle", nargs="?", help="path to bundle.json")
    ap.add_argument("--demo", action="store_true", help="run the built-in NoteHunter example")
    args = ap.parse_args()

    if args.demo:
        bundle = DEMO
    elif args.bundle:
        with open(args.bundle, encoding="utf-8") as f:
            bundle = json.load(f)
    else:
        ap.print_help()
        return 2
    return validate(bundle)


if __name__ == "__main__":
    sys.exit(main())
