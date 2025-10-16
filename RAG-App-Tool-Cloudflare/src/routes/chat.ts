import { Hono } from "hono";
import { embedText } from "../services/embedding";
import { querySimilar } from "../services/vectorstore";
import { generateResponse } from "../services/llm";

export const chatRoute = new Hono<{
  Bindings: { AI: Ai; VECTORIZE: VectorizeIndex; SYSTEM_PROMPT: string };
}>();

chatRoute.post("/chat", async (c) => {
  const { question } = await c.req.json();

  // Create embedding to the question received from chat
  const queryEmbedding = await embedText(c.env.AI, question);
  // Query the vector database and pass the embeded values for the received question and tell the database to only requturn the top 3
  const topK = Number(process?.env?.TOP_K_VALUE) || 3;
  const similars = await querySimilar(c.env, queryEmbedding, topK);

  // Create the context list.
  const context = similars.map((v: { metadata: { chunkText: any; }; }) => v.metadata?.chunkText ?? "").join("\n\n");
  const systemPrompt = process?.env?.SYSTEM_PROMPT;
  const temperature = process?.env?.LLM_CHAT_TEMPERATURE;
  const max_tokens = process?.env?.LLM_CHAT_MAX_TOKENS;
  const top_p = process?.env?.LLM_CHAT_TOP_P;
  const top_k = process?.env?.LLM_CHAT_TOP_K;
  
  // Ask the LLM to generate a response based on context, question and system prompt
  const answer = await generateResponse(c.env.AI, context, question, systemPrompt, Number(max_tokens), Number(temperature), Number(top_p), Number(top_k));

  return c.json({
    answer,
    contextUsed: similars.map((v: { id: any; }) => v.id),
  });
});
