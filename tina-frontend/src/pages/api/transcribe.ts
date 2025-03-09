import type { NextApiRequest, NextApiResponse } from "next";
import fs from "fs";
import { IncomingForm } from "formidable";

// Add TypeScript declaration for formidable
type FormidableFile = {
    filepath: string;
    originalFilename?: string;
    mimetype?: string;
    size: number;
};

type FormidableFiles = {
    [key: string]: FormidableFile[];
};

type FormidableFields = {
    [key: string]: string[];
};

export const config = {
    api: {
        bodyParser: false,
    },
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    // Set CORS headers to allow requests from any origin (for development/testing purposes)
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type, Accept, Authorization");

    if (req.method !== "POST") {
        return res.status(405).json({ message: "Method Not Allowed" });
    }

    try {
        const formidable = await import("formidable");
        const form = new formidable.IncomingForm();

        form.parse(req, async (err: Error | null, fields: FormidableFields, files: FormidableFiles) => {
            if (err) {
                console.error("Error parsing form:", err);
                return res.status(400).json({ message: "Error parsing form data", error: err.message });
            }

            if (!files.file || !files.file[0]) {
                console.error("No file uploaded");
                return res.status(400).json({ message: "No file uploaded" });
            }

            const file = files.file[0];

            console.log("File received:", {
                originalFilename: file.originalFilename,
                mimetype: file.mimetype,
                size: file.size,
                filepath: file.filepath,
            });

            try {
                const fileBuffer = fs.readFileSync(file.filepath);
                const formData = new FormData();
                formData.append("file", new Blob([fileBuffer], { type: file.mimetype || "audio/webm" }), file.originalFilename || "audio.webm");

                console.log("Sending request to backend API...");
                
                // Use local backend API instead of the obsolete hostname
                const response = await fetch("http://localhost:8000/transcribe_timestamps", {
                    method: "POST",
                    headers: {
                        accept: "application/json",
                        access_token: "JOUW_VEILIGE_API_SLEUTEL",
                    },
                    body: formData,
                });

                console.log("Backend API response status:", response.status);
                const responseBody = await response.text();
                console.log("Backend API response body:", responseBody);

                if (!response.ok) {
                    console.error("Backend API error:", response.status, responseBody);
                    return res.status(response.status).json({ 
                        message: "Backend API error", 
                        status: response.status,
                        details: responseBody 
                    });
                }

                // Always end the request with a response
                return res.status(200).json(JSON.parse(responseBody));
            } catch (error) {
                console.error("Error in API request:", error);
                return res.status(500).json({ 
                    message: "Error processing request", 
                    error: error instanceof Error ? error.message : String(error)
                });
            }
        });
    } catch (error) {
        console.error(" Error:", error);
        res.status(500).json({ message: "Internal Server Error", error: (error as Error).message });
    }
}
