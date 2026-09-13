from app.services.llm import generate_response


print("=" * 60)
print("TESTING HUGGING FACE LLM")
print("=" * 60)


question = "Explain PWM in simple terms for a beginner."


system_prompt = """
You are EduMentor, an AI teaching assistant.

Explain technical concepts clearly and simply.

Use examples when useful.

Do not make the explanation unnecessarily complicated.
"""


print("\nQuestion:")
print(question)

print("\nGenerating answer...\n")


answer = generate_response(
    prompt=question,
    system_prompt=system_prompt
)


print("=" * 60)
print("EDUMENTOR ANSWER")
print("=" * 60)

print(answer)


print("\n" + "=" * 60)
print("LLM TEST COMPLETE")
print("=" * 60)