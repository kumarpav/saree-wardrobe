# Saree Wardrobe

A mobile-responsive web app for cataloging sarees and blouses, pairing them into outfits, and finding what you already own.

## Features

- **Catalog** — separate catalogs for sarees and blouses with a responsive 2–5 column grid. Each card shows the image, name, detected colors, and tags, with hover edit/delete.
- **Rich item details** — body/border/general colors, region (Kanjivaram, Banarasi, …), fabric, occasion, price, purchase date, notes, and image (file upload or URL).
- **Bulk upload (sarees)** — drop in many photos at once; body and border colors are auto-detected via k-means clustering on a canvas, then editable inline before saving.
- **Check Catalog** — upload a saree photo, detect its colors, and find similar sarees already in your wardrobe (or get a "this looks unique" message).
- **Search & filters** — quick text search, an advanced filter panel (color, border, region, fabric, occasion), and a natural-language search ("show me all blue silk wedding sarees").
- **Outfits** — pair a saree with a blouse, track "last worn", and mark as worn today.
- **Export / Import** — download your whole wardrobe as a dated JSON backup and restore it later (merge or replace).

## Stack

- **Backend:** FastAPI + SQLAlchemy + SQLite, data scoped per user via an `X-User-Token` header.
- **Frontend:** a single self-contained `public/index.html` (vanilla JS, no build step). Color detection and natural-language parsing run client-side.
- **Deploy:** Docker on Fly.io with a persistent volume mounted at `/data`.

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8088
```

Open http://localhost:8088.
