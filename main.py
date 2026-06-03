import os
from datetime import datetime
from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel
from typing import Optional

from models import Base, Saree, Blouse, Outfit

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wardrobe.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Saree Wardrobe")
app.mount("/public", StaticFiles(directory="public"), name="public")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_token(x_user_token: str = Header(default="")) -> str:
    return x_user_token


@app.get("/")
def root():
    return FileResponse("public/index.html")


# ── Schemas ──
class SareeIn(BaseModel):
    name: str = ""
    saree_name: str = ""
    body_color: str = ""
    border_color: str = ""
    region_name: str = ""
    color: str = ""
    fabric: str = ""
    occasion: str = ""
    price: str = ""
    purchase_date: str = ""
    notes: str = ""
    image: str = ""


class BlouseIn(BaseModel):
    name: str = ""
    color: str = ""
    fabric: str = ""
    occasion: str = ""
    price: str = ""
    purchase_date: str = ""
    notes: str = ""
    image: str = ""


class OutfitIn(BaseModel):
    name: str = ""
    saree_id: Optional[int] = None
    blouse_id: Optional[int] = None
    occasion: str = ""
    last_worn: str = ""


class ImportData(BaseModel):
    sarees: list[dict] = []
    blouses: list[dict] = []
    outfits: list[dict] = []
    replace: bool = False


# ── Serializers ──
def saree_dict(s: Saree) -> dict:
    return {
        "id": s.id, "name": s.name, "saree_name": s.saree_name,
        "body_color": s.body_color, "border_color": s.border_color,
        "region_name": s.region_name, "color": s.color, "fabric": s.fabric,
        "occasion": s.occasion, "price": s.price, "purchase_date": s.purchase_date,
        "notes": s.notes, "image": s.image,
    }


def blouse_dict(b: Blouse) -> dict:
    return {
        "id": b.id, "name": b.name, "color": b.color, "fabric": b.fabric,
        "occasion": b.occasion, "price": b.price, "purchase_date": b.purchase_date,
        "notes": b.notes, "image": b.image,
    }


def outfit_dict(o: Outfit) -> dict:
    return {
        "id": o.id, "name": o.name, "saree_id": o.saree_id, "blouse_id": o.blouse_id,
        "occasion": o.occasion, "last_worn": o.last_worn,
    }


# ── Sarees ──
@app.get("/sarees")
def list_sarees(db: Session = Depends(get_db), token: str = Depends(get_token)):
    rows = db.query(Saree).filter(Saree.token == token).order_by(Saree.created_at.desc()).all()
    return [saree_dict(s) for s in rows]


@app.post("/sarees")
def create_saree(req: SareeIn, db: Session = Depends(get_db), token: str = Depends(get_token)):
    s = Saree(token=token, **req.model_dump())
    db.add(s)
    db.commit()
    db.refresh(s)
    return saree_dict(s)


@app.put("/sarees/{item_id}")
def update_saree(item_id: int, req: SareeIn, db: Session = Depends(get_db), token: str = Depends(get_token)):
    s = db.query(Saree).filter(Saree.id == item_id, Saree.token == token).first()
    if not s:
        raise HTTPException(404, "Saree not found")
    for k, v in req.model_dump().items():
        setattr(s, k, v)
    db.commit()
    db.refresh(s)
    return saree_dict(s)


@app.delete("/sarees/{item_id}")
def delete_saree(item_id: int, db: Session = Depends(get_db), token: str = Depends(get_token)):
    s = db.query(Saree).filter(Saree.id == item_id, Saree.token == token).first()
    if not s:
        raise HTTPException(404, "Saree not found")
    db.delete(s)
    db.commit()
    return {"ok": True}


# ── Blouses ──
@app.get("/blouses")
def list_blouses(db: Session = Depends(get_db), token: str = Depends(get_token)):
    rows = db.query(Blouse).filter(Blouse.token == token).order_by(Blouse.created_at.desc()).all()
    return [blouse_dict(b) for b in rows]


@app.post("/blouses")
def create_blouse(req: BlouseIn, db: Session = Depends(get_db), token: str = Depends(get_token)):
    b = Blouse(token=token, **req.model_dump())
    db.add(b)
    db.commit()
    db.refresh(b)
    return blouse_dict(b)


@app.put("/blouses/{item_id}")
def update_blouse(item_id: int, req: BlouseIn, db: Session = Depends(get_db), token: str = Depends(get_token)):
    b = db.query(Blouse).filter(Blouse.id == item_id, Blouse.token == token).first()
    if not b:
        raise HTTPException(404, "Blouse not found")
    for k, v in req.model_dump().items():
        setattr(b, k, v)
    db.commit()
    db.refresh(b)
    return blouse_dict(b)


