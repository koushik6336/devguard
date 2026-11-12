from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

# In-memory storage (resets when the app restarts)
tasks = []
_next_id = 1


def _find_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


@app.route("/")
def home():
    pending = sum(1 for t in tasks if not t["complete"])
    return render_template(
        "home.html",
        tasks=tasks,
        total=len(tasks),
        pending=pending,
        done=len(tasks) - pending,
    )


@app.route("/add", methods=["POST"])
def add():
    global _next_id
    name = request.form.get("task", "").strip()
    if name:
        tasks.append({"id": _next_id, "name": name[:200], "complete": False})
        _next_id += 1
    return redirect(url_for("home"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    task = _find_task(task_id)
    if task:
        task["complete"] = True
    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    task = _find_task(task_id)
    if task:
        tasks.remove(task)
    return redirect(url_for("home"))


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # nosec B104
