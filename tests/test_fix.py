import os
import sys
from fastapi.testclient import TestClient

# Mock Environment
os.environ["BASE_PATH"] = "/opds"
os.environ["AUTH_ENABLED"] = "true"

sys.path.append(os.getcwd())

from opds_abs.main import app, build_url
from opds_abs.utils.auth_utils import require_auth

# Mock require_auth to return a success
async def mock_require_auth():
    return ("josh.knutson", "mock_token", "josh.knutson")

app.dependency_overrides[require_auth] = mock_require_auth

client = TestClient(app)

def test_redirect():
    print(f"BASE_PATH is: {os.environ.get('BASE_PATH')}")
    print(f"build_url('/josh.knutson') -> {build_url('/josh.knutson')}")
    
    # Test the root redirect
    response = client.get("/", follow_redirects=False)
    print(f"GET / -> Status {response.status_code}, Location: {response.headers.get('location')}")

if __name__ == "__main__":
    test_redirect()
