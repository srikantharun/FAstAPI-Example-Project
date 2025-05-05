#!/usr/bin/env python3
import requests
import sys
import time
import socket
import argparse
from urllib.parse import urljoin

def is_port_in_use(port, host='localhost'):
    """Check if a port is in use on the host."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except socket.error:
        return False
    finally:
        s.close()

def check_swagger_docs(base_url):
    """Check if Swagger documentation is accessible."""
    # Try default FastAPI Swagger UI paths
    paths = [
        '/docs',            # Default FastAPI docs path
        '/redoc',           # Default FastAPI redoc path
        '/openapi.json',    # Default OpenAPI schema
        '/api/v1/docs',     # Common version-prefixed docs path
        '/api/v1/redoc',    # Common version-prefixed redoc path
        '/api/v1/openapi.json'  # Common version-prefixed schema
    ]
    
    results = {}
    
    for path in paths:
        url = urljoin(base_url, path)
        try:
            print(f"Checking {url}...")
            response = requests.get(url)
            status = response.status_code
            content_type = response.headers.get('content-type', '')
            
            if status == 200:
                if 'html' in content_type and path.endswith(('docs', 'redoc')):
                    result = "✅ SUCCESS: HTML documentation page"
                elif 'json' in content_type and path.endswith('.json'):
                    result = "✅ SUCCESS: JSON schema"
                else:
                    result = f"❓ UNEXPECTED: Status 200 but content-type is {content_type}"
            else:
                result = f"❌ FAILED: Status code {status}"
            
            results[path] = result
        except requests.RequestException as e:
            results[path] = f"❌ ERROR: {str(e)}"
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Check FastAPI Swagger documentation')
    parser.add_argument('--port', type=int, default=8000, help='Port number (default: 8000)')
    parser.add_argument('--host', default='127.0.0.1', help='Host (default: 127.0.0.1)')
    args = parser.parse_args()
    
    port = args.port
    host = args.host
    base_url = f"http://{host}:{port}"
    
    # Check if the port is in use
    if not is_port_in_use(port, host):
        print(f"❌ ERROR: No server running at {base_url}")
        sys.exit(1)
    
    # Check Swagger documentation
    results = check_swagger_docs(base_url)
    
    # Print results
    print("\nResults:")
    print("=" * 80)
    for path, result in results.items():
        print(f"{path}: {result}")

if __name__ == "__main__":
    main()