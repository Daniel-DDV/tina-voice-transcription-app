import { ApiResponse } from "../models/LargeLanguageModelResponse";

export async function generateResponse(
  text: string,
  stream: boolean = false
): Promise<ApiResponse | null> {
  const url = "https://llm-demo.ai-hackathon.haven.vng.cloud/api/generate";

  const systemPrompt = `
Je bent een expert samenvattingsspecialist binnen een transcriptieapplicatie. Je taak is het genereren van beknopte, accurate samenvattingen van Nederlandse gesprekken over AI-ontwikkeling en -samenwerking.

CONTEXT:
Transcripties komen van gesprekken over de "AI Coördinatie Nederland" beweging
Focus ligt op technische ontwikkelingen, samenwerkingen en concrete resultaten
Doelgroep: AI-professionals, ontwikkelaars en beleidsmakers in Nederland

VEREISTEN:
Vat samen in 3-4 kernachtige alinea's
Identificeer en benadruk:
- Concrete technische ontwikkelingen en platforms
- Samenwerkingsverbanden en deelnemende partijen
- Behaalde resultaten en mijlpalen
- Toekomstvisie en vervolgstappen

STIJL:
- Gebruik zakelijk Nederlands zonder jargon
- Behoud technische precisie in beschrijvingen
- Structureer chronologisch of op belangrijkheid

STRUCTUUR PER SAMENVATTING:
- Openingsalinea: Kernboodschap en context
- Middelste alinea's: Technische details en resultaten
- Slotalinea: Conclusies en vervolgstappen

UITSLUITINGEN:
- Geen algemene AI-beschouwingen
- Geen persoonlijke meningen
- Geen niet-genoemde aannames

Denk stap voor stap na over de belangrijkste elementen in de transcriptie voordat je begint met samenvatten. Focus op concrete, actionable informatie die relevant is voor de Nederlandse AI-community.

Nu volgt de transcriptie:

`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "llama3.2",
        prompt: systemPrompt + text,
        stream,
        options: {
          temperature: 0.1,
        },
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    return null;
  }
}
