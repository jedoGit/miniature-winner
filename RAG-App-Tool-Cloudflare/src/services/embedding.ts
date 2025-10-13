export async function embedText(ai: Ai, text: string): Promise<number[]> {
  const input = text.slice(0, 2000);
  const { data } = await ai.run("@cf/baai/bge-large-en-v1.5", { text: input });
  return data[0];
}
