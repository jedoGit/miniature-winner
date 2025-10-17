import { Hono } from "hono";
import { embedText } from "../services/embedding";
import { querySimilar } from "../services/vectorstore";
import { generateResponse } from "../services/llm";
import { env } from "cloudflare:workers";

interface KV_RATE_LIMIT_RETURN_TYPE {
  start: number;
  count: number;
}

export const chatRoute = new Hono<{
  Bindings: Env
}>();

// Helper: rate-limit key
function rateLimitKey(ip: string) {
  return `rate:${ip}`;
}

// Rate limit settings
const RATE_LIMIT_MAX = 10; // 10 requests
const RATE_LIMIT_WINDOW_MS = 60 * 1000; // per minute
const RATE_KV_TTL = 120

chatRoute.post("/chat", async (c) => {
  const body = await c.req.json();
  const turnstileToken = body["cf-turnstile-response"];
  const question = body["question"];

  const ip = c.req.header("CF-Connecting-IP") || "unknown";

  // Rate limiting
  if (!c.env.RATE_LIMIT_KV) {
    console.warn("RATE_LIMIT_KV binding not found.");
  } else {
    const key = rateLimitKey(ip);
    const current : KV_RATE_LIMIT_RETURN_TYPE | null = await c.env.RATE_LIMIT_KV.get(key, "json");
    const now = Date.now();

    if (current && now - current.start < RATE_LIMIT_WINDOW_MS) {
      if (current.count >= RATE_LIMIT_MAX) {
        return c.json({ error: "Rate limit exceeded. Try again later." }, 429);
      } else {
        await c.env.RATE_LIMIT_KV.put(
          key,
          JSON.stringify({ start: current.start, count: current.count + 1 }),
          { expirationTtl: RATE_KV_TTL }
        );
      }
    } else {
      await c.env.RATE_LIMIT_KV.put(
        key,
        JSON.stringify({ start: now, count: 1 }),
        { expirationTtl: RATE_KV_TTL }
      );
    }
  }

  // console.log(question)
  // console.log(turnstileToken)

  // Check if we receive the turnstile token
  // if (!question || !turnstileToken) {
  //   return c.json({ error: "Missing required field." }, 400);
  // }

  // Verify Turnstile Token
  
  // console.log(ip)

  // const formData = new FormData();
  // formData.append("secret", String(env.TURNSTILE_SECRET_KEY));
  // formData.append("response", String(turnstileToken));
  // formData.append("remoteip", ip);

  // const turnstileRes = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
  //   method: "POST",
  //   body: formData,
  // });

  // console.log(turnstileRes)

  // const turnstileData = await turnstileRes.json<{ success: boolean }>();
  // if (!turnstileData.success) {
  //   return c.json({ error: "Failed Turnstile verification." }, 403);
  // }

  // Create embedding to the question received from chat
  const queryEmbedding = await embedText(c.env.AI, question);
  // Query the vector database and pass the embeded values for the received question and tell the database to only requturn the top 3
  const topK = Number(env.CHAT_TOP_K_VALUE) || 3;
  const similars = await querySimilar(c.env, queryEmbedding, topK);

  // Create the context list.
  const context = similars.map((v: { metadata: { chunkText: any; }; }) => v.metadata?.chunkText ?? "").join("\n\n");
  const systemPrompt = env.CHAT_SYSTEM_PROMPT;
  const temperature = env.LLM_CHAT_TEMPERATURE;
  const max_tokens = env.LLM_CHAT_MAX_TOKENS;
  const top_p = env.LLM_CHAT_TOP_P;
  const top_k = env.LLM_CHAT_TOP_K;
  
  // Ask the LLM to generate a response based on context, question and system prompt
  const answer = await generateResponse(c.env.AI, context, question, systemPrompt, Number(max_tokens), Number(temperature), Number(top_p), Number(top_k));

  return c.json({
    answer,
    contextUsed: similars.map((v: { id: any; }) => v.id),
  });
});
