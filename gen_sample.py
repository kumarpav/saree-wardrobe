import base64, json

HEX = {
    "Blue":"#2c6fd6","Gold":"#d4af37","Red":"#c8102e","Green":"#1c8c4a","Emerald":"#0f9b6c",
    "Peach":"#ffb59a","Cream":"#f5ecd2","Mustard":"#d4a017","Maroon":"#6e1423","Lavender":"#b39ddb",
    "Silver":"#c9c9d1","Teal":"#0f8a8a","Magenta":"#c026a6","Pink":"#ec4899","Navy":"#1b2a52",
    "Black":"#1a1a1a","White":"#f7f7f7",
}

def svg(body, border, label):
    b = HEX.get(body, "#cccccc"); br = HEX.get(border, "#999999")
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="400" viewBox="0 0 300 400">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{b}"/><stop offset="1" stop-color="{b}" stop-opacity="0.78"/></linearGradient></defs>
<rect width="300" height="400" fill="url(#g)"/>
<rect x="0" y="0" width="300" height="22" fill="{br}"/>
<rect x="0" y="378" width="300" height="22" fill="{br}"/>
<rect x="0" y="0" width="16" height="400" fill="{br}"/>
<rect x="284" y="0" width="16" height="400" fill="{br}"/>
<g fill="{br}" opacity="0.85">
<circle cx="60" cy="120" r="7"/><circle cx="150" cy="90" r="7"/><circle cx="240" cy="150" r="7"/>
<circle cx="90" cy="220" r="7"/><circle cx="210" cy="260" r="7"/><circle cx="150" cy="320" r="7"/></g>
<text x="150" y="205" font-family="Georgia,serif" font-size="20" fill="#ffffff" text-anchor="middle" opacity="0.92">{label}</text>
</svg>'''
    return "data:image/svg+xml;base64," + base64.b64encode(s.encode()).decode()

sarees = [
    ("Royal Blue Banarasi","Royal Banarasi","Blue","Gold","Banarasi","Blue","Silk","Wedding","₹18,000","2025-11-02"),
    ("Crimson Kanjivaram","Temple Red","Red","Gold","Kanjivaram","Red","Silk","Wedding","₹24,000","2024-10-18"),
    ("Emerald Festive Silk","","Emerald","Gold","Mysore","Green","Silk","Festival","₹12,500","2025-08-30"),
    ("Peach Chiffon Drape","Sunset Peach","Peach","Cream","","Peach","Chiffon","Party","₹4,200","2026-01-12"),
    ("Mustard Cotton Daily","","Mustard","Maroon","Sambalpuri","Mustard","Cotton","Casual","₹1,800","2025-06-05"),
    ("Lavender Georgette","","Lavender","Silver","","Lavender","Georgette","Party","₹5,600","2025-12-21"),
    ("Teal Patola Heirloom","Grandma's Patola","Teal","Magenta","Patola","Teal","Silk","Festival","₹32,000","2023-04-09"),
    ("Blush Pink Chanderi","","Pink","Gold","Chanderi","Pink","Chanderi","Traditional","₹6,900","2025-09-14"),
]
blouses = [
    ("Gold Silk Blouse","Gold","Silk","Wedding","₹1,500","2025-11-02"),
    ("Red Cotton Blouse","Red","Cotton","Casual","₹600","2025-06-05"),
    ("Black Velvet Blouse","Black","Velvet","Party","₹1,200","2025-12-01"),
    ("Cream Brocade Blouse","Cream","Brocade","Festival","₹1,800","2025-08-30"),
    ("Navy Raw Silk Blouse","Navy","Silk","Formal","₹1,100","2025-07-19"),
]
outfits = [
    ("Reception Look", 1, 1, "Wedding", "2025-11-05"),
    ("Diwali Festive", 3, 4, "Festival", "2025-10-31"),
    ("Sangeet Night", 7, 3, "Party", ""),
]

S = []
for i,(name,sn,bc,brd,reg,col,fab,occ,price,pd) in enumerate(sarees, 1):
    S.append({"id":i,"name":name,"saree_name":sn,"body_color":bc,"border_color":brd,
              "region_name":reg,"color":col,"fabric":fab,"occasion":occ,"price":price,
              "purchase_date":pd,"notes":"","image":svg(bc,brd,bc)})
B = []
for i,(name,col,fab,occ,price,pd) in enumerate(blouses, 1):
    B.append({"id":i,"name":name,"color":col,"fabric":fab,"occasion":occ,"price":price,
              "purchase_date":pd,"notes":"","image":svg(col,col,col)})
O = []
for name,sid,bid,occ,worn in outfits:
    O.append({"name":name,"saree_id":sid,"blouse_id":bid,"occasion":occ,"last_worn":worn})

data = {"exported_at":"2026-06-03T00:00:00","sarees":S,"blouses":B,"outfits":O}
json.dump(data, open("sample-wardrobe.json","w"), indent=2)
print("wrote sample-wardrobe.json:", len(S), "sarees,", len(B), "blouses,", len(O), "outfits")
