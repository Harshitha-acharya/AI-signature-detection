from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from signature_ai import compare_signatures
from database import save_analysis


app = FastAPI(
    title="SignGuard AI",
    description="AI Signature Forgery Detection API",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():

    return {
        "message": "SignGuard AI Backend Running",
        "status": "online"
    }


@app.post("/analyze")
async def analyze_signature(
    real_signature: UploadFile = File(...),
    doubted_signature: UploadFile = File(...)
):

    # Read uploaded images
    real_bytes = await real_signature.read()
    doubt_bytes = await doubted_signature.read()

    # AI comparison
    result = compare_signatures(
        real_bytes,
        doubt_bytes
    )

    # Save result to MySQL
    save_analysis(
        real_signature=real_signature.filename,
        doubted_signature=doubted_signature.filename,
        similarity=result["similarity"],
        forgery_risk=result["forgery_risk"],
        pixel_similarity=result["pixel_similarity"],
        shape_similarity=result["shape_similarity"],
        stroke_similarity=result["stroke_similarity"],
        result=result["result"]
    )

    return {
        "success": True,

        "real_signature":
            real_signature.filename,

        "doubted_signature":
            doubted_signature.filename,

        "analysis": result
    }