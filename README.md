# HipoBuySpreadsheet

Static HTML site for [hipobuyqcsheets.com](https://hipobuyqcsheets.com).

## Stack

Plain HTML + CSS + JS. Product catalog in `js/catalog.js`. Images in `img/products` (symlink to the local image library).

## Open locally

```bash
cd ~/Desktop/hipobuyqcsheets
python3 -m http.server 8080
```

Then visit http://localhost:8080

## Main pages

- `index.html` — home
- `finder.html` — QC Finder (name / item ID search)
- `sheets.html` — QC Sheets
- `browse.html` — full spreadsheet catalog
- `item/...` — product detail pages
