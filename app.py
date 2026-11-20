from flask import Flask, request, redirect, url_for, render_template_string
from urllib.parse import urlparse
import json
from pathlib import Path

app = Flask(__name__)
SUBMISSIONS_FILE = Path("submissions.json")

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Assignment Submission Portal</title>
  <style>
    body{font-family:Arial,sans-serif;background:#f3f6fb;margin:0;padding:35px;color:#172033}
    .wrap{max-width:850px;margin:auto}.card{background:white;padding:25px;border-radius:14px;
    box-shadow:0 5px 22px #14213d12;margin-bottom:22px}
    h1{color:#173b68}label{display:block;font-weight:bold;margin-top:13px}
    input{box-sizing:border-box;width:100%;padding:11px;margin-top:6px;border:1px solid #ccd4df;border-radius:7px}
    button{margin-top:18px;padding:12px 20px;background:#1769aa;color:white;border:0;border-radius:7px;cursor:pointer}
    .error{background:#ffe8e8;color:#9c2020;padding:10px;border-radius:7px}
    .success{background:#e6f7eb;color:#176534;padding:10px;border-radius:7px}
    li{padding:10px;border-bottom:1px solid #eee;overflow-wrap:anywhere}
  </style>
</head>
<body><div class="wrap">
  <div class="card">
    <h1>Assignment Submission Portal</h1>
    <p>Enter your details and submit your assignment link.</p>
    {% if message %}<p class="{{ 'error' if error else 'success' }}">{{ message }}</p>{% endif %}
    <form method="post" action="/submit">
      <label>Student Name</label><input name="name" value="{{ values.get('name','') }}" required>
      <label>Registration Number</label><input name="registration_number" value="{{ values.get('registration_number','') }}" required>
      <label>Assignment Title</label><input name="assignment_title" value="{{ values.get('assignment_title','') }}" required>
      <label>Submission URL</label><input name="submission_url" type="url" value="{{ values.get('submission_url','') }}" required>
      <button type="submit">Submit Assignment</button>
    </form>
  </div>
  <div class="card"><h2>Saved Submissions ({{ submissions|length }})</h2>
    {% if submissions %}
      <ul>{% for item in submissions %}
        <li><b>{{ item.name }}</b> ({{ item.registration_number }}) - {{ item.assignment_title }} - <a href="{{ item.submission_url }}">{{ item.submission_url }}</a></li>
        {{ item.assignment_title }} Ã¢â‚¬â€
        <a href="{{ item.submission_url }}" target="_blank">{{ item.submission_url }}</a></li>
      {% endfor %}</ul>
    {% else %}<p>No submissions yet.</p>{% endif %}
  </div>
</div></body></html>
"""

def load_submissions():
    if not SUBMISSIONS_FILE.exists():
        return []
    try:
        return json.loads(SUBMISSIONS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

def save_submissions(items):
    SUBMISSIONS_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")

def validate_submission(data):
    required = ["name", "registration_number", "assignment_title", "submission_url"]
    for field in required:
        if not str(data.get(field, "")).strip():
            return False, f"{field.replace('_', ' ').title()} is required."
    parsed = urlparse(str(data["submission_url"]).strip())
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return False, "Please enter a valid HTTP or HTTPS submission URL."
    return True, ""

@app.get("/")
def home():
    return render_template_string(PAGE, submissions=load_submissions(),
                                  message="", error=False, values={})

@app.post("/submit")
def submit():
    data = {key: request.form.get(key, "").strip() for key in
            ["name", "registration_number", "assignment_title", "submission_url"]}
    valid, message = validate_submission(data)
    if not valid:
        return render_template_string(PAGE, submissions=load_submissions(),
                                      message=message, error=True, values=data), 400
    items = load_submissions()
    items.append(data)
    save_submissions(items)
    return render_template_string(PAGE, submissions=items,
                                  message="Submission saved successfully.", error=False, values={})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
