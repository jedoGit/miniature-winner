import { env } from "cloudflare:workers";

export async function generateResponse(
  ai: Ai,
  context: string,
  question: string,
  systemPrompt: string,
  max_tokens: number,
  temperature: number,
  top_p: number,
  top_k: number
): Promise<string> {

  const chatModel = env.LLM_CHAT_MODEL;

  const result = await ai.run((chatModel as keyof AiModels), {
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: `Context:\n${context}\n\nQuestion: ${question}` }
    ],
    stream: false,
    max_tokens: max_tokens,
    temperature: temperature,
    top_p: top_p,
    top_k: top_k
  });

  if (typeof result === "string") return result;

  const response = (result as any).response ?? JSON.stringify(result);
  return typeof response === "string" ? response : JSON.stringify(response);
}
