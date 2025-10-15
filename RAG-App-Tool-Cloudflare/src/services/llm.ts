export async function generateResponse(
  ai: Ai,
  context: string,
  question: string,
  systemPrompt: string
): Promise<string> {
  
  const chatModel = process?.env?.LLM_CHAT_MODEL;

  const result = await ai.run((chatModel as keyof AiModels), {
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: `Context:\n${context}\n\nQuestion: ${question}` }
    ],
    stream: false
  });

  if (typeof result === "string") return result;

  const response = (result as any).response ?? JSON.stringify(result);
  return typeof response === "string" ? response : JSON.stringify(response);
}
