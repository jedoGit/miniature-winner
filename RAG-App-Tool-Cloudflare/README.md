# Prepare the database

Create your resources:

```
wrangler vectorize create rag-chatbot-index --dimensions 1024
wrangler d1 create rag-chatbot-db

```

Initialize D1 Schema:

```
wrangler d1 execute rag-chatbot-db --file=./schema/D1schema.sql
```

# Setup Cloudflare types

Ensure Wrangler is installed

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
