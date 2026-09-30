from fastapi import Depends, APIRouter,HTTPException, Response
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.schemas.contacts_schema import ContactSchema, ContactPartialSchema
from app.models.contacts import Contacts
from app.utils.contact_utils import normalize_num
import datetime

router = APIRouter()

@router.get('/contacts')
def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contacts).all()
    return contacts

@router.get('/contacts/{contact_id}')
def get_contact(contact_id: int, db: Session=Depends(get_db)):
    contact = db.query(Contacts).filter(Contacts.id==contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact Not Found")
    return contact

@router.post('/contacts/create')
def create_contact(contact_data: ContactSchema, db: Session = Depends(get_db)):
    contact = Contacts(name=contact_data.name, country_code=contact_data.country_code, phn_num=contact_data.phn_num, email=contact_data.email)
    contact.normalised_num = normalize_num(contact.phn_num)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

@router.put('/contacts/update/{contact_id}')
def update_contact(contact_id: int, contact_info: ContactSchema, db: Session = Depends(get_db)):
    contact = db.query(Contacts).filter(Contacts.id==contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact Not Found")
    contact.name = contact_info.name
    contact.country_code = contact_info.country_code
    contact.phn_num = contact_info.phn_num
    contact.normalised_num = normalize_num(contact_info.phn_num)
    contact.email = contact_info.email
    contact.last_modified = datetime.datetime.now()
    db.commit()
    db.refresh(contact)
    return contact
        

@router.patch("/contacts/part_update/{contact_id}")
def part_update(contact_id: int, contact_info: ContactPartialSchema, db: Session = Depends(get_db)):
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact Not Found")
    updated = False
    if contact_info.name is not None:
        contact.name = contact_info.name
        updated = True
    if contact_info.country_code is not None:
        contact.country_code = contact_info.country_code
        updated = True
    if contact_info.phn_num is not None:
        contact.phn_num = contact_info.phn_num
        contact.normalised_num = normalize_num(contact_info.phn_num)
        updated = True
    if contact_info.email is not None:
        contact.email = contact_info.email
        updated = True
    if updated:
        contact.last_modified = datetime.datetime.now()
    db.commit()
    db.refresh(contact)
    return contact
        
@router.delete('/contacts/delete/{contact_id}')
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contacts).filter(Contacts.id==contact_id).first()
    if contact is not None:
        db.delete(contact)
        db.commit()
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Contact Not Found")