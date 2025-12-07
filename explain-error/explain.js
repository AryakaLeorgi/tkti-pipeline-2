import fs from "fs";
import { GoogleGenerativeAI } from "@google/generative-ai";

async function run() {
    const apiKey = process.env.GEMINI_API_KEY;

    if (!apiKey) {
        console.error("ERROR: GEMINI_API_KEY is not set.");
        process.exit(1);
    }

    const logPath = process.argv[2];
    if (!logPath) {
        console.error("Usage: node explain.js <logfile>");
        process.exit(1);
    }

    const logs = fs.readFileSync(logPath, "utf8");

    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });

    const prompt = `
    You are an expert CI/CD assistant. Explain the following Jenkins pipeline error.
    Provide:
    1. Root cause  
    2. Component that failed  
    3. How to fix it  

    Logs:
    ${logs}
    `;

    const result = await model.generateContent(prompt);

    console.log("\n===== AI Explanation =====\n");
    console.log(result.response.text());
}

run();
