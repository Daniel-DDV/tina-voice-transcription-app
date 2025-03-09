import { generateLLMResponse } from "../repositories/WhisperRepository";

export default async function TranscribeFile(file: File): Promise<{ transcription: string | undefined; summary: string | undefined } | undefined> {
    try {
        // Get transcription and summary from the backend API
        const response = await generateLLMResponse(file);

        if (!response) return undefined;

        // Extract transcription from the response
        const transcription = response.transcriptions && response.transcriptions[0]?.text;
        
        // Extract summary directly from the backend response
        const summary = response.summary;

        console.log("Transcription received:", transcription);
        console.log("Summary received:", summary);

        return { transcription, summary };
    } catch (error) {
        console.error("Error in TranscribeFile:", error);
        return undefined;
    }
}