import fs from "fs";
import { GoogleGenerativeAI } from "@google/generative-ai";

async function main() {
    const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });

    const log = fs.readFileSync(process.argv[2], "utf8");

    const prompt = `
    You are an expert CI/CD assistant. Explain the following Jenkins pipeline error.
    Provide:

    1. The root cause  
    2. What component failed  
    3. How to fix it  

    Logs:
        ${log}
    `;

    const result = await model.generateContent(prompt);
    console.log("AI Explanation:\n", result.response.text());
}

main();
