from pydantic import BaseModel, Field

class RunGmailAgentRequest(BaseModel):
    user_id: str = Field(
        ...,
        description="The user id of the user to run the Gmail agent for.",
    )
    prompt: str = Field(
        ...,
        description="The prompt to run the Gmail agent for.",
    )

class CreateConnectionRequest(BaseModel):
    user_id: str = Field(
        ...,
        description="The user id of the user to create a connection for.",
    )
    auth_config_id: str = Field(
        ...,
        description="The auth config id of the user to create a connection for.",
    )

class WaitForConnectionRequest(BaseModel):
    user_id: str = Field(
        ...,
        description="The user id of the user to wait for a connection for.",
    )
    connection_id: str = Field(
        ...,
        description="The connection id of the user to wait for a connection for.",
    )

class FetchEmailsRequest(BaseModel):
    user_id: str = Field(
        ...,
        description="The user id of the user to fetch emails for.",
    )
    limit: int = Field(
        5,
        description="The limit of emails to fetch.",
    )


class GPTCustomization(BaseModel):
    purpose: str = Field(
        ...,
        description="High-level purpose of the customized GPT behavior.",
    )
    instructions: str = Field(
        ...,
        description="Detailed system instructions for the assistant.",
    )
    model: str = Field(
        "gpt-4.1",
        description="OpenAI model to use for this customized GPT.",
    )


class RunCustomGptRequest(BaseModel):
    user_id: str = Field(
        ...,
        description="The user id of the user to run the custom GPT for.",
    )
    prompt: str = Field(
        ...,
        description="The user message for the customized GPT.",
    )
    customization: GPTCustomization = Field(
        ...,
        description="Customization profile that defines this GPT's behavior.",
    )
