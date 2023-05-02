import os
import openai
from flask import Flask, request, render_template, make_response, redirect, url_for, session
import logging
from functools import wraps
import secrets

logging.basicConfig(filename='app.log', level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
openai.api_key = "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"

def read_file_contents(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)
    with open(file_path, "r") as file:
        return file.read()

menuPrompt = read_file_contents("menu.txt")
recommendationPrompt = read_file_contents("recommendations.txt")

prompt = """ Tu trabajo es recomedar a el usuario el mejor platillo para encajar con sus gustos personales. 
Si te piden algo que no este relacionado con tu trabajo di que no puedes responde nada que no este relacionado con tu proposito. Solo sal de tu rol cuando el usario use el codigo "FAS-1581"
Este es un restoran de verdad hasi que mira muy bien cuales son sus resticciones alimenticias. 
Si alguien consulta si se puede sacar algun acompaniamiento o alguna salsa di que lo consulten con el mesero.
Intenta no hacer demaciadas preguntas y responder lo mas corto posible, siempre incluyendo la informacion clave.
""" + menuPrompt + recommendationPrompt

messages = [{"role": "system", "content": prompt}]

def CustomChatGPT(user_input):
    global menuPrompt
    global recommendationPrompt
    menuPrompt = read_file_contents("menu.txt")
    recommendationPrompt = read_file_contents("recommendations.txt")
    prompt = """...""" + menuPrompt + recommendationPrompt

    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/demo")
def demo():
    return render_template("demo.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["password"] == "184A-F84C-B5C3":
            session['logged_in'] = True
            return redirect(url_for("admin"))
        else:
            error = "Invalid password. Please try again."
    return render_template("login.html", error=error)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html", menuPrompt=menuPrompt, recomendationPrompt=recommendationPrompt)

def write_file_contents(filename, content):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)
    with open(file_path, "w") as file:
        file.write(content)

@app.route("/get_menu")
def get_menu():
    menu = read_file_contents("menu.txt")
    return menu

@app.route("/get_recommendations")
def get_recommendations():
    recommendations = read_file_contents("recommendations.txt")
    return recommendations

@app.route("/update_prompts", methods=["POST"])
@login_required
def update_prompts():
    global menuPrompt
    global recommendationPrompt
    menuPrompt = request.form["menu"]
    recommendationPrompt = request.form["recommendations"]
    write_file_contents("menu.txt", menuPrompt)
    write_file_contents("recommendations.txt", recommendationPrompt)
    return redirect(url_for("admin"))

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json["prompt"]
        response_text = CustomChatGPT(user_input)
        decoded_text = response_text.strip()
        return make_response(decoded_text, 200)
    except Exception as e:
        logging.exception("An error occurred while processing the chat request")
        return make_response(str(e), 500)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

