'''
This file contains example JSON data for the OCR API.
- invoice
- receipt
- other (TODO)
'''


invoice_example = '''
{
     "title": "領収書/請求書",
     "recipient": "OOXX株式会社",
     "issue_date": "OO年OO月OO日",
     "description": "飲食代",
     "issuer": "XXOO株式会社",
     "post_code": "123-4567",
     "address": "東京都千代田区駿河台2-2",
     "tel": "987-6543-210",
     "registration_number": "T9010901044466", # optonal
     "before_tax_10_percentage": 60000, # optonal
     "tax_10_percentage": 6000, # optonal
     "before_tax_8_percentage": 10000, # optonal
     "tax_8_percentage": 800, # optonal
     "amount_before_tax": 70000, # optonal
     "total_amount": 76800,
     "items": [],
}
'''

