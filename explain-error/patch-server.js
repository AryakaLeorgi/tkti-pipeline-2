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

// Generate a valid fallback patch for diagnostic
function createDiagnosticPatch(title, content) {
  const lines = content.split("\n").slice(0, 50); // Limit to 50 lines
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

  console.log("=== Logs received ===");
  console.log(logs.substring(0, 500) + "...");
  console.log("=====================");

  const prompt = `You are an expert AI code fixer. Your job is to analyze CI/CD build errors and generate a Git unified diff patch to fix the code.

TASK: Analyze the error logs and source code below. Generate a VALID unified diff patch to fix the bug.

CRITICAL PATCH FORMAT RULES:
1. For modifying existing files:
   --- a/src/filename.js
   +++ b/src/filename.js
   
2. Hunk header: @@ -start,count +start,count @@
   - start = line number where chunk begins (1-indexed)
   - count = number of lines in that section

3. Line prefixes (MUST have exactly one space or +/- at start):
   - Lines with "-" prefix are REMOVED
   - Lines with "+" prefix are ADDED  
   - Lines with " " (single space) are CONTEXT (unchanged)

4. Include 2-3 lines of CONTEXT before and after each change

5. Output ONLY the raw patch. NO markdown, NO backticks, NO explanations.

EXAMPLE - Fixing a typo (.tset → .test):
--- a/src/auth.js
+++ b/src/auth.js
@@ -32,7 +32,7 @@
         }
         
         // Bug: typo in method name
-        if (!/[A-Z]/.tset(password)) {
+        if (!/[A-Z]/.test(password)) {
             errors.push("Password must contain uppercase letter");
         }

BUILD ERROR LOGS AND SOURCE CODE:
${logs}

Generate the patch to fix this error:`;

  try {
    const result = await model.generateContent(prompt);
    let patch = result.response.text().trim();

    console.log("=== Raw AI Response ===");
    console.log(patch);
    console.log("=======================");

    // Remove markdown code blocks if present
    patch = patch.replace(/^```[\w]*\n?/gm, "").replace(/\n?```$/gm, "").trim();

    // Remove any leading text before the patch
    const patchStart = patch.indexOf("--- ");
    if (patchStart > 0) {
      patch = patch.substring(patchStart);
    }

    // Validate patch has required format
    if (!patch || !patch.includes("---") || !patch.includes("+++") || !patch.includes("@@")) {
      console.log("Invalid patch format detected, using diagnostic fallback");
      patch = createDiagnosticPatch("AI Analysis", `The AI analyzed the error but could not generate a valid code fix.\n\nError logs:\n${logs.substring(0, 1000)}`);
    }

    console.log("=== Final Patch ===");
    console.log(patch);
    console.log("===================");

    res.json({ patch });

  } catch (err) {
    console.error("Gemini error:", err.message);

    const fallbackPatch = createDiagnosticPatch("AI Patch Error", `Gemini API Error: ${err.message}\n\nOriginal logs:\n${logs.substring(0, 500)}`);
    res.json({ patch: fallbackPatch });
  }
});

app.listen(3000, () => {
  console.log("🚀 AI Patch Server running on http://localhost:3000");
});
