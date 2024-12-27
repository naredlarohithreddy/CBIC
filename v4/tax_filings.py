import pandas as pd
import numpy as np
from faker import Faker
import random
import csv
from datetime import datetime, timedelta, date
from decimal import Decimal

fake = Faker('en_IN')

# Define the taxpayer IDs
taxpayer_df = []
with open('./v4/taxpayer_info.csv', 'r') as file:
    reader = csv.DictReader(file, delimiter='|')
    for row in reader:
        taxpayer_df.append(row)


taxpayer_df = pd.DataFrame(taxpayer_df)
taxpayer_ids = taxpayer_df['Taxpayer ID'].tolist()


# Define the filing statuses

filing_probability=[0.30,0.25,0.30,0.15]

for_filed=random.randint(30,60)
for_submitted=random.randint(20,50)
for_valid=random.randint(20,40)
for_invalid=random.randint(10,30)

total_status_profiles=for_filed+for_submitted+for_valid+for_invalid
status_distribution = [for_filed/total_status_profiles, for_submitted/total_status_profiles, for_valid/total_status_profiles,for_invalid/total_status_profiles]
filing_statuses = ['TO BE FILED', 'SUBMITTED BUT NOT FILED', 'FILED VALID', 'FILED INVALID']


# Define the return types
return_types = ['ITR1', 'ITR2', 'ITR3', 'ITR4', 'ITR5', 'ITR6', 'ITR7']

