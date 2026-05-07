
import os
import sys
from fastapi.testclient import TestClient

# Add current directory to sys.path
sys.path.append(os.getcwd())

# Mock environment
os.environ["BASE_PATH"] = "/opds"
os.environ["AUTH_ENABLED"] = "false"

from opds_abs.main import app

client = TestClient(app)

def test_root_redirect():
    # Test the redirect from /
    # Since root_path is /opds, we need to request /opds/ or use the client with base_url
    # TestClient handle root_path by prepending it if we use the right base_url or just request it
    
    print("\nRequesting /opds/")
    response = client.get("/", follow_redirects=False)
    print(f"Status: {response.status_code}")
    print(f"Location Header: {response.headers.get(\"location\")}")

if __name__ == "__main__":
    test_root_redirect()
