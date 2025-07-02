import math

def draw_meat_veg_section(pdf, xpos, col_w, ch, pad, bottom, start_y=None, meal_recipes=None, bulk_sections=None):
    # Use start_y if given, otherwise current y
    if start_y is not None:
        pdf.set_y(start_y)
    else:
        start_y = pdf.get_y()

    pdf.add_page()
    y = pdf.get_y()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align='C')
    pdf.ln(5)

    # --- Meat Order Table ---
    meat_types = [
        "CHUCK ROLL (LEBO)",
        "BEEF TOPSIDE (MONG)",
        "MINCE",
        "TOPSIDE STEAK",
        "LAMB SHOULDER",
        "MORROCAN CHICKEN",
        "ITALIAN CHICKEN",
        "NORMAL CHICKEN",
        "CHICKEN THIGH"
    ]

    # Default all 0, calculations for top five below
    amounts = [0] * len(meat_types)

    # Lookup: ensure uppercase keys
    if meal_recipes is None:
        meal_recipes = {}
    if bulk_sections is None:
        bulk_sections = []

    # CHUCK ROLL (LEBO): 'Chuck Diced' from Lebanese Beef Stew
    lebo = meal_recipes.get("Lebanese Beef Stew", {})
    if lebo:
        ingr = lebo["ingredients"]
        q = ingr.get("Chuck Diced", 0)
        # 'Amount' from meal_totals and 'Chuck Diced' quantity per meal
        # Just do 'Quantity x Amount'
        amounts[0] = q

    # BEEF TOPSIDE (MONG): 'Chuck' from Mongolian Beef
    mong = meal_recipes.get("Mongolian Beef", {})
    if mong:
        q = mong["ingredients"].get("Chuck", 0)
        amounts[1] = q

    # MINCE: Sum of 'Beef Mince' across several recipes
    mince_sum = 0
    for meal in ["Spaghetti Bolognese", "Shepherd's Pie", "Beef Chow Mein", "Beef Burrito Bowl"]:
        rec = meal_recipes.get(meal, {})
        if rec:
            mince_sum += rec["ingredients"].get("Beef Mince", 0)
    # Add Beef Meatballs 'Mince'
    meatballs = meal_recipes.get("Beef Meatballs", {})
    if meatballs:
        mince_sum += meatballs["ingredients"].get("Mince", 0)
    amounts[2] = mince_sum

    # TOPSIDE STEAK: 'Steak' row in 'Steak' bulk area
    steak_amt = 0
    for s in bulk_sections:
        if s["title"].upper().startswith("STEAK"):
            steak_amt = s["ingredients"].get("Steak", 0)
    amounts[3] = steak_amt

    # LAMB SHOULDER: 'Lamb Shoulder' from 'Lamb Marinate' in bulk area
    lamb_amt = 0
    for s in bulk_sections:
        if s["title"].upper().startswith("LAMB MARINATE"):
            lamb_amt = s["ingredients"].get("Lamb Shoulder", 0)
    amounts[4] = lamb_amt

    # MORROCAN CHICKEN: 'Chicken' from 'Moroccan Chicken' bulk area
    moroccan_amt = 0
    for s in bulk_sections:
        if s["title"].upper().startswith("MOROCCAN CHICKEN"):
            moroccan_amt = s["ingredients"].get("Chicken", 0)
    amounts[5] = moroccan_amt

    # Leave the others as 0 for now

    # Table header
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Meat Type", 1, 0, 'C', fill=True)
    pdf.cell(col_w, ch, "Amount", 1, 1, 'C', fill=True)
    pdf.set_font("Arial", "", 8)
    for i, meat in enumerate(meat_types):
        pdf.cell(col_w, ch, meat, 1)
        pdf.cell(col_w, ch, str(amounts[i]), 1, 1)

    pdf.ln(8)

    # --- Veg Prep Table ---
    veg_types = [
        "10MM DICED CARROT",
        "10MM DICED POTATO (LEBO)",
        "10MM DICED ZUCCHINI",
        "5MM DICED CABBAGE",
        "5MM DICED CAPSICUM",
        "5MM DICED CARROTS",
        "5MM DICED CELERY",
        "5MM DICED MUSHROOMS",
        "5MM DICED ONION",
        "5MM MONGOLIAN CAPSICUM",
        "5MM MONGOLIAN ONION",
        "5MM SLICED MUSHROOMS",
        "BROCCOLI",
        "CRATED CARROTS",
        "CRATED ZUCCHINI",
        "LEMON POTATO",
        "ROASTED POTATO",
        "THAI POTATOS",
        "POTATO MASH",
        "SWEET POTATO MASH",
        "SPINACH",
        "RED ONION",
        "PARSLEY"
    ]
    veg_amounts = [0] * len(veg_types)  # Fill out calculations as needed

    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Veg Prep", 1, 0, 'C', fill=True)
    pdf.cell(col_w, ch, "Amount", 1, 1, 'C', fill=True)
    pdf.set_font("Arial", "", 8)
    for i, veg in enumerate(veg_types):
        pdf.cell(col_w, ch, veg, 1)
        pdf.cell(col_w, ch, str(veg_amounts[i]), 1, 1)

    # Return y for next section
    return pdf.get_y() + pad
