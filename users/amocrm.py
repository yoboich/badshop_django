
from badshop_django.logger import logger
try:
    from amocrm.v2 import tokens, Lead, Contact, Company
except Exception as e:
    logger.debug(f'{e}')
    

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
    logger.debug(f'lead created = {lead}')
    lead.contacts.append(contact)
    logger.debug(f'lead.contacts = {lead.contacts}')


def create_new_lead_and_contact(price, email):
    logger.debug(f'creating_new_lead')
    contact = get_amo_contact(email)
    logger.debug(f'get_contact = {contact}')
    if contact is None:
        create_amo_contact(email)
        logger.debug(f'created contact = {contact}')
    
    lead = create_amo_lead_with_contact(
        price, contact
        )
    