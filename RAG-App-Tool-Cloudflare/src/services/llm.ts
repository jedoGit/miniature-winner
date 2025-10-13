export async function generateResponse(
  ai: Ai,
  context: string,
  question: string,
  systemPrompt: string
): Promise<string> {
  const result = await ai.run("@cf/meta/llama-3.1-8b-instruct-fp8", {
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
