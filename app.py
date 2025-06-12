import script
from flask import Flask, render_template, request

# Create an instance of Flask
app = Flask(__name__)

# Create a view function for /
@app.route("/")
def index():
    return render_template("about.html")

@app.route("/form")
def form():
    if request.method == "GET":
        return render_template("index.html")
    else:
        return "Error: Wrong HTTP method, expecting GET", 400

@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "GET":
        return render_template("about.html")
    else:
        return "Error: Wrong HTTP method, expecting GET", 400

@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "POST":



        caffeine_pref = []
        caffeine_pref_form_choices = {"user_caffeine_very_high": "very high",
                                      "user_caffeine_high": "high",
                                      "user_caffeine_moderate": "moderate",
                                      "user_caffeine_low": "low",
                                      "user_caffeine_very_low": "very low",
                                      "user_caffeine_none": "none"}
        for choice in caffeine_pref_form_choices:
            choice_value = request.form.get(choice, False)
            if choice_value:
                caffeine_pref.append(caffeine_pref_form_choices[choice])

        tea_keywords = [request.form["user_tea_word1"]]
        if not request.form["user_tea_word2"] == "":
            tea_keywords.append(request.form["user_tea_word2"])
        if not request.form["user_tea_word3"] == "":
            tea_keywords.append(request.form["user_tea_word3"])

        user_poem_keyword = request.form["user_poem_keyword"]

        if tea_keywords == [""] or user_poem_keyword == "":
            return render_template("oopsie.html")

        tea_results = script.tea_pick(user_keywords=tea_keywords, caffeine_prefs=caffeine_pref)
        poem_result = script.poetry_pick(user_poem_keyword)
        if poem_result:
            poem_result = script.poetry_format(poem_result)

        print_keywords = script.format_tea_keywords(tea_keywords)

        user_poem_keyword = '"' + user_poem_keyword + '"'

        return render_template("results.html",
                               tea_keywords=print_keywords, user_poem_keyword=user_poem_keyword,
                               tea_results=tea_results, poem_result=poem_result)

    else:
        return "Error: Wrong HTTP method, expecting POST", 400