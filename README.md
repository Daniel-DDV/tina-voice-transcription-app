# Tina - Voice Transcription and Summarization Application

Tina is a web application that transcribes voice recordings and generates summaries using Azure AI services.

## Features

- Voice recording through the browser
- Real-time audio transcription using Azure Speech Services
- Summarization of transcribed content using Azure OpenAI GPT-4o
- Modern responsive UI with Next.js frontend

## Project Structure

The application consists of two main components:

1. **Backend API** (tina-api): A FastAPI Python application that handles:
   - Audio file processing
   - Azure Speech Services integration
   - Azure OpenAI integration

2. **Frontend** (tina-frontend): A Next.js web application that provides:
   - User interface for recording audio
   - Display of transcription and summary results

## Prerequisites

- Python 3.8+ with pip
- Node.js and npm
- Azure Speech Services account
- Azure OpenAI Services account with GPT-4o access

## Setup

### Environment Setup

1. Clone this repository

2. Create a Python virtual environment in the root directory:

   ```bash
   python -m venv venv
   ```

3. Install backend dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Navigate to the frontend directory and install dependencies:

   ```bash
   cd tina-frontend
   npm install
   ```

### Configuration

1. Create a `.env` file in the root directory based on the provided `.env.example` file:

   ```bash
   cp .env.example .env
   ```

   Then edit the `.env` file with your own Azure credentials:

   ```ini
   AZURE_SPEECH_KEY=your_speech_key
   AZURE_SPEECH_REGION=your_speech_region
   AZURE_OPENAI_ENDPOINT=your_openai_endpoint
   AZURE_OPENAI_KEY=your_openai_key
   AZURE_OPENAI_DEPLOYMENT=your_openai_deployment_name
   AZURE_OPENAI_API_VERSION=2024-12-01-preview
   ```

## Running the Application

You can start both the frontend and backend with a single command using the provided batch script:

```bash
start_app.bat
```

Or start them separately:

1. Start the backend:

   ```bash
   python start_api.py
   ```

2. Start the frontend (in a new terminal):

   ```bash
   cd tina-frontend
   npm run dev
   ```

The application will be accessible at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## API Endpoints

- `POST /transcribe`: Transcribes audio file
- `POST /transcribe_timestamps`: Transcribes audio with timestamps
- `GET /health`: Health check endpoint

## License

[MIT License](LICENSE)
