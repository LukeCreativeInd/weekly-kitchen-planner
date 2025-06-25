import streamlit as st
import pandas as pd
import math
from fpdf import FPDF
from datetime import datetime

# ----------------------------
# BULK RECIPE DEFINITIONS
# ----------------------------
bulk_sections = [
    {"title": "Spaghetti Order", "batch_ingredient": "Spaghetti", "batch_size": 85, "ingredients": {"Spaghetti": 68, "Oil": 0.7}, "meals": ["Spaghetti Bolognese"]},
    {"title": "Penne Order", "batch_ingredient": "Penne", "batch_size": 157, "ingredients": {"Penne": 59, "Oil": 0.7}, "meals": ["Chicken Pesto Pasta","Chicken and Broccoli Pasta"]},
    {"title": "Rice Order", "batch_ingredient": "Rice", "batch_size": 180, "ingredients": {"Rice":60,"Oil":0.7}, "meals":["Beef Chow Mein","Beef Burrito Bowl","Lebanese Beef Stew","Mongolian Beef","Butter Chicken","Thai Green Chicken Curry","Beans Nacho","Chicken Fajita Bowl"]},
    {"title": "Moroccan Chicken","batch_ingredient":"Chicken","batch_size":0,"ingredients": {"Chicken":180,"Oil":2,"Lemon Juice":6,"Moroccan Chicken Mix":4},"meals":["Moroccan Chicken"]},
    {"title":"Steak","batch_ingredient":"Steak","batch_size":0,"ingredients": {"Steak":110,"Oil":1.5,"Baking Soda":3},"meals":["Steak with Mushroom Sauce","Steak On Its Own"]},
    {"title":"Lamb Marinate","batch_ingredient":"Lamb Shoulder","batch_size":0,"ingredients": {"Lamb Shoulder":162,"Oil":2,"Salt":1.5,"Oregano":1.2},"meals":["Naked Chicken Parma","Lamb Souvlaki"]},
    {"title":"Potato Mash","batch_ingredient":"Potato","batch_size":0,"ingredients": {"Potato":150,"Cooking Cream":20,"Butter":7,"Salt":1.5,"White Pepper":0.5},"meals":["Beef Meatballs","Steak with Mushroom Sauce"]},
    {"title":"Sweet Potato Mash","batch_ingredient":"Sweet Potato","batch_size":0,"ingredients": {"Sweet Potato":185,"Salt":1,"White Pepper":0.5},"meals":["Shepherd's Pie","Chicken Sweet Potato and Beans"]},
    {"title":"Roasted Potatoes","batch_ingredient":"Roasted Potatoes","batch_size":60,"ingredients": {"Roasted Potatoes":190,"Oil":1,"Spices Mix":2.5},"meals":[]},
    {"title":"Roasted Lemon Potatoes","batch_ingredient":"Potatoes","batch_size":60,"ingredients": {"Potatoes":207,"Oil":1,"Salt":1.2},"meals":["Roasted Lemon Chicken"]},
    {"title":"Roasted Thai Potatoes","batch_ingredient":"Potato","batch_size":0,"ingredients": {"Potato":60,"Salt":1},"meals":["Thai Green Chicken Curry"]},
    {"title":"Lamb Onion Marinated","batch_ingredient":"Red Onion","batch_size":0,"ingredients": {"Red Onion":30,"Parsley":1.5,"Paprika":0.5},"meals":["Lamb Souvlaki"]},
    {"title":"Green Beans","batch_ingredient":"Green Beans","batch_size":0,"ingredients": {"Green Beans":60},"meals":["Chicken with Vegetables","Chicken Sweet Potato and Beans","Steak with Mushroom Sauce"]}
]

