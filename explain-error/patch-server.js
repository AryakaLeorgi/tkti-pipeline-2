import express from "express";
import { GoogleGenerativeAI } from "@google/generative-ai";

const app = express();
app.use(express.json());

app.post("/patch", async (req, res) => {
    try {
        const logs = req.body.logs;
        const apiKey = process.env.GEMINI_API_KEY;

        const genAI = new GoogleGenerativeAI(apiKey);
        const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });

        const prompt = `
You are an AI automated CI/CD repair assistant.

Given the following Jenkins logs, output ONLY a unified diff patch.
Wrap it between:

PATCH_START
<diff>
PATCH_END

Logs:
${logs}
`;

        const result = await model.generateContent(prompt);
        const patch = result.response.text();

        res.json({ patch });

    } catch (err) {
        console.error(err);
        res.status(500).json({ error: "Patch generation failed." });
    }
});

app.listen(3000, () => console.log("AI Patch server running on port 3000"));
