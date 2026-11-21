
# Company Intelligence Data - 150+ Companies Preloaded

COMPANY_DATA = [
    # --- EXISTING INDIAN COMPANIES (WITH METADATA) ---
    {"id": "hdfc-bank", "name": "FC Bank Limited", "industry": "Banking", "company_type": "Indian", "skills_required": ["Finance", "Banking", "Risk Management", "Accounting"], "career_page": "https://www.hdfcbank.com/personal/about-us/careers"},
    {"id": "icici-bank", "name": "ICICI Bank Limited", "industry": "Banking", "company_type": "Indian", "skills_required": ["Banking", "Finance", "Customer Relationship Management", "SQL"], "career_page": "https://www.icicicareers.com"},
    {"id": "infosys", "name": "Infosys Limited", "industry": "Information Technology", "company_type": "MNC", "skills_required": ["Java", "Python", "Cloud Computing", "Problem Solving"], "fresher_friendly": True, "role_description": "Regular campus & off-campus hiring for software & analyst roles", "offers_internships": True, "career_page": "https://www.infosys.com/careers"},
    {"id": "mahindra-mahindra", "name": "Mahindra & Mahindra Ltd", "industry": "Manufacturing", "company_type": "Indian", "skills_required": ["Mechanical Engineering", "Manufacturing", "Supply Chain", "Automobile"], "career_page": "https://www.mahindra.com/careers"},
    {"id": "axis-bank", "name": "Axis Bank Ltd", "industry": "Banking", "company_type": "Indian", "skills_required": ["Finance", "Banking", "Digital Banking", "Accounting"], "career_page": "https://www.axisbank.com/careers"},
    {"id": "wipro", "name": "Wipro Limited", "industry": "Information Technology", "company_type": "MNC", "skills_required": ["JavaScript", "Cloud", "QA Testing", "Java"], "fresher_friendly": True, "role_description": "Mass hiring for Project Engineers and Analyst roles", "offers_internships": True, "career_page": "https://careers.wipro.com/global-india"},
    {"id": "vedanta", "name": "Vedanta Limited", "industry": "Mining & Metals", "company_type": "Indian", "skills_required": ["Mining", "Operations", "Safety Management", "Supply Chain"], "career_page": "https://www.vedantalimited.com/eng/careers.php"},
    {"id": "irfc", "name": "Indian Railway Finance Corp Ltd", "industry": "Finance", "company_type": "Indian", "skills_required": ["Finance", "Accounting", "Auditing", "Compliance"]},
    {"id": "tata-motors", "name": "Tata Motors Limited", "industry": "Manufacturing", "company_type": "Indian", "skills_required": ["Automobile", "Design Engineering", "Manufacturing", "Operations"], "career_page": "https://www.tatamotors.com/careers/"},
    {"id": "bse", "name": "BSE Ltd", "industry": "Finance", "company_type": "Indian", "skills_required": ["Stock Market", "Trading Systems", "Finance", "Cybersecurity"]},
    {"id": "dr-reddy", "name": "Dr. Reddy's Laboratories Limited", "industry": "Pharmaceuticals", "company_type": "Indian", "skills_required": ["Pharma", "R&D", "Chemistry", "Quality Control"], "career_page": "https://www.drreddys.com/careers/"},
    
    # --- GLOBAL MNCs (NEW) ---
    # Technology & IT
    {"id": "apple", "name": "Apple Inc.", "industry": "Technology & IT", "company_type": "MNC", "skills_required": ["Swift", "C++", "Product Design", "AI/ML"], "about": "Global leader in consumer electronics and software.", "career_page": "https://www.apple.com/careers", "offers_internships": True},
    {"id": "microsoft", "name": "Microsoft Corporation", "industry": "Technology & IT", "company_type": "MNC", "skills_required": ["C#", "Azure", "Python", "Problem Solving"], "about": "Empowers every person and every organization on the planet to achieve more.", "career_page": "https://careers.microsoft.com", "offers_internships": True, "fresher_friendly": True, "role_description": "Software Engineering Intern & Graduate roles"},
    {"id": "alphabet", "name": "Alphabet Inc.", "industry": "Technology & IT", "company_type": "MNC", "skills_required": ["Python", "Go", "Distributed Systems", "Data Structures"], "about": "Google's parent company, focusing on search, cloud, and AI.", "career_page": "https://careers.google.com", "offers_internships": True},
    {"id": "amazon-global", "name": "Amazon.com Inc.", "industry": "Technology & IT", "company_type": "MNC", "skills_required": ["Java", "AWS", "SQL", "Systems Design"], "about": "Earth's most customer-centric company.", "career_page": "https://www.amazon.jobs", "offers_internships": True},
    {"id": "meta", "name": "Meta Platforms Inc.", "industry": "Technology & IT", "company_type": "MNC", "skills_required": ["React", "Python", "Product Growth", "Data Analysis"], "about": "Building the future of social connection.", "career_page": "https://www.metacareers.com", "offers_internships": True},
    {"id": "ibm-global", "name": "IBM", "industry": "Technology & IT", "company_type": "MNC", "skills_required": ["Cloud", "AI", "Blockchain", "Enterprise Software"], "about": "A global technology and innovation company.", "career_page": "https://www.ibm.com/employment", "offers_internships": True},
    {"id": "oracle", "name": "Oracle Corporation", "industry": "Technology & IT", "company_type": "MNC", "skills_required": ["Java", "SQL", "Cloud Infrastructure", "ERP"], "about": "Cloud applications and platform services.", "career_page": "https://www.oracle.com/corporate/careers"},
    {"id": "sap", "name": "SAP SE", "industry": "Technology & IT", "company_type": "MNC", "skills_required": ["ABAP", "Java", "Enterprise Architecture", "Analytics"], "about": "Market leader in enterprise application software.", "career_page": "https://www.sap.com/about/careers.html"},

    # Banking & Financial Services
    {"id": "jpmorgan", "name": "JPMorgan Chase & Co.", "industry": "Banking & Financial Services", "company_type": "MNC", "skills_required": ["Finance", "Investment Banking", "Python", "Risk Analytics"], "about": "A leader in investment banking and financial services.", "career_page": "https://careers.jpmorganchase.com", "offers_internships": True},
    {"id": "goldman-sachs", "name": "Goldman Sachs", "industry": "Banking & Financial Services", "company_type": "MNC", "skills_required": ["Finance", "Quantitative Analysis", "Java", "Economics"], "about": "Global investment banking and management firm.", "career_page": "https://www.goldmansachs.com/careers", "offers_internships": True, "fresher_friendly": True, "role_description": "Analyst & graduate programs for finance & technology"},
    {"id": "hsbc", "name": "HSBC Holdings plc", "industry": "Banking & Financial Services", "company_type": "MNC", "skills_required": ["Banking", "Compliance", "Credit Risk", "Customer Relations"], "about": "One of the world's largest banking and financial health organizations.", "career_page": "https://www.hsbc.com/careers"},
    {"id": "citigroup", "name": "Citigroup Inc.", "industry": "Banking & Financial Services", "company_type": "MNC", "skills_required": ["Banking", "Capital Markets", "Financial Analysis", "Project Management"], "career_page": "https://jobs.citi.com"},
    {"id": "bofa", "name": "Bank of America", "industry": "Banking & Financial Services", "company_type": "MNC", "skills_required": ["Finance", "Technology", "Wealth Management", "Corporate Banking"], "career_page": "https://careers.bankofamerica.com"},
    {"id": "visa", "name": "Visa Inc.", "industry": "Banking & Financial Services", "company_type": "MNC", "skills_required": ["Payments Technology", "Cybersecurity", "Data Science", "API"], "career_page": "https://www.visa.com/careers"},
    {"id": "mastercard", "name": "Mastercard Incorporated", "industry": "Banking & Financial Services", "company_type": "MNC", "skills_required": ["Payments", "Product Management", "Data Analytics", "Security"], "career_page": "https://www.mastercard.com/careers"},

    # Energy & Oil & Gas
    {"id": "aramco", "name": "Saudi Aramco", "industry": "Energy & Oil & Gas", "company_type": "MNC", "skills_required": ["Chemical Engineering", "Petroleum Engineering", "Operations", "Geology"], "career_page": "https://www.aramco.com/en/careers"},
    {"id": "exxonmobil", "name": "ExxonMobil", "industry": "Energy & Oil & Gas", "company_type": "MNC", "skills_required": ["Engineering", "Finance", "Supply Chain", "IT"], "career_page": "https://corporate.exxonmobil.com/careers"},
    {"id": "shell", "name": "Shell plc", "industry": "Energy & Oil & Gas", "company_type": "MNC", "skills_required": ["Energy Management", "Sustainability", "Chemical Engineering", "Finance"], "career_page": "https://www.shell.com/careers"},
    {"id": "chevron", "name": "Chevron Corporation", "industry": "Energy & Oil & Gas", "company_type": "MNC", "skills_required": ["Engineering", "Operations", "Environmental Science", "Finance"], "career_page": "https://www.chevron.com/careers"},
    {"id": "totalenergies", "name": "TotalEnergies", "industry": "Energy & Oil & Gas", "company_type": "MNC", "skills_required": ["Renewable Energy", "Oil & Gas", "Project Management", "Trading"], "career_page": "https://www.totalenergies.com/careers"},
    {"id": "bp", "name": "BP plc", "industry": "Energy & Oil & Gas", "company_type": "MNC", "skills_required": ["Engineering", "Sustainability", "Low Carbon Energy", "Finance"], "career_page": "https://www.bp.com/careers"},

    # Consumer Goods & Retail
    {"id": "pg", "name": "Procter & Gamble", "industry": "Consumer Goods & Retail", "company_type": "MNC", "skills_required": ["Marketing", "Supply Chain", "Finance", "Consumer Research"], "career_page": "https://www.pgcareers.com"},
    {"id": "unilever", "name": "Unilever", "industry": "Consumer Goods & Retail", "company_type": "MNC", "skills_required": ["Sustainability", "Supply Chain", "Marketing", "Finance"], "career_page": "https://www.unilever.com/careers"},
    {"id": "nestle", "name": "Nestlé", "industry": "Consumer Goods & Retail", "company_type": "MNC", "skills_required": ["Nutrition", "Supply Chain", "Marketing", "Food Science"], "career_page": "https://www.nestle.com/jobs"},
    {"id": "cocacola", "name": "Coca-Cola Company", "industry": "Consumer Goods & Retail", "company_type": "MNC", "skills_required": ["Marketing", "Logistics", "Sales", "Finance"], "career_page": "https://www.coca-colacompany.com/careers"},
    {"id": "pepsico", "name": "PepsiCo", "industry": "Consumer Goods & Retail", "company_type": "MNC", "skills_required": ["FMCG", "Operations", "Sales", "Supply Chain"], "career_page": "https://www.pepsicojobs.com"},
    {"id": "walmart", "name": "Walmart Inc.", "industry": "Consumer Goods & Retail", "company_type": "MNC", "skills_required": ["Retail Tech", "Supply Chain", "E-commerce", "Finance"], "career_page": "https://careers.walmart.com"},
    {"id": "costco", "name": "Costco Wholesale", "industry": "Consumer Goods & Retail", "company_type": "MNC", "skills_required": ["Retail Operations", "Logistics", "Customer Service", "Finance"], "career_page": "https://www.costco.com/jobs.html"},

    # Automotive & Manufacturing
    {"id": "tesla", "name": "Tesla Inc.", "industry": "Automotive & Manufacturing", "company_type": "MNC", "skills_required": ["EV Tech", "Battery Systems", "Autonomous Systems", "Manufacturing"], "career_page": "https://www.tesla.com/careers"},
    {"id": "toyota-global", "name": "Toyota Motor Corporation", "industry": "Automotive & Manufacturing", "company_type": "MNC", "skills_required": ["Auto Engineering", "Lean Manufacturing", "Robotics", "Finance"], "career_page": "https://www.toyota-global.com/company/careers"},
    {"id": "volkswagen", "name": "Volkswagen AG", "industry": "Automotive & Manufacturing", "company_type": "MNC", "skills_required": ["Automotive Software", "Engineering", "Production", "Supply Chain"], "career_page": "https://www.volkswagenag.com/en/careers.html"},
    {"id": "bmw", "name": "BMW Group", "industry": "Automotive & Manufacturing", "company_type": "MNC", "skills_required": ["Auto Design", "Logistics", "Mechanical Engineering", "Software Development"], "career_page": "https://www.bmwgroup.jobs"},
    {"id": "mercedes", "name": "Mercedes-Benz Group", "industry": "Automotive & Manufacturing", "company_type": "MNC", "skills_required": ["Luxury Branding", "Engineering", "Digitalization", "Finance"], "career_page": "https://group.mercedes-benz.com/careers"},
    {"id": "gm", "name": "General Motors", "industry": "Automotive & Manufacturing", "company_type": "MNC", "skills_required": ["Electrification", "Software", "Supply Chain", "Finance"], "career_page": "https://search-careers.gm.com"},

    # Healthcare & Pharma
    {"id": "pfizer", "name": "Pfizer Inc.", "industry": "Healthcare & Pharma", "company_type": "MNC", "skills_required": ["Bio-Pharma", "R&D", "Clinical Trials", "Manufacturing"], "career_page": "https://www.pfizer.com/about/careers"},
    {"id": "jj", "name": "Johnson & Johnson", "industry": "Healthcare & Pharma", "company_type": "MNC", "skills_required": ["Medical Devices", "Pharma", "Consumer Health", "R&D"], "career_page": "https://www.careers.jnj.com"},
    {"id": "roche", "name": "Roche Holding AG", "industry": "Healthcare & Pharma", "company_type": "MNC", "skills_required": ["Diagnostics", "Clinical Research", "Bio-Tech", "Finance"], "career_page": "https://www.roche.com/careers"},
    {"id": "novartis", "name": "Novartis", "industry": "Healthcare & Pharma", "company_type": "MNC", "skills_required": ["Pharma Operations", "Data Science", "Compliance", "Sales"], "career_page": "https://www.novartis.com/careers"},
    {"id": "merck", "name": "Merck & Co.", "industry": "Healthcare & Pharma", "company_type": "MNC", "skills_required": ["Vaccines", "Pharma Research", "Operations", "Finance"], "career_page": "https://www.merck.com/careers"},

    # --- TOP MNCs HIRING FRESHERS IN INDIA ---
    {"id": "accenture-india", "name": "Accenture", "industry": "Technology & IT", "company_type": "MNC", "skills_required": ["Cloud", "Analytics", "Project Management", "Consulting"], "fresher_friendly": True, "role_description": "Global IT & consulting firm hiring freshers as Analysts & Associates", "career_page": "https://www.accenture.com/in-en/careers", "offers_internships": True},
    {"id": "ibm-india", "name": "IBM India", "industry": "Technology & IT", "company_type": "MNC", "skills_required": ["IT", "Cloud", "AI", "Business Operations"], "fresher_friendly": True, "role_description": "Fresher roles in IT, Cloud, AI & Business Operations", "career_page": "https://www.ibm.com/in-en/employment", "offers_internships": True},
    {"id": "deloitte-india", "name": "Deloitte", "industry": "Consulting & Finance", "company_type": "MNC", "skills_required": ["Tax", "Audit", "Consulting", "Finance", "Analytics", "Tech"], "fresher_friendly": True, "role_description": "Graduate roles in consulting, finance, analytics & tech", "career_page": "https://www2.deloitte.com/in/en/careers/careers.html", "offers_internships": True},
    {"id": "amazon-india", "name": "Amazon India", "industry": "Technology & IT", "company_type": "MNC", "skills_required": ["Software", "Operations", "Data", "Business"], "fresher_friendly": True, "role_description": "Fresher roles in software, operations, data & business", "career_page": "https://www.amazon.jobs/en/locations/india", "offers_internships": True},
    {"id": "hsbc-india", "name": "HSBC India", "industry": "Banking & Financial Services", "company_type": "MNC", "skills_required": ["Banking", "Finance", "Economics", "Compliance"], "fresher_friendly": True, "role_description": "Early-career banking & finance roles", "career_page": "https://www.hsbc.com/careers/where-we-hire/india"},
    {"id": "nestle-india", "name": "Nestlé India", "industry": "Consumer Goods & Retail", "company_type": "MNC", "skills_required": ["Marketing", "Supply Chain", "Operations", "FMCG"], "fresher_friendly": True, "role_description": "Entry-level roles in marketing, supply chain & operations", "career_page": "https://www.nestle.in/jobs"},
    {"id": "capgemini-india", "name": "Capgemini", "industry": "Technology & IT", "company_type": "MNC", "skills_required": ["Java", "React", "Cloud", "Consulting"], "fresher_friendly": True, "role_description": "Fresher hiring across IT & consulting domains", "career_page": "https://www.capgemini.com/in-en/careers", "offers_internships": True},
]

