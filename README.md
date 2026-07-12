# aso-cross-localization

A Claude Code skill that teaches your agent an App Store trick agencies charge for: cross-localization keyword expansion, run end to end from the agent.

**Repo:** [github.com/akoskomuves/aso-cross-localization](https://github.com/akoskomuves/aso-cross-localization) · **Article:** [tallpoppy.xyz/aso-cross-localization](https://tallpoppy.xyz/aso-cross-localization/)

Cross-localization is not a secret. Agencies know it, the big ASO tools all have guides on it, and almost no indie developer actually uses it, because doing it properly means juggling ten localizations, two rules that fail silently, and App Store Connect's worst UI.

Which is exactly the kind of work agents are good at. This skill, plus three MCP servers, runs the whole loop from a single Claude Code session: keyword research, allocation, validation, writing to App Store Connect, and checking two weeks later whether it actually worked.

## The trick: one market, ten titles

On paper, your US listing gives you about 160 characters of search real estate: a 30-character title, a 30-character subtitle, and a hidden 100-character keyword field.

Except that's not what Apple indexes. Every storefront also reads metadata from localizations that people in that market never see. For the US store there are ten: English (US), plus Arabic (Saudi), Chinese Simplified, Chinese Traditional, French, Korean, Portuguese (Brazil), Russian, Spanish (Mexico), and Vietnamese.

Each of those has its own title, subtitle, and keyword field, and every word in them ranks in US search. Nobody browsing the US store will ever see your Spanish (Mexico) listing. Apple indexes it anyway. Use all ten and your 160 characters become roughly 1,600.

You're stacking hidden titles that all feed one market's search. Other storefronts have their own bundles; [REFERENCE.md](REFERENCE.md) has the US table and the traps (Spanish *Spain* buys you nothing, don't English-ify a locale that earns real money).

## Why nobody does it by hand

Two rules govern the whole thing, and breaking either one fails silently. No error, no warning. You just don't rank.

1. **Every word counts once, across everything.** All fields, all localizations, one pool. Repeat a word anywhere and the repeat is dead weight. De-duplication has to happen across the entire bundle, not per locale.
2. **Phrases never combine across locales.** "sight" in one localization plus "singing" in another does not rank you for "sight singing". You get the two words separately, which is close to worthless. Every phrase you care about has to live complete inside one localization.

On top of that, ranking weight runs Title > Subtitle > keyword field, so your strongest new terms belong in the titles of the added locales, keyword-first. Your brand name shouldn't appear in the secondaries at all: it already ranks from your primary locale, and repeating it burns rule 1. And Apple's [guideline 2.3.7](https://developer.apple.com/app-store/review/guidelines/#2.3.7) rejects names that are obviously keyword salad, so the titles still have to read like names.

Ten locales, per-field character limits, one global word pool, phrase placement constraints. It's bookkeeping with silent failure modes. Tedious for a human, trivial for an agent with a validator.

## What's in this repo

- [`SKILL.md`](SKILL.md) — the playbook the agent follows: the indexing mechanic, the two rules, KEI scoring (popularity divided by difficulty), locale selection by revenue, title/subtitle allocation, and how to execute in App Store Connect.
- [`REFERENCE.md`](REFERENCE.md) — the US locale table with "safe to fill with English?" guidance, the traps, a worked three-locale example, and sources.
- [`scripts/validate_keywords.py`](scripts/validate_keywords.py) — checks character limits (glyph-counted), keyword-field hygiene, and rule 1 violations across the whole bundle before anything ships.

```
python3 scripts/validate_keywords.py --demo        # worked example
python3 scripts/validate_keywords.py bundle.json   # your own bundle
```

## Install

```
git clone https://github.com/akoskomuves/aso-cross-localization ~/.claude/skills/aso-cross-localization
```

Claude Code picks up personal skills from `~/.claude/skills/` automatically. For a single project, put it in the project's `.claude/skills/` instead.

## The rest of the setup: 3 MCPs

The skill covers the thinking. Three MCP servers make it end to end — kranked and appstoreconnect-mcp are mine, all three are open source:

- **[kranked](https://github.com/akoskomuves/kranked)** does the keyword research: difficulty, popularity, suggestions, and live rank checks. The rank checks are how the agent confirms secondary-locale terms really index on the US store.
- **[appstoreconnect-mcp](https://github.com/akoskomuves/appstoreconnect-mcp)** is what makes this more than a research toy: it writes the name and subtitle onto each AppInfo localization, keywords onto each version localization, and files the new version. Live, in App Store Connect, from the agent. It also handles pricing, PPP, subscriptions, and offers.
- **[apple-search-ads-mcp](https://github.com/AppVisionOS/apple-search-ads-mcp)** covers the paid side and doubles as a data source. The ASA search-terms report gives real popularity and conversion numbers for KEI scoring, and the same winning terms can get paid campaigns later.

## What a session looks like

1. **Research.** The agent pulls keywords, popularity, and conversion data, then scores by KEI (kranked plus the ASA search-terms report).
2. **Allocate.** It picks the secondary locales worth repurposing, distributes de-duped keywords into title, subtitle, and keyword field per locale, and runs the validator.
3. **Ship.** It pushes every localization to App Store Connect and submits the version. No clicking through ten locale forms.
4. **Verify.** After release, it tracks the secondary-only terms on the US store. If a locale's terms don't index within about two weeks, revert that locale.
5. **Amplify.** Optionally, put ASA budget on the terms that prove out.

Step 4 is the one humans skip and an agent doesn't. Cross-localization is observed behavior, not a documented API. Apple can change it, and sometimes a locale just doesn't take. If you never check whether the secondary terms rank, you have no idea whether any of this worked.

## The judgment calls stay human

The agent doesn't decide whether to do this. In practice you run out of relevant, non-duplicate keywords somewhere around your primary plus two or three secondaries. Filling all ten slots buys impressions that never turn into installs.

There's also a real cost: a locale you fill with English keywords stops serving its actual market. So the first input to a session is revenue by territory, and I only repurpose locales whose real market earns me approximately nothing. Those calls are yours. Everything after them is the agent's.

## Sources

On the indexing behavior: [aso.dev's cross-localization guide](https://aso.dev/metadata/cross-localization/), [AppTweak on primary and secondary languages](https://www.apptweak.com/en/aso-blog/how-to-benefit-from-cross-localization-on-the-app-store), [MobileAction on territory-level indexation](https://www.mobileaction.co/blog/app-store-cross-localization/).

## License

MIT. I'm Akos — I run [tallpoppy](https://tallpoppy.xyz), an independent software studio: mobile apps, web platforms, AI systems.
