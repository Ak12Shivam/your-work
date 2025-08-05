#!/usr/bin/env python3
"""
Your-Work Innovations Website Server
A simple HTTP server to run the responsive website locally
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# Configuration
PORT = int(os.environ.get('PORT', 8000))  # Use environment PORT for deployment
HOST = os.environ.get('HOST', '0.0.0.0')  # Use 0.0.0.0 for deployment compatibility

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler with better error handling and logging"""
    
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # Security headers
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests with custom routing"""
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()
    
    def log_message(self, format, *args):
        """Custom logging format"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def find_free_port(start_port=8000, max_attempts=10):
    """Find a free port starting from start_port"""
    import socket
    
    # If PORT is set by environment (deployment), use it directly
    if 'PORT' in os.environ:
        return int(os.environ['PORT'])
    
    # Otherwise, find a free port for local development
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))  # Bind to 0.0.0.0 instead of HOST
                return port
        except OSError:
            continue
    
    raise OSError(f"Could not find a free port in range {start_port}-{start_port + max_attempts}")

def check_files():
    """Check if required files exist"""
    current_dir = Path.cwd()
    index_file = current_dir / 'index.html'
    
    if not index_file.exists():
        print(f"❌ Error: index.html not found in {current_dir}")
        print("   Make sure you're running this script from the same directory as index.html")
        return False
    
    # Check for logo file
    logo_files = ['logo.png', 'logo.svg', 'logo.jpg', 'logo.jpeg']
    logo_found = any((current_dir / logo).exists() for logo in logo_files)
    
    if not logo_found:
        print("⚠️  Warning: Logo file not found. The website may not display logos correctly.")
        print("   Expected files: logo.png, logo.svg, logo.jpg, or logo.jpeg")
    
    return True

def start_server():
    """Start the HTTP server"""
    try:
        # Change to the directory containing this script
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # Check if required files exist
        if not check_files():
            return
        
        # Find a free port
        try:
            port = find_free_port(PORT)
        except OSError as e:
            print(f"❌ Error: {e}")
            return
        
        # Create server with deployment-friendly settings
        with socketserver.TCPServer((HOST, port), CustomHTTPRequestHandler) as httpd:
            # Allow address reuse for deployment
            httpd.allow_reuse_address = True
            
            server_url = f"http://{HOST}:{port}"
            local_url = f"http://localhost:{port}"
            
            print("=" * 60)
            print("🚀 Your-Work Innovations Website Server")
            print("=" * 60)
            print(f"📍 Server running at: {server_url}")
            if HOST == '0.0.0.0':
                print(f"� Local access: {local_url}")
            print(f"�📁 Serving files from: {Path.cwd()}")
            print("=" * 60)
            print("📱 Test your responsive website on different devices:")
            if HOST == '0.0.0.0':
                print(f"   • Desktop: {local_url}")
                print(f"   • Mobile: Use your computer's IP address with port {port}")
                print(f"   • Deployment: Server accessible on all interfaces")
            else:
                print(f"   • Desktop: {server_url}")
                print(f"   • Mobile: Use your computer's IP address instead of 'localhost'")
            print("=" * 60)
            print("💡 Tips:")
            print("   • Press Ctrl+C to stop the server")
            print("   • Refresh the page after making changes to HTML/CSS")
            print("   • Use browser dev tools to test different screen sizes")
            if HOST == '0.0.0.0':
                print("   • This server is configured for deployment compatibility")
            print("=" * 60)
            
            # Open browser automatically
            try:
                webbrowser.open(server_url)
                print("🌐 Opening website in your default browser...")
            except Exception as e:
                print(f"Could not open browser automatically: {e}")
                print(f"Please manually open: {server_url}")
            
            print("\n✅ Server started successfully! Waiting for requests...")
            print("   (Press Ctrl+C to stop)")
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("   Make sure the port is not already in use")

def show_network_info():
    """Show network information for mobile testing"""
    import socket
    
    try:
        # Get local IP address
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        print(f"\n🌐 Network Information:")
        print(f"   • Computer Name: {hostname}")
        print(f"   • Local IP Address: {local_ip}")
        print(f"   • For mobile testing, use: http://{local_ip}:{PORT}")
        print("   • Make sure your mobile device is on the same WiFi network")
    except Exception as e:
        print(f"Could not determine network info: {e}")

def main():
    """Main function"""
    print("🎯 Your-Work Innovations Website Server")
    print("   A simple HTTP server for testing your responsive website\n")
    
    # Show network info for mobile testing
    show_network_info()
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
