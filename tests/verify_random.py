import sys
import os
import sqlite3
from fastapi.testclient import TestClient

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from xer.database import get_connection

client = TestClient(app)


def test_random_tale_basic():
    print("\nTesting /api/v1/tales/random Basic Response...")
    response = client.get("/api/v1/tales/random")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "title" in data
    assert "text" in data
    assert "selection_count" in data
    print(
        f"Success: Received tale '{data['title']}' with ID {data['id']} and count {data['selection_count']}"
    )


def test_random_fairness():
    print("\nTesting Selection Fairness...")

    # Get total number of tales
    with get_connection() as conn:
        total_tales = conn.execute("SELECT COUNT(*) FROM tales").fetchone()[0]

    print(f"Total tales in DB: {total_tales}")

    selected_ids = set()
    for i in range(total_tales):
        response = client.get("/api/v1/tales/random")
        assert response.status_code == 200
        tale_id = response.json()["id"]
        selected_ids.add(tale_id)
        print(f"Iteration {i + 1}: Selected ID {tale_id}")

    print(f"Unique tales selected: {len(selected_ids)}/{total_tales}")
    assert len(selected_ids) == total_tales, (
        "Not all tales were selected before repeating!"
    )
    print("Fairness test passed: All stories appeared exactly once before any repeat.")


if __name__ == "__main__":
    try:
        test_random_tale_basic()
        test_random_fairness()
    except Exception as e:
        print(f"Failure: {e}")
        sys.exit(1)