@app.delete("/blouses/{item_id}")
def delete_blouse(item_id: int, db: Session = Depends(get_db), token: str = Depends(get_token)):
    b = db.query(Blouse).filter(Blouse.id == item_id, Blouse.token == token).first()
    if not b:
        raise HTTPException(404, "Blouse not found")
    db.delete(b)
    db.commit()
    return {"ok": True}


# ── Outfits ──
@app.get("/outfits")
def list_outfits(db: Session = Depends(get_db), token: str = Depends(get_token)):
    rows = db.query(Outfit).filter(Outfit.token == token).order_by(Outfit.created_at.desc()).all()
    return [outfit_dict(o) for o in rows]


@app.post("/outfits")
def create_outfit(req: OutfitIn, db: Session = Depends(get_db), token: str = Depends(get_token)):
    o = Outfit(token=token, **req.model_dump())
    db.add(o)
    db.commit()
    db.refresh(o)
    return outfit_dict(o)


@app.put("/outfits/{item_id}")
def update_outfit(item_id: int, req: OutfitIn, db: Session = Depends(get_db), token: str = Depends(get_token)):
    o = db.query(Outfit).filter(Outfit.id == item_id, Outfit.token == token).first()
    if not o:
        raise HTTPException(404, "Outfit not found")
    for k, v in req.model_dump().items():
        setattr(o, k, v)
    db.commit()
    db.refresh(o)
    return outfit_dict(o)


@app.post("/outfits/{item_id}/worn")
def mark_worn(item_id: int, db: Session = Depends(get_db), token: str = Depends(get_token)):
    o = db.query(Outfit).filter(Outfit.id == item_id, Outfit.token == token).first()
    if not o:
        raise HTTPException(404, "Outfit not found")
    o.last_worn = datetime.utcnow().strftime("%Y-%m-%d")
    db.commit()
    db.refresh(o)
    return outfit_dict(o)


@app.delete("/outfits/{item_id}")
def delete_outfit(item_id: int, db: Session = Depends(get_db), token: str = Depends(get_token)):
    o = db.query(Outfit).filter(Outfit.id == item_id, Outfit.token == token).first()
    if not o:
        raise HTTPException(404, "Outfit not found")
    db.delete(o)
    db.commit()
    return {"ok": True}


# ── Export / Import ──
@app.get("/export")
def export_data(db: Session = Depends(get_db), token: str = Depends(get_token)):
    sarees = db.query(Saree).filter(Saree.token == token).all()
    blouses = db.query(Blouse).filter(Blouse.token == token).all()
    outfits = db.query(Outfit).filter(Outfit.token == token).all()
    return {
        "exported_at": datetime.utcnow().isoformat(),
        "sarees": [saree_dict(s) for s in sarees],
        "blouses": [blouse_dict(b) for b in blouses],
        "outfits": [outfit_dict(o) for o in outfits],
    }


@app.post("/import")
def import_data(req: ImportData, db: Session = Depends(get_db), token: str = Depends(get_token)):
    if req.replace:
        db.query(Saree).filter(Saree.token == token).delete()
        db.query(Blouse).filter(Blouse.token == token).delete()
        db.query(Outfit).filter(Outfit.token == token).delete()
        db.flush()

    saree_fields = set(SareeIn.model_fields.keys())
    blouse_fields = set(BlouseIn.model_fields.keys())
    outfit_fields = set(OutfitIn.model_fields.keys())

    # Map old saree/blouse ids -> new ids so outfit references survive import
    saree_id_map: dict = {}
    blouse_id_map: dict = {}

    for item in req.sarees:
        old_id = item.get("id")
        data = {k: v for k, v in item.items() if k in saree_fields}
        s = Saree(token=token, **data)
        db.add(s)
        db.flush()
        if old_id is not None:
            saree_id_map[old_id] = s.id

    for item in req.blouses:
        old_id = item.get("id")
        data = {k: v for k, v in item.items() if k in blouse_fields}
        b = Blouse(token=token, **data)
        db.add(b)
        db.flush()
        if old_id is not None:
            blouse_id_map[old_id] = b.id

    for item in req.outfits:
        data = {k: v for k, v in item.items() if k in outfit_fields}
        if data.get("saree_id") in saree_id_map:
            data["saree_id"] = saree_id_map[data["saree_id"]]
        if data.get("blouse_id") in blouse_id_map:
            data["blouse_id"] = blouse_id_map[data["blouse_id"]]
        db.add(Outfit(token=token, **data))

    db.commit()
    return {
        "ok": True,
        "imported": {
            "sarees": len(req.sarees),
            "blouses": len(req.blouses),
            "outfits": len(req.outfits),
        },
    }
