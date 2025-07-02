import math

def draw_sauces_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y):
    sauces = {
        "Thai Sauce": {"ingredients":[("Green Curry Paste",7),("Coconut Cream",82)], "meal_key":"THAI GREEN CHICKEN CURRY"},
        "Lamb Sauce": {"ingredients":[("Greek Yogurt",20),("Garlic",2),("Salt",1)], "meal_key":"LAMB SOUVLAKI"}
    }
    pdf.set_xy(xpos[0], start_y)
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"Sauces",ln=1,align='C')
    pdf.ln(5)
    y0 = pdf.get_y()
    heights = []
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
        heights.append(pdf.get_y())
    # Return the lower Y so the next section starts after both columns
    return max(heights) + pad
