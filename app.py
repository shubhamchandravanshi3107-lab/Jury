

import subprocess
import sys
import threading
import queue
import webbrowser
import os
import json

from flask import Flask, render_template, request, Response

app = Flask(__name__)

SCRIPT_NAME = "subscription.py"  # <- the file this launches, completely unchanged

process = None
output_queue = queue.Queue()
reader_thread = None


def start_process():
    """Launches subscription.py exactly as-is, unbuffered, and starts
    a background thread that copies its output into a queue."""
    global process, reader_thread
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), SCRIPT_NAME)
    process = subprocess.Popen(
        [sys.executable, "-u", script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=0,
    )

    def read_output():
        while True:
            byte = process.stdout.read(1)
            if not byte:
                output_queue.put(None)  # signal: process ended
                break
            output_queue.put(byte.decode(errors="ignore"))

    reader_thread = threading.Thread(target=read_output, daemon=True)
    reader_thread.start()


@app.route("/")
def index():
    # (re)start a fresh run of subscription.py every time the page loads
    start_process()
    return render_template("terminal.html")


@app.route("/stream")
def stream():
    def event_stream():
        while True:
            chunk = output_queue.get()
            if chunk is None:
                yield "event: done\ndata: process finished\n\n"
                break
            # JSON-encode so newlines/quotes inside the chunk survive SSE transport
            yield f"data: {json.dumps(chunk)}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")


@app.route("/input", methods=["POST"])
def send_input():
    global process
    line = request.json.get("line", "")
    if process and process.stdin:
        try:
            process.stdin.write((line + "\n").encode())
            process.stdin.flush()
        except Exception:
            pass
    return {"ok": True}


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5050")


if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(host="127.0.0.1", port=5050, debug=False, threaded=True)
