def test_get_activities_returns_activity_details(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert {
        "description",
        "schedule",
        "max_participants",
        "participants",
    } <= activities["Chess Club"].keys()


def test_student_can_sign_up_for_activity(client):
    email = "student@mergington.edu"

    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email in response.json()["message"]
    assert email in client.get("/activities").json()["Chess Club"]["participants"]


def test_student_cannot_sign_up_twice_for_activity(client):
    email = "newstudent@mergington.edu"
    signup_url = "/activities/Chess%20Club/signup"

    first_response = client.post(signup_url, params={"email": email})
    second_response = client.post(signup_url, params={"email": email})

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == (
        "Student already signed up for this activity"
    )
    participants = client.get("/activities").json()["Chess Club"]["participants"]
    assert participants.count(email) == 1


def test_sign_up_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_student_can_unregister_from_activity(client):
    email = "michael@mergington.edu"
    unregister_url = "/activities/Chess%20Club/signup"

    response = client.delete(unregister_url, params={"email": email})

    assert response.status_code == 200
    assert email in response.json()["message"]
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]


def test_unregister_rejects_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_student_not_signed_up(client):
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "notregistered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up"
