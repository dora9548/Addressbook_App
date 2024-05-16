from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import SessionLOcal,engine,init_db
from math import radians,cos,sin,sqrt,atan2


models.Base.metadata.create_all(bind=engine)
app=FastAPI()

def get_db():
    db=SessionLOcal()
    try:
        yield db
    finally:
        db.close()

@app.post("/addresses/",response_model=schemas.Adress)
def create_address(address:schemas.AddressCreate,db:Session=Depends(get_db)):
    db_address=models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.get("/addresses/{address_id}",response_model=schemas.Adress)
def read_address(address_id:int,db:Session=Depends(get_db)):
    db_address=db.query(models.Address).filter(models.Address.id==address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404,details="address not found" )
    return db_address


@app.put("/addresses/{address_id}",response_model=schemas.Adress)
def update_address(address_id:int,address:schemas.AddressCreate,db:Session=Depends(get_db)):
    db_address=db.query(models.Address).filter(models.Address.id==address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404,details="address not found" )
    for key,value in address.dict().items():
        setattr(db_address,key,value)
    db.commit()
    db.refresh(db_address)
    return db_address


@app.delete("/addresses/{address_id}")
def delete_address(address_id:int,db:Session=Depends(get_db)):
    db_address=db.query(models.Address).filter(models.Address.id==address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404,details="address not found" )
    db.delete(db_address)
    db.commit()
    return {"details":"Addresss deleted"}

def calculate_distance(lat1,lon1,lat2,lon2):
    R=6371
    dlat=radians(lat2-lat1)
    dlon=radians(lon2-lon1)
    a=sin(dlat/2)**2+cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c=2*atan2(sqrt(a),sqrt(1-a))
    distance=R*c
    return distance


@app.put("/addresses/",response_model=List[schemas.Adress])
def get_address_within_distance (lat:float,lon:float,distance:float,db:Session=Depends(get_db)):
    addresses= db.query(models.Address).all()
    result=[]
    for address in addresses:
        dist=calculate_distance(lat,lon,address.latitude,address.longitude)
        if dist<=distance:
            result.append(address)
        return result







