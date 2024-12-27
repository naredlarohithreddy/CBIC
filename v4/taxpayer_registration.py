import pandas as pd
import numpy as np
from faker import Faker
import random
import uuid
import csv

fake = Faker('en_IN')

# Define the region codes and their corresponding names
region_codes = {
    "01": "Jammu & Kashmir",
    "02": "Himachal Pradesh",
    "03": "Punjab",
    "04": "Chandigarh",
    "05": "Uttarakhand",
    "06": "Haryana",
    "07": "Delhi",
    "08": "Rajasthan",
    "09": "Uttar Pradesh",
    "10": "Bihar",
    "11": "Sikkim",
    "12": "Arunachal Pradesh",
    "13": "Nagaland",
    "14": "Manipur",
    "15": "Mizoram",
    "16": "Tripura",
    "17": "Meghalaya",
    "18": "Assam",
    "19": "West Bengal",
    "20": "Jharkhand",
    "21": "Odisha",
    "22": "Chhattisgarh",
    "23": "Madhya Pradesh",
    "24": "Gujarat",
    "25": "Daman & Diu",
    "26": "Dadra & Nagar Haveli",
    "27": "Maharashtra",
    "28": "Andhra Pradesh",
    "29": "Karnataka",
    "30": "Goa",
    "36": "Telangana"
}

# Define the taxpayer types
taxpayer_types = ['employees','business','e-commerce operators','suppliers']

# Define the registration types
registration_types = [
    "regular gst (GSTIN)", "composition scheme registration", "casual taxable person registration",
    "non-resident taxable person registration", "input service distributor(isd) registration", 
    "tds(tax deducted at source)", "e-commerce operator registration", "urd composition scheme"
]

filing_frequencies = ['MONTHLY', 'QUARTERLY','ANNUALLY']

# Define the registration statuses
for_active=random.randint(30,60)
for_inactive=random.randint(20,50)
for_suspended=random.randint(20,40)

total_status_profiles=for_active+for_inactive+for_suspended
status_distribution = [for_active/total_status_profiles, for_inactive/total_status_profiles, for_suspended/total_status_profiles]
status_choices = ['active', 'inactive', 'suspended']



def generate_registration_date(year):
    mean_date = pd.to_datetime(f'{year}-07-01')  # Mean date as December 2023
    std_dev_months = 1  # Standard deviation as 2 months
    std_dev_days = std_dev_months * 30  # Convert months to days
    start_date = pd.to_datetime(f'{year}-01-01')
    end_date = pd.to_datetime(f'{year}-12-31')
    dates = pd.date_range(start_date, end_date)
    dates_normal = np.random.normal(loc=(mean_date - start_date).days, scale=std_dev_days, size=len(dates))
    dates_normal = np.clip(dates_normal, 0, (end_date - start_date).days).astype(int)
    random_date = start_date + pd.to_timedelta(np.random.choice(dates_normal, 1)[0], unit='D')
    return random_date.date()

# Function to generate a unique PAN card number
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
    pan_card_number = first_three_chars + fourth_char + fifth_char + next_four_chars + random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return pan_card_number

# Function to generate a unique GSTIN number
def generate_gstin_number(state_code, pan_card_number):
    first_two_digits = str(state_code)
    next_ten_digits = str(pan_card_number)
    thirteenth_digit = str(random.randint(0, 9))
    fourteenth_digit = 'Z'
    last_digit = str(random.randint(0, 9))
    gstin_number = first_two_digits + next_ten_digits + thirteenth_digit + fourteenth_digit + last_digit
    return gstin_number

# Function to generate a unique CIN number
def generate_cin_number():
    return 'L' + ''.join(random.choices('0123456789', k=5)) + 'MH' + ''.join(random.choices('0123456789', k=4)) + 'PLC' + ''.join(random.choices('0123456789', k=6))

# Create a pandas DataFrame for taxpayer registration
taxpayer_registration_df = pd.DataFrame(columns=['Taxpayer ID', 'PAN Card Number', 'GSTIN Number', 'Registration Date', 'CIN Number', 'Registration Type', 'Filing Frequency', 'Registration Status'])

# Read the taxpayer info from the CSV file
taxpayer_df = pd.read_csv('./v4/taxpayer_info.csv',sep='|')


# Generate taxpayer registration data
for index, row in taxpayer_df.iterrows():
    taxpayer_id = row['Taxpayer ID']
    taxpayer_type = row['Taxpayer Type']
    last_name = row['Taxpayer Name'].split()[-1]
    state_code = row['Region Code']
    pan_card_number = generate_pan_card_number(taxpayer_type, last_name)
    gstin_number = ''
    cin_number = ''
    if taxpayer_type in ['business', 'e-commerce operators']:
        gstin_number = generate_gstin_number(state_code, pan_card_number)
        cin_number = generate_cin_number()
    years=['2017','2018','2019','2020','2021','2022','2023','2024']
    registration_date = generate_registration_date(random.choice(years))
    registration_type = random.choice(registration_types)
    registration_status = np.random.choice(status_choices, p=status_distribution)

    # Probability mapping for filing frequencies based on employee type
    filing_probabilities = {
        'employees': [[10,30],[20,40],[40,60]],  # [Monthly, Quarterly, Annually]
        'business': [[40,80],[30,50],[10,30]],
        'e-commerce operators': [[40,70],[20,40],[10,30]],
        'suppliers': [[30,60],[20,40],[10,30]]
    }
    
    probabilities = filing_probabilities[taxpayer_type]
    
    for_month=random.randint(probabilities[0][0],probabilities[0][1])
    for_quarter=random.randint(probabilities[1][0],probabilities[1][1])
    for_annual=random.randint(probabilities[2][0],probabilities[2][1])

    total_frequencies=for_month+for_quarter+for_annual
    frequency_distribution = [for_month/total_frequencies, for_quarter/total_frequencies, for_annual/total_frequencies]

    filing_frequency=  random.choices(filing_frequencies, frequency_distribution)[0]

    taxpayer_registration_df = taxpayer_registration_df._append({
        'Taxpayer ID': taxpayer_id,
        'PAN Card Number': pan_card_number,
        'GSTIN Number': gstin_number,
        'Registration Date': registration_date,
        'CIN Number': cin_number,
        'Registration Type': registration_type,
        'Filing Frequency': filing_frequency,
        'Registration Status': registration_status
    }, ignore_index=True)

