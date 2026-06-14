"""
Generate cURL command + output files for capstone tasks.
Runs the cURL commands and writes the actual command + actual response.
"""
import subprocess
import os

BASE = "http://127.0.0.1:8000"
OUT_DIR = r"c:\Users\exorc\Downloads\ABC"


def run_curl(args):
    """Run a cURL and return the (command_str, stdout)."""
    full = ["curl.exe", "-s"] + args
    result = subprocess.run(full, capture_output=True, text=True)
    # Build a human-friendly, shell-quoted version of the command
    parts = ["curl"]
    for a in args:
        if any(c in a for c in [' ', '&', '{', '}', '"']):
            parts.append('"' + a.replace('"', '\\"') + '"')
        else:
            parts.append(a)
    cmd = " \\\n    ".join(parts)

    # Pretty-print JSON output if possible
    raw = (result.stdout + result.stderr).strip()
    try:
        import json
        parsed = json.loads(raw)
        pretty = json.dumps(parsed, indent=2)
        return cmd, pretty
    except Exception:
        return cmd, raw


def write_file(name, header, cmd, output):
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write(header + "\n")
        f.write("=" * 80 + "\n\n")
        f.write("Command:\n  " + cmd + "\n\n")
        f.write("Output:\n")
        f.write(output + "\n")


# ===== Task 5: LOGIN =====
cmd, out = run_curl([
    "-X", "POST", f"{BASE}/djangoapp/login",
    "-H", "Content-Type: application/json",
    "-d", '{"userName": "testuser", "password": "TestPass123"}',
])
write_file("loginuser.txt", "Task 5: cURL command and output - LOGIN", cmd, out)

# ===== Task 6: LOGOUT =====
# Need to login first to set the session cookie, then logout (GET)
cookies = os.path.join(OUT_DIR, "cookies.txt")
subprocess.run(["curl.exe", "-s", "-X", "POST", f"{BASE}/djangoapp/login",
                "-H", "Content-Type: application/json",
                "-c", cookies,
                "-d", '{"userName": "testuser", "password": "TestPass123"}'],
               capture_output=True)
cmd, out = run_curl([
    f"{BASE}/djangoapp/logout",
    "-b", cookies,
])
write_file("logoutuser.txt", "Task 6: cURL command and output - LOGOUT", cmd, out)

# ===== Task 8: get dealer reviews (for dealer id=1) =====
cmd, out = run_curl([f"{BASE}/djangoapp/reviews/dealer/1"])
write_file("getdealerreviews.txt", "Task 8: cURL command and output - DEALER REVIEWS (dealer id=1)", cmd, out)

# ===== Task 9: get all dealers =====
cmd, out = run_curl([f"{BASE}/djangoapp/dealers"])
write_file("getalldealers.txt", "Task 9: cURL command and output - ALL DEALERS", cmd, out)

# ===== Task 10: get dealer by id =====
cmd, out = run_curl([f"{BASE}/djangoapp/dealer/1"])
write_file("getdealerbyid.txt", "Task 10: cURL command and output - DEALER BY ID (1)", cmd, out)

# ===== Task 11: get dealers by state (Kansas) =====
cmd, out = run_curl([f"{BASE}/djangoapp/dealers/state/KS"])
write_file("getdealersbyState.txt", "Task 11: cURL command and output - DEALERS BY STATE (Kansas)", cmd, out)

# ===== Tasks 14-15: get all car makes =====
cmd, out = run_curl([f"{BASE}/djangoapp/carmakes"])
write_file("getallcarmakes.txt", "Tasks 14-15: cURL command and output - ALL CAR MAKES (with models)", cmd, out)

# Also generate /get_cars (uses CarModels key) for the rubric
cmd, out = run_curl([f"{BASE}/djangoapp/get_cars"])
write_file("getcars.txt", "Tasks 14-15: cURL command and output - ALL CARS (CarModels key)", cmd, out)

# ===== Task 16: analyze review sentiment (path parameter form) =====
cmd, out = run_curl([f"{BASE}/djangoapp/analyze/Fantastic%20services"])
write_file("analyzereview.txt", "Task 16: cURL command and output - ANALYZE REVIEW SENTIMENT (\"Fantastic services\")", cmd, out)

print("All cURL output files created.")
