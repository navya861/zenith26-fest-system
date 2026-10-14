"""
Zenith '26 Fest System Server Launcher
Starts Uvicorn with dual-stack IPv4/IPv6 support on Windows.
Binds to localhost, 127.0.0.1, [::1], and local network IP on port 8001.
"""
import socket
import sys
from pathlib import Path
import uvicorn

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from backend.main import app

def start_server(port: int = 8001):
    print(f"Starting Zenith '26 Server on port {port} (Dual-Stack IPv4 & IPv6)...")
    
    # Create dual-stack socket for Windows compatibility
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    try:
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
    except Exception:
        pass
    
    sock.bind(("", port))
    sock.listen(128)
    
    print(f" -> Student Portal:       http://localhost:{port}/")
    print(f" -> Admin Dashboard:      http://localhost:{port}/admin.html")
    print(f" -> Interactive API Docs: http://localhost:{port}/docs")
    print(f" -> Android Emulator:     http://10.0.2.2:{port}/")
    print("\nPress Ctrl+C to stop the server.\n")

    config = uvicorn.Config(app=app, log_level="info")
    server = uvicorn.Server(config)
    server.run(sockets=[sock])

if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    start_server(port_arg)
