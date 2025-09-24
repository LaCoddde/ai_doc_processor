import base64
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field # <-- Updated import
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# --- 1. Define the Data Schema ---
# Create a Pydantic model to specify the exact structure of the data we want.
# This guides the AI to be precise and consistent.
class CertificateDetails(BaseModel):
    """The structured data extracted from a certificate document."""
    certificate_number: str = Field(
        ..., # The '...' means this field is required
        description="The unique identifier or number for the certificate. e.g., ABC-12345-XYZ"
    )
    client_name: str = Field(
        ...,
        description="The name of the person or company the certificate was issued to."
    )
    issue_date: str = Field(
        ...,
        description="The date the certificate was issued, in YYYY-MM-DD format."
    )
    expiry_date: str = Field(
        ...,
        description="The date the certificate expires, in YYYY-MM-DD format."
    )

# --- 2. Image Processing and AI Model Setup ---

def image_to_base64(image_path: str) -> str:
    """Converts a local image file to a base64 encoded string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_certificate_data(image_path: str) -> CertificateDetails:
    """
    Extracts structured data from a certificate image using GPT-4 Vision.
    
    This function takes the path to an image, sends it to the AI with a
    structured schema (CertificateDetails), and returns the extracted data.
    """
    # Initialize the AI model. We use gpt-4o as it's powerful and cost-effective.
    # .with_structured_output() is the key LangChain method that forces the AI
    # to return data in the format of our Pydantic model.
    llm = ChatOpenAI(model="gpt-4o").with_structured_output(CertificateDetails)
    
    # Encode the image to base64
    base64_image = image_to_base64(image_path)
    
    # --- 3. Construct the Prompt ---
    # We create a message containing both the text prompt and the image data.
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "You are an expert at extracting information from documents. "
                        "Analyze the attached certificate image and extract the "
                        "key details according to the provided schema. Ensure dates are in YYYY-MM-DD format."
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image}"}
            }
        ]
    )
    
    # --- 4. Call the AI Model ---
    print(f"Analyzing document: {image_path}...")
    response = llm.invoke([message])
    return response

# --- Main Execution Block ---
if __name__ == "__main__":
    # Specify the path to the certificate you want to process
    file_path = "data/cert_02.png"
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
    else:
        extracted_data = extract_certificate_data(file_path)
        
        # Print the structured data beautifully
        print("\n--- Extracted Data ---")
        print(f"Certificate Number: {extracted_data.certificate_number}")
        print(f"Client Name: {extracted_data.client_name}")
        print(f"Issue Date: {extracted_data.issue_date}")
        print(f"Expiry Date: {extracted_data.expiry_date}")
        print("----------------------\n")