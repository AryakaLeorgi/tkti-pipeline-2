#!/usr/bin/env node
const express = require("express");
const bodyParser = require("body-parser");
const { GoogleGenerativeAI } = require("@google/generative-ai");

const apiKey = process.env.GEMINI_API_KEY;

if (!apiKey) {
  console.error("❌ Missing GEMINI_API_KEY");
  process.exit(1);
}

const genAI = new GoogleGenerativeAI(apiKey);
const model = genAI.getGenerativeModel({ model: "gemini-pro" });

const app = express();
app.use(bodyParser.json());

// Health check for Jenkins
app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

app.post("/patch", async (req, res) => {
  const logs = req.body.logs || "";

  console.log("Logs received:", logs);

  const prompt = `
You are an AI that generates Git patches.

### TASK
Given CI build logs, produce a correct unified diff (patch) to fix the error.

### RULES
- Always return a unified diff starting with --- and +++.
- If the logs are vague or no fix is possible:
  - Create a fallback patch that adds a diagnostic.md file containing the logs.
- NEVER output empty text.

### LOGS:
${logs}
`;

  try {
    const result = await model.generateContent(prompt);
    let patch = result.response.text().trim();

    if (!patch || !patch.includes("---")) {
      patch = `
--- /dev/null
+++ b/diagnostic.md
@@ -0,0 +1,5 @@
# Fallback Diagnostic
The AI could not determine a fix.

## Logs
${logs.split("\n").map((l) => "+ " + l).join("\n")}
`;
    }

    res.json({ patch });

  } catch (err) {
    console.error("Gemini error:", err);

    res.json({
      patch: `
--- /dev/null
+++ b/diagnostic.md
@@ -0,0 +1,5 @@
# AI Patch Error
Gemini API failed.

## Logs
${logs}
`
    });
  }
});

app.listen(3000, () => {
  console.log("🚀 AI Patch Server running on http://localhost:3000");
});
