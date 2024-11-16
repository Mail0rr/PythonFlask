from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

DATABASE_URL = "sqlite:///pizzas.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Pizza(Base):
    __tablename__ = "pizzas"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)

Base.metadata.create_all(engine)


@app.get("/")
def index():
    pizzas = session.query(Pizza).all()
    return render_template("main.html", pizzas=pizzas)

@app.get("/join/")
def get_add_pizza():
    return render_template("join.html")

@app.post("/join/")
def post_add_pizza():
    name = request.form["name"]
    description = request.form["description"]
    price = float(request.form["price"])

    new_pizza = Pizza(name=name, description=description, price=price)
    session.add(new_pizza)
    session.commit()
    return redirect(url_for("index"))

@app.get("/participants/")
def participants():
    pizzas = session.query(Pizza).all()
    return render_template("participants.html", pizzas=pizzas)

if __name__ == "__main__":
    app.run(port=5005, debug=True)