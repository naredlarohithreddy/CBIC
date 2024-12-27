import pandas as pd
import numpy as np
from faker import Faker
import random
import uuid

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
    "22": "Chattisgarh",
    "23": "Madhya Pradesh",
    "24": "Gujarat",
    "25": "Daman & Diu",
    "26": "Dadra & Nagar Haveli",
    "27": "Maharashtra",
    "28": "Andhra Pradesh",
    "29": "Karnataka",
    "30": "Goa",
    "32": "Kerala",
    "33": "Tamil Nadu",
    "36": "Telangana"
}

# Define the sector/industry codes

sector_codes = [
    'AGRICULTURE', 
    'ANIMAL HUSBANDRY & FORESTRY',
    'FISH FARMING',
    'MINING AND QUARRYING',
    'MANUFACTURING',
    'ELECTRICITY, GAS AND WATER',
    'CONSTRUCTION',
    'REAL ESTATE AND RENTING SERVICES',
    'RENTING OF MACHINERY',
    'WHOLESALE AND RETAIL TRADE',
    'HOTELS, RESTAURANTS AND HOSPITALITY SERVICES',
    'TRANSPORT & LOGISTICS SERVICES',
    'POST AND TELECOMMUNICATION SERVICES',
    'FINANCIAL INTERMEDIATION SERVICES',
    'COMPUTER AND RELATED SERVICES',
    'RESEARCH AND DEVELOPMENT',
    'PROFESSIONS',
    'EDUCATION SERVICES',
    'HEALTH CARE SERVICES',
    'SOCIAL AND COMMUNITY WORK',
    'CULTURE AND SPORT',
    'OTHER SERVICES',
    'EXTRA TERRITORIAL ORGANISATIONS AND BODIES',
    'CO-OPERATIVE SOCIETY ACTIVITIES'
]
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

# Define the email address domains
email_domains = ['@gmail.com', '@yahoo.com', '@hotmail.com']

# Function to generate a unique taxpayer ID
def generate_taxpayer_id(region_code):
    return region_code + str(uuid.uuid4().int)[:7]

# Function to generate a registration date centered around May
def generate_registration_date():
    years = [2022, 2023, 2024]
    year = random.choice(years)
    start_date = pd.to_datetime(f'{year}-01-01')
    end_date = pd.to_datetime(f'{year}-12-31')
    dates = pd.date_range(start_date, end_date)
    mean_date = pd.to_datetime(f'{year}-05-15')
    std_dev = 30  # Standard deviation in days
    dates_normal = np.random.normal(loc=(mean_date - start_date).days, scale=std_dev, size=len(dates))
    dates_normal = np.clip(dates_normal, 0, (end_date - start_date).days).astype(int)
    random_date = start_date + pd.to_timedelta(np.random.choice(dates_normal, 1)[0], unit='D')
    return random_date.date()
#deviation may be small 

# Function to generate a phone number in the Indian format
def generate_phone_number():
    prefix = random.choice(['7', '8', '9'])
    return prefix + ''.join(random.choices('0123456789', k=9))



states = list(industries_by_state_updated.keys())
num_states = len(states)



