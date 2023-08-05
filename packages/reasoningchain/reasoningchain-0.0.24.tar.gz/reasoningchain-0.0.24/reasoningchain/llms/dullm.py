#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Wrapper around OpenAI APIs."""
from typing import Any, Dict, List, Mapping, Optional
import requests
import json
import os
import sys

from typing import Union, Tuple

from pydantic import BaseModel, Extra, Field, root_validator

from langchain.llms.base import BaseLLM
from langchain.schema import Generation, LLMResult
from langchain.utils import get_from_dict_or_env

class DuLLM(BaseLLM, BaseModel):
    client: Any  #: :meta private:
    model_name: str = "glm-10b"
    """Model name to use."""
    temperature: float = 0.7
    """What sampling temperature to use."""
    max_tokens: int = 256
    """The maximum number of tokens to generate in the completion.
    -1 returns as many tokens as possible given the prompt and
    the models maximal context size."""
    top_p: float = 1
    """Total probability mass of tokens to consider at each step."""
    frequency_penalty: float = 0
    """Penalizes repeated tokens according to frequency."""
    presence_penalty: float = 0
    """Penalizes repeated tokens."""
    n: int = 1
    """How many completions to generate for each prompt."""
    best_of: int = 1
    """Generates best_of completions server-side and returns the "best"."""
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    """Holds any model parameters valid for `create` call not explicitly specified."""
    openai_api_key: Optional[str] = None
    batch_size: int = 20
    """Batch size to use when passing multiple documents to generate."""
    request_timeout: Optional[Union[float, Tuple[float, float]]] = None
    """Timeout for requests to OpenAI completion API. Default is 600 seconds."""
    logit_bias: Optional[Dict[str, float]] = Field(default_factory=dict)
    """Adjust the probability of specific tokens being generated."""
    max_retries: int = 6
    """Maximum number of retries to make when generating."""
    streaming: bool = False
    """Whether to stream the results or not."""

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.ignore

    @root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Build extra kwargs from additional params that were passed in."""
        all_required_field_names = {field.alias for field in cls.__fields__.values()}

        extra = values.get("model_kwargs", {})
        for field_name in list(values):
            if field_name not in all_required_field_names:
                if field_name in extra:
                    raise ValueError(f"Found {field_name} supplied twice.")
                extra[field_name] = values.pop(field_name)
        values["model_kwargs"] = extra
        return values

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        values["client"] = '-'
        if values["streaming"] and values["n"] > 1:
            raise ValueError("Cannot stream results when n > 1.")
        if values["streaming"] and values["best_of"] > 1:
            raise ValueError("Cannot stream results when best_of > 1.")
        return values

    @property
    def _default_params(self) -> Dict[str, Any]:
        """Get the default parameters for calling OpenAI API."""
        normal_params = {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "n": self.n,
            "best_of": self.best_of,
            "request_timeout": self.request_timeout,
            "logit_bias": self.logit_bias,
        }
        return {**normal_params, **self.model_kwargs}

    def _generate(
        self, prompts: List[str], stop: Optional[List[str]] = None
    ) -> LLMResult:
        choices = []
        for prompt in prompts:
            res = self.generate_answer(prompt, stop)
            choices.append(res)
        return self.create_llm_result(choices, prompts, {})

    async def _agenerate(
        self, prompts: List[str], stop: Optional[List[str]] = None
    ) -> LLMResult:
        """Call out to OpenAI's endpoint async with k unique prompts."""
        choices = []
        for prompt in prompts:
            res = self.generate_answer(prompt, stop)
            choices.append(res)
        return self.create_llm_result(choices, prompts, token_usage)

    def generate_answer(self, prompt:str, stop:list=[]) -> str:
        if not stop:
            stop = []
        req = {
            **self._default_params,
            "input":prompt,
            "model_type":self.model_name,
        }
        DU_LLM_API = os.environ['DU_LLM_API']

        resp = requests.post(DU_LLM_API, json=req)
        if resp.status_code >= 300:
            raise RuntimeError(f"Request DuLLM(self.model_name) failed with http status:{resp.status_code}")

        res = json.loads(resp.content)
        if res['status'] != 0:
            raise RuntimeError(f"Request DuLLM(self.model_name) failed with api status:{res['status']}, msg:{res['msg']}")
        
        answer = res['data']['output'].lstrip('<|startofpiece|>')
        finish_reason = "end"
        for item in stop:
            pos = answer.find(item)
            if pos >= 0:
                answer = answer[:pos+len(item)]
                finish_reason = "stop"
        return {"text":answer, "finish_reason":finish_reason}

    def create_llm_result(
        self, choices: Any, prompts: List[str], token_usage: Dict[str, int]
    ) -> LLMResult:
        """Create the LLMResult from the choices and prompts."""
        generations = []
        for i, prompt in enumerate(prompts):
            res = choices[i]
            print(res)
            generations.append(
                [
                    Generation(
                        text=res['text'],
                        generation_info=dict(
                            finish_reason=res['finish_reason'],
                            logprobs=1.0,
                        ),
                    )
                ]
            )
        llm_output = {"token_usage": token_usage, "model_name": self.model_name}
        return LLMResult(generations=generations, llm_output=llm_output)

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {**{"model_name": self.model_name}, **self._default_params}

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "dullm"

    def get_num_tokens(self, text: str) -> int:
        """Calculate num tokens with tiktoken package."""
        # calculate the number of tokens in the encoded text
        return len(text)

    def modelname_to_contextsize(self, modelname: str) -> int:
        if modelname == "glm-10b":
            return 4097
        elif modelname == "bloomz_7b1":
            return 4000
        else:
            return 4097

    def max_tokens_for_prompt(self, prompt: str) -> int:
        """Calculate the maximum number of tokens possible to generate for a prompt.

        Args:
            prompt: The prompt to pass into the model.

        Returns:
            The maximum number of tokens to generate for a prompt.

        Example:
            .. code-block:: python

                max_tokens = openai.max_token_for_prompt("Tell me a joke.")
        """
        num_tokens = self.get_num_tokens(prompt)

        # get max context size for model by name
        max_size = self.modelname_to_contextsize(self.model_name)
        return max_size - num_tokens

if __name__ == '__main__':
    prompt = "My name is "
    if len(sys.argv) > 1:
        prompt = sys.argv[1]

    llm = DuLLM(model_name="glm-10b", max_tokens=1000)

    answer = llm._generate([prompt])
    print(f"Answer: {answer}")
