from fpdf import FPDF
from datetime import datetime
import random
from connection import get_db_connection
import getters

# Setting header/footer PDF config
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(205, 178, 138)  # Primary by root.css
        self.cell(0, 10, 'Monthly Report', 0, 1, 'C', fill=True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Function to generate monthly report PDF
def generate_monthly_report(user_id, email):
    cnx = get_db_connection()
    success, msg, transactions = getters.get_transactions(cnx, user_id)
    if not success:
        return None
    
    cnx = get_db_connection()
    success_w, msg_w, wishlist = getters.get_wishlist(cnx, user_id)
    
    # Filter transactions on this month
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    monthly_trans = [t for t in transactions if t['transaction_date'].month == current_month and t['transaction_date'].year == current_year]
    
    # Calculate totals
    total_gains = sum(t['amount'] for t in monthly_trans if t['type'] == 'gain')
    total_expenses = sum(t['amount'] for t in monthly_trans if t['type'] == 'expense')
    balance = total_gains - total_expenses
    
    # Expenses per category (Amounts sum)
    exp_cat = {}
    for t in monthly_trans:
        if t['type'] == 'expense':
            cat = t['category']
            exp_cat[cat] = exp_cat.get(cat, 0) + t['amount']
    
    # Percentages (Just for category expense)
    perc = {}
    if total_expenses > 0:
        perc = {cat: (amt / total_expenses * 100) for cat, amt in exp_cat.items()}
    
    # Insights (Variables with random)
    tips = [
        "Consider tracking your daily expenses to identify savings opportunities.",
        "Great balance this month! Keep up the good work.",
        "Try setting a budget for your top categories to avoid overspending."
    ]
    if perc:
        max_cat = max(perc, key=perc.get)
        insight = f"You spent {perc[max_cat]:.2f}% on {max_cat}, which is your highest expense. Consider alternatives to reduce it."
        tips.append(insight)
    random_insight = random.choice(tips)
    
    # Create PDF
    pdf = PDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(122, 100, 72)  # Fifth color of root.css
    pdf.cell(0, 10, f"Monthly report of {email}", 0, 1, 'C')
    pdf.ln(10)
    
    # Summary
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(212, 221, 177)  # Third cor
    pdf.cell(0, 10, "Summary Highlights:", 0, 1, fill=True)
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(54, 180, 40)  #Green gains
    pdf.cell(0, 10, f"Gains: R$ {total_gains:.2f}", 0, 1)
    pdf.set_text_color(240, 46, 46)  # Red expenses
    pdf.cell(0, 10, f"Expenses: R$ {total_expenses:.2f}", 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Balance: R$ {balance:.2f}", 0, 1)
    pdf.ln(10)
    
    # Insights
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(205, 178, 138)
    pdf.cell(0, 10, "Insights:", 0, 1, fill=True)
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, random_insight)
    pdf.ln(10)
    
    # Transactions (Table with all DB columns)
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(212, 221, 177)
    pdf.cell(0, 10, "Transactions:", 0, 1, fill=True)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_draw_color(181, 181, 181)  # Border gray
    pdf.cell(25, 10, "Date", 1)
    pdf.cell(30, 10, "Category", 1)
    pdf.cell(25, 10, "Amount", 1)
    pdf.cell(20, 10, "Type", 1)
    pdf.cell(20, 10, "Fixed Cost", 1)
    pdf.cell(40, 10, "Description", 1)
    pdf.cell(30, 10, "Has Receipt", 1)
    pdf.ln()
    
    pdf.set_font('Arial', '', 10)
    for t in monthly_trans:
        pdf.cell(25, 10, t['transaction_date'].strftime('%d/%m/%Y'), 1)
        pdf.cell(30, 10, t['category'].capitalize(), 1)
        pdf.cell(25, 10, f"R$ {t['amount']:.2f}", 1)
        pdf.cell(20, 10, t['type'].capitalize(), 1)
        pdf.cell(20, 10, t['fixed_cost'].capitalize() if not t['fixed_cost'] == "N/A" else 'Not a cost', 1)
        description = t['description']
        limit = 20
        result_desc = description[:limit].capitalize() + "..." if len(description) > limit else description 
        pdf.cell(40, 10, result_desc if description else 'No description', 1)
        pdf.cell(30, 10, t['has_receipt'].capitalize(), 1)
        pdf.ln()
        if pdf.get_y() > 250:  # Add page if necessary
            pdf.add_page()
    
    # Percentages
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(240, 128, 128)  # Light red for expenses
    pdf.cell(0, 10, "Expenses by Percentage:", 0, 1, fill=True)
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    if perc:
        for cat, p in sorted(perc.items(), key=lambda x: x[1], reverse=True):
            pdf.cell(0, 10, f"{cat.capitalize()}: {p:.2f}%", 0, 1)
    else:
        pdf.cell(0, 10, "No expenses this month.", 0, 1)
    pdf.ln(10)
    
    # Wish List
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(205, 178, 138)
    pdf.cell(0, 10, "Wish List:", 0, 1, fill=True)
    pdf.set_font('Arial', '', 12)
    if wishlist:
        for w in wishlist:
            pdf.cell(0, 10, f"- {w['wish_name']} (Done: {w['its_done']})", 0, 1)
    else:
        pdf.cell(0, 10, "No wishes added yet.", 0, 1)
    
    return pdf.output(dest='S').encode('latin-1')