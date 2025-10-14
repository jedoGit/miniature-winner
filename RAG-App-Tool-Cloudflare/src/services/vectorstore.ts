export async function insertVectors(env: any, vectors: any[]) {
  await env.VECTORIZE.upsert(vectors);
}

export async function querySimilar(env: any, embedding: number[], topK = 3) {
  const results = await env.VECTORIZE.query(embedding, {
    topK: topK,
    returnValues: true,
    returnMetadata: "all",
  });
  return results.matches || [];
}
