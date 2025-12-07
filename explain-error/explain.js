import axios from "axios";
import dotenv from "dotenv";
dotenv.config();

const MODEL = process.env.MODEL || "gemini-2.5-flash";
const API_KEY = process.env.GEMINI_API_KEY;

export async function explainError(logs) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${API_KEY}`;

    const payload = {
        contents: [{
            parts: [{
                text:
`You are an expert CI/CD assistant. Explain the following Jenkins pipeline error.
Be concise and provide:

1. The root cause  
2. What part failed  
3. How to fix it  

Logs:
${logs}`
            }]
        }]
    };

    const res = await axios.post(url, payload);
    return res.data.candidates[0].content.parts[0].text;
}
