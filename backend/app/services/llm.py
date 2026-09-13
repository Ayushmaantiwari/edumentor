from huggingface_hub import InferenceClient

from app.config import HF_TOKEN, HF_MODEL


# ======================================================
# HUGGING FACE CLIENT
# ======================================================

client = InferenceClient(
    api_key=HF_TOKEN
)


# ======================================================
# GENERATE LLM RESPONSE
# ======================================================

def generate_response(
    prompt: str,
    system_prompt: str | None = None
) -> str:

    messages = []

    if system_prompt:
        messages.append(
            {
                "role": "system",
                "content": system_prompt
            }
        )

    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    response = client.chat_completion(
        model=HF_MODEL,
        messages=messages,
        max_tokens=2500,
        temperature=0.3
    )

    answer = response.choices[0].message.content

    return answer.strip()