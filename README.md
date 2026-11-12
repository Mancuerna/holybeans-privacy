# HolyBeans website

Public information and a bilingual user guide for HolyBeans, hosted on GitHub
Pages at https://holybeans.jacortes.me/.

| Page | English | Español |
| --- | --- | --- |
| Application homepage | `/home/` | `/es/home/` |
| User guide | `/docs/` | `/es/docs/` |
| Privacy policy | `/` | `/es/` |
| Terms of use | `/terms/` | `/es/terms/` |

The root remains the privacy policy to preserve the original Google Play link.
Use `/home/` as the OAuth application homepage, `/` for privacy, and `/terms/`
for terms. Preserve `CNAME`. Domain verification and OAuth publication are
configured separately in the owner's Google account.

## Editing the guide

The guide has ten chapters and an index in each language. Edit original prose
in `_guide/chapters.json`; keep Spanish and English section IDs aligned. Shared
page structure and navigation live in `tools/build_guide.py`; visual rules live
in `guide.css`, using the existing `styles.css` color tokens. Generated HTML is
committed so GitHub Pages needs no custom build dependency.

With Python 3.9 or newer:

```sh
python3 tools/build_guide.py
python3 tools/build_guide.py --check
python3 tools/check_site.py
git diff --check
python3 -m http.server 8765 --bind 127.0.0.1
```

Visit `http://127.0.0.1:8765/es/docs/` and `/docs/`. Serve from the repository root:
guide links use the domain root, matching the existing custom-domain hosting.
The `CI result` GitHub Actions check runs generation consistency, site validation
and whitespace checks on pull requests and `main`. GitHub Pages publishes merged
changes from `main`.

The checker verifies local links, anchors, canonical URLs, heading hierarchy,
languages and translation coverage. GitHub Pages excludes maintenance sources
through `_config.yml`.

Before publishing, review both languages, mobile navigation, language switching
within a chapter, keyboard focus, narrow screens and enlarged text. Confirm the
public URL serves the committed content after the Pages deployment completes.

## Content and privacy

Static HTML and local CSS; no JavaScript, trackers, forms or external fonts.
The public identity is CaffeinatedDev and the existing approved support email.
Never add personal addresses, phone numbers, private journal data, photos,
credentials, diagnostics or device identifiers. Examples are explicitly
fictional. This edition contains no app screenshots; future screenshots must
come from an isolated demonstration journal and be reviewed before publication.

Document app behavior and actual control labels; do not copy internal handoffs
or another application's prose. Update the edition note when changing feature
coverage. The current guide covers features introduced through 1.10.0 and marks
experimental device support. It does not claim to document every app feature.
The coverage review includes extraction profiles and live guides, portafilter
tares, photo overlays, yearly recap cards, scale and printer additions, machine
imports, catalog search and recovery workflows.

Drive now provides independent per-device backups, with explicit restoration,
not automatic journal synchronization or merging. Keep homepage, privacy,
terms and guide consistent. Disabling uploads, revoking permission and deleting
remote data are different actions.

## Keeping coverage current

When the app adds or changes a user workflow, compare its release notes and
actual UI labels in [the app repository](https://github.com/Mancuerna/holybeans-public)
with the affected chapters in both languages. Update existing instructions,
compatibility limits and index shortcuts together, then regenerate HTML and run
the checks above. Keep the edition version and review date in
`tools/build_guide.py` current only after reviewing that coverage. A guide edition
does not establish whether a release is available to every Google Play user.

## Design review

The guide extends the existing brand in Impeccable's Read mode: clear hierarchy,
comfortable prose width, task-oriented sections, native mobile disclosure and
no decorative motion. It requires no Impeccable runtime on the published site.

Reviewed with the official Impeccable 4.8.0 skill and mechanical detector. The
source scan flagged decorative top borders on the existing homepage; removed.
It also inferred black text on the guide's primary link in normal/hover states;
rendered colors are checked independently because that inference does not match
the browser. Record automated checks separately from visual judgment; a detector
finding dismissed with evidence is not a zero-finding detector run.
