import base64
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8000
SECRET_PATH = "/sub"

# Target server address and SNI
SNI_HOST = "firebaseremoteconfigrealtime.googleapis.com"
TARGET_PORT = 443

def extract_run_app_host(host_header):
    """Extracts host without port from HTTP Host header for host/authority."""
    if host_header:
        return host_header.split(':')[0]
    return "127.0.0.1"

def generate_subscription(host_header):
    run_app_host = extract_run_app_host(host_header)

    # WS Links
    vless_ws = (
        f"vless://7c9b83e1-4f12-4c6e-82df-13928e4692ba@{SNI_HOST}:{TARGET_PORT}"
        f"?encryption=none&type=ws&host={run_app_host}&headerType=none"
        f"&path=%2Fvlws%3Fed%3D2560&security=tls&sni={SNI_HOST}#vless-ws"
    )
    trojan_ws = (
        f"trojan://qD6fG9b@{SNI_HOST}:{TARGET_PORT}"
        f"?type=ws&host={run_app_host}&headerType=none"
        f"&path=%2Ftrws%3Fed%3D2560&security=tls&sni={SNI_HOST}#trojan-ws"
    )

    # SSH Link
    ssh_ws = (
        "ssh://geto:suguru@fcmtoken.googleapis.com:443"
        "?KUX3sw04Vw3D4VZXnUUdx9wLQqoKz1VHc0qkYCkif8etF3bt0wEm/JbY/fxDc3c8qx/lDmfQ6iI+mBoX3mFLV6wCkbjg0xsKogoy7tgNkvc67HyBpBa+VcEoaTbr0uWEuWDmdk3eSXNh5/PxnNYgY1zwCqOSnIJCcQ0O6gKTmtfcvE9jXmXcERZubqBh4bdtVsyB54jAEaacaGX5ITyDykKnV1i7rgXJTC6Z4A3aEWAwEFnrhXgtcXXIHikP1+iDaHXmfdg1YkBv+3vpkDID5maL74NWI/Sq34XivhGlDp60bferuwDGzaSxcWMbwtu8EX3B2gv5zdirM/oFztsPug+GvZ8MozziFM/CaCtsi1mXrsqCkOp3O3+BuyJKl1liETUdgJ9fDW5jf+xz8z/1ABLydfTVE/PH5Yp+5AxPr5XpYzQtcS85NkXj5x/n+ABmL9nfn6t00Mevbmxdk4EAm8JRptrkMhYmP8UzhrAa/yhoMny/zhHMdtjOqW926SzPEIPxMjUReZIELt50MZudZHzw93D5zzlYEyTmgSHGnOHGj0Av+becrEmiDEvLlVmJ6FIyBZIaSba87/OProkJshP0A/ik9z1lQ6RxIK0lcmXDE5f+vSm2Q/HqfsYjjN14WogiWN9QdazYHRRxtjG3uobShtZIwf4vE7TAob7nCCXjv7MBogZDMMCubDq8qTMnQeAQXowmF+rWFoMZ2RrdDtzZH8KqXtqoLwz+1UFuXk+x7e1s9m9GBVkrqo/G12Z1#ssh-ws"
    )

    # XHTTP Links
    vless_xhttp = (
        f"vless://7c9b83e1-4f12-4c6e-82df-13928e4692ba@{SNI_HOST}:{TARGET_PORT}"
        f"?encryption=none&type=xhttp&host={run_app_host}&headerType=auto"
        f"&path=%2Fvlxh%3Fed%3D2560&security=tls&sni={SNI_HOST}&alpn=h2#vless-xhttp"
    )
    trojan_xhttp = (
        f"trojan://qD6fG9b@{SNI_HOST}:{TARGET_PORT}"
        f"?type=xhttp&host={run_app_host}&headerType=auto"
        f"&path=%2Ftrxh%3Fed%3D2560&security=tls&sni={SNI_HOST}&alpn=h2#trojan-xh"
    )

    # Combine all links into the payload
    raw_payload = (
        f"{vless_ws}\n"
        f"{trojan_ws}\n"
        f"{ssh_ws}\n"
        f"{vless_xhttp}\n"
        f"{trojan_xhttp}\n"
    )
    return base64.b64encode(raw_payload.encode('utf-8'))

class SubHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        host_header = self.headers.get('Host', '')
        
        if self.path == SECRET_PATH or self.path.startswith(f"{SECRET_PATH}?"):
            sub_body = generate_subscription(host_header)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Subscription-Userinfo', 'upload=0; download=0; total=107374182400; expire=0')
            self.send_header('Profile-Update-Interval', '24')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(sub_body)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', PORT), SubHandler)
    print(f"Subscription server running on port {PORT}...")
    server.serve_forever()
