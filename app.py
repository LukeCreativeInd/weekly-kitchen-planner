import streamlit as st
import pandas as pd
import math
from fpdf import FPDF
from datetime import datetime

# ----------------------------
# BULK RECIPE DEFINITIONS
# ----------------------------
bulk_sections = [
    {"title":"Spaghetti Order","batch_ingredient":"Spaghetti","batch_size":85,
     "ingredients":{"Spaghetti":68,"Oil":0.7},"meals":["Spaghetti Bolognese"]},
    {"title":"Penne Order","batch_ingredient":"Penne","batch_size":157,
     "ingredients":{"Penne":59,"Oil":0.7},"meals":["Chicken Pesto Pasta","Chicken and Broccoli Pasta"]},
    {"title":"Rice Order","batch_ingredient":"Rice","batch_size":180,
     "ingredients":{"Rice":60,"Oil":0.7},
     "meals":["Beef Chow Mein","Beef Burrito Bowl","Lebanese Beef Stew","Mongolian Beef","Butter Chicken","Thai Green Chicken Curry","Beans Nacho","Chicken Fajita Bowl"]},
    {"title":"Moroccan Chicken","batch_ingredient":"Chicken","batch_size":0,
     "ingredients":{"Chicken":180,"Oil":2,"Lemon Juice":6,"Moroccan Chicken Mix":4},"meals":["Moroccan Chicken"]},
    {"title":"Steak","batch_ingredient":"Steak","batch_size":0,
     "ingredients":{"Steak":110,"Oil":1.5,"Baking Soda":3},"meals":["Steak with Mushroom Sauce","Steak On Its Own"]},
    {"title":"Lamb Marinate","batch_ingredient":"Lamb Shoulder","batch_size":0,
     "ingredients":{"Lamb Shoulder":162,"Oil":2,"Salt":1.5,"Oregano":1.2},"meals":["Naked Chicken Parma","Lamb Souvlaki"]},
    {"title":"Potato Mash","batch_ingredient":"Potato","batch_size":0,
     "ingredients":{"Potato":150,"Cooking Cream":20,"Butter":7,"Salt":1.5,"White Pepper":0.5},"meals":["Beef Meatballs","Steak with Mushroom Sauce"]},
    {"title":"Sweet Potato Mash","batch_ingredient":"Sweet Potato","batch_size":0,
     "ingredients":{"Sweet Potato":185,"Salt":1,"White Pepper":0.5},"meals":["Shepherd's Pie","Chicken Sweet Potato and Beans"]},
    {"title":"Roasted Potatoes","batch_ingredient":"Roasted Potatoes","batch_size":60,
     "ingredients":{"Roasted Potatoes":190,"Oil":1,"Spices Mix":2.5},"meals":[]},
    {"title":"Roasted Lemon Potatoes","batch_ingredient":"Potatoes","batch_size":60,
     "ingredients":{"Potatoes":207,"Oil":1,"Salt":1.2},"meals":["Roasted Lemon Chicken"]},
    {"title":"Roasted Thai Potatoes","batch_ingredient":"Potato","batch_size":0,
     "ingredients":{"Potato":60,"Salt":1},"meals":["Thai Green Chicken Curry"]},
    {"title":"Lamb Onion Marinated","batch_ingredient":"Red Onion","batch_size":0,
     "ingredients":{"Red Onion":30,"Parsley":1.5,"Paprika":0.5},"meals":["Lamb Souvlaki"]},
    {"title":"Green Beans","batch_ingredient":"Green Beans","batch_size":0,
     "ingredients":{"Green Beans":60},"meals":["Chicken with Vegetables","Chicken Sweet Potato and Beans","Steak with Mushroom Sauce"]}
]

# ----------------------------
# Streamlit App
# ----------------------------
st.title("📦 Bulk Ingredient Summary Report")
uploaded_file = st.file_uploader("Upload Production File (CSV or Excel)", type=["csv","xlsx"])
if not uploaded_file:
    st.stop()

# Read data
if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_excel(uploaded_file)

