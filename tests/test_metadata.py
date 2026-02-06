import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_tale_metadata_conjugation():
    # Get a list of tales
    response = client.get("/api/v1/tales")
    assert response.status_code == 200
    data = response.json()
    tales = data["tales"]

    if tales:
        for tale in tales:
            # Check if metadata is present if author or region exists
            # We can't be sure about the data in the DB without more queries,
            # but we can check if the field exists in the response.
            assert "metadata" in tale
            assert "author" in tale
            assert "region" in tale

            # If we find one with both, verify conjugation
            if tale["author"] and tale["region"]:
                assert f"{tale['author']} ({tale['region']})" == tale["metadata"]
            elif tale["author"]:
                assert tale["author"] == tale["metadata"]
            elif tale["region"]:
                assert tale["region"] == tale["metadata"]


def test_tale_detail_metadata():
    # Get first tale ID
    list_response = client.get("/api/v1/tales")
    if list_response.status_code == 200 and list_response.json()["tales"]:
        tale_id = list_response.json()["tales"][0]["id"]

        response = client.get(f"/api/v1/tales/{tale_id}")
        assert response.status_code == 200
        data = response.json()

        assert "metadata" in data
        assert "author" in data
        assert "region" in data

        # Verify conjugation logic
        expected_metadata = None
        author = data["author"]
        region = data["region"]
        if author and region:
            expected_metadata = f"{author} ({region})"
        elif author:
            expected_metadata = author
        elif region:
            expected_metadata = region

        assert data["metadata"] == expected_metadata
