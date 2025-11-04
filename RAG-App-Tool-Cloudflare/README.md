# Retreival Augmented Generation (RAG) Application Flow
Use-case: Chatbot for Sports and Fitness Facility that responds to guests for questions about company FAQ. It uses a company FAQ document as source of context to generate the response.

## Infrastructure
This applicattion is written in typescript and is hosted in Cloudflare using Cloudflare Workers and Workers AI.

## Parameter definition:
- top_p: Adjusts how many words that are available for the LLM model to choose from. Lower value means less words available and less creative and higher value means more choices of words and more creative.
- top_k: Limits the LLM to use the top k most probable words. Lower value means focused response and higher value means more variety and potential surprises.
- temperature: Controls the randomness of the output. Higher values produce more random results.

## Upload Flow
<img width="833" height="336" alt="image" src="https://github.com/user-attachments/assets/66802056-ee2a-44d4-bde7-d27475cd0c7b" />

## Chat Flow
<img width="979" height="376" alt="image" src="https://github.com/user-attachments/assets/06d97f93-dab0-4113-8fc3-89a99a5b1ef8" />

## Future plans
Implement an agentic AI flow using OSS-GPT-20B and provide access to tools such as web search, gmail, google sheets and google calendar using Langchain agent executor library.

# Prepare the database

## Create your resources:

### Vectorize DB Init:

If using `@cf/baai/bge-base-en-v1.5`

```
npx wrangler vectorize create rag-chatbot-index --dimensions 768 --metric=cosine
```

If using `@cf/baai/bge-small-en-v1.5`

```
npx wrangler vectorize create rag-chatbot-index --dimensions 384 --metric=cosine
```

### D1 DB Init:

```
npx wrangler d1 create rag-chatbot-db
```

# Initialize D1 DB Schema:

## Local DB Schema:

```
npx wrangler d1 execute rag-chatbot-db --local --file=./schema/D1schema.sql
```

## Remote DB Schema:

```
npx wrangler d1 execute rag-chatbot-db --remote --file=./schema/D1schema.sql
```

# Setup Cloudflare types

Ensure `Wrangler` is installed

```
npm install -g wrangler
```

Generate types. Run this everytime you update the wrangler.toml file

```
npx wrangler types
```

# Local Development

1. Install dependencies

```
npm install
tsc --init
```

2. Create .env

```
SYSTEM_PROMPT="You are a helpful and knowledgeable AI assistant."
VECTORIZE_INDEX="rag-chatbot-index"
D1_DATABASE="rag-chatbot-db"
CLOUD_FLARE_ORIGIN_CORS="list-of-urls-for CORS"
CLOUD_FLARE_ACCOUNT_ID="your account id"
CLOUD_FLARE_WORKER_AI_API_KEY="your api key"
TOP_K_VALUE="6"
CHUNK_SIZE="200"
CHUNK_OVERLAP="30"
LLM_CHAT_MODEL="@cf/meta/llama-3.2-1b-instruct"
LLM_EMBED_MODEL="@cf/baai/bge-base-en-v1.5"
```

3. Run locally

```
npm run dev
```

4. Send REST Calls to:

```
http://localhost:8787
```

# Deploy to Cloudflare

1. Login

```
npx wrangler login
```

2. Deploy

```
npm run deploy
```

3. Verify your endpoints:

| Method | Endpoint    | Description                                         |
| ------ | ----------- | --------------------------------------------------- |
| POST   | /api/upload | Upload .md file → Embeds to Vectorize + saves to D1 |
| POST   | /api/chat   | Ask a question                                      |
| GET    | /health     | Health check                                        |

# CURL Commands

## Health Endpoint

```
curl -G  "http://127.0.0.1:8787/health"
```

## Upload Endpoint

```
curl -X POST "http://127.0.0.1:8787/api/upload" -F "file=@./docs/company_faq.md" -H "Accept: application/json"
```

## Chat Endpoint

```
curl -X POST "http://127.0.0.1:8787/api/chat" -H "Content-Type: application/json" -d '{"question": "What are the membership packages available?"}'
```

# D1 DB Usefull Calls

## LOCAL DB:

### List all documents:

```
npx wrangler d1 execute rag-chatbot-db --local --command "SELECT * FROM documents;"
```

### Delete a record:

```
npx wrangler d1 execute rag-chatbot-db --local --command "DELETE FROM documents WHERE id='<record_id>';"
```

## REMOTE DB:

### List all documents:

```
npx wrangler d1 execute rag-chatbot-db --remote --command "SELECT * FROM documents;"
```

### Delete a record:

```
npx wrangler d1 execute rag-chatbot-db --remote --command "DELETE FROM documents WHERE id='<record_id>';"
```

# Vectorize DB Usefull Calls

### Delete a vector index:

```
curl -X DELETE "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/vectorize/v2/indexes/<VECTOR_INDEX>" -H "Authorization: Bearer <VECTORIZE_API_KEY>"
```
