import { Hono } from "hono";
import { chatRoute } from "./routes/chat";
import { uploadRoute } from "./routes/upload";

// Load .env locally (not in production)
if (typeof process !== "undefined") {
  await import("dotenv/config");
}

const app = new Hono<{
  Bindings: {
    AI: Ai;
    VECTORIZE: VectorizeIndex;
    DB: D1Database;
    SYSTEM_PROMPT: string;
  };
}>();

app.get("/", (c) => c.text("🤖 RAG Chatbot Worker is running!"));

app.route("/api", chatRoute);
app.route("/api", uploadRoute);

export default app;
