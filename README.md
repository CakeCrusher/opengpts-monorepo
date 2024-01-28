_This project is part of the OpenGPTs initiative aimed at providing a fully open-source GPTs alternative._

# OpenGPTs Monorepo

The OpenGPTs Monorepo consists of two services a [Svelte client (/frontend)](/frontend) and [the GPTs to Assistants API (/backend)](/backend).

This repo consists of the client and business layer of an initiative to open-source GPTs.

If you would like to connect it to an open-source Assistants API simply add the [`ASSISTANTS_API`env variable](.env.example) otherwise it will direct requests to OpenAI Assistants API, which is limited in features.

## Quickstart
1. Create `.env` file with contents of [`.env.example`](.env.example) and fill the missing fields.
2. Run [`./runprod.sh`](runprod.sh)

## Development Quickstart
1. Create `.env` file with contents of [`.env.example`](.env.example) and fill the missing fields.
2. Run [`./rundev.sh`](rundev.sh)
3. Run `cd [./frontend](/frontend)`
4. Run `npm install`
5. Run `npm run dev`

## Others involved in OpenGPTs 
-  [assistants](https://github.com/stellar-amenities/assistants): open-sourced OpenAI assistants api
- [Agent Artificial (discord link)](https://discord.gg/yKE2Q52R): Provide LLM infrastructure.
