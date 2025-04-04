from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import requests
import json
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    # Add Pakistan legal context to the query
    search_query = f"{query} Pakistan law legal"
    
    try:
        # Get legal information based on the query
        legal_info = get_legal_information(query.lower())
        
        if legal_info:
            return jsonify({'results': legal_info})
        else:
            # Fallback to generic legal resources
            fallback_info = get_fallback_info()
            return jsonify({'results': fallback_info})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_legal_information(query):
    """Return specific legal information based on the query"""
    legal_database = {
        "robbery": {
            "title": "How to Report a Robbery in Pakistan",
            "content": """
To report a robbery in Pakistan, follow these steps:

1. **Immediate Action**: Contact the nearest police station or call emergency helpline 15.

2. **Visit the Police Station**: Go to the nearest police station to file a First Information Report (FIR).

3. **Filing the FIR**: 
   - Provide your personal details
   - Describe the incident with time, date and location
   - Mention any witnesses
   - List all stolen items with approximate values
   - Any identification details of perpetrators if available

4. **Documentation Required**:
   - Your CNIC (National ID card)
   - Any evidence related to the crime (photographs, receipts of stolen items)

5. **Follow Up**: 
   - Obtain a copy of the FIR
   - Note the name and contact of the investigating officer
   - Request regular updates on your case

6. **Legal Assistance**:
   - Consider consulting a lawyer if the case is complicated
   - Legal aid services are available if you cannot afford legal representation

In Pakistan, robbery (dacoity) falls under Section 392 of the Pakistan Penal Code. The maximum punishment can be up to 10 years imprisonment and fine.

Important: File your report as soon as possible. Delays may complicate the investigation process.
            """,
            "sources": ["Pakistan Penal Code, Section 392-394", "Criminal Procedure Code of Pakistan"]
        },
        "divorce": {
            "title": "Divorce Process in Pakistan",
            "content": """
Divorce procedures in Pakistan vary based on religious laws. Here's the process:

For Muslims:

1. **Talaq (by husband)**:
   - Pronouncement of talaq (verbal or written)
   - Filing the divorce deed with the Union Council
   - 90-day waiting period (iddat)
   - Union Council issues divorce certificate after reconciliation attempts fail

2. **Khula (by wife)**:
   - File suit in Family Court
   - May require returning the dower (mahr)
   - Court proceedings typically take 4-8 months
   - Decree becomes final after judicial decision

3. **Required Documents**:
   - Marriage certificate (Nikah Nama)
   - CNICs of both parties
   - Recent photographs
   - Details of dower amount (paid/unpaid)

For non-Muslims:
- Christians: Under the Divorce Act 1869
- Hindus: Under the Hindu Marriage Act 2017
- Other minorities: Specific personal laws apply

**Child Custody**: The welfare of children is paramount. Generally, mother receives custody of young children, while father may get custody of older male children.

**Financial Settlements**: The wife can claim:
- Unpaid dower (mahr)
- Maintenance during iddat period
- Child maintenance

Seek legal counsel to understand your specific rights under Pakistani law.
            """,
            "sources": ["Muslim Family Laws Ordinance 1961", "Family Courts Act 1964"]
        },
        "inheritance": {
            "title": "Islamic Inheritance Law in Pakistan",
            "content": """
In Pakistan, inheritance is primarily governed by Islamic law (Sharia) for Muslims, while non-Muslims follow their respective personal laws.

**For Muslims**:

1. **Fixed Shares (Fard)**:
   - Spouse: Husband receives 1/4 if children exist, 1/2 if no children
   - Wife receives 1/8 if children exist, 1/4 if no children
   - Daughter receives 1/2 if single daughter, multiple daughters share 2/3
   - Father always receives 1/6
   - Mother receives 1/6 if children exist, 1/3 if no children

2. **Residuary Shares (Asaba)**:
   - Male relatives receive the remaining estate
   - Son receives twice the share of daughter
   - If no heirs with fixed shares, estate goes to closest male agnate

3. **Legal Procedure**:
   - Obtain death certificate
   - Prepare list of legal heirs
   - Submit succession certificate application to court
   - Court verifies heirs and issues certificate
   - Transfer of property/assets per certificate

**For Non-Muslims**:
- Christians: Indian Succession Act 1925
- Hindus: Hindu Succession laws
- Others: Respective personal laws

**Important Considerations**:
- No more than 1/3 of property can be willed outside the Islamic shares
- Property division often requires court intervention
- Succession certificate necessary for bank accounts, investments

Consult a lawyer specializing in inheritance law for specific guidance.
            """,
            "sources": ["Al Quran", "Muslim Personal Law (Shariat) Application Act 1962"]
        }
    }
    
    # Search for relevant topics in the query
    results = []
    
    for topic, info in legal_database.items():
        if topic in query or any(word in query for word in topic.split()):
            results.append({
                'title': info['title'],
                'snippet': info['content'].strip(),
                'link': '#',
                'displayLink': info['sources'][0] if info['sources'] else ''
            })
    
    # Check for more general legal topics
    general_terms = {
        "police report": "robbery",
        "theft report": "robbery",
        "crime report": "robbery",
        "marriage dissolution": "divorce",
        "talaq": "divorce",
        "khula": "divorce",
        "child custody": "divorce",
        "property division": "inheritance",
        "will": "inheritance",
        "estate": "inheritance"
    }
    
    for term, topic in general_terms.items():
        if term in query and not results:
            info = legal_database[topic]
            results.append({
                'title': info['title'],
                'snippet': info['content'].strip(),
                'link': '#',
                'displayLink': info['sources'][0] if info['sources'] else ''
            })
    
    return results

def get_fallback_info():
    """Provide general legal information when specific query isn't recognized"""
    return [{
        'title': 'Legal Process for Common Issues in Pakistan',
        'snippet': """
Here are some important legal processes in Pakistan:

1. **Criminal Complaints**:
   - File FIR at local police station
   - Emergency police number: 15
   - Criminal proceedings follow Code of Criminal Procedure
   - Right to legal representation guaranteed by Constitution

2. **Civil Disputes**:
   - File suit in Civil Court of appropriate jurisdiction
   - Limitation periods apply (generally 3 years for most cases)
   - Alternative Dispute Resolution mechanisms available

3. **Family Matters**:
   - Family Courts handle marriage, divorce, custody, maintenance
   - Governed by personal laws based on religion
   - Legal aid available through Pakistan Bar Council

4. **Property Issues**:
   - Land disputes handled by Revenue Courts
   - Property registration through local land registry
   - Documents like sale deed, mutation record required

5. **Consumer Rights**:
   - Consumer Protection Councils in each province
   - File complaints for defective products/services

For specific legal advice, please consult a qualified lawyer in Pakistan. The Pakistan Bar Council can provide referrals to licensed attorneys.
""",
        'link': '#',
        'displayLink': 'Legal Information'
    }]

if __name__ == '__main__':
    app.run(debug=True)