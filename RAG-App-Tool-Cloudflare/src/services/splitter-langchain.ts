import { Document } from '@langchain/core/documents';
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter'

export async function splitRecursively(
  text: string,
  chunkSize = 800,
  chunkOverlap = 100
): Promise<Document<Record<string, any>>[]> {
  
    const splitter = new RecursiveCharacterTextSplitter({
        chunkSize: chunkSize,
        chunkOverlap: chunkOverlap
    });

    const chunks = await splitter.createDocuments([text])
  
    return chunks;
}
