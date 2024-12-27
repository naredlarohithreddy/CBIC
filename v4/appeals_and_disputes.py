import random
import string
from datetime import datetime, timedelta
from faker import Faker
import csv
import pandas as pd

fake = Faker('en_IN')

# Define dispute types
dispute_types = [
    'Assessment Dispute', 'Demand Dispute', 'Refund Dispute', 'Transfer Pricing Dispute', 
    'Double Taxation Avoidance Agreement (DTAA) Dispute', 'GST Dispute', 'Service Tax Dispute', 
    'Customs Dispute', 'Wealth Tax Dispute', 'Appeals and Revisions'
]

industry_dispute_mapping = {
    'AGRICULTURE': [
        'Assessment Dispute', 
        'Demand Dispute', 
        'Refund Dispute', 
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute', 
        'Service Tax Dispute',
        'Customs Dispute', 
        'Appeals and Revisions'
    ],
    'ANIMAL HUSBANDRY & FORESTRY': [
        'Assessment Dispute', 
        'Demand Dispute', 
        'Refund Dispute', 
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute', 
        'Service Tax Dispute',
        'Customs Dispute', 
        'Appeals and Revisions'
    ],
    'FISH FARMING': [
        'Assessment Dispute', 
        'Demand Dispute', 
        'Refund Dispute', 
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute', 
        'Service Tax Dispute',
        'Customs Dispute', 
        'Appeals and Revisions'
    ],
    'MINING AND QUARRYING': [
        'Assessment Dispute', 
        'Demand Dispute', 
        'Refund Dispute', 
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute', 
        'Service Tax Dispute',
        'Customs Dispute', 
        'Appeals and Revisions'
    ],
    'MANUFACTURING': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Transfer Pricing Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Customs Dispute',
        'Appeals and Revisions'
    ],
    'ELECTRICITY, GAS AND WATER': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'CONSTRUCTION': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'REAL ESTATE AND RENTING SERVICES': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Wealth Tax Dispute',
        'Appeals and Revisions'
    ],
    'RENTING OF MACHINERY': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'WHOLESALE AND RETAIL TRADE': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Customs Dispute',
        'Appeals and Revisions'
    ],
    'HOTELS, RESTAURANTS AND HOSPITALITY SERVICES': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'TRANSPORT & LOGISTICS SERVICES': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Customs Dispute',
        'Appeals and Revisions'
    ],
    'POST AND TELECOMMUNICATION SERVICES': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'FINANCIAL INTERMEDIATION SERVICES': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Transfer Pricing Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'COMPUTER AND RELATED SERVICES': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Transfer Pricing Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'RESEARCH AND DEVELOPMENT': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Transfer Pricing Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'PROFESSIONS': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'EDUCATION SERVICES': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'HEALTH CARE SERVICES': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'SOCIAL AND COMMUNITY WORK': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'CULTURE AND SPORT': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'OTHER SERVICES': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Transfer Pricing Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'EXTRA TERRITORIAL ORGANISATIONS AND BODIES': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ],
    'CO-OPERATIVE SOCIETY ACTIVITIES': [
        'Assessment Dispute',
        'Demand Dispute',
        'Refund Dispute',
        'Double Taxation Avoidance Agreement (DTAA) Dispute',
        'GST Dispute',
        'Service Tax Dispute',
        'Appeals and Revisions'
    ]
}

dispute_statuses = ['open', 'closed', 'in review']

resolution_outcomes = ['in favour', 'against']

# Helper functions
def generate_dispute_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Read taxpayer data
taxpayer_data = []
taxpayer_data=pd.read_csv('./v4/tax_filing.csv',sep='|')
taxpayer_info=pd.read_csv('./v4/taxpayer_info.csv',sep='|')



# Generate appeals and disputes data
with open('./v4/appeals_and_disputes.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerow([
        "Dispute_id", "Taxpayer_id", "Dispute_type", "filing_date", "resolution_date", 
        "dispute_status", "Resolution_outcome"
    ])

    merged_df = pd.merge(taxpayer_info, taxpayer_data, on="Taxpayer ID", how="left")
    unique_taxpayer_df = merged_df.groupby("Taxpayer ID").head(1).reset_index(drop=True)

    for _, taxpayer in unique_taxpayer_df.iterrows():
        if pd.isna(taxpayer['Filing ID']): 
            continue
        else:
            taxpayer_id = taxpayer["Taxpayer ID"]
            industry = taxpayer['Sector_Industry_Code'].upper()
            dispute_id = generate_dispute_id()
            dispute_type = random.choice(industry_dispute_mapping[industry])
            filing_date_str = taxpayer['Filing Date']
            
            # Convert the filing_date string to a datetime object
            filing_date = datetime.strptime(filing_date_str, '%Y-%m-%d')
            
            # Determine the resolution_date
            resolution_date = filing_date + timedelta(days=random.randint(30, 365))
            
            today=datetime.today()

            diffy=resolution_date.year-today.year
            diffm=resolution_date.month-today.month
            diffd=resolution_date.day-today.day

            resolution_date_str = resolution_date.strftime('%Y-%m-%d') if resolution_date else None

            if diffy>0 or diffm>0 or diffd>0:
                dispute_status = random.choice(['closed', 'in review'])
                resolution_outcome = random.choices(resolution_outcomes,weights=[0.4,0.6])[0] if dispute_status == 'closed' else None
            else:
                dispute_status=random.choices(['open', 'in review'],weights=[0.3,0.7])[0]
                resolution_outcome=None

            writer.writerow([
                dispute_id, taxpayer_id, dispute_type, filing_date_str, resolution_date_str, 
                dispute_status, resolution_outcome
            ])

print("Appeals and disputes data generation complete. CSV file created.")