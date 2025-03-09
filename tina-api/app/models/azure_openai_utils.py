import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from root project directory
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env')
load_dotenv(dotenv_path)

def get_openai_client():
    """
    Create and return an Azure OpenAI client using environment variables or provided values.
    """
    # Try to get from environment first, fall back to placeholders if not found
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-openai-endpoint.openai.azure.com/")
    api_key = os.getenv("AZURE_OPENAI_KEY", "your-api-key-here")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "new-azure-openai-gpt-4o")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
    
    # Create OpenAI client
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=api_key,
    )
    
    return client, deployment_name

def generate_summary(transcription_text):
    """
    Generate a summary of the transcription using Azure OpenAI.
    
    Args:
        transcription_text (str): The transcribed text to summarize
        
    Returns:
        str: The generated summary
    """
    if not transcription_text or transcription_text.startswith("Error:") or transcription_text.startswith("No speech"):
        return "Unable to generate summary: Invalid transcription"

    print(f"Generating summary for transcription: {transcription_text[:100]}...")
    
    try:
        client, deployment_name = get_openai_client()
        
        # Create prompt for summarization
        prompt = f"""
        Je bent een behulpzame assistent die een samenvatting geeft van een getranscribeerde audio opname.
        Maak een beknopte en duidelijke samenvatting van de volgende transcriptie in het Nederlands.
        Focus op de belangrijkste punten en zorg ervoor dat de samenvatting de kern van de inhoud weergeeft.
        
        Transcriptie:
        {transcription_text}
        """
        
        # Call the Azure OpenAI API for summarization
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Je bent een behulpzame assistent die gespecialiseerd is in het samenvatten van Nederlandse tekst.",
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            max_completion_tokens=500,
            model=deployment_name
        )
        
        # Extract the summary from the response
        summary = response.choices[0].message.content
        print(f"Summary generated: {summary[:100]}...")
        
        return summary
        
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return f"Error generating summary: {str(e)}"
