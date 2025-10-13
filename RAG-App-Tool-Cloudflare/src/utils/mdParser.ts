import { marked } from "marked";

export async function parseMarkdown(md: string): Promise<string> {
  const html = await marked(md); // `marked()` is async now
  const text = html.replace(/<[^>]*>?/gm, ""); // strip HTML tags
  return text.replace(/\s+/g, " ").trim();
}