# Add default interview process and other fields if not present
for company in COMPANY_DATA:
    if "interview_process" not in company:
        company["interview_process"] = [
            {"round": 1, "name": "Aptitude Assessment", "type": "Online", "details": "Logical, verbal, and technical aptitude."},
            {"round": 2, "name": "Technical Interview", "type": "Technical", "details": "Discussion on skills and project work."},
            {"round": 3, "name": "HR Interview", "type": "Behavioral", "details": "Culture fit and salary discussion."}
        ]
    if "logo_text" not in company:
        company["logo_text"] = company["name"][:2].upper()
    if "color" not in company:
        import hashlib
        hash_obj = hashlib.md5(company["name"].encode())
        company["color"] = f"#{hash_obj.hexdigest()[:6]}"
    if "experience" not in company:
        company["experience"] = "Fresher & Experienced"
    if "difficulty" not in company:
        company["difficulty"] = "Medium"
    if "technologies" not in company:
        company["technologies"] = {
            "Core Skills": company["skills_required"],
            "Industry Tools": ["Excel", "Tally"] if company["industry"] in ["Banking", "Finance", "Banking & Financial Services"] else ["Jira", "Slack"]
        }
    if "company_type" not in company:
        company["company_type"] = "Indian"
    if "about" not in company:
        company["about"] = f"{company['name']} is a leading player in the {company['industry']} sector, committed to excellence and innovation."
    if "roles" not in company:
        company["roles"] = ["Software Engineer", "Analyst", "Internship"] if company.get("offers_internships") else ["Software Engineer", "Analyst"]
    if "locations" not in company:
        company["locations"] = ["Mumbai", "Bangalore", "Hyderabad", "Noida", "Pune"]
    if "fresher_friendly" not in company:
        company["fresher_friendly"] = False
    if "offers_internships" not in company:
        company["offers_internships"] = False
