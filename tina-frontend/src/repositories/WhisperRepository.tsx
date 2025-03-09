import { ApiResponse } from "../models/WhisperResponse";

export async function generateLLMResponse(
  file: File
): Promise<any> {
  console.log("Transcribing file test");
  const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/api/transcribe", {
        method: "POST",
        body: formData,
    });

    const data = await response.json();
    console.log("data received form backend: "+ data);
    return data;
}
