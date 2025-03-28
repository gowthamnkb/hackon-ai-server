from __future__ import annotations

import httpx
from openai import AsyncAzureOpenAI, DefaultAsyncHttpxClient

from . import _openai_shared
from .interface import Model, ModelProvider
from .openai_chatcompletions import OpenAIChatCompletionsModel
from .openai_responses import OpenAIResponsesModel

DEFAULT_MODEL: str = "gpt-4o"


_http_client: httpx.AsyncClient | None = None


# If we create a new httpx client for each request, that would mean no sharing of connection pools,
# which would mean worse latency and resource usage. So, we share the client across requests.
def shared_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None:
        _http_client = DefaultAsyncHttpxClient()
    return _http_client


class OpenAIProvider(ModelProvider):
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        openai_client: AsyncAzureOpenAI | None = None,
        organization: str | None = None,
        project: str | None = None,
        use_responses: bool | None = None,
        api_version: str | None = None,
    ) -> None:
        self.api_version = None
        if openai_client is not None:
            assert api_key is None and base_url is None, (
                "Don't provide api_key or base_url if you provide openai_client"
            )
            self._client: AsyncAzureOpenAI | None = openai_client
        else:
            self._client = None
            self._stored_api_key = api_key
            self._stored_base_url = base_url
            self._stored_organization = organization
            self._stored_project = project

        if use_responses is not None:
            self._use_responses = use_responses
        else:
            self._use_responses = _openai_shared.get_use_responses_by_default()

    # We lazy load the client in case you never actually use OpenAIProvider(). Otherwise
    # AsyncOpenAI() raises an error if you don't have an API key set.
    def _get_client(self) -> AsyncAzureOpenAI:
        if self._client is None:
            self._stored_api_key = "G8H494sbtvOtW0nmKAiDPaSnhsXliRGuFF0xMPK2Ni6h5RT0cx7hJQQJ99BCACfhMk5XJ3w3AAABACOGAOC7"
            self._stored_base_url = "https://exp-e2etest-analysis.openai.azure.com/openai/deployments/engage-hackon-fy25/chat/completions?api-version=2024-10-21"
            self.api_version = "2024-10-21"
            # print("self._stored_api_key is - ", self._stored_api_key)
            # print("self._stored_base_url is - ", self._stored_base_url)
            # print("self._stored_base_url is - ", self.api_version)
            self._client = _openai_shared.get_default_openai_client() or AsyncAzureOpenAI(
                api_key=self._stored_api_key or _openai_shared.get_default_openai_key(),
                base_url=self._stored_base_url,
                organization=self._stored_organization,
                project=self._stored_project,
                http_client=shared_http_client(),
                api_version=self.api_version
            )

        return self._client

    def get_model(self, model_name: str | None) -> Model:
        if model_name is None:
            model_name = DEFAULT_MODEL
        # print("m anme is - ", model_name)

        client = self._get_client()

        return (
            # OpenAIResponsesModel(model=model_name, openai_client=client)
            # if self._use_responses
            OpenAIChatCompletionsModel(model=model_name, openai_client=client)
        )
