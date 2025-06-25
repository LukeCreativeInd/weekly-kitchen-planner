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
    {"title": "Penne Order", "batch_ingredient": "Penne", "batch_size": 157, "ingredients": {"Penne": 59, "Oil": 0.7}, "meals": ["Chicken Pesto Pasta", "Chicken and Broccoli Pasta"]},
    {"title": "Rice Order", "batch_ingredient": "Rice", "batch_size": 180, "ingredients": {"Rice": 60, "Oil": 0.7}, "meals": ["Beef Chow Mein", "Beef Burrito Bowl", "Lebanese Beef Stew", "Mongolian Beef", "Butter Chicken", "Thai Green Chicken Curry", "Beans Nacho", "Chicken Fajita Bowl"]},
    {"title": "Moroccan Chicken", "batch_ingredient": "Chicken", "batch_size": 0, "ingredients": {"Chicken": 180, "Oil": 2, "Lemon Juice": 6, "Moroccan Chicken Mix": 4}, "meals": ["Moroccan Chicken"]},
    {"title": "Steak", "batch_ingredient": "Steak", "batch_size": 0, "ingredients": {"Steak": 110, "Oil": 1.5, "Baking Soda": 3}, "meals": ["Steak with Mushroom Sauce", "Steak On Its Own"]},
    {"title": "Lamb Marinate", "batch_ingredient": "Lamb Shoulder", "batch_size": 0, "ingredients": {"Lamb Shoulder": 162, "Oil": 2, "Salt": 1.5, "Oregano": 1.2}, "meals": ["Naked Chicken Parma", "Lamb Souvlaki"]},
    {"title": "Potato Mash", "batch_ingredient": "Potato", "batch_size": 0, "ingredients": {"Potato": 150, "Cooking Cream": 20, "Butter": 7, "Salt": 1.5, "White Pepper": 0.5}, "meals": ["Beef Meatballs", "Steak with Mushroom Sauce"]},
    {"title": "Sweet Potato Mash", "batch_ingredient": "Sweet Potato", "batch_size": 0, "ingredients": {"Sweet Potato": 185, "Salt": 1, "White Pepper": 0.5}, "meals": ["Shepherd's Pie", "Chicken Sweet Potato and Beans"]},
    {"title": "Roasted Potatoes", "batch_ingredient": "Roasted Potatoes", "batch_size": 60, "ingredients": {"Roasted Potatoes": 190, "Oil": 1, "Spices Mix": 2.5}, "meals": []},
    {"title": "Roasted Lemon Potatoes", "batch_ingredient": "Potatoes", "batch_size": 60, "ingredients": {"Potatoes": 207, "Oil": 1, "Salt": 1.2}, "meals": ["Roasted Lemon Chicken"]},
    {"title": "Roasted Thai Potatoes", "batch_ingredient": "Potato", "batch_size": 0, "ingredients": {"Potato": 60, "Salt": 1}, "meals": ["Thai Green Chicken Curry"]},
    {"title": "Lamb Onion Marinated", "batch_ingredient": "Red Onion", "batch_size": 0, "ingredients": {"Red Onion": 30, "Parsley": 1.5, "Paprika": 0.5}, "meals": ["Lamb Souvlaki"]},
    {"title": "Green Beans", "batch_ingredient": "Green Beans", "batch_size": 0, "ingredients": {"Green Beans": 60}, "meals": ["Chicken with Vegetables", "Chicken Sweet Potato and Beans", "Steak with Mushroom Sauce"]}
]

