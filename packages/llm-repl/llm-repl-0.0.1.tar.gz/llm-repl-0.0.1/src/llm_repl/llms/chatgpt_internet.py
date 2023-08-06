from __future__ import annotations

import os

from typing import Optional, Any

from langchain.callbacks.base import CallbackManager
from langchain import LLMChain
from langchain.schema import LLMResult
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, PromptTemplate

from langchain.agents import load_tools, AgentExecutor, ZeroShotAgent

from rich.markdown import Markdown

from llm_repl.repl import LLMRepl
from llm_repl.llms import BaseLLM, StreamingCallbackHandler


class ChatGPTInternetCallbackHandler(StreamingCallbackHandler):

    def __init__(self, repl: LLMRepl) -> None:
        super().__init__()
        self.console = repl.console
        self.server_color = repl.server_color
        self.is_code_mode = False
        self.code_block = ""

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        # FIXME: This is just an hack to make the code blocks work
        #        This should be done properly in the future
        if token == "\n\n":
            token = ""
        if token == "``" or token == "```":
            if self.code_block:
                self.console.print(Markdown(self.code_block + "```\n"))
                self.code_block = ""
                self.is_code_mode = not self.is_code_mode
                return
            self.is_code_mode = not self.is_code_mode
            self.code_block = token
        elif self.is_code_mode:
            self.code_block += token
        else:
            if token == "`\n" or token == "`\n\n":
                token = "\n"
            self.console.print(token, end="")


class ChatGPTInternet(BaseLLM):
    def __init__(self, api_key: str, repl: LLMRepl):
        self.api_key = api_key
        # TODO: Make options configurable
        self.streaming_mode = True

        # TODO: Make it customizable
        # prompt = ChatPromptTemplate.from_messages(
        #     [
        #         SystemMessagePromptTemplate.from_template(
        #             """
        #     If AI does not know the answer to a question, it truthfully says it does not know.
        #     """
        #         ),
        #         MessagesPlaceholder(variable_name="history"),
        #         HumanMessagePromptTemplate.from_template("{input}"),
        #     ]
        # )

        template = """This is a conversation between a human and a bot:

        {history}

        Answer for {input}:
        """

        llm = OpenAI(
            openai_api_key=self.api_key,
            streaming=self.streaming_mode,
            callback_manager=CallbackManager([ChatGPTInternetCallbackHandler(repl)]),
            verbose=True,
            # temperature=0,
        )  # type: ignore
        tools = load_tools(["serpapi", "llm-math"], llm=llm)
        prompt = ZeroShotAgent.create_prompt(tools=tools)
        memory = ConversationBufferMemory(return_messages=True)
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=False)
        agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=False, memory=memory)
        self.model = agent_chain

    @property
    def is_in_streaming_mode(self) -> bool:
        return self.streaming_mode

    @classmethod
    def load(cls, repl: LLMRepl) -> Optional[BaseLLM]:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            repl.print_error_msg(
                "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
            )
            return None

        # TODO: Add autocomplete in repl
        model = cls(api_key, repl)
        return model

    def process(self, msg: str) -> str:
        resp = self.model.run(input=msg)
        return resp.strip()
