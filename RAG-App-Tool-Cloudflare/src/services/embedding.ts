import { env } from "cloudflare:workers";

export async function embedText(ai: Ai, text: string): Promise<number[]> {

  const input = text.slice(0, 2000);

  const embedModel = env.LLM_EMBED_MODEL;
  const pooling = env.LLM_EMBED_POOLING;

  const result = await ai.run((embedModel as keyof AiModels), { text: input, pooling: pooling });

  // Type-safe extraction (AI model output is not strongly typed)
  const data = (result as any).data;
  
  if (!data || !Array.isArray(data) || !Array.isArray(data[0])) {
    throw new Error("Unexpected embedding format from AI model");
  }

  return data[0];
}