# ----------------------------
# Streamlit App
# ----------------------------
st.title("📦 Bulk Ingredient Summary Report")
uploaded_file = st.file_uploader("Upload Production File (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Load and validate data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()
    if not {"product name", "quantity"}.issubset(df.columns):
        st.error("CSV must contain 'Product name' and 'Quantity' columns.")
        st.stop()
    st.success("File uploaded successfully!")
    st.dataframe(df)
    meal_totals = dict(zip(df["product name"].str.upper(), df["quantity"]))

    # Initialize PDF constants
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)
    left_margin = 10
    page_width = 210 - 2 * left_margin
    col_width = page_width / 2 - 5
    cell_height = 6
    padding_after = 4
    bottom_limit = 280
    column_x = [left_margin, left_margin + col_width + 10]

    # Utility: start new column or page
    def new_position(heights, cur_col):
        if cur_col == 1:
            pdf.add_page()
            y = pdf.get_y()
            return [y, y], 0
        else:
            return heights, 1

    # ----------------------------
    # Page 1: Bulk Summary
    # ----------------------------
    pdf.add_page()
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,f"Daily Production Report - {datetime.today().strftime('%d/%m/%Y')}",ln=1,align="C")
    pdf.ln(5)

    heights = [pdf.get_y(), pdf.get_y()]
    col = 0

    def draw_section(idx, sec):
        x = column_x[idx]; y = heights[idx]
        pdf.set_xy(x,y)
        pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
        pdf.cell(col_width,cell_height,sec["title"],ln=1,fill=True)
        pdf.set_x(x); pdf.set_font("Arial","B",8)
        for head in ["Ingredient","Qty/Meal","Meals","Total","Batches"]:
            w=[col_width*0.4,col_width*0.15,col_width*0.15,col_width*0.15,col_width*0.15][["Ingredient","Qty/Meal","Meals","Total","Batches"].index(head)]
            pdf.cell(w,cell_height,head,1)
        pdf.ln(cell_height)
        pdf.set_font("Arial","",8)
        total_meals = sum(meal_totals.get(m.upper(),0) for m in sec["meals"] )
        batches = math.ceil(total_meals/sec["batch_size"]) if sec["batch_size"]>0 else 0
        for ingr,per in sec["ingredients"].items():
            total_qty=per*total_meals
            adj=round(total_qty/batches) if batches>0 else round(total_qty,2)
            lbl=batches if ingr==sec["batch_ingredient"] else ""
            pdf.set_x(x)
            pdf.cell(col_width*0.4,cell_height,ingr[:20],1)
            pdf.cell(col_width*0.15,cell_height,str(per),1)
            pdf.cell(col_width*0.15,cell_height,str(total_meals),1)
            pdf.cell(col_width*0.15,cell_height,str(adj),1)
            pdf.cell(col_width*0.15,cell_height,str(lbl),1)
            pdf.ln(cell_height)
        heights[idx]=pdf.get_y()+padding_after

    for sec in bulk_sections:
        block_h=(len(sec["ingredients"] )+2)*cell_height+padding_after
        if heights[col]+block_h>bottom_limit:
            heights,col=new_position(heights,col)
        draw_section(col,sec)

    # ----------------------------
    # Page 2: Meal Recipes
    # ----------------------------
    pdf.add_page()
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"Meal Recipes",ln=1,align="C"); pdf.ln(5)
    heights=[pdf.get_y(),pdf.get_y()]; col=0

    meal_recipes={
        "Spaghetti Bolognese": {"batch":90,"ingredients":{"Beef Mince":100,"Napoli Sauce":65,"Crushed Tomatoes":45,"Beef Stock":30,"Onion":15,"Zucchini":15,"Carrot":15,"Vegetable Oil":1,"Salt":2,"Pepper":0.5,"Spaghetti":68}},
        "Beef Chow Mein": {"batch":80,"ingredients":{"Beef Mince":120,"Celery":42,"Carrot":42,"Cabbage":42,"Onion":42,"Oil":2,"Pepper":0.8,"Soy Sauce":13,"Oyster Sauce":13,"Rice":130}},
        "Shepherd's Pie": {"batch":82,"ingredients":{"Beef Mince":100,"Oil":2,"Carrots":15,"Capsicum":15,"Onion":15,"Mushroom":15,"Peas":15,"Tomato Paste":6,"Beef Stock":20,"Salt":2,"Pepper":0.5,"Napoli Sauce":70}},
        "Beef Burrito Bowl": {"batch":130,"ingredients":{"Beef Mince":95,"Onion":12,"Capsicum":12,"Vegetable Oil":2,"Taco Seasoning":7,"Salt":1.5,"Pepper":0.5,"Beef Stock":40}},
        "Beef Meatballs": {"batch":0,"ingredients":{"Mince":150,"Onion":10,"Parsley":3,"Salt":1.5,"Pepper":0.2}},
        "Lebanese Beef Stew": {"batch":80,"ingredients":{"Chuck Diced":97,"Onion":30,"Carrot":30,"Potato":30,"Peas":30,"Oil":2,"Salt":2.5,"Pepper":0.5,"Tomato Paste":20,"Water":30,"Beef Stock":30,"Rice":130}},
        "Mongolian Beef": {"batch":0,"ingredients":{"Chuck":97,"Baking Soda":2.5,"Water":10,"Soy Sauce":5,"Cornflour":2.5}},
        "Chicken With Vegetables": {"batch":0,"ingredients":{"Chicken":135,"Corn":52,"Beans":60,"Broccoli":67}},
        "Chicken Sweet Potato and Beans": {"batch":0,"ingredients":{"Chicken":135,"Beans":60}},
        "Naked Chicken Parma": {"batch":0,"ingredients":{"Chicken":150}},
        "Chicken Pesto Pasta": {"batch":0,"ingredients":{"Chicken":130,"Penne":59,"Sundried Tomatoes":24}},
        "Chicken and Broccoli Pasta": {"batch":0,"ingredients":{"Chicken":130,"Penne":59,"Broccoli":40}},
        "Butter Chicken": {"batch":0,"ingredients":{"Chicken":140,"Peas":40,"Rice":130}},
        "Thai Green Chicken Curry": {"batch":0,"ingredients":{"Chicken":140,"Rice":130}},
        "Moroccan Chicken": {"batch":0,"ingredients":{"Chicken":180},"sub_section":{"title":"Chickpea Recipe","ingredients":{"Onion":20,"Zucchini":30,"Red Capsicum":30,"Garlic":2,"Oil":2,"Chickpeas":115,"Mix Spices":1.7,"Chicken Stock":50}}}
    }

    def draw_recipe(idx,name,data):
        x=column_x[idx];y=heights[idx]
        pdf.set_xy(x,y)
        pdf.set_font("Arial","B",11);pdf.set_fill_color(230,230,230)
        pdf.cell(col_width,cell_height,name,ln=1,fill=True)
        pdf.set_x(x);pdf.set_font("Arial","B",8)
        for head,w in [("Ingredient",0.3),("Qty/Meal",0.15),("Meals",0.15),("Batch Total",0.25),("Batch",0.15)]:
            pdf.cell(col_width*w,cell_height,head,1)
        pdf.ln(cell_height);pdf.set_font("Arial","",8)
        tot=meal_totals.get(name.upper(),0);batches=math.ceil(tot/data.get("batch",1)) if data.get("batch",0)>0 else 0
        for i,(ing,qty) in enumerate(data["ingredients"].items()):
            total_qty=qty*tot;bt=round(total_qty/batches) if batches>0 else 0;bl=str(batches) if i==0 else ""
            pdf.set_x(x);pdf.cell(col_width*0.3,cell_height,ing[:20],1);pdf.cell(col_width*0.15,cell_height,str(qty),1);pdf.cell(col_width*0.15,cell_height,str(tot),1);pdf.cell(col_width*0.25,cell_height,str(bt),1);pdf.cell(col_width*0.15,cell_height,bl,1);pdf.ln(cell_height)
        if "sub_section" in data:
            sub=data["sub_section"]
            pdf.set_x(x);pdf.set_font("Arial","B",9);pdf.cell(col_width,cell_height,sub["title"],ln=1)
            pdf.set_x(x);pdf.set_font("Arial","B",8)
            for head,w in [("Ingredient",0.3),("Qty/Meal",0.15),("Meals",0.15),("Total",0.25),("",0.15)]: pdf.cell(col_width*w,cell_height,head,1)
            pdf.ln(cell_height);pdf.set_font("Arial","",8)
            for ingr,per in sub["ingredients"].items():
                total_qty=per*tot;adj=round(total_qty/batches) if batches>0 else round(total_qty,2)
                pdf.set_x(x);pdf.cell(col_width*0.3,cell_height,ingr[:20],1);pdf.cell(col_width*0.15,cell_height,str(per),1);pdf.cell(col_width*0.15,cell_height,str(tot),1);pdf.cell(col_width*0.25,cell_height,str(adj),1);pdf.cell(col_width*0.15,cell_height,"");pdf.ln(cell_height)
        heights[idx]=pdf.get_y()+padding_after

    for name,data in meal_recipes.items():
        block_h=(len(data["ingredients"])+(1 if "sub_section" in data else 0)+2)*cell_height+padding_after
        if heights[col]+block_h>bottom_limit:
            heights,col=new_position(heights,col)
        draw_recipe(col,name,data)

    # ----------------------------
    # Page 3: Sauces
    # ----------------------------
    pdf.add_page();pdf.set_font("Arial","B",14);pdf.cell(0,10,"Sauces",ln=1,align="C");pdf.ln(5)
    sauces={"Thai Sauce":{"ingredients":[("Green Curry Paste",7),("Coconut Cream",82)],"meal_key":"THAI GREEN CHICKEN CURRY"},"Lamb Sauce":{"ingredients":[("Greek Yogurt",20),("Garlic",2),("Salt",1)],"meal_key":"LAMB SOUVLAKI"}}
    heights=[pdf.get_y(),pdf.get_y()];col=0
    for nm,sd in sauces.items():
        block_h=(len(sd["ingredients"])+2)*cell_height+padding_after
        if heights[col]+block_h>bottom_limit:
            heights,col=new_position(heights,col)
        x=column_x[col];y=heights[col];pdf.set_xy(x,y)
        pdf.set_font("Arial","B",11);pdf.set_fill_color(230,230,230);pdf.cell(col_width,cell_height,nm,ln=1,fill=True)
        pdf.set_x(x);pdf.set_font("Arial","B",8)
        for head,w in [("Ingredient",0.3),("Meal Amount",0.2),("Total Meals",0.2),("Required Ingredient",0.3)]:pdf.cell(col_width*w,cell_height,head,1)
        pdf.ln(cell_height);pdf.set_font("Arial","",8)
        tm=meal_totals.get(sd["meal_key"],0)
        for ing,am in sd["ingredients"]:
            pdf.set_x(x);pdf.cell(col_width*0.3,cell_height,ing[:20],1);pdf.cell(col_width*0.2,cell_height,str(am),1);pdf.cell(col_width*0.2,cell_height,str(tm),1);pdf.cell(col_width*0.3,cell_height,str(am*tm),1);pdf.ln(cell_height)
        heights[col]=pdf.get_y()+padding_after

    # Save and download
    fname=f"daily_production_report_{datetime.today().strftime('%d-%m-%Y')}.pdf";pdf.output(fname)
    with open(fname,"rb") as f:st.download_button("📄 Download Bulk Order PDF",f,file_name=fname,mime="application/pdf")