def generate_data_for_state(region_code,state, industries):

    if state=="Maharashtra" or state=="Tamil Nadu" or state=="Uttar Pradesh":
        num_rows = 5000
        data = []
        # Distribution percentages
        for_active=random.randint(30,60)
        for_inactive=random.randint(20,50)
        for_suspended=random.randint(20,40)

        total_status_profiles=for_active+for_inactive+for_suspended
        status_distribution = [for_active/total_status_profiles, for_inactive/total_status_profiles, for_suspended/total_status_profiles]
        status_choices = ['active', 'inactive', 'suspended']

        for_employees=random.randint(40,75)
        for_business=random.randint(30,60)
        for_e_commerce=random.randint(20,40)
        for_suppliers=random.randint(30,50)
        total_taxpayer_choices=for_employees+for_business+for_e_commerce+for_suppliers

        taxpayer_distribution=[for_employees/total_taxpayer_choices,for_business/total_taxpayer_choices,for_e_commerce/total_taxpayer_choices,for_suppliers/total_taxpayer_choices]
        taxpayer_choices = ['employees', 'business', 'e-commerce operators', 'suppliers']


        for industry in industries:
            total_rows=int(num_rows*(random.randint(60,100)/100))
            industries_per_state = 24
            total_rows_industry = int(total_rows / 24)
            # number_of_rows_per_industry=int(total_rows_industry*((random.randint(60,140))/100))
            status_list = random.choices(status_choices, status_distribution, k=total_rows_industry)
            taxpayer_list = random.choices(taxpayer_choices, taxpayer_distribution, k=total_rows_industry)
            status_counter = 0
            taxpayer_counter = 0
            for _ in range(total_rows_industry):
                taxpayer_name = fake.name()
                contact_number = generate_phone_number()
                email_address = f"{taxpayer_name.lower().replace(' ', '')}{random.choice(email_domains)}"
                taxpayer_id = generate_taxpayer_id(region_code)
                business_address = f"{fake.name()}, {fake.company()}, {fake.building_number()}, {fake.street_address()}, {fake.city()}, {state}, {fake.postcode()}, India"
                data.append({
                    'Taxpayer ID': taxpayer_id,
                    'Taxpayer Name': taxpayer_name,
                    'Taxpayer Type': taxpayer_list[taxpayer_counter],
                    'Status': status_list[status_counter],
                    'Sector_Industry_Code': industry.upper(),
                    'Region Code': region_code,
                    'State Name': state,
                    'Address': business_address,
                    'Contact Number': contact_number,
                    'Email Address': email_address
                })
                status_counter += 1
                taxpayer_counter += 1   
        
        return data
    else:
       data = []
       num_rows = 300
       # Distribution percentages
       for_active=random.randint(30,60)
       for_inactive=random.randint(20,50)
       for_suspended=random.randint(20,40)
   
       total_status_profiles=for_active+for_inactive+for_suspended
       status_distribution = [for_active/total_status_profiles, for_inactive/total_status_profiles, for_suspended/total_status_profiles]
       status_choices = ['active', 'inactive', 'suspended']
   
       for_employees=random.randint(40,75)
       for_business=random.randint(30,60)
       for_e_commerce=random.randint(20,40)
       for_suppliers=random.randint(30,50)
       total_taxpayer_choices=for_employees+for_business+for_e_commerce+for_suppliers
   
       taxpayer_distribution=[for_employees/total_taxpayer_choices,for_business/total_taxpayer_choices,for_e_commerce/total_taxpayer_choices,for_suppliers/total_taxpayer_choices]
       taxpayer_choices = ['employees', 'business', 'e-commerce operators', 'suppliers']
   
   
       for industry in industries:
           total_rows=int(num_rows*(random.randint(60,100)/100))
           industries_per_state = 24
           total_rows_industry = int(total_rows / 24)
        #    number_of_rows_per_industry=int(total_rows_industry*((random.randint(60,140))/100))
           status_list = random.choices(status_choices, status_distribution, k=total_rows_industry)
           taxpayer_list = random.choices(taxpayer_choices, taxpayer_distribution, k=total_rows_industry)
           status_counter = 0
           taxpayer_counter = 0
           for _ in range(total_rows_industry):
               taxpayer_name = fake.name()
               contact_number = generate_phone_number()
               email_address = f"{taxpayer_name.lower().replace(' ', '')}{random.choice(email_domains)}"
               taxpayer_id = generate_taxpayer_id(region_code)
               business_address = f"{fake.name()}, {fake.company()}, {fake.building_number()}, {fake.street_address()}, {fake.city()}, {state}, {fake.postcode()}, India"
               data.append({
                   'Taxpayer ID': taxpayer_id,
                   'Taxpayer Name': taxpayer_name,
                   'Taxpayer Type': taxpayer_list[taxpayer_counter],
                   'Status': status_list[status_counter],
                   'Sector_Industry_Code': industry.upper(),
                   'Region Code': region_code,
                   'State Name': state,
                   'Address': business_address,
                   'Contact Number': contact_number,
                   'Email Address': email_address
               })
               status_counter += 1
               taxpayer_counter += 1   
       
       return data

data = []


for state, industries in industries_by_state_updated.items():
    data.extend(generate_data_for_state(state,region_codes[state], industries))

# Create a DataFrame and save to a CSV file
df = pd.DataFrame(data)
df = df.replace({r'\n': ' ', r'\r': ' '}, regex=True)
df.to_csv('./v4/taxpayer_info.csv', index=False, sep='|')

print("Data generation complete. Saved to 'taxpayer_info.csv'.")