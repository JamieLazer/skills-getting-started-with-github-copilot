"""Tests for the GET /activities endpoint using AAA pattern."""

import pytest


class TestGetActivities:
    """Test suite for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all available activities.
        
        AAA Pattern:
        - Arrange: Prepare the test client
        - Act: Make GET request to /activities
        - Assert: Verify response status and contains activity data
        """
        # Arrange
        # (client fixture is already set up)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_get_activities_response_contains_expected_fields(self, client):
        """
        Test that each activity has required fields in the response.
        
        AAA Pattern:
        - Arrange: Define expected activity fields
        - Act: Make GET request and check first activity
        - Assert: Verify all required fields are present
        """
        # Arrange
        required_fields = {
            "description",
            "schedule",
            "max_participants",
            "participants"
        }

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_details in activities.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_details, dict)
            assert required_fields.issubset(activity_details.keys())

    def test_get_activities_participants_is_list(self, client):
        """
        Test that participants field is always a list.
        
        AAA Pattern:
        - Arrange: Prepare test client
        - Act: Fetch activities
        - Assert: Verify participants is a list for all activities
        """
        # Arrange
        # (client fixture is already set up)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_details in activities.values():
            assert isinstance(activity_details["participants"], list)
            for participant in activity_details["participants"]:
                assert isinstance(participant, str)

    def test_get_activities_chess_club_exists(self, client, existing_activity):
        """
        Test that the Chess Club activity exists in the response.
        
        AAA Pattern:
        - Arrange: Set expected activity name
        - Act: Fetch activities
        - Assert: Verify Chess Club exists in response
        """
        # Arrange
        expected_activity = existing_activity

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert expected_activity in data

    def test_get_activities_response_structure(self, client):
        """
        Test the overall structure of the activities response.
        
        AAA Pattern:
        - Arrange: Define expected structure
        - Act: Fetch activities
        - Assert: Validate structure matches expectations
        """
        # Arrange
        # Expected structure: {activity_name: {description, schedule, max_participants, participants}}

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert isinstance(data, dict)
        assert all(
            isinstance(name, str) and isinstance(details, dict)
            for name, details in data.items()
        )
        assert all(
            isinstance(details["max_participants"], int)
            and details["max_participants"] > 0
            for details in data.values()
        )

    def test_get_activities_max_participants_positive(self, client):
        """
        Test that max_participants is always a positive integer.
        
        AAA Pattern:
        - Arrange: Prepare test client
        - Act: Fetch activities
        - Assert: Verify max_participants > 0 for all activities
        """
        # Arrange
        # (client fixture is already set up)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity in activities.values():
            assert isinstance(activity["max_participants"], int)
            assert activity["max_participants"] > 0

    def test_get_activities_participants_count_not_exceeds_max(self, client):
        """
        Test that actual participants count doesn't exceed max_participants.
        
        AAA Pattern:
        - Arrange: Prepare test client
        - Act: Fetch activities
        - Assert: Verify participants <= max_participants
        """
        # Arrange
        # (client fixture is already set up)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity in activities.values():
            assert len(activity["participants"]) <= activity["max_participants"]
