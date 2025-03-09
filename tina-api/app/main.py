# app/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends  
from fastapi.responses import JSONResponse  
import uvicorn  
import os
from dotenv import load_dotenv
import tempfile
from app.helpers.audio_utils import convert_to_supported_format, split_audio_file  
from app.models.model_utils import load_model, transcribe, transcribe_with_timestamps
from app.models.azure_openai_utils import generate_summary
from fastapi.security.api_key import APIKeyHeader, APIKey  
from starlette.status import HTTP_403_FORBIDDEN  
  
# Load environment variables from root project directory
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path)

# Laad het model bij het starten van de app - nu een compatibility layer voor Azure Speech  
model, processor, asr_pipeline = load_model()  
  
app = FastAPI()
  
# Haal API key uit environment variables
API_KEY = os.getenv("API_KEY", "JOUW_VEILIGE_API_SLEUTEL")
API_KEY_NAME = os.getenv("API_KEY_NAME", "access_token")
  
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)  
  
async def get_api_key(api_key_header: str = Depends(api_key_header)):  
    if api_key_header == API_KEY:  
        return api_key_header  
    else:  
        raise HTTPException(  
            status_code=HTTP_403_FORBIDDEN, detail="Kon API-sleutel niet valideren"  
        )  
  
# Endpoint voor normale transcriptie  
@app.post("/transcribe")  
async def transcribe_audio_endpoint(  
    file: UploadFile = File(...), api_key: APIKey = Depends(get_api_key)  
):  
    """Transcribeert het geüploade audiobestand en retourneert de tekst."""  
    temp_file_path = f"temp_{file.filename}"
    # Sla het geüploade bestand tijdelijk op
    with open(temp_file_path, "wb") as temp_file:  
        temp_file.write(await file.read())  
  
    # Converteer naar ondersteund formaat  
    converted_file_path = convert_to_supported_format(temp_file_path)  
    if not converted_file_path:  
        os.remove(temp_file_path)  
        raise HTTPException(status_code=400, detail="Niet-ondersteund audioformaat.")  
  
    try:
        # Transcribeer het bestand met Azure Speech
        transcription = transcribe(converted_file_path)
        
        # Verwijder tijdelijke bestanden  
        os.remove(temp_file_path)  
        if converted_file_path != temp_file_path:  
            os.remove(converted_file_path)  
      
        return JSONResponse({"transcription": transcription})
    except Exception as e:
        # Verwijder tijdelijke bestanden in geval van een fout
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if converted_file_path != temp_file_path and os.path.exists(converted_file_path):
            os.remove(converted_file_path)
        
        raise HTTPException(status_code=500, detail=f"Fout bij transcriptie: {str(e)}")
  
# Endpoint voor transcriptie met timestamps  
@app.post("/transcribe_timestamps")  
async def transcribe_with_timestamps_endpoint(  
    file: UploadFile = File(...), api_key: APIKey = Depends(get_api_key)  
):  
    """Transcribeert het geüploade audiobestand en retourneert tekst met tijdstempels."""  
    # Sla het geüploade bestand tijdelijk op
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as temp_file:  
        temp_file.write(await file.read())  
  
    # Converteer naar ondersteund formaat  
    converted_file_path = convert_to_supported_format(temp_file_path)  
    if not converted_file_path:  
        os.remove(temp_file_path)  
        raise HTTPException(status_code=400, detail="Niet-ondersteund audioformaat.")  
  
    try:
        # Met Azure Speech hebben we geen segmenten nodig, we verwerken het hele bestand
        transcription_result = transcribe_with_timestamps(converted_file_path)
        
        # Genereer een samenvatting van de transcriptie
        summary = None
        if transcription_result and "text" in transcription_result:
            summary = generate_summary(transcription_result["text"])
        
        # Add summary to the result
        result = {"transcriptions": [transcription_result]}
        if summary:
            result["summary"] = summary
        
        # Verwijder tijdelijke bestanden
        os.remove(temp_file_path)
        if converted_file_path != temp_file_path:
            os.remove(converted_file_path)
        
        return JSONResponse(result)
    except Exception as e:
        # Verwijder tijdelijke bestanden in geval van een fout
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if converted_file_path != temp_file_path and os.path.exists(converted_file_path):
            os.remove(converted_file_path)
        
        raise HTTPException(status_code=500, detail=f"Fout bij transcriptie: {str(e)}")
  
if __name__ == "__main__":  
    uvicorn.run("main:app", host="0.0.0.0", port=8000)