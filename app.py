# app.py

import time
import base64
import io
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field

# --- Import AI Logic Components ---
# We are moving the core components from our main.py script here.
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# --- 1. Pydantic Data Schema ---
# This is the same schema we defined before. It will be used to structure the AI's output
# and also defines the structure of the JSON response from our API.
class CertificateDetails(BaseModel):
    """The structured data extracted from a certificate document."""
    certificate_number: str = Field(..., description="The unique identifier for the certificate.")
    client_name: str = Field(..., description="The name of the entity the certificate was issued to.")
    issue_date: str = Field(..., description="The issue date in YYYY-MM-DD format.")
    expiry_date: str = Field(..., description="The expiry date in YYYY-MM-DD format.")

# --- 2. FastAPI App Initialization ---
app = FastAPI(
    title="AI Document Processor",
    description="An API to extract structured data from documents using AI.",
    version="1.0.0"
)

# --- 3. The AI Extraction Logic ---
# This function is now adapted to take raw image bytes instead of a file path.
def extract_certificate_data(image_bytes: bytes) -> CertificateDetails:
    """Extracts structured data from image bytes using GPT-4 Vision."""
    llm = ChatOpenAI(model="gpt-4o").with_structured_output(CertificateDetails)
    
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": "You are an expert at extracting information from documents. Analyze the certificate image and extract the key details into the provided JSON schema."},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
        ]
    )
    
    try:
        response = llm.invoke([message])
        return response
    except Exception as e:
        # If the AI call fails, we raise an exception that FastAPI will handle.
        raise HTTPException(status_code=500, detail=f"AI model processing failed: {e}")

# --- 4. API Endpoints ---
@app.get("/", tags=["General"])
def read_root():
    """Returns a welcome message."""
    return {"message": "Welcome! Navigate to /docs to see the API documentation."}

@app.post("/process-document/", response_model=CertificateDetails, tags=["Document Processing"])
async def process_document(file: UploadFile = File(...)):
    """
    Accepts an uploaded document image, processes it, and returns the extracted data.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    # --- Start Measuring ---
    start_time = time.time()
    
    print(f"Received file: {file.filename}, Content-Type: {file.content_type}")

    image_bytes = await file.read()
    
    try:
        extracted_data = extract_certificate_data(image_bytes)
        
        # --- Stop Measuring on Success ---
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"SUCCESS: Document processed in {processing_time:.2f} seconds.")
        
        return extracted_data
    
    except HTTPException as e:
        # --- Log Failure ---
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"FAILURE: Processing failed after {processing_time:.2f} seconds. Reason: {e.detail}")
        
        # Re-raise the exception to send the error response to the user
        raise e
