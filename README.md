# Smokey Road build: outstanding items

A public, running list of the outstanding items on our Schumacher Homes build,
with photos, status, and change history. The page is `index.html`; all of its
content comes from `data/issues.yaml`.

## Updating the list

Everything lives in **`data/issues.yaml`**:

- **Change a status.** Edit the item's `status:` line, add a dated line under its
  `history:`, and change `last_updated` at the top of the file.
- **Record the builder's answer.** Add a `response:` line to the item. It shows
  on the page as "Builder response."
- **Add an item.** Copy an existing block and give it the next ID (`SR-42`, ...).
  Put its photos in `photos/` (full size) and `photos/thumbs/` (small copy),
  named `SR-42-a.jpg`, `SR-42-b.jpg`, ...
- **Never renumber or reuse an ID.** The builder's responses refer to these numbers.

Allowed values:

| Field      | Values |
|------------|--------|
| `status`   | Open, Acknowledged, Scheduled, In progress, Resolved, Not correctable |
| `type`     | Incomplete, Defect, Workmanship, Not as contracted |
| `contract` | Schumacher, Troyer (homeowner contract) |

Every commit is timestamped, so the repo's commit history shows what the list
said on any given date.

## Weekly PDF

```bash
pip install playwright pyyaml
python -m playwright install chromium
python scripts/make_pdf.py                  # full report
python scripts/make_pdf.py --party Troyer   # just the Troyer items
```

The PDF is saved to `reports/` with the date in its name. Commit it after you
email it, so the repo keeps a copy of exactly what was sent.

## Publishing (GitHub Pages)

Settings → Pages → Source: *Deploy from a branch* → `main` / root. The site will
be at `https://<user>.github.io/<repo>/`. Set `repo:` at the top of
`data/issues.yaml` to `<user>/<repo>` so each item gets a "Comment" link that
opens a GitHub issue (commenters need a GitHub account).

## Privacy

Photos are stored with location (GPS) and camera data removed. Don't commit the
contract, financing documents, or anything with account numbers, phone numbers,
or email addresses. The page cites contract page numbers instead.

## Preview locally

```bash
python -m http.server 8000   # then open http://localhost:8000
```
(Opening `index.html` directly from disk won't load the data file.)
