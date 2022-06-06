from sqlalchemy import delete
from sqlalchemy.orm import Session
from datetime import date

import models
import schemas


def get_event_by_date(db: Session, event_date: str):
    return db.query(models.Event).filter(models.Event.date == event_date)


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def create_event(db: Session, event: schemas.EventCreate):
    event_date = event.date
    event_name = event.event
    date_added = date.today().strftime("%Y-%m-%d")
    db_event = models.Event(name=event_name, date=event_date, date_added=date_added)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )


def get_suppliers(db: Session):
    return db.query(models.Supplier).all()


def get_supplier(db: Session, supplier_id: int):
    return (
        db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first()
    )


def get_categories(db: Session, category_id: int):
    return (
        db.query(models.Category).filter(models.Category.CategoryID == category_id).first()
    )


def get_products(db: Session, supplier_id: int):
    return (
        db.query(models.Product)
        .filter(models.Product.SupplierID == supplier_id)
        .order_by(models.Product.ProductID.desc())
        .all()
    )


def create_suppliers(db: Session, supplier: schemas.SupplierCreate):
    last_id = db.query(models.Supplier).order_by(models.Supplier.SupplierID.desc()).first().SupplierID
    db_supplier = models.Supplier(SupplierID=last_id + 1, CompanyName=supplier.CompanyName,
                                  ContactName=supplier.ContactName,
                                  ContactTitle=supplier.ContactTitle, Address=supplier.Address,
                                  City=supplier.City, PostalCode=supplier.PostalCode,
                                  Country=supplier.Country, Phone=supplier.Phone)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


def update_suppliers(db: Session, supplier: schemas.SupplierUpdate, supplier_id: int):
    chosen_supplier = db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first()
    if supplier.CompanyName:
        chosen_supplier.CompanyName = supplier.CompanyName
    if supplier.ContactName:
        chosen_supplier.ContactName = supplier.ContactName
    if supplier.ContactTitle:
        chosen_supplier.ContactTitle = supplier.ContactTitle
    if supplier.Address:
        chosen_supplier.Address = supplier.Address
    if supplier.City:
        chosen_supplier.City = supplier.City
    if supplier.PostalCode:
        chosen_supplier.PostalCode = supplier.PostalCode
    if supplier.Country:
        chosen_supplier.Country = supplier.Country
    if supplier.Phone:
        chosen_supplier.Phone = supplier.Phone
    if supplier.Fax:
        chosen_supplier.Fax = supplier.Fax
    if supplier.HomePage:
        chosen_supplier.HomePage = supplier.HomePage
    if supplier.Region:
        chosen_supplier.Region = supplier.Region
    db.commit()
    db.refresh(chosen_supplier)
    return chosen_supplier


def delete_supplier(db: Session, supplier_id: int):
    db.execute(delete(models.Supplier).where(models.Supplier.SupplierID == supplier_id))
    db.commit()
    return
