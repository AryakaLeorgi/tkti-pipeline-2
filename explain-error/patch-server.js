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

  console.log("=== Logs received ===");
  console.log(logs);
  console.log("=====================");

  const prompt = `You are an expert AI that analyzes CI/CD build errors and generates Git unified diff patches to fix the code.

TASK: Analyze the build error logs and source code below. Generate a VALID unified diff patch to fix the bug.

CRITICAL RULES FOR PATCH FORMAT:
1. For modifying existing files use:
   --- a/path/to/file.js
   +++ b/path/to/file.js
   
2. For new files use:
   --- /dev/null
   +++ b/path/to/newfile.js

3. Hunk header format: @@ -start,count +start,count @@
   - start = line number where changes begin
   - count = number of lines in that section

4. Line prefixes:
   - Lines starting with "-" are REMOVED
   - Lines starting with "+" are ADDED  
   - Lines with " " (space) are CONTEXT (unchanged)

5. Include 3 lines of context before and after changes

6. NO markdown code blocks (\`\`\`), NO backticks, NO extra explanation
7. Output ONLY the raw patch content, nothing else

EXAMPLE of a valid patch that fixes a typo:
--- a/src/calculator.js
+++ b/src/calculator.js
@@ -23,7 +23,7 @@
 // Export functions
 module.exports = {
     add,
-    subtrac,  // typo: should be "subtract"
+    subtract,
     multiply,
     divide
 };

BUILD LOGS AND SOURCE CODE:
${logs}

Generate the patch now:`;

  try {
    const result = await model.generateContent(prompt);
    let patch = result.response.text().trim();

    console.log("=== Raw AI Response ===");
    console.log(patch);
    console.log("=======================");

    // Remove markdown code blocks if present
    patch = patch.replace(/^```[\w]*\n?/gm, "").replace(/\n?```$/gm, "").trim();

    // Validate patch has required format
    if (!patch || !patch.includes("---") || !patch.includes("+++") || !patch.includes("@@")) {
      console.log("Invalid patch format detected, using diagnostic fallback");
      patch = createDiagnosticPatch("AI Analysis", `The AI analyzed the error but could not generate a valid code fix.\n\nError logs:\n${logs}`);
    }

    console.log("=== Final Patch ===");
    console.log(patch);
    console.log("===================");

    res.json({ patch });

  } catch (err) {
    console.error("Gemini error:", err.message);

    const fallbackPatch = createDiagnosticPatch("AI Patch Error", `Gemini API Error: ${err.message}\n\nOriginal logs:\n${logs}`);
    res.json({ patch: fallbackPatch });
  }
});

app.listen(3000, () => {
  console.log("🚀 AI Patch Server running on http://localhost:3000");
});
