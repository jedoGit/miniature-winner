import { Hono } from "hono";
import { cors } from "hono/cors";
import { chatRoute } from "./routes/chat";
import { uploadRoute } from "./routes/upload";
import { env } from "cloudflare:workers";

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

const corsOrigin = String(env.CLOUD_FLARE_CORS_ORIGIN).split(/[, ]+/);
const corsAllowHeaders = String(env.CLOUD_FLARE_CORS_ALLOW_HEADERS).split(/[, ]+/);
const corsAllowMethods = String(env.CLOUD_FLARE_CORS_ALLOW_METHODS).split(/[, ]+/);
const corsMaxAge = Number(env.CLOUD_FLARE_CORS_MAX_AGE);
const corsCredentials = Boolean(env.CLOUD_FLARE_CORS_CREDENTIALS)

app.use("/*",
  cors({
    origin: corsOrigin,
    allowHeaders: corsAllowHeaders,
    allowMethods: corsAllowMethods,
    maxAge: corsMaxAge,
    credentials: corsCredentials
  })
);

// app.get("/", (c) => c.text("🤖 RAG Chatbot Worker is running!"));
app.get("/health", (c) => c.json({
  status: "ok",
}));
app.route("/api", chatRoute);
app.route("/api", uploadRoute);

export default app;
