from . import models
from fastapi import FastAPI, HTTPException
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def get_all_users():
    db = SessionLocal()
    users = db.query(models.User).all()
    return users

@app.post("/user/")
def create_user(firstname: str, lastname: str, job: str):
    db = SessionLocal()
    db_user = models.User(firstname=firstname, lastname=lastname, job=job)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/user/{user_id}")
def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/user/{user_id}")
def update_user(user_id: int, firstname: str, lastname: str, job: str):
    db = SessionLocal()
    db_user = db.query(models.User).filter(models.User.id==user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.firstname = firstname
    db_user.lastname = lastname
    db_user.job = job
    db.commit()
    return {"message": "User updated successfully"}

@app.delete("/user/{user_id}")
def delete_item(user_id: int):
    db = SessionLocal()
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app)