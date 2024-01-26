
from badshop_django.logger import logger
try:
    from amocrm.v2 import tokens, Lead, Contact, Company
except Exception as e:
    logger.debug(f'{e}')
    

def create_amo_contact(order):
    contact = Contact.objects.create({
        'name':order.full_name,
        "custom_fields_values": [
            {
                "field_id": 437643,
                "values": [
                    {
                        "value": order.email if order.email else '',
                        "enum_id": 238079
                    },

                ]
            }, 
            {
                "field_id": 437641,
                "values": [
                    {
                        "value": order.phone if order.phone else '',
                        "enum_id": 238067
                    },

                ]
            },
        ],})
    return contact
    

def get_amo_contact(email):
    try:
        contact = Contact.objects.get(query=email)
    except Exception as e:
        logger.debug(f'get_contact exception = {e}')
        contact = None
    return contact


def create_amo_lead_with_contact(price, contact):
    
    logger.debug(f'starting to create new lead')
    try:
        lead = Lead.objects.create(price=price)
        logger.debug(f'lead created = {lead}')
    except Exception as e:
        logger.debug(f'lead creating exception = {e}')
    
    try:
        logger.debug(f'trying to append contact to lead')
        lead.contacts.append(contact)
    except Exception as e:
        logger.debug(f'lead_contact_appending_exception = {e}')

    logger.debug(f'lead.contacts = {lead.contacts}')


def create_new_lead_and_contact(order, price):
    tokens.default_token_manager(
        client_id="791071cc-9300-470d-803c-a5efe12ff67a",
        client_secret="zDwKY1A5DQJhtqv9Bl2YWrwR6EwPGcGcKThhMd1W9Axtlr9totWAEq1fkuIByRUH",
        subdomain="infovitanowru",
        redirect_url="https://vitanow.ru",
        storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
    )
    logger.debug(f'creating_new_lead')
    contact = get_amo_contact(order.email)
    logger.debug(f'get_contact = {contact}')
    if contact is None:
        contact = create_amo_contact(order)
        logger.debug(f'created contact = {contact}')
    
    lead = create_amo_lead_with_contact(
        price, contact
        )
