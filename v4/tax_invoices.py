import random
import string
from faker import Faker
import csv
from datetime import datetime, timedelta
import numpy as np

fake = Faker('en_IN')

# Define constants
invoice_types = [
    "Tax Invoice", "Bill of Supply", "Receipt Voucher", "Refund Voucher",
    "Payment Voucher", "Credit Note", "Debit Note", "Delivery Challan"
]

generated_ids = set()

def generate_invoice_id():
    date_part = datetime.now().strftime('%d%m%Y')
    unique_part=''
    while True:
        unique_part = ''.join(random.choices(string.digits, k=5))
        if unique_part not in generated_ids:
            generated_ids.add(unique_part)
            break
    return f"{date_part}{unique_part}"

def generate_hsn_code(turnover):
    if turnover < 15000000:
        return ''.join(random.choices(string.digits, k=2))
    elif 15000000 <= turnover <= 50000000:
        return ''.join(random.choices(string.digits, k=4))
    else:
        return ''.join(random.choices(string.digits, k=6))

def generate_gstin_number(state_code, pan_card_number):
    first_two_digits = state_code
    next_ten_digits = pan_card_number
    thirteenth_digit = str(random.randint(1, 9)) # Checksum digit, simplified here
    fourteenth_digit = 'Z'
    last_digit = str(random.randint(0, 9))
    gstin_number = first_two_digits + next_ten_digits + thirteenth_digit + fourteenth_digit + last_digit
    return gstin_number

def generate_pan_card_number(taxpayer_type, last_name):
    first_three_chars = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
    fourth_char = ''
    if taxpayer_type == 'employees':
        fourth_char = 'P'
    elif taxpayer_type == 'business':
        fourth_char = 'C'
    elif taxpayer_type == 'e-commerce operators':
        fourth_char = 'F'
    else:
        fourth_char = 'H'
    fifth_char = last_name[0].upper()
    next_four_chars = ''.join(random.choices('0123456789', k=4))
    last_char = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    pan_card_number = first_three_chars + fourth_char + fifth_char + next_four_chars + last_char
    return pan_card_number

tax_gst_percentage = [0.10, 0.05, 0.18]


def taxation(taxable_income):
    percentage=np.random.randint(0,3)
    return taxable_income * tax_gst_percentage[percentage]



with open('./v4/new_tax_invoices.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerow([
        "invoice_id", "payment_id", "invoice_date", "invoice_amount", "invoice_tax",
        "invoice_type", "hsn_code", "counterparty_gstin", "reverse_charge", "place_of_supply"
    ])
    
    for _ in range(100):  # Generate 100 invoices as an example
        invoice_id = generate_invoice_id()
        invoice_date = fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
        invoice_amount = round(random.uniform(1000, 10000000), 2)  # Random invoice amount between 1000 and 100000
        tax_amount=round(taxation(invoice_amount),2)
        invoice_type = random.choice(invoice_types)
        
        # Generate random state code and PAN card number for GSTIN
        state_code = ''.join(random.choices(string.digits, k=2))
        pan_card_number = generate_pan_card_number('business', fake.last_name())
        counterparty_gstin = generate_gstin_number(state_code, pan_card_number)
        
        reverse_charge = random.choice(['Yes', 'No'])
        place_of_supply = fake.state()
        hsn_code = generate_hsn_code(invoice_amount)
        
        writer.writerow([
            invoice_id, 'PAY' + ''.join(random.choices(string.digits, k=10)), invoice_date, round(invoice_amount,2), round(tax_amount,2),
            invoice_type, hsn_code, counterparty_gstin, reverse_charge, place_of_supply
        ])

print("Invoice data generation complete. CSV file created.")