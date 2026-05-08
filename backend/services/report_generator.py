def generate_report(prediction, confidence):
    return {
        "prediction": prediction,
        "confidence": confidence,
        "description": "This is a generated NLP report.",
        "causes": "Possible causes depend on the predicted pigmentation category.",
        "management": "Use sun protection and consult a dermatologist for professional advice.",
        "severity": "Demo severity",
        "disclaimer": "This system provides educational information only and does not provide medical diagnosis."
    }