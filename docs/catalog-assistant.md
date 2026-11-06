# Catalog assistant

Ordinary text sent outside a command flow is answered by an OpenAI Responses API
assistant. It can call three read-only functions: list categories, search available
products, and inspect an available product by ID. Commands, admin changes,
checkout, and payment stay in the existing deterministic Telegram handlers.

Set `OPENAI_API_KEY` in the ignored `.env` file. `OPENAI_MODEL` defaults to
`gpt-5.4-mini` and can be overridden there. The assistant has a 1,000 character
input cap, four tool call cap, three response round cap, and 15 second API timeout.
It returns a localized service message if the API fails.

The model sees the message sent to the assistant and catalog data returned by
its chosen tools. Do not send payment details, passwords, addresses, or other
personal information in an ordinary chat message. Catalog descriptions are
treated as untrusted input, and no model tool can write to the database.

For manual verification, run the bot and ask a product question in ordinary
chat. Then test `/search` and a purchase separately to confirm the existing
checkout path still handles payments.
