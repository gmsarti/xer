import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_list_tales():
    response = client.get("/api/v1/tales")
    assert response.status_code == 200
    data = response.json()
    assert "tales" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert isinstance(data["tales"], list)
    # Check default page size
    assert data["page_size"] == 20

def test_get_tale_detail():
    # First get a list to find a valid ID
    list_response = client.get("/api/v1/tales")
    if list_response.status_code == 200 and list_response.json()["tales"]:
        tale_id = list_response.json()["tales"][0]["id"]
        
        response = client.get(f"/api/v1/tales/{tale_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == tale_id
        assert "title" in data
        assert "text" in data
        assert "classifications" in data

def test_get_tale_not_found():
    response = client.get("/api/v1/tales/999999999")
    assert response.status_code == 404

def test_search_tales_by_title():
    # Search for a common term
    response = client.get("/api/v1/tales/search?title=The")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["tales"], list)
    if data["tales"]:
        assert "The" in data["tales"][0]["title"]

def test_search_tales_by_classification():
    # Assuming seed data exists: ATU 333
    response = client.get("/api/v1/tales/search?classification=ATU 333")
    assert response.status_code == 200
    data = response.json()
    # If we have data, verify structure
    if data["tales"]:
        tale = data["tales"][0]
        class_names = [c["name"] for c in tale["classifications"]]
        assert "ATU 333" in class_names

def test_search_keywords_fallback():
    # Test the keyword search (fallback to LIKE since FTS might not be there)
    response = client.get("/api/v1/tales/keywords?q=forest")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["tales"], list)
