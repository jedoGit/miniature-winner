import { marked } from "marked";

export function parseMarkdown(md: string): string {
  const html = marked(md);
  const text = html.replace(/<[^>]*>?/gm, ""); // strip HTML tags
  return text.replace(/\s+/g, " ").trim();
}
