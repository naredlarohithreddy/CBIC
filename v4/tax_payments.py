import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Load the tax filing data
tax_filing_df = pd.read_csv('./v4/tax_filing.csv', sep='|')

# Load the taxpayer data
taxpayer_df = pd.read_csv('./v4/taxpayer_info.csv', sep='|')

# Define the payment types
payment_types = [
    'Down Payments', 'Security Deposits', 'Advance Payments',
    'Installment Payments', 'Progress Payments', 'Prepayments'
]

# Define the payment modes
payment_modes = [
    'Cheque Payment', 'RTGS', 'IMPS', 'Online Payment',
    'TAN (Tax Deduction and Collection Number) Payment',
    'E-Payment', 'Cash Payment', 'NEFT'
]

# Define the payment statuses
payment_statuses = ['cancelled', 'failed', 'completed']

# Define the probabilities for payment status

# Generate the payment data
payment_data = []
today_date = datetime.now()



for index, row in tax_filing_df.iterrows():
    payment_id = f"{random.randint(1000, 9999):04}R{random.choice(['C', 'T', 'I'])}{datetime.now().strftime('%Y%m')}{random.randint(100000, 999999):06}"
    taxpayer_id = row['Taxpayer ID']
    taxpayer_type = taxpayer_df.loc[taxpayer_df['Taxpayer ID'] == taxpayer_id, 'Taxpayer Type'].values[0]
    filing_date = datetime.strptime(row['Filing Date'], '%Y-%m-%d')

    max_days_from_filing = max((today_date - filing_date).days, 1)
    payment_date = filing_date + timedelta(days=np.random.randint(0, max_days_from_filing))
    
    payment_type = random.choice(payment_types)
    tax_amount = row['Total Tax Paid']
    tax_offset = row['Tax Offset Claimed']
    penalty_amount = row['Penalties incurred']
    interest_amount = row['Late Fees incurred']
    tax_after_offset=round(tax_amount-tax_offset,2)
    total_payment_amount = round(tax_amount + penalty_amount + interest_amount-tax_offset,2)
    
    # Determine CGST, SGST, IGST, and UTGST based on taxpayer type and probabilities
    if taxpayer_type == 'employees':
        cgst = round(total_payment_amount,2)
        sgst = 0
        igst = 0
        utgst = 0
    elif taxpayer_type == 'business' or taxpayer_type == 'e-commerce operators':
        prob = np.random.rand()
        if prob < 0.7:
            cgst = round(total_payment_amount * 0.5,2)
            sgst = round(total_payment_amount * 0.5,2)
            igst = 0
            utgst = 0
        elif prob < 0.85:
            cgst = 0
            sgst = 0
            igst = round(total_payment_amount,2)
            utgst = 0
        else:
            cgst = round(total_payment_amount * 0.5,2)
            sgst = 0
            igst = 0
            utgst = round(total_payment_amount * 0.5,2)
    else:
        cgst = round(total_payment_amount * 0.5,2)
        sgst = round(total_payment_amount * 0.5,2)
        igst = 0
        utgst = 0
    
    for_cancelled=random.randint(10,30)
    for_failed=random.randint(10,30)
    for_completed=random.randint(40,80)

    total_status_profiles=for_cancelled+for_failed+for_completed
    payment_status_probabilities = [for_cancelled/total_status_profiles, for_failed/total_status_profiles, for_completed/total_status_profiles]

    payment_mode = random.choice(payment_modes)
    payment_status = np.random.choice(payment_statuses, p=payment_status_probabilities)
    
    payment_data.append({
        'Payment ID': payment_id,
        'Taxpayer ID': taxpayer_id,
        'Payment Date': payment_date.strftime('%Y-%m-%d'),
        'Payment Type': payment_type,
        'Amount to be paid': tax_after_offset,
        'CGST': cgst,
        'SGST': sgst,
        'IGST': igst,
        'UTGST': utgst,
        'Penalty incurred': penalty_amount,
        'Interest incurred': interest_amount,
        'Total tax paid': total_payment_amount,
        'Payment Mode': payment_mode,
        'Payment Status': payment_status
    })

# Create a pandas DataFrame from the payment data
payment_df = pd.DataFrame(payment_data)

# Store the payment DataFrame in a CSV file
payment_df = payment_df.replace({r'\n': ' ', r'\r': ' '}, regex=True)
payment_df.to_csv('./v4/tax_payment.csv', index=False, sep='|')

print("Payment data generation complete. CSV file created.")
