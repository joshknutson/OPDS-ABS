
import os
import sys

# Add current directory to sys.path
sys.path.append(os.getcwd())

from opds_abs.config import BASE_PATH
from opds_abs.main import build_url

def test_build_url(test_base_path):
    print(f"\nTesting with BASE_PATH=\"{test_base_path}\"")
    # Manually override for testing
    import opds_abs.main
    opds_abs.main.BASE_PATH = test_base_path
    
    paths = ["/", "/josh", "/opds/josh", "anonymous"]
    for p in paths:
        print(f"  build_url(\"{p}\") -> {build_url(p)}")

if __name__ == "__main__":
    test_build_url("")
    test_build_url("/opds")
    test_build_url("/service")
