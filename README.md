# Legal Multi-Agent MVP

This repository now contains a prompt-driven legal multi-agent backend with local RAG retrieval and SQLite persistence.

## Implemented

- 5-agent orchestration pipeline: intake, facts, retrieval, reasoning, review
- pluggable LLM provider interface
- default mock provider for offline development
- optional OpenAI-compatible chat completion provider through environment variables
- local legal knowledge base loaded from `data/legal_knowledge.json`
- lexical RAG retriever that ranks statutes and case-like materials
- SQLite persistence for cases, materials, and analysis results
- `POST /analysis` to create an analysis
- `GET /analysis/{analysis_id}` to fetch a stored analysis

## Configuration

Environment variables:

- `LEGAL_LLM_PROVIDER=mock` or `openai-compatible`
- `LEGAL_LLM_MODEL=<model-name>`
- `LEGAL_LLM_API_KEY=<api-key>`
- `LEGAL_LLM_BASE_URL=<chat-completions-base-url>`

If no provider is configured, the app falls back to the built-in mock provider.

## Run

```bash
python -m uvicorn app.main:app --reload
```

## Example Request

```json
{
  "user_query": "请审查这份合同中的解除条款和违约责任风险",
  "materials": [
    {
      "title": "服务合同",
      "content": "甲方委托乙方提供服务。若乙方逾期15日未完成交付，甲方可以解除合同。违约金按合同总价的30%计算。"
    }
  ]
}
```

## Persistence

SQLite database path:

- `data/legal_agent.db`

Tables:

- `cases`
- `materials`
- `analyses`

## Next Steps

- replace lexical retrieval with embeddings and vector search
- add statute versioning and effective-date filters
- add separate prompts and tools for labor, litigation, and compliance agents
- add document parsers for PDF, DOCX, and OCR inputs