st.title("📦 Bulk Ingredient Summary Report")
uploaded_file = st.file_uploader("Upload Production File (CSV or Excel)", type=["csv","xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()
    if not {"product name","quantity"}.issubset(df.columns):
        st.error("CSV must contain 'Product name' and 'Quantity'")
        st.stop()
    st.dataframe(df)
    meal_totals = dict(zip(df["product name"].str.upper(), df["quantity"]))

    pdf = FPDF()
    pdf.set_auto_page_break(False)
    left, page_w = 10, 190
    col_w = page_w/2 - 5
    ch, pad, bottom = 6,4,280
    xpos = [left, left+col_w+10]

    def next_pos(heights,col,block_h,title=None):
        if heights[col]+block_h>bottom:
            col=1-col
            if heights[col]+block_h>bottom:
                pdf.add_page()
                if title:
                    pdf.set_font("Arial","B",14)
                    pdf.cell(0,10,title,ln=1,align='C')
                    pdf.ln(5)
                heights=[pdf.get_y(),pdf.get_y()]
        return heights,col

    # Bulk Page
    title=f"Daily Production Report - {datetime.today().strftime('%d/%m/%Y')}"
    pdf.add_page();pdf.set_font("Arial","B",14);pdf.cell(0,10,title,ln=1,align='C');pdf.ln(5)
    heights=[pdf.get_y(),pdf.get_y()];col=0
    for sec in bulk_sections:
        block_h=(len(sec['ingredients'])+2)*ch+pad
        heights,col=next_pos(heights,col,block_h,title)
        x,y=xpos[col],heights[col]
        pdf.set_xy(x,y);pdf.set_font("Arial","B",11);pdf.set_fill_color(230,230,230);pdf.cell(col_w,ch,sec['title'],ln=1,fill=True)
        pdf.set_x(x);pdf.set_font("Arial","B",8)
        for h,w in [("Ingredient",0.4),("Qty/Meal",0.15),("Meals",0.15),("Total",0.15),("Batches",0.15)]:pdf.cell(col_w*w,ch,h,1)
        pdf.ln(ch);pdf.set_font("Arial","",8)
        totm=sum(meal_totals.get(m.upper(),0) for m in sec['meals']);batches=math.ceil(totm/sec['batch_size']) if sec['batch_size']>0 else 0
        for ingr,per in sec['ingredients'].items():adj=round(per*totm/batches) if batches else round(per*totm,2);lbl=str(batches) if ingr==sec['batch_ingredient'] else "";pdf.set_x(x);pdf.cell(col_w*0.4,ch,ingr[:20],1);pdf.cell(col_w*0.15,ch,str(per),1);pdf.cell(col_w*0.15,ch,str(totm),1);pdf.cell(col_w*0.15,ch,str(adj),1);pdf.cell(col_w*0.15,ch,lbl,1);pdf.ln(ch)
        heights[col]=pdf.get_y()+pad

    # Meal Recipes Page
    recipes={
        "Spaghetti Bolognese":{"batch":90,"ingredients":{"Beef Mince":100,"Napoli Sauce":65,"Crushed Tomatoes":45,"Beef Stock":30,"Onion":15,"Zucchini":15,"Carrot":15,"Vegetable Oil":1,"Salt":2,"Pepper":0.5,"Spaghetti":68}},
        "Beef Chow Mein":{"batch":80,"ingredients":{"Beef Mince":120,"Celery":42,"Carrot":42,"Cabbage":42,"Onion":42,"Oil":2,"Pepper":0.8,"Soy Sauce":13,"Oyster Sauce":13,"Rice":130}},
        "Shepherd's Pie":{"batch":82,"ingredients":{"Beef Mince":100,"Oil":2,"Carrots":15,"Capsicum":15,"Onion":15,"Mushroom":15,"Peas":15,"Tomato Paste":6,"Beef Stock":20,"Salt":2,"Pepper":0.5,"Napoli Sauce":70}},
        "Beef Burrito Bowl":{"batch":130,"ingredients":{"Beef Mince":95,"Onion":12,"Capsicum":12,"Vegetable Oil":2,"Taco Seasoning":7,"Salt":1.5,"Pepper":0.5,"Beef Stock":40}},
        "Beef Meatballs":{"batch":0,"ingredients":{"Mince":150,"Onion":10,"Parsley":3,"Salt":1.5,"Pepper":0.2}},
        "Lebanese Beef Stew":{"batch":80,"ingredients":{"Chuck Diced":97,"Onion":30,"Carrot":30,"Potato":30,"Peas":30,"Oil":2,"Salt":2.5,"Pepper":0.5,"Tomato Paste":20,"Water":30,"Beef Stock":30,"Rice":130}},
        "Mongolian Beef":{"batch":0,"ingredients":{"Chuck":97,"Baking Soda":2.5,"Water":10,"Soy Sauce":5,"Cornflour":2.5}},
        "Chicken With Vegetables":{"batch":0,"ingredients":{"Chicken":135,"Corn":52,"Beans":60,"Broccoli":67}},
        "Chicken Sweet Potato and Beans":{"batch":0,"ingredients":{"Chicken":135,"Beans":60}},
        "Naked Chicken Parma":{"batch":0,"ingredients":{"Chicken":150}},
        "Chicken Pesto Pasta":{"batch":0,"ingredients":{"Chicken":130,"Penne":59,"Sundried Tomatoes":24}},
        "Chicken and Broccoli Pasta":{"batch":0,"ingredients":{"Chicken":130,"Penne":59,"Broccoli":40}},
        "Butter Chicken":{"batch":0,"ingredients":{"Chicken":140,"Peas":40,"Rice":130}},
        "Thai Green Chicken Curry":{"batch":0,"ingredients":{"Chicken":140,"Rice":130}},
        "Moroccan Chicken":{"batch":0,"ingredients":{"Chicken":180},"sub_section":{"title":"Chickpea Recipe","ingredients":{"Onion":20,"Zucchini":30,"Red Capsicum":30,"Garlic":2,"Oil":2,"Chickpeas":115,"Mix Spices":1.7,"Chicken Stock":50}}}
    }
    title="Meal Recipes";pdf.add_page();pdf.set_font("Arial","B",14);pdf.cell(0,10,title,ln=1,align='C');pdf.ln(5)
    heights=[pdf.get_y(),pdf.get_y()];col=0
    for name,data in recipes.items():
        main=len(data["ingredients"])# rows calc
        sub=len(data.get("sub_section",{}).get("ingredients",{}))
        rows=1+1+main+(2+sub if sub else 0);block_h=rows*ch+pad
        heights,col=next_pos(heights,col,block_h,title)
        x,y=xpos[col],heights[col]
        pdf.set_xy(x,y);pdf.set_font("Arial","B",11);pdf.set_fill_color(230,230,230);pdf.cell(col_w,ch,name,ln=1,fill=True)
        pdf.set_x(x);pdf.set_font("Arial","B",8)
        for h,w in [("Ingredient",0.3),("Qty/Meal",0.15),("Meals",0.15),("Batch Total",0.25),("Batch",0.15)]:pdf.cell(col_w*w,ch,h,1)
        pdf.ln(ch);pdf.set_font("Arial","",8)
        tot=meal_totals.get(name.upper(),0);batches=math.ceil(tot/data.get("batch",1)) if data.get("batch",0)>0 else 0
        for i,(ing,qty) in enumerate(data["ingredients"].items()):pdf.set_x(x);pdf.cell(col_w*0.3,ch,ing[:20],1);pdf.cell(col_w*0.15,ch,str(qty),1);pdf.cell(col_w*0.15,ch,str(tot),1);pdf.cell(col_w*0.25,ch,str(round(qty*tot/batches) if batches else 0),1);pdf.cell(col_w*0.15,ch,str(batches) if i==0 else "",1);pdf.ln(ch)
        if "sub_section" in data:
            sub=data["sub_section"];pdf.set_x(x);pdf.set_font("Arial","B",9);pdf.cell(col_w,ch,sub["title"],ln=1)
            pdf.set_x(x);pdf.set_font("Arial","B",8);
            for h,w in [("Ingredient",0.3),("Qty/Meal",0.15),("Meals",0.15),("Total",0.25),("",0.15)]:pdf.cell(col_w*w,ch,h,1)
            pdf.ln(ch);pdf.set_font("Arial","",8)
            for ingr,per in sub["ingredients"].items():pdf.set_x(x);pdf.cell(col_w*0.3,ch,ingr[:20],1);pdf.cell(col_w*0.15,ch,str(per),1);pdf.cell(col_w*0.15,ch,str(tot),1);pdf.cell(col_w*0.25,ch,str(round(per*tot/batches) if batches else round(per*tot,2)),1);pdf.cell(col_w*0.15,ch,"",1);pdf.ln(ch)
        heights[col]=pdf.get_y()+pad

        # Sauces side by side
    pdf.add_page()
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"Sauces",ln=1,align='C')
    pdf.ln(5)
    sauces={
        "Thai Sauce": {"ingredients":[("Green Curry Paste",7),("Coconut Cream",82)],"meal_key":"THAI GREEN CHICKEN CURRY"},
        "Lamb Sauce": {"ingredients":[("Greek Yogurt",20),("Garlic",2),("Salt",1)],"meal_key":"LAMB SOUVLAKI"}
    }
    y0 = pdf.get_y()
    heights = []
    for idx, (name, data) in enumerate(sauces.items()):
        x = xpos[idx]
        pdf.set_xy(x, y0)
        pdf.set_font("Arial","B",11)
        pdf.set_fill_color(230,230,230)
        pdf.cell(col_w, ch, name, ln=1, fill=True)
        # header row
        pdf.set_x(x)
        pdf.set_font("Arial","B",8)
        pdf.cell(col_w*0.3, ch, "Ingredient", 1)
        pdf.cell(col_w*0.2, ch, "Meal Amount", 1)
        pdf.cell(col_w*0.2, ch, "Total Meals", 1)
        pdf.cell(col_w*0.3, ch, "Required Ingredient", 1)
        pdf.ln(ch)
        # data rows
        pdf.set_font("Arial","",8)
        tm = meal_totals.get(data["meal_key"], 0)
        for ing, am in data["ingredients"]:
            pdf.set_x(x)
            pdf.cell(col_w*0.3, ch, ing[:20], 1)
            pdf.cell(col_w*0.2, ch, str(am), 1)
            pdf.cell(col_w*0.2, ch, str(tm), 1)
            pdf.cell(col_w*0.3, ch, str(am*tm), 1)
            pdf.ln(ch)
        heights.append(pdf.get_y())
    pdf.set_xy(left, max(heights) + pad)

    # To Pack In Fridge
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"To Pack In Fridge",ln=1,align='C')
    pdf.ln(5)
    # Table heading: Sauces to Prepare
    pdf.set_x(left)
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Sauces to Prepare", ln=1, fill=True)
    pdf.ln(2)
    # Header row
    pdf.set_x(left)
    pdf.set_font("Arial","B",8)
    pdf.cell(col_w*0.4, ch, "Sauce", 1)
    pdf.cell(col_w*0.2, ch, "Quantity", 1)
    pdf.cell(col_w*0.2, ch, "Amount", 1)
    pdf.cell(col_w*0.2, ch, "Total", 1)
    pdf.ln(ch)
    # Data rows
    pdf.set_font("Arial","",8)
    sauce_prep=[
        ("MONGOLIAN", 70, "MONGOLIAN BEEF"),
        ("MEATBALLS", 120, "BEEF MEATBALLS"),
        ("LEMON", 50, "ROASTED LEMON CHICKEN"),
        ("MUSHROOM", 100, "STEAK WITH MUSHROOM SAUCE"),
        ("FAJITA SAUCE", 33, "CHICKEN FAJITA BOWL"),
        ("BURRITO SAUCE", 43, "BEEF BURRITO BOWL")
    ]
    for sauce, qty, meal_key in sauce_prep:
        pdf.set_x(left)
        amt = meal_totals.get(meal_key.upper(), 0)
        total = qty * amt
        pdf.cell(col_w*0.4, ch, sauce, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(total), 1)
        pdf.ln(ch)

        # Chicken Mixing + Mixes
    pdf.ln(5)
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"Chicken Mixing",ln=1,align='C')
    pdf.ln(5)
    mixes=[
        ("Pesto", [("Chicken",110),("Sauce",80)],"CHICKEN PESTO PASTA",50),
        ("Butter Chicken", [("Chicken",120),("Sauce",90)],"BUTTER CHICKEN",50),
        ("Broccoli Pasta", [("Chicken",100),("Sauce",100)],"CHICKEN AND BROCCOLI PASTA",50),
        ("Thai", [("Chicken",110),("Sauce",90)],"THAI GREEN CHICKEN CURRY",50),
        ("Gnocchi", [("Gnocchi",150),("Chicken",80),("Sauce",200),("Spinach",25)],"CREAMY CHICKEN & MUSHROOM GNOCCHI",36)
    ]
    for mix_title, ingredients, meal_key, divisor in mixes:
        pdf.set_x(left)
        pdf.set_font("Arial","B",11)
        pdf.set_fill_color(230,230,230)
        pdf.cell(col_w, ch, mix_title, ln=1, fill=True)
        pdf.ln(2)
        pdf.set_x(left)
        pdf.set_font("Arial","B",8)
        # column headers
        pdf.cell(col_w*0.3, ch, "Ingredient", 1)
        pdf.cell(col_w*0.2, ch, "Quantity", 1)
        pdf.cell(col_w*0.2, ch, "Amount", 1)
        pdf.cell(col_w*0.2, ch, "Total", 1)
        pdf.cell(col_w*0.1, ch, "Batches", 1)
        pdf.ln(ch)
        pdf.set_font("Arial","",8)
        amt = meal_totals.get(meal_key.upper(), 0)
        raw_batches = math.ceil(amt/divisor) if amt > 0 else 0
        batches = raw_batches + (raw_batches % 2)
        for ingr, qty in ingredients:
            total = (qty * amt) / batches if batches else 0
            pdf.set_x(left)
            pdf.cell(col_w*0.3, ch, ingr, 1)
            pdf.cell(col_w*0.2, ch, str(qty), 1)
            pdf.cell(col_w*0.2, ch, str(amt), 1)
            pdf.cell(col_w*0.2, ch, str(round(total,2)), 1)
            pdf.cell(col_w*0.1, ch, str(batches), 1)
            pdf.ln(ch)

    # ------------------
    # Save & Download
    # ------------------
    fname=f"daily_production_report_{datetime.today().strftime('%d-%m-%Y')}.pdf";pdf.output(fname)
    with open(fname,"rb") as f: st.download_button(label="📄 Download Bulk Order PDF",data=f,file_name=fname,mime="application/pdf")
