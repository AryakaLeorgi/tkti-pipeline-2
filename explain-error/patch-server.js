#!/usr/bin/env node
const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");
const { GoogleGenerativeAI } = require("@google/generative-ai");

const apiKey = process.env.GEMINI_API_KEY;

if (!apiKey) {
  console.error("Missing GEMINI_API_KEY");
  process.exit(1);
}

const genAI = new GoogleGenerativeAI(apiKey);
const model = genAI.getGenerativeModel({ model: "gemini-pro" });

const app = express();
app.use(bodyParser.json());

app.post("/patch", async (req, res) => {
  const logs = req.body.logs || "";

  console.log("Logs received:", logs);

  const prompt = `
You are an AI that generates Git patches.

### TASK
Given CI build logs, produce a correct unified diff (patch) to fix the error.

### RULES
- Always return a unified diff starting with --- and +++.
- If the logs are vague and you cannot determine a fix:
  - Create a fallback patch that adds a file: "diagnostic.md" containing the logs.
- NEVER return empty output.

### LOGS:
${logs}
`;

  try {
    const result = await model.generateContent(prompt);
    const text = result.response.text().trim();

    let patch = text;

    // Fallback: ensure patch NEVER empty
    if (!patch || patch.length < 5) {
      patch = `
--- /dev/null
+++ b/diagnostic.md
@@ -0,0 +1,5 @@
# Automated Diagnostic
The build failed but logs were too vague to compute a fix.

## Logs
${logs.split("\n").map((l) => "+ " + l).join("\n")}
`;
    }

    res.json({ patch });
  } catch (err) {
    console.error("Gemini error:", err);

    // fallback patch on model failure
    const fallback = `
--- /dev/null
+++ b/diagnostic.md
@@ -0,0 +1,5 @@
# AI Patch Server Failure
Gemini API failed. Here are the logs:
${logs}
`;

    res.json({ patch: fallback });
  }
});

app.listen(3000, () => {
  console.log("AI Patch Server running on http://localhost:3000");
});
