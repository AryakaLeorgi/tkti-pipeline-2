#!/usr/bin/env node
import express from "express";
import { GoogleGenerativeAI } from "@google/generative-ai";

const apiKey = process.env.GEMINI_API_KEY;

if (!apiKey) {
  console.error("❌ Missing GEMINI_API_KEY");
  process.exit(1);
}

const genAI = new GoogleGenerativeAI(apiKey);
const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });

const app = express();
app.use(express.json());

// Health check for Jenkins
app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

// Generate a valid fallback patch
function createFallbackPatch(title, content) {
  const lines = content.split("\n");
  const lineCount = lines.length + 4;
  const patchLines = lines.map(l => `+${l}`).join("\n");

  return `--- /dev/null
+++ b/diagnostic.md
@@ -0,0 +1,${lineCount} @@
+# ${title}
+
+## Build Logs
+
${patchLines}
`;
}

app.post("/patch", async (req, res) => {
  const logs = req.body.logs || "";

  console.log("Logs received:", logs);

  const prompt = `You are an AI that generates Git unified diff patches.

TASK: Analyze the CI build error logs and generate a valid unified diff patch to fix the issue.

STRICT FORMAT RULES:
1. Start with: --- a/filename (or --- /dev/null for new files)
2. Then: +++ b/filename  
3. Then hunk header: @@ -start,count +start,count @@
4. Lines starting with - are removed
5. Lines starting with + are added
6. Context lines have no prefix (space at start)
7. NO markdown code blocks, NO backticks, NO extra text
8. Output ONLY the raw patch content

If you cannot determine a fix, create a diagnostic.md file with the error analysis.

LOGS:
${logs}`;

  try {
    const result = await model.generateContent(prompt);
    let patch = result.response.text().trim();

    // Remove markdown code blocks if present
    patch = patch.replace(/^```[\w]*\n?/gm, "").replace(/\n?```$/gm, "").trim();

    // Validate patch has required format
    if (!patch || !patch.includes("---") || !patch.includes("+++")) {
      console.log("Invalid patch format, using fallback");
      patch = createFallbackPatch("AI Analysis", `Error logs:\n${logs}\n\nAI could not generate a specific fix.`);
    }

    console.log("Generated patch:", patch);
    res.json({ patch });

  } catch (err) {
    console.error("Gemini error:", err.message);

    const fallbackPatch = createFallbackPatch("AI Patch Error", `Gemini API Error: ${err.message}\n\nOriginal logs:\n${logs}`);
    res.json({ patch: fallbackPatch });
  }
});

app.listen(3000, () => {
  console.log("🚀 AI Patch Server running on http://localhost:3000");
});
