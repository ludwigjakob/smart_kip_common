#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/shutdown":
            subprocess.Popen(["sudo", "shutdown", "-h", "now"])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Shutting down")
        else:
            self.send_response(404)
            self.end_headers()

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()