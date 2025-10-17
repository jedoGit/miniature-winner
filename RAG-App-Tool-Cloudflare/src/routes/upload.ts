import { Hono } from "hono";
import { embedText } from "../services/embedding";
import { insertVectors } from "../services/vectorstore";
import { splitRecursively } from "../services/splitter-langchain";
import { env } from "cloudflare:workers";

export const uploadRoute = new Hono<{
  Bindings: { AI: Ai; VECTORIZE: VectorizeIndex; DB: D1Database };
}>();

uploadRoute.post("/upload", async (c) => {
  // Get the form data. This is a markdown file.
  const formData = await c.req.formData();
  const file = formData.get("file") as File;

  // If there's no file received, return a 400 status
  if (!file) return c.text("No file uploaded", 400);

  // Get the content of the markdown file received then split the file recursively
  const mdFileContent = await file.text();

  const chunkSize = Number(env.UPLOAD_CHUNK_SIZE) || 800
  const chunkOverlap = Number(env.UPLOAD_CHUNK_OVERLAP) || 100

  const chunks = await splitRecursively(mdFileContent, chunkSize, chunkOverlap);

  // Let's process each chunks from after splitting recursively
  const vectors = [];
  for (const chunk of chunks) {
    // Get the chunk text
    const chunkText = chunk.pageContent
    // Call the embedding model to get the embedded values of the chunk text
    const embedding = await embedText(c.env.AI, chunkText);
    // Add the vectors to our vectors list
    const saveToVector = { id: crypto.randomUUID(), values: embedding, metadata: { chunkText } }
    vectors.push(saveToVector);
  }

  // Upsert the vectors to our vector database
  await insertVectors(c.env, vectors);

  // Save document metadata to D1
  // We want to save the the file name of the uploaded document and how many chunks were generated
  const docId = crypto.randomUUID();
  await c.env.DB.prepare(
    "INSERT INTO documents (id, name, chunks) VALUES (?1, ?2, ?3)"
  )
    .bind(docId, file.name, chunks.length)
    .run();

  return c.json({ message: "File uploaded and processed", chunks: chunks.length });
});
