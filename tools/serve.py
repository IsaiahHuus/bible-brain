"""Local preview for Bible Brain.

Serves app/index.html on http://localhost:4890, wrapped in the same minimal
document skeleton the published artifact gets, plus the data files in docs/.
With --site it serves the generated GitHub Pages site (docs/) as-is.

    python -I tools/serve.py
    python -I tools/serve.py --site
"""
import http.server
import os
import socketserver
import sys

SITE = "--site" in sys.argv

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "docs")
APP = os.path.join(HERE, "..", "app")
PORT = 4891 if "--site" in sys.argv else 4890
HEAD = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
</head><body>
"""


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):
        if not SITE and self.path.split("?")[0] in ("/", "/index.html"):
            with open(os.path.join(APP, "index.html"), encoding="utf-8") as fh:
                body = (HEAD + fh.read() + "\n</body></html>").encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


socketserver.ThreadingTCPServer.allow_reuse_address = True
socketserver.ThreadingTCPServer.daemon_threads = True
with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), Handler) as httpd:
    print(f"Bible Brain preview on http://localhost:{PORT}", flush=True)
    httpd.serve_forever()
