import express from "express";
import { explainError } from "./explain.js";
import dotenv from "dotenv";
dotenv.config();

const app = express();
app.use(express.json({ limit: "5mb" }));

app.post("/explain", async (req, res) => {
    try {
        const logs = req.body.logs || "";
        if (!logs.trim()) {
            return res.status(400).json({ error: "Logs are required" });
        }

        const result = await explainError(logs);
        res.json({ explanation: result });

    } catch (err) {
        console.error("Error:", err.message);
        res.status(500).json({ error: "Failed to process logs" });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Explain Error API running on port ${PORT}`));