# Define tax slabs
tax_slabs = {
    'AGRICULTURE': {
        'employees': [(1000000, 5), (10000000, 10), (100000000, 15), (float('inf'), 20)],
        'business': [(1000000, 10), (10000000, 15), (100000000, 20), (float('inf'), 25)],
        'e-commerce operators': [(1000000, 8), (10000000, 12), (100000000, 18), (float('inf'), 22)],
        'suppliers': [(1000000, 6), (10000000, 12), (100000000, 18), (float('inf'), 24)],
    },
      'ANIMAL HUSBANDRY & FORESTRY': {
        'employees': [(1000000, 5), (10000000, 10), (100000000, 15), (float('inf'), 20)],
        'business': [(1000000, 10), (10000000, 15), (100000000, 20), (float('inf'), 25)],
        'e-commerce operators': [(1000000, 8), (10000000, 12), (100000000, 18), (float('inf'), 22)],
        'suppliers': [(1000000, 6), (10000000, 12), (100000000, 18), (float('inf'), 24)],
    },
    'FISH FARMING': {
        'employees': [(1000000, 5), (5000000, 10), (50000000, 15), (float('inf'), 20)],
        'business': [(1000000, 10), (5000000, 15), (50000000, 20), (float('inf'), 25)],
        'e-commerce operators': [(1000000, 8), (5000000, 12), (50000000, 18), (float('inf'), 22)],
        'suppliers': [(1000000, 6), (5000000, 12), (50000000, 18), (float('inf'), 24)],
    },
    'MINING AND QUARRYING': {
        'employees': [(5000000, 10), (50000000, 15), (500000000, 20), (float('inf'), 25)],
        'business': [(5000000, 15), (50000000, 20), (500000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
        'suppliers': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
    },
    'MANUFACTURING': {
        'employees': [(10000000, 10), (100000000, 15), (1000000000, 20), (float('inf'), 25)],
        'business': [(10000000, 15), (100000000, 20), (1000000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
        'suppliers': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
    },
    'ELECTRICITY, GAS AND WATER': {
        'employees': [(10000000, 10), (100000000, 15), (500000000, 20), (float('inf'), 25)],
        'business': [(10000000, 15), (100000000, 20), (500000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(10000000, 12), (100000000, 18), (500000000, 22), (float('inf'), 28)],
        'suppliers': [(10000000, 12), (100000000, 18), (500000000, 22), (float('inf'), 28)],
    },
    'CONSTRUCTION': {
        'employees': [(10000000, 10), (100000000, 15), (1000000000, 20), (float('inf'), 25)],
        'business': [(10000000, 15), (100000000, 20), (1000000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
        'suppliers': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
    },
    'REAL ESTATE AND RENTING SERVICES': {
        'employees': [(10000000, 10), (100000000, 15), (1000000000, 20), (float('inf'), 25)],
        'business': [(10000000, 15), (100000000, 20), (1000000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
        'suppliers': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
    },
    'RENTING OF MACHINERY': {
        'employees': [(5000000, 10), (50000000, 15), (500000000, 20), (float('inf'), 25)],
        'business': [(5000000, 15), (50000000, 20), (500000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
        'suppliers': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
    },
    'WHOLESALE AND RETAIL TRADE': {
        'employees': [(5000000, 10), (50000000, 15), (500000000, 20), (float('inf'), 25)],
        'business': [(5000000, 15), (50000000, 20), (500000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
        'suppliers': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
    },
    'HOTELS, RESTAURANTS AND HOSPITALITY SERVICES': {
        'employees': [(5000000, 10), (50000000, 15), (500000000, 20), (float('inf'), 25)],
        'business': [(5000000, 15), (50000000, 20), (500000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
        'suppliers': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'),28)]
    },
    'TRANSPORT & LOGISTICS SERVICES': {
        'employees': [(5000000, 10), (50000000, 15), (500000000, 20), (float('inf'), 25)],
        'business': [(5000000, 15), (50000000, 20), (500000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
        'suppliers': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
    },
    'POST AND TELECOMMUNICATION SERVICES': {
        'employees': [(10000000, 10), (100000000, 15), (1000000000, 20), (float('inf'), 25)],
        'business': [(10000000, 15), (100000000, 20), (1000000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
        'suppliers': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
    },
    'FINANCIAL INTERMEDIATION SERVICES': {
        'employees': [(10000000, 10), (100000000, 15), (1000000000, 20), (float('inf'), 25)],
        'business': [(10000000, 15), (100000000, 20), (1000000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
        'suppliers': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
    },
    'COMPUTER AND RELATED SERVICES': {
        'employees': [(10000000, 10), (100000000, 15), (1000000000, 20), (float('inf'), 25)],
        'business': [(10000000, 15), (100000000, 20), (1000000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
        'suppliers': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
    },
    'RESEARCH AND DEVELOPMENT': {
        'employees': [(5000000, 10), (50000000, 15), (500000000, 20), (float('inf'), 25)],
        'business': [(5000000, 15), (50000000, 20), (500000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
        'suppliers': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
    },
    'PROFESSIONS': {
        'employees': [(5000000, 10), (50000000, 15), (500000000, 20), (float('inf'), 25)],
        'business': [(5000000, 15), (50000000, 20), (500000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
        'suppliers': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
    },
    'EDUCATION SERVICES': {
        'employees': [(10000000, 10), (100000000, 15), (1000000000, 20), (float('inf'), 25)],
        'business': [(10000000, 15), (100000000, 20), (1000000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
        'suppliers': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
    },
    'HEALTH CARE SERVICES': {
        'employees': [(10000000, 10), (100000000, 15), (1000000000, 20), (float('inf'), 25)],
        'business': [(10000000, 15), (100000000, 20), (1000000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
        'suppliers': [(10000000, 12), (100000000, 18), (1000000000, 22), (float('inf'), 28)],
    },
    'SOCIAL AND COMMUNITY WORK': {
        'employees': [(5000000, 10), (50000000, 15), (500000000, 20), (float('inf'), 25)],
        'business': [(5000000, 15), (50000000, 20), (500000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
        'suppliers': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
    },
    'CULTURE AND SPORT': {
        'employees': [(5000000, 10), (50000000, 15), (500000000, 20), (float('inf'), 25)],
        'business': [(5000000, 15), (50000000, 20), (500000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
        'suppliers': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
    },
    'OTHER SERVICES': {
        'employees': [(5000000, 10), (50000000, 15), (500000000, 20), (float('inf'), 25)],
        'business': [(5000000, 15), (50000000, 20), (500000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
        'suppliers': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
    },
    'EXTRA TERRITORIAL ORGANISATIONS AND BODIES': {
        'employees': [(5000000, 10), (50000000, 15), (500000000, 20), (float('inf'), 25)],
        'business': [(5000000, 15), (50000000, 20), (500000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
        'suppliers': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
    },
    'CO-OPERATIVE SOCIETY ACTIVITIES': {
        'employees': [(5000000, 10), (50000000, 15), (500000000, 20), (float('inf'), 25)],
        'business': [(5000000, 15), (50000000, 20), (500000000, 25), (float('inf'), 30)],
        'e-commerce operators': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
        'suppliers': [(5000000, 12), (50000000, 18), (500000000, 22), (float('inf'), 28)],
    }
}


state_tax_revenue_order = {
    "Maharashtra": 1,
    "Tamil Nadu": 2,
    "Uttar Pradesh": 3,
    "Karnataka": 4,
    "Gujarat": 5,
    "Delhi": 6,
    "Rajasthan": 7,
    "West Bengal": 8,
    "Telangana": 9,
    "Kerala": 10,
    "Bihar": 11,
    "Andhra Pradesh": 12,
    "Madhya Pradesh": 13,
    "Punjab": 14,
    "Haryana": 15,
    "Chattisgarh": 16,
    "Odisha": 17,
    "Jammu & Kashmir": 18,
    "Assam": 19,
    "Uttarakhand": 20,
    "Goa": 21,
    "Himachal Pradesh": 22,
    "Jharkhand": 23,
    "Chandigarh": 24,
    "Puducherry": 25,
    "Sikkim": 26,
    "Nagaland": 27,
    "Meghalaya": 28,
    "Tripura": 29,
    "Manipur": 30,
    "Arunachal Pradesh": 31,
    "Mizoram": 32,
    "Andaman & Nicobar Islands": 33,
    "Lakshadweep": 34,
    "Dadra & Nagar Haveli": 35,
    "Daman & Diu": 36
}


state_tax_revenue = {
    "Maharashtra": 2500000000000,
    "Tamil Nadu": 1750000000000,
    "Karnataka": 1500000000000,
    "Gujarat": 1300000000000,
    "Uttar Pradesh": 1200000000000,
    "West Bengal": 1000000000000,
    "Delhi": 900000000000,
    "Telangana": 850000000000,
    "Rajasthan": 750000000000,
    "Andhra Pradesh": 700000000000,
    "Madhya Pradesh": 650000000000,
    "Haryana": 600000000000,
    "Punjab": 550000000000,
    "Bihar": 500000000000,
    "Odisha": 450000000000,
    "Kerala": 400000000000,
    "Chattisgarh": 350000000000,
    "Jharkhand": 300000000000,
    "Assam": 250000000000,
    "Himachal Pradesh": 200000000000,
    "Uttarakhand": 180000000000,
    "Goa": 100000000000,
    "Tripura": 50000000000,
    "Meghalaya": 40000000000,
    "Nagaland": 35000000000,
    "Manipur": 30000000000,
    "Mizoram": 25000000000,
    "Sikkim": 20000000000,
    "Arunachal Pradesh": 18000000000,
    "Jammu & Kashmir": 15000000000,
    "Daman & Diu": 12000000000,
    "Dadra & Nagar Haveli": 10000000000,
    "Chandigarh": 9000000000
}

industries_by_state_updated = {
    "01": [
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "REAL ESTATE AND RENTING SERVICES",
        "AGRICULTURE",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "ANIMAL HUSBANDRY & FORESTRY",
        "CULTURE AND SPORT",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "WHOLESALE AND RETAIL TRADE",
        "MANUFACTURING",
        "ELECTRICITY, GAS AND WATER",
        "CONSTRUCTION",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "02": [
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "MANUFACTURING",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "ELECTRICITY, GAS AND WATER",
        "TRANSPORT & LOGISTICS SERVICES",
        "RENTING OF MACHINERY",
        "WHOLESALE AND RETAIL TRADE",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "03": [
        "AGRICULTURE",
        "MANUFACTURING",
        "REAL ESTATE AND RENTING SERVICES",
        "WHOLESALE AND RETAIL TRADE",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "ELECTRICITY, GAS AND WATER",
        "ANIMAL HUSBANDRY & FORESTRY",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "04": [
        "REAL ESTATE AND RENTING SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "TRANSPORT & LOGISTICS SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "SOCIAL AND COMMUNITY WORK",
        "CULTURE AND SPORT",
        "AGRICULTURE",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "MANUFACTURING",
        "ELECTRICITY, GAS AND WATER",
        "CONSTRUCTION",
        "RENTING OF MACHINERY",
        "WHOLESALE AND RETAIL TRADE",
        "POST AND TELECOMMUNICATION SERVICES",
        "PROFESSIONS",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "05": [
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "MANUFACTURING",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "ELECTRICITY, GAS AND WATER",
        "TRANSPORT & LOGISTICS SERVICES",
        "RENTING OF MACHINERY",
        "WHOLESALE AND RETAIL TRADE",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "06": [
        "MANUFACTURING",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "WHOLESALE AND RETAIL TRADE",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "ELECTRICITY, GAS AND WATER",
        "ANIMAL HUSBANDRY & FORESTRY",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "07": [
        "REAL ESTATE AND RENTING SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "TRANSPORT & LOGISTICS SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "SOCIAL AND COMMUNITY WORK",
        "CULTURE AND SPORT",
        "AGRICULTURE",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "MANUFACTURING",
        "ELECTRICITY, GAS AND WATER",
        "CONSTRUCTION",
        "RENTING OF MACHINERY",
        "WHOLESALE AND RETAIL TRADE",
        "POST AND TELECOMMUNICATION SERVICES",
        "PROFESSIONS",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "08": [
        "MINING AND QUARRYING",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "MANUFACTURING",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "ELECTRICITY, GAS AND WATER",
        "TRANSPORT & LOGISTICS SERVICES",
        "RENTING OF MACHINERY",
        "WHOLESALE AND RETAIL TRADE",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "09": [
        "AGRICULTURE",
        "MANUFACTURING",
        "REAL ESTATE AND RENTING SERVICES",
        "WHOLESALE AND RETAIL TRADE",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "ELECTRICITY, GAS AND WATER",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "10": [
        "AGRICULTURE",
        "MANUFACTURING",
        "REAL ESTATE AND RENTING SERVICES",
        "WHOLESALE AND RETAIL TRADE",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "ELECTRICITY, GAS AND WATER",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "11": [
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "MANUFACTURING",
        "ELECTRICITY, GAS AND WATER",
        "WHOLESALE AND RETAIL TRADE",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "12": [
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "MANUFACTURING",
        "ELECTRICITY, GAS AND WATER",
        "WHOLESALE AND RETAIL TRADE",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "13": [
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "MANUFACTURING",
        "ELECTRICITY, GAS AND WATER",
        "WHOLESALE AND RETAIL TRADE",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "14": [
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "MANUFACTURING",
        "ELECTRICITY, GAS AND WATER",
        "WHOLESALE AND RETAIL TRADE",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "15": [
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "MANUFACTURING",
        "ELECTRICITY, GAS AND WATER",
        "WHOLESALE AND RETAIL TRADE",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "16": [
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "MANUFACTURING",
        "ELECTRICITY, GAS AND WATER",
        "WHOLESALE AND RETAIL TRADE",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "17": [
        "MINING AND QUARRYING",
        "AGRICULTURE",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "REAL ESTATE AND RENTING SERVICES",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MANUFACTURING",
        "ELECTRICITY, GAS AND WATER",
        "WHOLESALE AND RETAIL TRADE",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "18": [
        "MINING AND QUARRYING",
        "AGRICULTURE",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "REAL ESTATE AND RENTING SERVICES",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MANUFACTURING",
        "ELECTRICITY, GAS AND WATER",
        "WHOLESALE AND RETAIL TRADE",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "19": [
        "MANUFACTURING",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "WHOLESALE AND RETAIL TRADE",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "ELECTRICITY, GAS AND WATER",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "20": [
        "MINING AND QUARRYING",
        "AGRICULTURE",
        "MANUFACTURING",
        "REAL ESTATE AND RENTING SERVICES",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "ELECTRICITY, GAS AND WATER",
        "WHOLESALE AND RETAIL TRADE",
        "TRANSPORT & LOGISTICS SERVICES",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "21": [
        "MINING AND QUARRYING",
        "AGRICULTURE",
        "MANUFACTURING",
        "REAL ESTATE AND RENTING SERVICES",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "ELECTRICITY, GAS AND WATER",
        "WHOLESALE AND RETAIL TRADE",
        "TRANSPORT & LOGISTICS SERVICES",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "22": [
        "MINING AND QUARRYING",
        "AGRICULTURE",
        "MANUFACTURING",
        "REAL ESTATE AND RENTING SERVICES",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "ELECTRICITY, GAS AND WATER",
        "WHOLESALE AND RETAIL TRADE",
        "TRANSPORT & LOGISTICS SERVICES",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "23": [
        "AGRICULTURE",
        "MANUFACTURING",
        "REAL ESTATE AND RENTING SERVICES",
        "WHOLESALE AND RETAIL TRADE",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "ELECTRICITY, GAS AND WATER",
        "TRANSPORT & LOGISTICS SERVICES",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "24": [
        "MANUFACTURING",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "WHOLESALE AND RETAIL TRADE",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "ELECTRICITY, GAS AND WATER",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "25": [
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "MANUFACTURING",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "ELECTRICITY, GAS AND WATER",
        "WHOLESALE AND RETAIL TRADE",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "26": [
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "MANUFACTURING",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "ELECTRICITY, GAS AND WATER",
        "WHOLESALE AND RETAIL TRADE",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "27": [
        "MANUFACTURING",
        "AGRICULTURE",
        "REAL ESTATE AND RENTING SERVICES",
        "WHOLESALE AND RETAIL TRADE",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "EDUCATION SERVICES",
        "HEALTH CARE SERVICES",
        "SOCIAL AND COMMUNITY WORK",
        "CONSTRUCTION",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "ELECTRICITY, GAS AND WATER",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "28": [
        "WHOLESALE AND RETAIL TRADE",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "REAL ESTATE AND RENTING SERVICES",
        "MANUFACTURING",
        "AGRICULTURE",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "HEALTH CARE SERVICES",
        "EDUCATION SERVICES",
        "CONSTRUCTION",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "ELECTRICITY, GAS AND WATER",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "SOCIAL AND COMMUNITY WORK",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "29": [
        "COMPUTER AND RELATED SERVICES",
        "WHOLESALE AND RETAIL TRADE",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "REAL ESTATE AND RENTING SERVICES",
        "MANUFACTURING",
        "AGRICULTURE",
        "HEALTH CARE SERVICES",
        "EDUCATION SERVICES",
        "CONSTRUCTION",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "ELECTRICITY, GAS AND WATER",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "SOCIAL AND COMMUNITY WORK",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "30": [
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "REAL ESTATE AND RENTING SERVICES",
        "MANUFACTURING",
        "AGRICULTURE",
        "HEALTH CARE SERVICES",
        "EDUCATION SERVICES",
        "CONSTRUCTION",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "ELECTRICITY, GAS AND WATER",
        "WHOLESALE AND RETAIL TRADE",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "COMPUTER AND RELATED SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "SOCIAL AND COMMUNITY WORK",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ],
    "31":[
        "Mining and Quarrying",
        "Manufacturing",
        "Electricity, Gas and Water",
        "Agriculture",
        "Construction",
        "Transport & Logistics Services",
        "Wholesale and Retail Trade",
        "Animal Husbandry & Forestry",
        "Real Estate and Renting Services",
        "Hotels, Restaurants and Hospitality Services",
        "Education Services",
        "Health Care Services",
        "Financial Intermediation Services",
        "Social and Community Work",
        "Culture and Sport",
        "Post and Telecommunication Services",
        "Research and Development",
        "Fish Farming",
        "Computer and Related Services",
        "Professions",
        "Renting of Machinery",
        "Other Services",
        "Co-operative Society Activities",
        "Extra Territorial Organisations and Bodies"
    ],
    "32":[
        "Hotels, Restaurants and Hospitality Services",
        "Wholesale and Retail Trade",
        "Health Care Services",
        "Transport & Logistics Services",
        "Financial Intermediation Services",
        "Agriculture",
        "Construction",
        "Real Estate and Renting Services",
        "Education Services",
        "Culture and Sport",
        "Animal Husbandry & Forestry",
        "Post and Telecommunication Services",
        "Fish Farming",
        "Computer and Related Services",
        "Professions",
        "Research and Development",
        "Manufacturing",
        "Electricity, Gas and Water",
        "Social and Community Work",
        "Renting of Machinery",
        "Mining and Quarrying",
        "Other Services",
        "Co-operative Society Activities",
        "Extra Territorial Organisations and Bodies"
    ],
    "33":[
        "Manufacturing",
        "Wholesale and Retail Trade",
        "Financial Intermediation Services",
        "Transport & Logistics Services",
        "Real Estate and Renting Services",
        "Agriculture",
        "Construction",
        "Electricity, Gas and Water",
        "Hotels, Restaurants and Hospitality Services",
        "Education Services",
        "Health Care Services",
        "Computer and Related Services",
        "Animal Husbandry & Forestry",
        "Post and Telecommunication Services",
        "Culture and Sport",
        "Research and Development",
        "Professions",
        "Social and Community Work",
        "Mining and Quarrying",
        "Fish Farming",
        "Renting of Machinery",
        "Other Services",
        "Co-operative Society Activities",
        "Extra Territorial Organisations and Bodies"
    ],
    "36": [
        "COMPUTER AND RELATED SERVICES",
        "WHOLESALE AND RETAIL TRADE",
        "TRANSPORT & LOGISTICS SERVICES",
        "FINANCIAL INTERMEDIATION SERVICES",
        "REAL ESTATE AND RENTING SERVICES",
        "MANUFACTURING",
        "AGRICULTURE",
        "HEALTH CARE SERVICES",
        "EDUCATION SERVICES",
        "CONSTRUCTION",
        "HOTELS, RESTAURANTS AND HOSPITALITY SERVICES",
        "ANIMAL HUSBANDRY & FORESTRY",
        "FISH FARMING",
        "MINING AND QUARRYING",
        "ELECTRICITY, GAS AND WATER",
        "RENTING OF MACHINERY",
        "POST AND TELECOMMUNICATION SERVICES",
        "RESEARCH AND DEVELOPMENT",
        "SOCIAL AND COMMUNITY WORK",
        "PROFESSIONS",
        "CULTURE AND SPORT",
        "OTHER SERVICES",
        "EXTRA TERRITORIAL ORGANISATIONS AND BODIES",
        "CO-OPERATIVE SOCIETY ACTIVITIES"
    ]
}

# Function to generate turnover based on normal distribution
def generate_normal_turnover(mean, std_dev, num_entities):
    turnover_values = np.random.normal(loc=mean, scale=std_dev, size=num_entities)
    turnover_values = np.clip(turnover_values, 0, None)  
    return turnover_values

percentages = [15, 12, 10, 8, 7, 6, 5, 5, 4, 4, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 0.5, 0.5]

tax_offsets = [0.10, 0.05]

def calculate_tax_offset(taxable_income, offset_type):
    return taxable_income * tax_offsets[offset_type]

# Read the taxpayer registration details
registration_df = pd.read_csv('./v4/taxpayer_registration.csv', delimiter='|')

# Helper functions
def get_last_day_of_month(year, month):
    if month == 12:
        return datetime(year + 1, 1, 7)
    else:
        return datetime(year, month + 1, 7)

def get_last_day_of_quarter(year, month):
    if month>=9 and month<=12:
        return datetime(year+1,1,16)
    if month>=1 and month<=3:
        return datetime(year,4,15)
    if month>=4 and month<=5:
        return datetime(year,6,17)
    return datetime(year,9,15)

def get_last_day_of_year(year,gross_turnover):
    if gross_turnover < 30000000:
        return datetime(year,7,31)
    return datetime(year, 11, 15)

# Generate the filing data
filing_data = []
today = datetime.today()

# maharashtra_gross_turnover = {}
sum_1=0
sum_2=0
mini=float('inf')
maxi=-1
punjab_gross={}
p_gross={}

for i in range(0,len(taxpayer_df)):
    taxpayer_info = taxpayer_df.iloc[i]
    registration_info = registration_df.iloc[i]
    
    taxpayer_id = taxpayer_info['Taxpayer ID']
    taxpayer_type = taxpayer_info['Taxpayer Type']
    sector = taxpayer_info['Sector_Industry_Code']
    state_name = taxpayer_info['State Name']
    region_code = taxpayer_info['Region Code']

    # Parse the registration date with multiple formats
    registration_date_str = registration_info['Registration Date']
    try:
        registration_date = datetime.strptime(registration_date_str, '%Y-%m-%d')
    except ValueError:
        try:
            registration_date = datetime.strptime(registration_date_str, '%Y-%m-%d')
        except ValueError:
            print(f"Unrecognized date format: {registration_date_str}")
            continue
    
    filing_frequency = registration_info['Filing Frequency']

    #grossturnover
    industries = industries_by_state_updated[region_code]
    count=0
    for j in industries:
        if j.upper()==sector:
            break
        count+=1
    
    per_industry_turnover = state_tax_revenue[state_name] * (percentages[count] / 100)
            
    # Scale the value
    scaled_value = per_industry_turnover / 10000
    gross_turnover= round(scaled_value*(random.randint(30,50)/100),2)

    if state_name=='Punjab':
        if sector in punjab_gross:
            punjab_gross[sector]+=gross_turnover
        else:
            punjab_gross[sector]=gross_turnover

    # Determine taxable value based on tax slabs
    slabs = tax_slabs.get(sector, {}).get(taxpayer_type, [])
    taxable_value = 0
    for slab in slabs:
        gross_turnover = np.float64(gross_turnover) 
        slab = [slab[0], np.float64(slab[1])] 

        if gross_turnover <= slab[0]:
            if gross_turnover<mini:
                mini=gross_turnover
            if gross_turnover>maxi:
                maxi=gross_turnover
            taxable_value = np.round((gross_turnover * slab[1]) / 100, 2)
            break
    
    # Determine total tax paid
    total_tax_paid = 0
    check=0

    if np.random.rand() < 0.5:
        check=1
        total_tax_paid = round(taxable_value * np.random.uniform(0.5, 0.9),2)
    elif np.random.rand() < 0.7:
        check=2
        total_tax_paid = round(taxable_value,2)
    else:
        check=3
        total_tax_paid = round(taxable_value * np.random.uniform(1.1, 1.5),2)
    tax_offset=0
    # Determine due date based on filing frequency
    current_year = registration_date.year
    current_month = registration_date.month

    if filing_frequency == 'MONTHLY':
        month=current_month+1
        gross_turnover/=12
        taxable_value/=12
        total_tax_paid/=12
        taxable_value=round(taxable_value,2)
        gross_turnover=round(gross_turnover,2)
        total_tax_paid=round(total_tax_paid,2)
        while current_year!=(today.year+1):
            while month<13:
                due_date = get_last_day_of_month(current_year, month)
                filing_date=due_date

                if np.random.rand() < 0.25:
                    filing_date = due_date + timedelta(days=np.random.randint(1, 29))
                else :
                    filing_date = due_date - timedelta(days=np.random.randint(1, 29))

                if filing_date > today:
                    filing_date = today
                
                penalties_paid = 0
                late_fees_paid = 0

                due_date = due_date.date()
                
                diffy=filing_date.year-due_date.year
                diffm=filing_date.month-due_date.month
                diffd=filing_date.day-due_date.day

                if diffy>0 or diffm>0 or diffd>0:
                    penalty_days = diffd+diffm*30+diffy*364
                    if penalty_days > 0 and taxable_value > 0:
                        penalties_paid = round((penalty_days // 30) * 0.01 * taxable_value, 2)
                        if taxable_value<50000000:
                            late_fees_paid=900
                        else:
                            late_fees_paid=5000
                    else:
                        penalties_paid=0 
                        late_fees_paid=0


                # Determine filing period
                if filing_date.month in [1, 2, 3]:
                    filing_period = f"FY{filing_date.year}Q3"
                elif filing_date.month in [4, 5]:
                    filing_period = f"FY{filing_date.year}Q4"
                elif filing_date.month in [6,7, 8]:
                    filing_period = f"FY{filing_date.year}Q1"
                else:
                    filing_period = f"FY{filing_date.year}Q2"

                if check==3:
                    offset_type=np.random.randint(0,2)
                    tax_offset = round(calculate_tax_offset(taxable_value, offset_type),2)
                
                # Generate filing data
                filing_data.append({
                    'Filing ID': i + 1,
                    'Taxpayer ID': taxpayer_id,
                    'Filing Period': filing_period,
                    'Filing Date': filing_date.strftime('%Y-%m-%d'),
                    'Filing Status': np.random.choice(filing_statuses,p=filing_probability),
                    'Return Type': np.random.choice(return_types),
                    'Gross Turnover': gross_turnover,
                    'Tax Revenue': taxable_value,
                    'Total Tax Paid': total_tax_paid,
                    'Tax Offset Claimed': tax_offset,
                    'Penalties incurred': penalties_paid,
                    'Late Fees incurred': late_fees_paid,
                    'Due Date': due_date
                })

                if state_name=='Punjab':
                    if sector in p_gross:
                        p_gross[sector]+=gross_turnover
                    else:
                        p_gross[sector]=gross_turnover

                month+=1
            month=1
            current_year+=1
            
    elif filing_frequency == 'QUARTERLY':
        gross_turnover/=4
        taxable_value/=4
        total_tax_paid/=4
        gross_turnover=round(gross_turnover,2)
        taxable_value=round(taxable_value,2)
        total_tax_paid=round(total_tax_paid,2)
        month=current_month+1
        while current_year!=today.year+1:
            while month<13:
                due_date = get_last_day_of_quarter(current_year, month)
                filing_date=due_date

                #chnaged this ratio
                if np.random.rand() < 0.25:
                    filing_date = due_date + timedelta(days=np.random.randint(1, 365))
                else:
                    if date.month==1:
                        filing_date = due_date - timedelta(days=np.random.randint(1, 135))
                    if date.month==4:
                        filing_date = due_date - timedelta(days=np.random.randint(1, 104))
                    if date.month==6:
                        filing_date = due_date - timedelta(days=np.random.randint(1, 76))
                    if date.month==9:
                        filing_date = due_date - timedelta(days=np.random.randint(1, 105))

                if filing_date > today:
                    filing_date = today
                
                penalties_paid = 0
                late_fees_paid = 0

                due_date = due_date.date()
                
                diffy=filing_date.year-due_date.year
                diffm=filing_date.month-due_date.month
                diffd=filing_date.day-due_date.day

                if diffy>0 or diffm>0 or diffd>0:
                    penalty_days = diffd+diffm*30+diffy*364
                    if penalty_days > 0 and taxable_value > 0:
                        penalties_paid = round((penalty_days // 30) * 0.01 * taxable_value, 2)
                        if taxable_value<50000000:
                            late_fees_paid=900
                        else:
                            late_fees_paid=5000
                    else:
                        penalties_paid=0 
                        late_fees_paid=0


                # Determine filing period
                if filing_date.month in [1, 2, 3]:
                    filing_period = f"FY{filing_date.year}Q3"
                elif filing_date.month in [4, 5]:
                    filing_period = f"FY{filing_date.year}Q4"
                elif filing_date.month in [6,7, 8]:
                    filing_period = f"FY{filing_date.year}Q1"
                else:
                    filing_period = f"FY{filing_date.year}Q2"

                if check==3:
                    offset_type=np.random.randint(0,2)
                    tax_offset = round(calculate_tax_offset(taxable_value, offset_type),2)

                # Generate filing data
                filing_data.append({
                    'Filing ID': i + 1,
                    'Taxpayer ID': taxpayer_id,
                    'Filing Period': filing_period,
                    'Filing Date': filing_date.strftime('%Y-%m-%d'),
                    'Filing Status': np.random.choice(filing_statuses,p=filing_probability),
                    'Return Type': np.random.choice(return_types),
                    'Gross Turnover': gross_turnover,
                    'Tax Revenue': taxable_value,
                    'Total Tax Paid': total_tax_paid,
                    'Tax Offset Claimed': tax_offset,
                    'Penalties incurred': penalties_paid,
                    'Late Fees incurred': late_fees_paid,
                    'Due Date': due_date
                })
                if state_name=='Punjab':
                    if sector in p_gross:
                        p_gross[sector]+=gross_turnover
                    else:
                        p_gross[sector]=gross_turnover
                if month>=9 and month<=12:
                    month=random.choices([1,2,3],weights=[0.33,0.33,0.34],k=1)[0]
                    break
                if month>=1 and month<=3:
                    month=random.choices([4,5],weights=[0.5,0.5],k=1)[0]
                if month>=4 and month<=5:
                    month=random.choices([6,7,8],weights=[0.33,0.33,0.34],k=1)[0]
                else:
                    month=random.choices([9,10,11,12],weights=[0.25,0.25,0.25,0.25],k=1)[0]
            current_year+=1
    elif filing_frequency == 'ANNUALLY':
        month=current_month+1
        while current_year!=(today.year+1):
            due_date = get_last_day_of_year(current_year,gross_turnover)
            filing_date=due_date
            if np.random.rand() < 0.25:
                filing_date = due_date + timedelta(days=np.random.randint(1, 365))
            else:
                filing_date = due_date - timedelta(days=np.random.randint(1, 365))
                    
            if filing_date > today:
                filing_date = today
            
            penalties_paid = 0
            late_fees_paid = 0

            due_date = due_date.date()
            
            diffy=filing_date.year-due_date.year
            diffm=filing_date.month-due_date.month
            diffd=filing_date.day-due_date.day

            if diffy>0 or diffm>0 or diffd>0:
                penalty_days = diffd+diffm*30+diffy*364
                if penalty_days > 0 and taxable_value > 0:
                    penalties_paid = round((penalty_days // 30) * 0.01 * taxable_value, 2)
                    if taxable_value<50000000:
                        late_fees_paid=900
                    else:
                        late_fees_paid=5000
                else:
                    penalties_paid=0 
                    late_fees_paid=0


            # Determine filing period
            if filing_date.month in [1, 2, 3]:
                filing_period = f"FY{filing_date.year}Q3"
            elif filing_date.month in [4, 5]:
                filing_period = f"FY{filing_date.year}Q4"
            elif filing_date.month in [6,7, 8]:
                filing_period = f"FY{filing_date.year}Q1"
            else:
                filing_period = f"FY{filing_date.year}Q2"

            if check==3:
                offset_type=np.random.randint(0,2)
                tax_offset = round(calculate_tax_offset(taxable_value, offset_type),2)

            # Generate filing data
            filing_data.append({
                'Filing ID': i + 1,
                'Taxpayer ID': taxpayer_id,
                'Filing Period': filing_period,
                'Filing Date': filing_date.strftime('%Y-%m-%d'),
                'Filing Status': np.random.choice(filing_statuses,p=filing_probability),
                'Return Type': np.random.choice(return_types),
                'Gross Turnover': round(gross_turnover,2),
                'Tax Revenue': taxable_value,
                'Total Tax Paid': total_tax_paid,
                'Tax Offset Claimed': tax_offset,
                'Penalties incurred': penalties_paid,
                'Late Fees incurred': late_fees_paid,
                'Due Date': due_date
            })
            if state_name=='Punjab':
                if sector in p_gross:
                    p_gross[sector]+=gross_turnover
                else:
                    p_gross[sector]=gross_turnover
            current_year+=1
    
df = pd.DataFrame(filing_data)
# Print the DataFrame
df.to_csv('./v4/tax_filing.csv', index=False, sep='|')
print("Data generation complete. CSV file created.")