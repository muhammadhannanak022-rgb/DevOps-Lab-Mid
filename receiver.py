from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
import os
import hmac

HOST = "0.0.0.0"
PORT = int(os.environ.get("RECEIVER_PORT", "9000"))
TOKEN = os.environ.get("RECEIVER_TOKEN")

if not TOKEN:
    raise RuntimeError("RECEIVER_TOKEN environment variable is required")

OUTPUT = Path("test-report.json")


class ReportHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/report":
            self.send_error(404, "Use POST /report")
            return

        received_token = self.headers.get("Authorization", "")
        expected_token = f"Bearer {TOKEN}"

        if not hmac.compare_digest(received_token, expected_token):
            self.send_error(401, "Unauthorized")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            report = json.loads(
                self.rfile.read(length).decode("utf-8")
            )

            if not isinstance(report, dict):
                raise ValueError("Report must be a JSON object")

            OUTPUT.write_text(
                json.dumps(report, indent=2),
                encoding="utf-8"
            )

            body = b"Report received and saved."
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

            print(f"Saved report to {OUTPUT.resolve()}", flush=True)

        except Exception as exc:
            self.send_error(400, str(exc))

    def log_message(self, fmt, *args):
        print(fmt % args, flush=True)


if __name__ == "__main__":
    print(
        f"Report receiver listening on http://{HOST}:{PORT}",
        flush=True
    )
    HTTPServer((HOST, PORT), ReportHandler).serve_forever()
