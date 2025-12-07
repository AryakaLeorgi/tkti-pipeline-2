import express from "express";
import { explainError } from "../src/explain.js";

const app = express();
app.use(express.json({ limit: "5mb" }));

app.post("/explain", async (req, res) => {
    try {
        const logs = req.body.logs;

        const result = await explainError(logs);
        res.json({ explanation: result });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: "AI processing failed" });
    }
});

app.listen(3000, () => console.log("Explain server running on port 3000"));