# Store the DataFrame in a CSV file
taxpayer_registration_df.to_csv('./v4/taxpayer_registration.csv', index=False, sep='|')

print("Data generation complete. CSV file created.")









# industry_to_registration_mapping = {
#     'AGRICULTURE': {
#         'employees': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'business': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'e-commerce operators': [
#             "e-commerce operator registration",
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "input service distributor(isd) registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#         ],
#         'suppliers': [
#             "regular gst (GSTIN)",
#             "suppliers",
#             "composition scheme registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ]
#     },
#     'ANIMAL HUSBANDRY & FORESTRY': {
#         'employees': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'business': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'e-commerce operators': [
#             "e-commerce operator registration",
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "input service distributor(isd) registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#         ],
#         'suppliers': [
#             "regular gst (GSTIN)",
#             "suppliers",
#             "composition scheme registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ]
#     },
#     'FISH FARMING': {
#         'employees': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'business': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'e-commerce operators': [
#             "e-commerce operator registration",
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "input service distributor(isd) registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#         ],
#         'suppliers': [
#             "regular gst (GSTIN)",
#             "suppliers",
#             "composition scheme registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ]
#     },
#     'MINING AND QUARRYING': {
#         'employees': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'business': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'e-commerce operators': [
#             "e-commerce operator registration",
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "input service distributor(isd) registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#         ],
#         'suppliers': [
#             "regular gst (GSTIN)",
#             "suppliers",
#             "composition scheme registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ]
#     },
#     'MANUFACTURING': {
#         'employees': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'business': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'e-commerce operators': [
#             "e-commerce operator registration",
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "input service distributor(isd) registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#         ],
#         'suppliers': [
#             "regular gst (GSTIN)",
#             "suppliers",
#             "composition scheme registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ]
#     },
#     'ELECTRICITY, GAS AND WATER': {
#         'employees': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'business': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'e-commerce operators': [
#             "e-commerce operator registration",
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "input service distributor(isd) registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#         ],
#         'suppliers': [
#             "regular gst (GSTIN)",
#             "suppliers",
#             "composition scheme registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ]
#     },
#     'CONSTRUCTION': {
#         'employees': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'business': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'e-commerce operators': [
#             "e-commerce operator registration",
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "input service distributor(isd) registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#         ],
#         'suppliers': [
#             "regular gst (GSTIN)",
#             "suppliers",
#             "composition scheme registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ]
#     },
#     'REAL ESTATE AND RENTING SERVICES': {
#         'employees': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'business': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'e-commerce operators': [
#             "e-commerce operator registration",
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "input service distributor(isd) registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#         ],
#         'suppliers': [
#             "regular gst (GSTIN)",
#             "suppliers",
#             "composition scheme registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ]
#     },
#     'RENTING OF MACHINERY': {
#         'employees': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'business': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'e-commerce operators': [
#             "e-commerce operator registration",
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "input service distributor(isd) registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#         ],
#         'suppliers': [
#             "regular gst (GSTIN)",
#             "suppliers",
#             "composition scheme registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ]
#     },
#     'WHOLESALE AND RETAIL TRADE': {
#         'employees': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'business': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'e-commerce operators': [
#             "e-commerce operator registration",
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "input service distributor(isd) registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#         ],
#         'suppliers': [
#             "regular gst (GSTIN)",
#             "suppliers",
#             "composition scheme registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ]
#     },
#     'HOTELS, RESTAURANTS AND HOSPITALITY SERVICES': {
#         'employees': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'business': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'e-commerce operators': [
#             "e-commerce operator registration",
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "input service distributor(isd) registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#         ],
#         'suppliers': [
#             "regular gst (GSTIN)",
#             "suppliers",
#             "composition scheme registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ]
#     },
#     'TRANSPORT & LOGISTICS SERVICES': {
#         'employees': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'business': [
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ],
#         'e-commerce operators': [
#             "e-commerce operator registration",
#             "regular gst (GSTIN)",
#             "composition scheme registration",
#             "suppliers",
#             "input service distributor(isd) registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#         ],
#         'suppliers': [
#             "regular gst (GSTIN)",
#             "suppliers",
#             "composition scheme registration",
#             "casual taxable person registration",
#             "non-resident taxable person registration",
#             "input service distributor(isd) registration",
#             "tds(tax deducted at source)",
#         ]
#     }
# }