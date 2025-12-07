const fs = require("fs");
const axios = require("axios");

const MODEL = process.env.MODEL || "gemini-2.5-flash";
const API_KEY = process.env.GEMINI_API_KEY;

async function explainError(logs) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${API_KEY}`;

    const payload = {
        contents: [
            {
                parts: [
                    {
                        text: `You are an expert CI/CD assistant. Explain this Jenkins error:\n\n${logs}`
                    }
                ]
            }
        ]
    };

    const res = await axios.post(url, payload);
    return res.data.candidates[0].content.parts[0].text;
}

async function main() {
    const logPath = process.argv[2];
    const logs = fs.readFileSync(logPath, "utf8");
    const result = await explainError(logs);
    console.log(result);
}

main();
