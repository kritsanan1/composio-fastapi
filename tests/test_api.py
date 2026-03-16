import unittest
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from simple_gmail_agent.server.api import create_app
from simple_gmail_agent.server.dependencies import (
    provide_composio_client,
    provide_openai_client,
)


class ApiCustomGptTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.dependency_overrides[provide_composio_client] = lambda: Mock()
        self.app.dependency_overrides[provide_openai_client] = lambda: Mock()
        self.client = TestClient(self.app)

    def tearDown(self):
        self.app.dependency_overrides.clear()

    @patch("simple_gmail_agent.server.api.run_gmail_agent")
    @patch("simple_gmail_agent.server.api.check_connected_account_exists", return_value=True)
    def test_agent_custom_builds_system_prompt_from_customization(
        self,
        _mock_connected,
        mock_run_gmail_agent,
    ):
        mock_run_gmail_agent.return_value = [{"data": {}, "error": None, "successful": True}]

        payload = {
            "user_id": "user-42",
            "prompt": "Draft a payment follow-up",
            "customization": {
                "purpose": "Finance assistant",
                "instructions": "Use concise and professional language.",
                "model": "gpt-4.1",
            },
        }

        response = self.client.post("/agent/custom", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"data": {}, "error": None, "successful": True}])
        mock_run_gmail_agent.assert_called_once()
        kwargs = mock_run_gmail_agent.call_args.kwargs
        self.assertEqual(kwargs["user_id"], "user-42")
        self.assertEqual(kwargs["prompt"], "Draft a payment follow-up")
        self.assertEqual(kwargs["model"], "gpt-4.1")
        self.assertEqual(
            kwargs["system_prompt"],
            "Purpose: Finance assistant\nInstructions: Use concise and professional language.",
        )

    @patch("simple_gmail_agent.server.api.run_gmail_agent")
    @patch("simple_gmail_agent.server.api.check_connected_account_exists", return_value=True)
    def test_agent_endpoint_uses_request_user_id(
        self,
        _mock_connected,
        mock_run_gmail_agent,
    ):
        mock_run_gmail_agent.return_value = [{"data": {}, "error": None, "successful": True}]

        payload = {
            "user_id": "real-user",
            "prompt": "List latest unread emails",
        }

        response = self.client.post("/agent", json=payload)

        self.assertEqual(response.status_code, 200)
        kwargs = mock_run_gmail_agent.call_args.kwargs
        self.assertEqual(kwargs["user_id"], "real-user")
        self.assertEqual(kwargs["system_prompt"], "You are a helpful Gmail assistant.")


if __name__ == "__main__":
    unittest.main()
