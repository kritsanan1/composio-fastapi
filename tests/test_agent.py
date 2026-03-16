import unittest
from unittest.mock import Mock

from simple_gmail_agent.agent import run_gmail_agent


class RunGmailAgentTests(unittest.TestCase):
    def test_run_gmail_agent_uses_custom_model_and_system_prompt(self):
        composio_client = Mock()
        openai_client = Mock()

        tools_payload = [{"type": "function", "function": {"name": "GMAIL_FETCH_EMAILS"}}]
        composio_client.tools.get.return_value = tools_payload

        response_payload = {"id": "resp_123"}
        openai_client.chat.completions.create.return_value = response_payload

        handled_payload = [{"tool": "GMAIL_FETCH_EMAILS", "status": "ok"}]
        composio_client.provider.handle_tool_calls.return_value = handled_payload

        result = run_gmail_agent(
            composio_client=composio_client,
            openai_client=openai_client,
            user_id="user-1",
            prompt="Summarize latest messages",
            system_prompt="You are an inbox triage assistant.",
            model="gpt-4.1-mini",
        )

        self.assertEqual(result, handled_payload)
        composio_client.tools.get.assert_called_once_with(
            user_id="user-1",
            tools=[
                "GMAIL_FETCH_EMAILS",
                "GMAIL_SEND_EMAIL",
                "GMAIL_CREATE_EMAIL_DRAFT",
            ],
        )
        openai_client.chat.completions.create.assert_called_once_with(
            model="gpt-4.1-mini",
            tools=tools_payload,
            messages=[
                {"role": "system", "content": "You are an inbox triage assistant."},
                {"role": "user", "content": "Summarize latest messages"},
            ],
        )
        composio_client.provider.handle_tool_calls.assert_called_once_with(
            response=response_payload,
            user_id="user-1",
        )


if __name__ == "__main__":
    unittest.main()
