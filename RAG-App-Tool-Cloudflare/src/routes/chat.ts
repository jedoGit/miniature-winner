import { Hono } from "hono";
import { embedText } from "../services/embedding";
import { querySimilar } from "../services/vectorstore";
import { generateResponse } from "../services/llm";

export const chatRoute = new Hono<{
  Bindings: { AI: Ai; VECTORIZE: VectorizeIndex; SYSTEM_PROMPT: string };
}>();

chatRoute.post("/chat", async (c) => {
  const { question } = await c.req.json();

  const queryEmbedding = await embedText(c.env.AI, question);
  const similars = await querySimilar(c.env, queryEmbedding, 3);

  const context = similars.map((v: { metadata: { chunk: any; }; }) => v.metadata?.chunk ?? "").join("\n\n");
  const systemPrompt =
    process?.env?.SYSTEM_PROMPT || c.env.SYSTEM_PROMPT;

  const answer = await generateResponse(c.env.AI, context, question, systemPrompt);

  return c.json({
    answer,
    contextUsed: similars.map((v: { id: any; }) => v.id),
  });
});
