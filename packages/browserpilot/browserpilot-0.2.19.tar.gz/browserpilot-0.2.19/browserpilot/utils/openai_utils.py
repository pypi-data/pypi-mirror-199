"""Helper functions for OpenAI."""
import tiktoken


# If you are seeing this, then I apologize for the hardcoding...
MODEL_INFO = {
    # For tokenizers, see source:
    # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    "gpt-3.5-turbo": {
        "max_tokens": 4000,  # Really 4097, but just be safe.
        "tokenizer": "cl100k_base",
    },
    "text-davinci-003": {
        "max_tokens": 4000,  # Really 4097, but just be safe.
        "tokenizer": "p50k_base",
    },
}


def get_num_tokens(text, model_name="gpt-3.5-turbo"):
    """Get the number of tokens that a particular text will be for OpenAI."""
    tokenizer = MODEL_INFO[model_name]["tokenizer"]
    encoding = tiktoken.get_encoding(tokenizer)
    return len(encoding.encode(text))


def get_max_tokens_for_response(prompt, model_name="gpt-3.5-turbo"):
    """Get the maximum number of tokens for a response given a prompt."""
    max_tokens = MODEL_INFO[model_name]["max_tokens"]
    max_tokens_for_response = max_tokens - get_num_tokens(prompt)
    return max_tokens_for_response
