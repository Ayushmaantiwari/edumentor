import os

from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, GEMINI_MODEL


# ======================================================
# GEMINI API KEY VALIDATION
# ======================================================

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is not set."
    )


# ======================================================
# GEMINI CLIENT
# ======================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ======================================================
# GENERATE LLM RESPONSE
# ======================================================

def generate_response(
    prompt: str,
    system_prompt: str | None = None
) -> str:

    if not prompt or not prompt.strip():
        raise ValueError(
            "Prompt cannot be empty."
        )

    # --------------------------------------------------
    # Gemini generation configuration
    # --------------------------------------------------

    config = types.GenerateContentConfig(
        temperature=0.3,
        max_output_tokens=2500,
    )

    # --------------------------------------------------
    # Add system instruction if provided
    # --------------------------------------------------

    if system_prompt:
        config.system_instruction = system_prompt

    # --------------------------------------------------
    # Generate response
    # --------------------------------------------------

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=config
    )

    # --------------------------------------------------
    # Validate response
    # --------------------------------------------------

    if not response:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    if not response.text:
        raise RuntimeError(
            "Gemini returned no text response."
        )

    return response.text.strip()