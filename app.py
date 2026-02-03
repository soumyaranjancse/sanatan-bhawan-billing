import streamlit as st
import csv
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# =========================
# APP CONFIG
# =========================
st.set_page_config(page_title="Sanatan Bhawan Billing", layout="centered")

st.title("🏠 Sanatan Bhawan – Electricity Billing System")
st.write("Automatic electricity calculation and bill generation")

# =========================
# BASIC INPUTS
# =========================
month = st.text_input("Billing Month", "August 2026")
rate_per_unit = st.number_input("Electricity Rate per Unit (Rs.)", value=7.0)

# =========================
# ROOM RENT (FINAL LOGIC)
# =========================
room_rent = {
    101: 5500, 102: 5000, 103: 5500, 104: 5000, 105: 9000,
    201: 5500, 202: 5500, 203: 7500, 204: 8000, 205: 7500,
    301: 5500, 302: 5500, 303: 7500, 304: 8000, 305: 8000,
    401: 5000, 402: 5000
}

# =========================
# LAST MONTH METER READINGS (YOUR DATA)
# =========================
previous_units = {
    101: 2030, 102: 1065, 103: 2499, 104: 754, 105: 2901,
    201: 1274, 202: 5536, 203: 5555, 204: 3340, 205: 1150,
    301: 4556, 302: 2877, 303: 2615, 304: 7735, 305: 4031,
    401: 4196, 402: 2928
}

# =========================
# ELECTRICITY INPUT UI
# =========================
st.subheader("🔌 Enter Current Month Ending Units")

current_units = {}

for room in room_rent:
    current_units[room] = st.number_input(
        f"Room {room} – Ending Unit",
        min_value=previous_units[room],
        value=previous_units[room] + 10,
        step=1
    )

# =========================
# CALCULATION & GENERATION
# =========================
if st.button("⚡ Calculate & Generate Bills"):
    os.makedirs("bills", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    csv_file = f"data/Sanatan_Bhawan_Electricity_{month}.csv"

    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Month",
            "Room",
            "Start Unit",
            "End Unit",
            "Units Used",
            "Rate per Unit",
            "Electricity Amount (Rs.)"
        ])

        st.subheader("📊 Electricity Summary")

        for room in room_rent:
            units_used = current_units[room] - previous_units[room]
            amount = units_used * rate_per_unit

            writer.writerow([
                month,
                room,
                previous_units[room],
                current_units[room],
                units_used,
                rate_per_unit,
                amount
            ])

            st.write(
                f"Room {room} → Units Used: {units_used}, Amount: Rs. {amount}"
            )

            # =========================
            # PDF GENERATION (B/W)
            # =========================
            pdf_file = f"bills/Bill_Room_{room}_{month}.pdf"
            c = canvas.Canvas(pdf_file, pagesize=A4)
            width, height = A4

            left_x = 70
            right_x = width - 70

            c.setFont("Helvetica-Bold", 22)
            c.drawCentredString(width / 2, height - 110, "SANATAN BHAWAN")
            c.line(left_x, height - 150, right_x, height - 150)

            y = height - 190
            c.setFont("Helvetica", 12)
            c.drawString(left_x, y, f"Room Number : {room}")
            c.drawRightString(right_x, y, f"Month : {month}")

            y -= 30
            c.drawString(left_x, y, "Electricity Charges")
            c.drawRightString(right_x, y, f"Rs. {amount}")

            y -= 40
            c.setFont("Helvetica-Oblique", 10)
            c.drawCentredString(
                width / 2, y,
                "This is a system generated bill. No signature required."
            )

            c.showPage()
            c.save()

    st.success("✅ CSV and PDF bills generated successfully!")
    st.info("📂 Check the 'data' and 'bills' folders")
