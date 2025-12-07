#!/usr/bin/env node
const express = require("express");
const bodyParser = require("body-parser");
const { GoogleGenerativeAI } = require("@google/generative-ai");

const apiKey = process.env.GEMINI_API_KEY;

if (!apiKey) {
  console.error("[AI] ERROR: GEMINI_API_KEY missing.");
  process.exit(1);
}

console.log("[AI] Starting Patch Server…");

const genAI = new GoogleGenerativeAI(apiKey);
const model = genAI.getGenerativeModel({ model: "gemini-pro" });

const app = express();
app.use(bodyParser.json());

// ---------- Health Check ----------
app.get("/health", (req, res) => {
  res.json({ ok: true, ts: Date.now() });
});

// ---------- Patch Route ----------
app.post("/patch", async (req, res) => {
  const logs = req.body.logs || "";

  console.log("[AI] Logs received:", logs.substring(0, 200)); // Don't spam

  const prompt = `
You are an AI that generates Git patches.

### TASK
Given CI build logs, produce a correct unified diff (patch) to fix the error.

### RULES
- Always return a unified diff starting with --- and +++.
- If the logs do not contain a clear error, create a fallback patch
  that adds a diagnostic.md file containing the logs.
- NEVER return empty output.

### LOGS:
${logs}
`;

  try {
    const result = await model.generateContent(prompt);
    let text = result.response.text().trim();

    if (!text || text.length < 10 || !text.includes("---")) {
      console.log("[AI] Empty or invalid patch from Gemini. Using fallback.");
      text = `
--- /dev/null
+++ b/diagnostic.md
@@ -0,0 +1,20 @@
# Automatic Diagnostic File
Gemini could not determine a fix.

## Logs
${logs.split("\n").map((l) => "+ " + l).join("\n")}
`;
    }

    res.json({ patch: text });
  } catch (err) {
    console.error("[AI] Gemini error:", err);

    const fallback = `
--- /dev/null
+++ b/diagnostic.md
@@ -0,0 +1,20 @@
# AI Patch Server Failure
Gemini API failed.

## Logs
${logs}
`;

    res.json({ patch: fallback });
  }
});

app.listen(3000, () => {
  console.log("[AI] Patch Server READY at http://localhost:3000");
});
