# tests/test_app.py
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    # Arrange: No special setup needed
    
    # Act: Make a GET request to the root endpoint
    response = client.get("/")
    
    # Assert: Check that it redirects to the static HTML
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_get_activities():
    # Arrange: No special setup needed (uses in-memory data)
    
    # Act: Fetch all activities
    response = client.get("/activities")
    
    # Assert: Verify response structure and content
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success():
    # Arrange: Use a unique email to avoid conflicts
    email = "success@example.com"
    
    # Act: Attempt to sign up for an activity
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    
    # Assert: Check for success message
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]

def test_signup_duplicate():
    # Arrange: Sign up once first
    email = "duplicate@example.com"
    client.post(f"/activities/Chess Club/signup?email={email}")
    
    # Act: Try to sign up again with the same email
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    
    # Assert: Should fail with duplicate error
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_activity_not_found():
    # Arrange: Use a non-existent activity name
    email = "notfound@example.com"
    
    # Act: Attempt to sign up for a non-existent activity
    response = client.post(f"/activities/Nonexistent Activity/signup?email={email}")
    
    # Assert: Should return 404
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # Arrange: Sign up first, then unregister
    email = "unregister@example.com"
    client.post(f"/activities/Chess Club/signup?email={email}")
    
    # Act: Unregister the participant
    response = client.delete(f"/activities/Chess Club/signup?email={email}")
    
    # Assert: Check for success message
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]

def test_unregister_not_signed_up():
    # Arrange: Use an email not signed up
    email = "notsigned@example.com"
    
    # Act: Try to unregister without being signed up
    response = client.delete(f"/activities/Chess Club/signup?email={email}")
    
    # Assert: Should fail
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]

def test_unregister_activity_not_found():
    # Arrange: Use a non-existent activity
    email = "notfound@example.com"
    
    # Act: Attempt to unregister from a non-existent activity
    response = client.delete(f"/activities/Nonexistent Activity/signup?email={email}")
    
    # Assert: Should return 404
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]