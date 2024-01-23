
from amocrm.v2 import tokens, Lead, Contact, Company
from badshop_django.logger import logger as logger

def create_amo_contact(email):
    contact = Contact.objects.create({"custom_fields_values": [
            {
                "field_id": 437643,
                "values": [
                    {
                        "value": email,
                        "enum_id": 238079
                    },

                ]
            }
        ],})
    return contact
    

def get_amo_contact(email):
    try:
        contact = Contact.objects.get(query=email)
    except:
        contact = None
    return contact


def create_amo_lead_with_contact(price, contact):
    lead = Lead.objects.create(price=100)
    lead.contacts.append(contact)


def create_new_lead_and_contact(price, email):
    contact = get_amo_contact(email)
    if contact is None:
        create_amo_contact(email)
    
    lead = create_amo_lead_with_contact(
        price, contact
        )