# Validate
df.columns = df.columns.str.strip().str.lower()
if not {"product name","quantity"}.issubset(df.columns):
    st.error("CSV must contain 'Product name' and 'Quantity'")
    st.stop()

st.dataframe(df)
meal_totals = dict(zip(df["product name"].str.upper(), df["quantity"]))

# PDF setup
a4_w, a4_h = 210, 297
pdf = FPDF()
pdf.set_auto_page_break(False)
left = 10
page_w = a4_w - 2*left
col_w = page_w/2 - 5
ch, pad, bottom = 6, 4, a4_h - 17
xpos = [left, left + col_w + 10]

def next_pos(heights, col, block_h, title=None):
    if heights[col] + block_h > bottom: 
        col = 1 - col
        if heights[col] + block_h > bottom:
            pdf.add_page()
            if title:
                pdf.set_font("Arial","B",14)
                pdf.cell(0,10,title,ln=1,align='C')
                pdf.ln(5)
            heights = [pdf.get_y(), pdf.get_y()]
    return heights, col

# ---- Page 1: Bulk Summary ----
title1 = f"Daily Production Report - {datetime.today().strftime('%d/%m/%Y')}"
pdf.add_page()
pdf.set_font("Arial","B",14)
pdf.cell(0,10,title1,ln=1,align='C')
pdf.ln(5)

heights = [pdf.get_y(), pdf.get_y()]
col = 0
for sec in bulk_sections:
    block_h = (len(sec['ingredients'])+2)*ch + pad
    heights, col = next_pos(heights, col, block_h, title1)
    x, y = xpos[col], heights[col]
    pdf.set_xy(x,y)
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w,ch,sec['title'],ln=1,fill=True)
    pdf.set_x(x); pdf.set_font("Arial","B",8)
    for h,w in [("Ingredient",0.4),("Qty/Meal",0.15),("Meals",0.15),("Total",0.15),("Batches",0.15)]:
        pdf.cell(col_w*w,ch,h,1)
    pdf.ln(ch); pdf.set_font("Arial","",8)
    total_meals = sum(meal_totals.get(m.upper(),0) for m in sec['meals'])
    batches = math.ceil(total_meals/sec['batch_size']) if sec['batch_size']>0 else 0
    for ingr,per in sec['ingredients'].items():
        qty = per * total_meals
        adj = round(qty/batches) if batches else round(qty,2)
        lbl = str(batches) if ingr==sec['batch_ingredient'] else ""
        pdf.set_x(x)
        pdf.cell(col_w*0.4,ch,ingr[:20],1)
        pdf.cell(col_w*0.15,ch,str(per),1)
        pdf.cell(col_w*0.15,ch,str(total_meals),1)
        pdf.cell(col_w*0.15,ch,str(adj),1)
        pdf.cell(col_w*0.15,ch,lbl,1)
        pdf.ln(ch)
    heights[col] = pdf.get_y() + pad

