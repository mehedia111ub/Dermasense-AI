from services.explainability import generate_explainability_overlay
from services.mistral_chat import generate_mistral_report
from services.classifier import classify_skin
from services.report_generator import generate_report
from fastapi import APIRouter, UploadFile, File
import shutil
import os

from services.image_preprocessing import preprocess_image
from services.classifier import classify_skin

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def generate_report_direct(prediction, confidence):
    return {
        "prediction": prediction,
        "confidence": confidence,
        "description": "This is an automatically generated Natural Language Generation report.",
        "causes": "Possible causes may include sun exposure, inflammation, hormonal changes, or genetics.",
        "management": "Use sun protection, avoid excessive UV exposure, and consult a dermatologist for professional advice.",
        "severity": "Demo severity level",
        "disclaimer": "This system provides educational information only and does not provide medical diagnosis."
    }

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    processed_path = preprocess_image(file_path)
    overlay_path = generate_explainability_overlay(processed_path)

    result = classify_skin(processed_path)

    # report = generate_report_direct(
    #     result["prediction"],
    #     result["confidence"]
    # )

    nlg_text = generate_mistral_report(
    result["prediction"],
    result["confidence"],
    result.get("raw_results")
    )

    report = {
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "nlg_report": nlg_text,
        "raw_results": result.get("raw_results"),
        "disclaimer": "This system provides educational information only and does not provide medical diagnosis."
    }

    return {
        "original_image": file.filename,
        "processed_image": processed_path,
        "overlay_image": overlay_path,
        "analysis_report": report,
        "status": "Full AI analysis completed"
    }