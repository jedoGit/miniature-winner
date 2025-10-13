export async function generateResponse(
  ai: Ai,
  context: string,
  question: string,
  systemPrompt: string
): Promise<string> {
  const { response } = await ai.run("@cf/meta/llama-3.1-8b-instruct", {
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: `Context:\n${context}\n\nQuestion: ${question}` }
    ],
  });
  return response;
}
