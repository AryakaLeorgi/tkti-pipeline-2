import express from "express";
import { GoogleGenerativeAI } from "@google/generative-ai";

const app = express();
app.use(express.json());

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });

app.post("/patch", async (req, res) => {
    try {
        const logs = req.body.logs || "";

        const prompt = `
You are an AI CI/CD assistant. Read the logs and produce ONLY a unified diff patch.

Wrap the output between:
PATCH_START
...patch here...
PATCH_END

Logs:
${logs}
`;

        const result = await model.generateContent(prompt);

        const text = result.response.text();

        const patchMatch = text.match(/PATCH_START([\s\S]*?)PATCH_END/);

        if (!patchMatch) {
            return res.json({ error: "No patch generated" });
        }

        const patch = patchMatch[1].trim();

        return res.json({ patch });

    } catch (err) {
        console.error(err);
        return res.json({ error: "Patch generation failed." });
    }
});

app.listen(3000, () =>
    console.log("AI Patch Server running on http://localhost:3000")
);
