from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
import secrets
import maze_runner

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = 6000
app.config["SECRET_KEY"] = secrets.token_hex(16)
Session(app)

@app.route("/", methods=["GET", "POST"])
def maze_run():
    session["answer"] = [["white" for i in range(20)] for j in range(20)]
    null = [["white" for i in range(20)] for j in range(20)]
    if request.method == "GET":
        session["string"] = (
            "Choose start cell (green). Choose goal cell (red). Drag/Click to put obstructions (black)."
        )
        session["obstructions"] = []
        return render_template(
            "maze_runner.html", answer=null, string=session["string"]
        )
    elif request.method == "POST":
        session["start"] = None
        session["goal"] = None
        session["obstructions"] = []
        session["solution"] = null
        session["explored"] = null
        for i in range(20):
            for j in range(20):
                if request.values.get(f"{i}_{j}") == "green":
                    session["start"] = (i, j)
                elif request.values.get(f"{i}_{j}") == "red":
                    session["goal"] = (i, j)
                elif request.values.get(f"{i}_{j}") == "black":
                    session["obstructions"].append((i, j))
                elif (i, j) in session["obstructions"] and request.values.get(
                    f"{i}_{j}"
                ) == "white":
                    session["obstructions"].remove((i, j))
        if not session["goal"] or not session["start"]:
            return jsonify({"answer": null, "string": "Start or Goal is undefined."})
        session["diagonal_movement"] = request.values.get("diagonal_movement")
        if session["diagonal_movement"]:
            session["diagonal_movement"] = True
        else:
            session["diagonal_movement"] = False
        session["solution"], session["string"], session["explored"] = (
            maze_runner.solve_maze(
                session["start"],
                session["goal"],
                session["obstructions"],
                session["diagonal_movement"],
            )
        )
        session["query_explore"] = request.values.get("explored")
        for i in range(20):
            for j in range(20):
                if (i, j) == session["start"]:
                    session["answer"][i][j] = "green"
                elif (i, j) == session["goal"]:
                    session["answer"][i][j] = "red"
                elif (i, j) in session["obstructions"]:
                    session["answer"][i][j] = "black"
                elif (i, j) in session["solution"]:
                    session["answer"][i][j] = "yellow"
                elif (i, j) in session["explored"] and session["query_explore"]:
                    session["answer"][i][j] = "blue"
                else:
                    session["answer"][i][j] = "white"
        return jsonify({"answer": session["answer"], "string": session["string"]})
