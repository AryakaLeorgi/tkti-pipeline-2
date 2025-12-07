import { GoogleGenerativeAI } from "@google/generative-ai";

export async function explainLogs(logs) {
    const apiKey = process.env.GEMINI_API_KEY;
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });

    const prompt = `
    Explain this Jenkins error:
    ${logs}
    `;

    const result = await model.generateContent(prompt);
    return result.response.text();
}
