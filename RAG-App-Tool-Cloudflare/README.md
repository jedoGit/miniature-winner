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
```

3. Run locally

```
npm run dev
```

→ Open: http://localhost:8787

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
| GET    | /           | Health check                                        |

# D1 DB Usefull Calls

## LOCAL DB:

### List all documents:

```
npx wrangler d1 execute rag-chatbot-db --local --command "select * from documents;"
```

### Delete a record:

```
npx wrangler d1 execute rag-chatbot-db --local --command "delete from documents where id='<record_id>';"
```

# CURL Commands

## Upload Endpoint

```
curl -X POST "http://127.0.0.1:8787/api/upload" -F "file=@./docs/company_faq.md" -H "Accept: application/json"
```

## Chat Endpoint

```
curl -X POST "http://127.0.0.1:8787/api/chat" -H "Content-Type: application/json" -d '{"question": "What are the membership packages available at nZone?"}'
```
