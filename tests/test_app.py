import app as portal

def test_valid_submission_is_saved_and_displayed(client, tmp_path, monkeypatch):
    monkeypatch.setattr(portal, "SUBMISSIONS_FILE", tmp_path / "submissions.json")
    response = client.post("/submit", data={
        "name": "Hussain Raza",
        "registration_number": "FA23-BAI-019",
        "assignment_title": "DevOps Lab Mid",
        "submission_url": "https://example.com/my-assignment"
    })
    assert response.status_code == 200
    assert b"Submission saved successfully" in response.data
    assert b"Hussain Raza" in response.data
    assert len(portal.load_submissions()) == 1

def test_missing_registration_number_is_rejected(client, tmp_path, monkeypatch):
    monkeypatch.setattr(portal, "SUBMISSIONS_FILE", tmp_path / "submissions.json")
    response = client.post("/submit", data={
        "name": "Hussain Raza",
        "registration_number": "",
        "assignment_title": "DevOps Lab Mid",
        "submission_url": "https://example.com/task"
    })
    assert response.status_code == 400
    assert b"Registration Number is required" in response.data
    assert portal.load_submissions() == []

def test_invalid_url_is_rejected_and_not_saved(client, tmp_path, monkeypatch):
    monkeypatch.setattr(portal, "SUBMISSIONS_FILE", tmp_path / "submissions.json")
    response = client.post("/submit", data={
        "name": "Hussain Raza",
        "registration_number": "FA23-BAI-019",
        "assignment_title": "DevOps Lab Mid",
        "submission_url": "not-a-valid-url"
    })
    assert response.status_code == 400
    assert b"valid HTTP or HTTPS" in response.data
    assert portal.load_submissions() == []

import pytest

@pytest.fixture
def client():
    portal.app.config["TESTING"] = True
    with portal.app.test_client() as test_client:
        yield test_client
