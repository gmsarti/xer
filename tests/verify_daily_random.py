import sys
import os
from fastapi.testclient import TestClient

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def test_random_with_seed():
    print("\nTesting /api/v1/tales/random with Seed...")
    seed = "test-seed-123"

    # First call with increment=False
    response1 = client.get(f"/api/v1/tales/random?seed={seed}&increment=false")
    assert response1.status_code == 200
    data1 = response1.json()

    # Second call with same seed and increment=False
    response2 = client.get(f"/api/v1/tales/random?seed={seed}&increment=false")
    assert response2.status_code == 200
    data2 = response2.json()

    assert data1["id"] == data2["id"], (
        "Seed consistency failed! Different stories for same seed."
    )
    assert data1["selection_count"] == data2["selection_count"], (
        "Increment happened despite increment=false"
    )
    print(f"Success: Consistency for seed '{seed}' verified (ID: {data1['id']})")


def test_daily_tale_persistence():
    print("\nTesting /api/v1/tales/daily Persistence...")

    # First call to daily
    response1 = client.get("/api/v1/tales/daily")
    assert response1.status_code == 200
    data1 = response1.json()

    # Second call to daily
    response2 = client.get("/api/v1/tales/daily")
    assert response2.status_code == 200
    data2 = response2.json()

    assert data1["id"] == data2["id"], "Daily tale changed! Persistence failed."
    print(f"Success: Daily tale is stable (ID: {data1['id']})")


def test_random_increment():
    print("\nTesting /api/v1/tales/random Increment...")

    # Get a random tale and note its count
    response1 = client.get("/api/v1/tales/random?increment=false")
    tale_id = response1.json()["id"]
    initial_count = response1.json()["selection_count"]

    # Now call specifically for that ID or just call random until we hit it?
    # Better: just call random with increment=true once and check if ANY record increased.
    # Or specifically test the increment logic by calling /random?increment=true

    response2 = client.get("/api/v1/tales/random?increment=true")
    new_tale_id = response2.json()["id"]
    new_count = response2.json()["selection_count"]

    # Check if the returned tale has an updated count (it should be initial + 1 if it was grabbed from DB)
    # Actually, get_random_tale increments and THEN returns the tale with get_tale.
    # Let's verify by calling again for that ID.

    verify_response = client.get(f"/api/v1/tales/{new_tale_id}")
    final_count = verify_response.json()["selection_count"]

    assert final_count >= 1, "Selection count did not increment"
    print(f"Success: Selection count for ID {new_tale_id} is {final_count}")


if __name__ == "__main__":
    try:
        test_random_with_seed()
        test_daily_tale_persistence()
        test_random_increment()
        print("\nAll tests passed!")
    except Exception as e:
        print(f"\nFailure: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
