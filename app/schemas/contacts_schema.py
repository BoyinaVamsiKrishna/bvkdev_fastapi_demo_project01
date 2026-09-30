from pydantic import BaseModel

class ContactSchema(BaseModel):
    name: str
    country_code : str
    phn_num: str
    email: str


class ContactPartialSchema(BaseModel):
    name: str | None = None
    country_code : str | None = None
    phn_num: str | None= None
    email: str | None= None

    