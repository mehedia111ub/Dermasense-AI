blocked_terms = [
    "give me a diagnosis",
    "diagnose me",
    "prescribe",
    "prescription",
    "cure this",
    "emergency treatment"
]

def apply_safety_filter(user_question, ai_response):

    lower_question = user_question.lower()

    for term in blocked_terms:
        if term in lower_question:
            return """
I cannot provide medical diagnosis, prescriptions, or emergency treatment advice.

Please consult a licensed dermatologist or healthcare professional.

This system is for educational purposes only.
"""

    return ai_response