# ---- Page 2: Meal Recipes ----
meal_recipes = {
    "Spaghetti Bolognese": {"batch":90, "ingredients":{"Beef Mince":100,"Napoli Sauce":65,"Crushed Tomatoes":45,"Beef Stock":30,"Onion":15,"Zucchini":15,"Carrot":15,"Vegetable Oil":1,"Salt":2,"Pepper":0.5,"Spaghetti":68}},
    "Beef Chow Mein":        {"batch":80, "ingredients":{"Beef Mince":120,"Celery":42,"Carrot":42,"Cabbage":42,"Onion":42,"Oil":2,"Pepper":0.8,"Soy Sauce":13,"Oyster Sauce":13,"Rice":130}},
    "Shepherd's Pie":        {"batch":82, "ingredients":{"Beef Mince":100,"Oil":2,"Carrots":15,"Capsicum":15,"Onion":15,"Mushroom":15,"Peas":15,"Tomato Paste":6,"Beef Stock":20,"Salt":2,"Pepper":0.5,"Napoli Sauce":70}},
    "Beef Burrito Bowl":     {"batch":130,"ingredients":{"Beef Mince":95,"Onion":12,"Capsicum":12,"Vegetable Oil":2,"Taco Seasoning":7,"Salt":1.5,"Pepper":0.5,"Beef Stock":40}},
    "Beef Meatballs":        {"batch":0,  "ingredients":{"Mince":150,"Onion":10,"Parsley":3,"Salt":1.5,"Pepper":0.2}},
    "Lebanese Beef Stew":     {"batch":80, "ingredients":{"Chuck Diced":97,"Onion":30,"Carrot":30,"Potato":30,"Peas":30,"Oil":2,"Salt":2.5,"Pepper":0.5,"Tomato Paste":20,"Water":30,"Beef Stock":30,"Rice":130}},
    "Mongolian Beef":         {"batch":0,  "ingredients":{"Chuck":97,"Baking Soda":2.5,"Water":10,"Soy Sauce":5,"Cornflour":2.5}},
    "Chicken With Vegetables":{"batch":0,  "ingredients":{"Chicken":135,"Corn":52,"Beans":60,"Broccoli":67}},
    "Chicken Sweet Potato and Beans": {"batch":0,"ingredients":{"Chicken":135,"Beans":60}},
    "Naked Chicken Parma":    {"batch":0,  "ingredients":{"Chicken":150}},
    "Chicken Pesto Pasta":    {"batch":0,  "ingredients":{"Chicken":130,"Penne":59,"Sundried Tomatoes":24}},
    "Chicken and Broccoli Pasta":{"batch":0,"ingredients":{"Chicken":130,"Penne":59,"Broccoli":40}},
    "Butter Chicken":         {"batch":0,  "ingredients":{"Chicken":140,"Peas":40,"Rice":130}},
    "Thai Green Chicken Curry":{"batch":0,  "ingredients":{"Chicken":140,"Rice":130}},
    "Moroccan Chicken":       {"batch":0,  "ingredients":{"Chicken":180},
                                "sub_section":{"title":"Chickpea Recipe","ingredients":{"Onion":20,"Zucchini":30,"Red Capsicum":30,"Garlic":2,"Oil":2,"Chickpeas":115,"Mix Spices":1.7,"Chicken Stock":50}}}
}
pdf.add_page()
pdf.set_font("Arial","B",14)
pdf.cell(0,10,"Meal Recipes",ln=1,align='C')
pdf.ln(5)
heights = [pdf.get_y(), pdf.get_y()]
col = 0
for name,data in meal_recipes.items():
    rows = 2 + len(data["ingredients"]) + (2 + len(data["sub_section"]["ingredients"]) if "sub_section" in data else 0)
    block_h = rows*ch + pad
    heights, col = next_pos(heights, col, block_h, "Meal Recipes")
    x,y = xpos[col], heights[col]
    pdf.set_xy(x,y)
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w,ch,name,ln=1,fill=True)
    pdf.set_x(x); pdf.set_font("Arial","B",8)
    for h,w in [("Ingredient",0.3),("Qty/Meal",0.15),("Meals",0.15),("Batch Total",0.25),("Batch",0.15)]:
        pdf.cell(col_w*w,ch,h,1)
    pdf.ln(ch); pdf.set_font("Arial","",8)
    tot = meal_totals.get(name.upper(),0)
    batches = math.ceil(tot/data["batch"]) if data["batch"]>0 else 0
    for i,(ing,qty) in enumerate(data["ingredients"].items()):
        bt = round(qty*tot/batches) if batches else 0
        bl = str(batches) if i==0 else ""
        pdf.set_x(x)
        pdf.cell(col_w*0.3,ch,ing[:20],1); pdf.cell(col_w*0.15,ch,str(qty),1)
        pdf.cell(col_w*0.15,ch,str(tot),1); pdf.cell(col_w*0.25,ch,str(bt),1)
        pdf.cell(col_w*0.15,ch,bl,1)
        pdf.ln(ch)
    if "sub_section" in data:
        sub = data["sub_section"]
        pdf.set_x(x); pdf.set_font("Arial","B",9)
        pdf.cell(col_w,ch,sub["title"],ln=1)
        pdf.set_x(x); pdf.set_font("Arial","B",8)
        for h,w in [("Ingredient",0.3),("Qty/Meal",0.15),("Meals",0.15),("Total",0.25),("",0.15)]:
            pdf.cell(col_w*w,ch,h,1)
        pdf.ln(ch); pdf.set_font("Arial","",8)
        for ingr,per in sub["ingredients"].items():
            adj = round(per*tot/batches) if batches else round(per*tot,2)
            pdf.set_x(x)
            pdf.cell(col_w*0.3,ch,ingr[:20],1); pdf.cell(col_w*0.15,ch,str(per),1)
            pdf.cell(col_w*0.15,ch,str(tot),1); pdf.cell(col_w*0.25,ch,str(adj),1)
            pdf.cell(col_w*0.15,ch,"",1)
            pdf.ln(ch)
    heights[col] = pdf.get_y() + pad

