from transformers import pipeline

# Load once when backend starts
classifier = pipeline(
    task="zero-shot-image-classification",
    model="openai/clip-vit-base-patch32"
)

candidate_labels = [
    "melasma skin hyperpigmentation",
    "post inflammatory hyperpigmentation dark skin marks",
    "solar lentigines sun spots on skin",
    "ephelides freckles on skin",
    "normal healthy skin"
]

label_map = {
    "melasma skin hyperpigmentation": "Melasma",
    "post inflammatory hyperpigmentation dark skin marks": "Post-Inflammatory Hyperpigmentation",
    "solar lentigines sun spots on skin": "Solar Lentigines",
    "ephelides freckles on skin": "Ephelides",
    "normal healthy skin": "Normal Skin"
}

def classify_skin(image_path):
    results = classifier(
        image_path,
        candidate_labels=candidate_labels
    )

    best_result = results[0]

    return {
        "prediction": label_map.get(best_result["label"], best_result["label"]),
        "confidence": round(best_result["score"] * 100, 2),
        "raw_results": [
            {
                "label": label_map.get(item["label"], item["label"]),
                "score": round(item["score"] * 100, 2)
            }
            for item in results
        ]
    }