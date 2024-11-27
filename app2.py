from flask import Flask, request, render_template
import requests

app = Flask(__name__)

pizzas = {
    "Summer": [("Пеперони", "Перетертые томаты, моцарелла, салями пикантные пепперони. Аллергены: злаки, лактоза.", 305)],
    "Winter": [("Сырная", "Моцарелла беби, фета, пармезан, горгонзола, проволоне, моцарелла. Аллергены: глютен, лактоза.", 280)],
    "Spring": [("Цезарь", "Томатный соус, моцарелла, куриное филе, салат айсберг, соус цезарь, пармезан. Аллергены: злаки, лактоза.", 340)]
}

def recommendation(temp):
    if temp <= 5:
        return pizzas["Winter"]
    elif 5 < temp < 20:
        return pizzas["Spring"]
    elif temp >= 20:
        return pizzas["Summer"]
    return None

@app.route("/", methods=["GET", "POST"])
def weather():
    weather_data = None
    pizza_recommendation = None

    if request.method == "POST":
        location = request.form.get("location")
        if location:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid=0ead5105eb0b05b10a0459b6fae480b1&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                weather_data = response.json()
                temp = weather_data["main"]["temp"]
                pizza_list = recommendation(temp)
                pizza_recommendation = pizza_list[0] if pizza_list else None
            else:
                weather_data = {"error": "Eta gde??????????????"}

    return render_template("main.html", weather=weather_data, pizza=pizza_recommendation)

if __name__ == "__main__":
    app.run(port=5005, debug=True)
