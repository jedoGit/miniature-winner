import { Hono } from "hono";
import { embedText } from "../services/embedding";
import { insertVectors } from "../services/vectorstore";
import { splitRecursively } from "../services/splitter";
import { parseMarkdown } from "../utils/mdParser";

export const uploadRoute = new Hono<{
  Bindings: { AI: Ai; VECTORIZE: VectorizeIndex; DB: D1Database };
}>();

uploadRoute.post("/upload", async (c) => {
  const formData = await c.req.formData();
  const file = formData.get("file") as File;

  if (!file) return c.text("No file uploaded", 400);

  const content = await file.text();
  const plainText = parseMarkdown(content);
  const chunks = splitRecursively(plainText, 800, 100);

  const vectors = [];
  for (const chunk of chunks) {
    const embedding = await embedText(c.env.AI, chunk);
    vectors.push({ id: crypto.randomUUID(), values: embedding, metadata: { chunk } });
  }

  await insertVectors(c.env, vectors);

  // Save document metadata to D1
  const docId = crypto.randomUUID();
  await c.env.DB.prepare(
    "INSERT INTO documents (id, name, chunks) VALUES (?1, ?2, ?3)"
  )
    .bind(docId, file.name, chunks.length)
    .run();

  return c.json({ message: "File uploaded and processed", chunks: chunks.length });
});
