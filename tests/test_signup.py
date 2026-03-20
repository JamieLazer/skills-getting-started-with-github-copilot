"""Tests for the POST /activities/{activity_name}/signup endpoint using AAA pattern."""

import pytest


class TestSignupForActivity:
    """Test suite for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful_for_valid_activity(self, client, existing_activity, sample_email):
        """
        Test successful signup for a valid activity with a valid email.
        
        AAA Pattern:
        - Arrange: Prepare activity name and unique email
        - Act: Make POST request to signup endpoint
        - Assert: Verify success response and user is added
        """
        # Arrange
        activity_name = existing_activity
        email = sample_email
        unique_email = f"unique_{email}"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": unique_email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert unique_email in data["message"]
        assert activity_name in data["message"]

    def test_signup_returns_correct_message_format(self, client, existing_activity, sample_email):
        """
        Test that signup response has the correct message format.
        
        AAA Pattern:
        - Arrange: Set up activity and email
        - Act: Make signup request
        - Assert: Verify message format
        """
        # Arrange
        activity_name = existing_activity
        email = f"format_test_{sample_email}"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity_name}"

    def test_signup_fails_for_nonexistent_activity(self, client, nonexistent_activity, sample_email):
        """
        Test that signup fails with 404 for a nonexistent activity.
        
        AAA Pattern:
        - Arrange: Set up nonexistent activity name
        - Act: Attempt signup for nonexistent activity
        - Assert: Verify 404 error with appropriate message
        """
        # Arrange
        activity_name = nonexistent_activity
        email = sample_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data.get("detail", "")

    def test_signup_fails_for_duplicate_signup(self, client, existing_activity):
        """
        Test that duplicate signup for same activity fails with 400.
        
        AAA Pattern:
        - Arrange: Sign up a student once
        - Act: Attempt to sign up the same student again
        - Assert: Verify 400 error for duplicate
        """
        # Arrange
        activity_name = existing_activity
        email = "duplicate_test@mergington.edu"
        
        # First signup
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data.get("detail", "")

    def test_signup_with_invalid_email_format(self, client, existing_activity):
        """
        Test signup with various email formats (valid and invalid).
        
        AAA Pattern:
        - Arrange: Prepare various email formats
        - Act: Attempt signal with each email
        - Assert: Verify endpoint accepts the email (validation is flexible)
        """
        # Arrange
        activity_name = existing_activity
        emails = [
            "valid.email@school.edu",
            "student123@mergington.edu",
            "simpleemail",  # May be accepted by endpoint
        ]

        # Act & Assert
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            # Should either succeed or fail consistently
            assert response.status_code in [200, 400]

    def test_signup_without_email_parameter(self, client, existing_activity):
        """
        Test that signup fails when email parameter is missing.
        
        AAA Pattern:
        - Arrange: Prepare activity without email
        - Act: Make signup request without email
        - Assert: Verify error response
        """
        # Arrange
        activity_name = existing_activity

        # Act
        response = client.post(f"/activities/{activity_name}/signup")

        # Assert
        # FastAPI will return 422 Unprocessable Entity for missing parameter
        assert response.status_code == 422

    def test_signup_persists_across_multiple_requests(self, client, existing_activity):
        """
        Test that signup persists and affects subsequent activity queries.
        
        AAA Pattern:
        - Arrange: Get initial participant count
        - Act: Sign up a new student
        - Assert: Verify participant count increased in subsequent request
        """
        # Arrange
        activity_name = existing_activity
        email = "persistence_test@mergington.edu"
        
        # Get initial state
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[activity_name]["participants"]
        initial_count = len(initial_participants)

        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert signup_response.status_code == 200
        
        # Verify in subsequent request
        subsequent_response = client.get("/activities")
        updated_participants = subsequent_response.json()[activity_name]["participants"]
        assert len(updated_participants) == initial_count + 1
        assert email in updated_participants

    def test_signup_multiple_different_students_same_activity(self, client, existing_activity):
        """
        Test that multiple different students can sign up for the same activity.
        
        AAA Pattern:
        - Arrange: Prepare multiple unique emails
        - Act: Sign up each student
        - Assert: Verify all signups succeed
        """
        # Arrange
        activity_name = existing_activity
        emails = [
            f"student_multi_1@mergington.edu",
            f"student_multi_2@mergington.edu",
            f"student_multi_3@mergington.edu",
        ]

        # Act & Assert
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

    def test_signup_case_sensitive_activity_name(self, client):
        """
        Test signup behavior with different case variations of activity name.
        
        AAA Pattern:
        - Arrange: Prepare case variations of activity name
        - Act: Attempt signup with different cases
        - Assert: Verify case sensitivity handling
        """
        # Arrange
        correct_name = "Chess Club"
        email = "case_test@mergington.edu"

        # Act - Try with correct case
        response_correct = client.post(
            f"/activities/{correct_name}/signup",
            params={"email": email}
        )

        # Act - Try with wrong case
        response_wrong_case = client.post(
            f"/activities/chess club/signup",
            params={"email": f"case_test2_{email}"}
        )

        # Assert
        assert response_correct.status_code == 200
        assert response_wrong_case.status_code == 404  # Should be case-sensitive