# ---- Page 3: Sauces Side by Side ----
pdf.add_page()
pdf.set_font("Arial","B",14)
pdf.cell(0,10,"Sauces",ln=1,align='C')
pdf.ln(5)
y0 = pdf.get_y()
heights3 = []
sauces = {
    "Thai Sauce": {"ingredients":[("Green Curry Paste",7),("Coconut Cream",82)], "meal_key":"THAI GREEN CHICKEN CURRY"},
    "Lamb Sauce": {"ingredients":[("Greek Yogurt",20),("Garlic",2),("Salt",1)], "meal_key":"LAMB SOUVLAKI"}
}
# draw sauces side-by-side
for idx,(name,data) in enumerate(sauces.items()):
    x = xpos[idx]
    pdf.set_xy(x, y0)
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, name, ln=1, fill=True)
    pdf.set_x(x); pdf.set_font("Arial","B",8)
    for h,w in [("Ingredient",0.3),("Meal Amount",0.2),("Total Meals",0.2),("Required Ingredient",0.3)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch); pdf.set_font("Arial","",8)
    tm = meal_totals.get(data["meal_key"], 0)
    for ing, am in data["ingredients"]:
        pdf.set_x(x)
        pdf.cell(col_w*0.3, ch, ing[:20], 1)
        pdf.cell(col_w*0.2, ch, str(am), 1)
        pdf.cell(col_w*0.2, ch, str(tm), 1)
        pdf.cell(col_w*0.3, ch, str(am*tm), 1)
        pdf.ln(ch)
    heights3.append(pdf.get_y())

# ---- To Pack In Fridge ----
fridge_y = max(heights3) + pad
pdf.set_xy(left, fridge_y)
pdf.set_font("Arial","B",14)
pdf.cell(0,10,"To Pack In Fridge",ln=1,align='C')
pdf.ln(5)

# Fixed dual-column start
fridge_start = pdf.get_y()

# Column 1: Sauces to Prepare
pdf.set_xy(xpos[0], fridge_start)
pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
pdf.cell(col_w, ch, "Sauces to Prepare", ln=1, fill=True)
pdf.set_x(xpos[0]); pdf.set_font("Arial","B",8)
for h,w in [("Sauce",0.4),("Qty",0.2),("Amt",0.2),("Total",0.2)]:
    pdf.cell(col_w*w, ch, h, 1)
pdf.ln(ch); pdf.set_font("Arial","",8)
for sauce, qty, key in [
    ("MONGOLIAN",70,"MONGOLIAN BEEF"),
    ("MEATBALLS",120,"BEEF MEATBALLS"),
    ("LEMON",50,"ROASTED LEMON CHICKEN"),
    ("MUSHROOM",100,"STEAK WITH MUSHROOM SAUCE"),
    ("FAJITA SAUCE",33,"CHICKEN FAJITA BOWL"),
    ("BURRITO SAUCE",43,"BEEF BURRITO BOWL")
]:
    amt = meal_totals.get(key.upper(),0)
    total = qty * amt
    pdf.set_x(xpos[0])
    pdf.cell(col_w*0.4, ch, sauce, 1)
    pdf.cell(col_w*0.2, ch, str(qty), 1)
    pdf.cell(col_w*0.2, ch, str(amt), 1)
    pdf.cell(col_w*0.2, ch, str(total), 1)
    pdf.ln(ch)

