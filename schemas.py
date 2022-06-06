from typing import Dict, Optional

from pydantic import BaseModel, PositiveInt, constr


class EventBase(BaseModel):
    name: str
    date: str


class EventCreate(BaseModel):
    date: str
    event: str


class Event(EventBase):
    id: int
    date_added: str

    class Config:
        orm_mode = True


class Shipper(BaseModel):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)

    class Config:
        orm_mode = True


class Supplier(BaseModel):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40)
    ContactName: constr(max_length=30) = None
    ContactTitle: constr(max_length=30) = None
    Address: constr(max_length=60) = None
    City: constr(max_length=15) = None
    Region: constr(max_length=15) = None
    PostalCode: constr(max_length=10) = None
    Country: constr(max_length=15) = None
    Phone: constr(max_length=24) = None
    Fax: constr(max_length=24) = None
    HomePage: constr() = None

    class Config:
        orm_mode = True


class SupplierBase(BaseModel):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40)

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):

    CategoryID: PositiveInt
    CategoryName: constr(max_length=15)

    class Config:
        orm_mode = True


class Product(BaseModel):

    ProductID: PositiveInt
    ProductName: constr(max_length=40)
    Category: CategoryBase
    Discontinued: int

    class Config:
        orm_mode = True


class SupplierCreate(BaseModel):
    CompanyName: constr(max_length=40)
    ContactName: constr(max_length=30) | None = None
    ContactTitle: constr(max_length=30) | None = None
    Address: constr(max_length=60) | None = None
    City: constr(max_length=15) | None = None
    PostalCode: constr(max_length=10) | None = None
    Country: constr(max_length=15) | None = None
    Phone: constr(max_length=24) | None = None
    Fax: constr(max_length=24) | None = None
    HomePage: constr() | None = None

    class Config:
        orm_mode = True


class SupplierUpdate(BaseModel):
    CompanyName:  Optional[constr(max_length=40)]
    ContactName: Optional[constr(max_length=30)]
    ContactTitle: Optional[constr(max_length=30)]
    Address: Optional[constr(max_length=60)]
    City: Optional[constr(max_length=15)]
    Region: Optional[constr(max_length=15)]
    PostalCode: Optional[constr(max_length=10)]
    Country: Optional[constr(max_length=15)]
    Phone: Optional[constr(max_length=24)]
    Fax: Optional[constr(max_length=24)]
    HomePage: Optional[constr()]

    class Config:
        orm_mode = True
