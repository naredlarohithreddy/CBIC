import random
import string
from datetime import datetime, timedelta
from faker import Faker
import csv
import pandas as pd

fake = Faker('en_IN')

# Define constants
refund_statuses = ['Issues', 'partially adjusted', 'fully adjusted', 'Failed']
adjustment_reasons = ['Carry-forward of losses', 'Tax Deducted at Source', 'Advance Tax', 'Exemptions and deductions', 'Residential status', 'Ind AS 12 and IAS 12', 'Import duties']

# Helper functions
def generate_refund_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))

def generate_payment_reference_number():
    ifsc = ''.join(random.choices(string.ascii_uppercase, k=4))
    transaction_type = random.choice(['R', 'N', 'I'])  # RTGS, NEFT, IMPS
    date_part = fake.date_this_decade().strftime('%Y%m')
    sequence_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(6, 10)))
    return f"{ifsc}{transaction_type}{date_part}{sequence_number}"

def calculate_refund_claim_date(filing_date, payment_date):
    three_years_from_filing = filing_date + timedelta(days=3*365)
    two_years_from_payment = payment_date + timedelta(days=2*365)
    return min(three_years_from_filing, two_years_from_payment)

# Read tax payments data
tax_payments_df = pd.read_csv('./v4/tax_payment.csv', sep='|')
# Read tax filing data
tax_filing_df = pd.read_csv('./v4/tax_filing.csv', sep='|')

# Generate refund and adjustments data
with open('./v4/refund_and_adjustments.csv', 'w', newline='') as file:
    file.truncate(0)
    writer = csv.writer(file, delimiter='|')
    writer.writerow([
        "refund_id", "Taxpayer_id", "refund_claim_date", "refund_amount", "refund_status", 
        "adjusted_amount", "adjustment_reason", "payment_reference_number"
    ])
    
    for index, row in tax_filing_df.iterrows():
        tax_offset = row['Tax Revenue']-row['Tax Offset Claimed']-row['Total Tax Paid']

        
        # Only process entries with negative tax offset
        if tax_offset < 0:
            taxpayer_id = row['Taxpayer ID']
            filing_date = datetime.strptime(row['Filing Date'], '%Y-%m-%d')
            
            # Find payment data for the taxpayer
            payment_data = tax_payments_df[tax_payments_df["Taxpayer ID"] == taxpayer_id]
            
            if payment_data.empty:
                print(f"No payment data found for Taxpayer ID: {taxpayer_id}")  # Debug statement
                continue
            
            payment_date = datetime.strptime(payment_data.iloc[0]["Payment Date"], '%Y-%m-%d')
            
            refund_id = generate_refund_id()
            refund_claim_date = calculate_refund_claim_date(filing_date, payment_date)
            refund_amount = round(abs(tax_offset),2)

            for_issues=random.randint(10,30)
            for_partially=random.randint(30,70)
            for_fully=random.randint(30,70)
            for_failed=random.randint(20,30)

            total_status_profiles=for_issues+for_failed+for_partially+for_fully+for_failed
            refund_statuses_probabilities = [for_issues/total_status_profiles, for_partially/total_status_profiles, for_fully/total_status_profiles, for_failed/total_status_profiles]

            refund_status = random.choices(refund_statuses, weights=refund_statuses_probabilities)[0]
            adjusted_amount = round(random.uniform(0, 0.5 * refund_amount), 2)
            adjustment_reason = random.choice(adjustment_reasons)
            payment_reference_number = generate_payment_reference_number()
            
            writer.writerow([
                refund_id, taxpayer_id, refund_claim_date.strftime('%Y-%m-%d'), refund_amount, refund_status, 
                adjusted_amount, adjustment_reason, payment_reference_number
            ])

print("Refund and adjustments data generation complete. CSV file created.")