# Column 2: Beef Burrito Mix (aligned to same fridge_start)
pdf.set_xy(xpos[1], fridge_start)
pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
pdf.cell(col_w, ch, "Beef Burrito Mix", ln=1, fill=True)
pdf.set_x(xpos[1]); pdf.set_font("Arial","B",8)
for h,w in [("Ingredient",0.4),("Qty",0.2),("Amt",0.2),("Total",0.2)]:
    pdf.cell(col_w*w, ch, h, 1)
pdf.ln(ch); pdf.set_font("Arial","",8)
for ing, qty in [("Salsa",43),("Black Beans",50),("Corn",50),("Rice",130)]:
    amt = meal_totals.get("BEEF BURRITO BOWL",0)
    total = (qty * amt) / 60 if amt else 0
    pdf.set_x(xpos[1])
    pdf.cell(col_w*0.4, ch, ing, 1)
    pdf.cell(col_w*0.2, ch, str(qty), 1)
    pdf.cell(col_w*0.2, ch, str(amt), 1)
    pdf.cell(col_w*0.2, ch, f"{total:.2f}", 1)
    pdf.ln(ch)

# Column 1 under Sauces: Parma Mix
parma_start = fridge_start + (len([
    ("MONGOLIAN",70),("MEATBALLS",120),("LEMON",50),("MUSHROOM",100),("FAJITA SAUCE",33),("BURRITO SAUCE",43)
]) + 2) * ch + pad
pdf.set_xy(xpos[0], parma_start)
pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
pdf.cell(col_w, ch, "Parma Mix", ln=1, fill=True)
pdf.set_x(xpos[0]); pdf.set_font("Arial","B",8)
for h,w in [("Ingredient",0.4),("Qty",0.2),("Amt",0.2),("Total",0.2)]:
    pdf.cell(col_w*w, ch, h, 1)
pdf.ln(ch); pdf.set_font("Arial","",8)
for ing, qty in [("Napoli Sauce",50),("Mozzarella Cheese",40)]:
    amt = meal_totals.get("NAKED CHICKEN PARMA",0)
    total = qty * amt
    pdf.set_x(xpos[0])
    pdf.cell(col_w*0.4, ch, ing, 1)
    pdf.cell(col_w*0.2, ch, str(qty), 1)
    pdf.cell(col_w*0.2, ch, str(amt), 1)
    pdf.cell(col_w*0.2, ch, str(total), 1)
    pdf.ln(ch)


# ---- Chicken Mixing ----
# Estimate height needed: assume worst-case 6 rows per mix * number of mixes + header
est_rows = sum(1 + len(m[1]) for m in mixes) + 2
est_h = est_rows * ch + 2*pad + 20  # +20 for title
current_y = pdf.get_y()
if current_y + est_h > bottom:
    pdf.add_page()
pdf.set_xy(left, pdf.get_y())
pdf.set_font("Arial","B",14)
pdf.cell(0,10,"Chicken Mixing", ln=1, align='C')
pdf.ln(5)

for title, ingredients, meal_key, divisor in mixes:
    pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, title, ln=1, fill=True)
    pdf.ln(2)
    pdf.set_font("Arial","B",8)
    for h,w in [("Ingredient",0.3),("Qty",0.2),("Amt",0.2),("Total",0.2),("Batch",0.1)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch); pdf.set_font("Arial","",8)
    amt = meal_totals.get(meal_key.upper(),0)
    raw_b = math.ceil(amt/divisor) if divisor>0 else 0
    batches = raw_b + (raw_b % 2)
    for ing, qty in ingredients:
        total = (qty * amt) / batches if batches else 0
        pdf.cell(col_w*0.3, ch, ing[:20], 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(round(total,2)), 1)
        pdf.cell(col_w*0.1, ch, str(batches), 1)
        pdf.ln(ch)
    pdf.ln(2)


# ---- Save & Download ----
fname = f"daily_production_report_{datetime.today().strftime('%d-%m-%Y')}.pdf"
pdf.output(fname)
with open(fname, "rb") as f:
    st.download_button("📄 Download Bulk Order PDF", f, file_name=fname, mime="application/pdf")
