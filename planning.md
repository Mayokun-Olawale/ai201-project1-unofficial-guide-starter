# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
<!-- Tips and tricks for solo traveling. Helpful because there is alot if information online that can be overwhelming to go through. -->

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | “Solo Travel, Together” Might Just Be Our Favorite New Trip Idea | Article | documents/“Solo Travel, Together” Might Just Be Our Favorite New Trip Idea.txt
| 2 | 17 Best Solo Travel Destinations Worldwide | Article | documents/17 Best Solo Travel Destinations Worldwide.txt
| 3 | 5 Reasons Solo Travel is Worth It | Article | documents/5 Reasons Solo Travel is Worth It.txt
| 4 | How To Travel Alone And Enjoy It (And It’s Much Easier Than You Think) | Article | documents/How To Travel Alone And Enjoy It (And It’s Much Easier Than You Think).txt
| 5 | How to Travel Alone for the First time | Article | documents/How to Travel Alone for the First time.txt
| 6 | I Traveled Around the World Alone and Without a Plan—Here's My No. 1 Tip for Solo Travelers | Article | documents/I Traveled Around the World Alone and Without a Plan—Here's My No. 1 Tip for Solo Travelers.txt
| 7 | r_solotravel's Introduction to Basic Trip Planning | Reddit (r/solotravel) | documents/r_solotravel's Introduction to Basic Trip Planning.txt
| 8 | Solo travel - Zimbabwe & Zambia | Reddit (r/solotravel) | documents/Solo travel - Zimbabwe & Zambia.txt
| 9 | Solo Travel Tips for First Timers | Reddit (r/solotravel) | documents/Solo Travel Tips for First Timers.txt
| 10 | What are the fun unusual things you do while solo traveling? | Reddit (r/solotravel) | documents/What are the fun unusual things you do while solo traveling_.txt
| 11 | Why Travelling Alone Will Change You Forever | Article | documents/Why Travelling Alone Will Change You Forever.txt


---

## Chunking Strategy

<!-- How will you split documents into chunks? 
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
I plan to split the documents into 100 token chunks. Decided to change from 200 to 100 tokens because I saw that the chunks were really large and contained multiple topics within one chunk.

**Overlap:**
A 25 token overlap

**Reasoning:**
This is because the documents are a combination of long articles and short reddit posts so I want a number that can try to accurately capture these difference

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)? 5
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
I used `all-MiniLM-L6-v2` (sentence-transformers). This model provides compact
384-dimensional embeddings with a good balance of speed, cost, and semantic
accuracy for short-to-medium-length articles and Reddit posts.
**Top-k:**
5
**Production tradeoff reflection:**

- **Accuracy vs cost:** If cost wasn't a constraint, I'd choose a higher-capacity
     model (e.g., `all-mpnet-base-v2` or a large commercial embedding like
     `text-embedding-3-large`) for better semantic matching on domain-specific text.
- **Context length:** For very long documents, prioritize chunking and retrieval
     strategy (larger chunks, overlap) or use models that support longer contexts.
- **Multilingual support:** Use multilingual embeddings (LaBSE, multilingual MPNet)
     if content or users are multilingual.
- **Latency & storage:** Larger embeddings increase latency, storage, and index
     size; balance with approximate nearest neighbor settings (HNSW/FAISS) and
     possible hybrid retrieval (cheap model for recall + expensive model for rerank).
- **Recommendation:** Start with `all-MiniLM-L6-v2` for development, evaluate
     retrieval quality on held-out Q&A, and upgrade to a higher-capacity or
     multilingual model if accuracy requirements demand it.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

Question 1
Question: How should I chose where to travel
Expected Answer: Something along the line of picking based on one's interests(maybe including a list of places based on interests)
Actual Answer: When choosing where to travel, consider your interests and personal attributes, as well as your timeframe and budget (r_solotravel's Introduction to Basic Trip Planning.txt). You can also look to popular guidebook series like Lonely Planet, the Rough Guide, and Rick Steves' Europe for recommended itineraries (r_solotravel's Introduction to Basic Trip Planning.txt). Additionally, consider your hobbies, skills you'd like to learn, historical events or cultural practices you're interested in, and cuisine you'd like to try (r_solotravel's Introduction to Basic Trip Planning.txt). It's also a good idea to be conservative with your first trip and consider the safety of the area, as the author of Solo travel - Zimbabwe & Zambia.txt advises against visiting certain areas alone.

Question 2
Question: what are some things i can do in japan
Expected Answer: Include visiting spots as mentioned in one of the articles
Actual Answer: In Japan, some things you can do include visiting spots like Shibuya, Shinjuku, and Ikebukuro, as mentioned in [Source: 17 Best Solo Travel Destinations Worldwide.txt]. Additionally, you can try the local cuisine, explore the efficient transportation system, and experience the respectful and polite culture, as noted in the same source. However, for more specific and unusual activities, the provided documents do not offer detailed information about Japan.

Question 3
Question: What cities can i visit in europe and what can i do in those cities?
Expected Answer: A list of about 10 countries
Actual Answer: You can visit Bratislava, Budapest, and Lisbon in Europe. In Bratislava, you can take the Post Communist Tour with Authentic Slovakia, which is highly recommended [1]. Budapest is another interesting and safe Eastern European city to visit, where you can walk across the Széchenyi Chain Bridge, visit Memento Park, and explore ruin bars like Szimpla Kert [2]. In Lisbon, you can join a free walking tour to get familiar with the city, explore its stunning architecture, and visit charming neighborhoods [3]. 


Question 4
Question: Could you give me an itenerary for naviagting Ghana for the first time
Expected Answer: Should refuse to answer or give an incorrect answer
Actual Answer: I don't have enough information on that.

Question 5
Question: Can i do a solo trip while traveling with someone
Expected Answer: Yes, mention artcile about "Solo Travel Together"
Actual Answer: I don't have enough information on that.



---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. A lot of hallucination especially for questions that are outside the contexts of the articles written

2. Irrelevant information: Because of the diverse length of articles, the chunks sizes are not optimal for all the documents which could lead to a bad retrival

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```text
Document Ingestion
     [Python file reads from documents/]
                    |
                    v
Chunking
     [Token-based splitter: 100 tokens + 25 token overlap]
                    |
                    v
Embedding + Vector Store
     [sentence-transformers: all-MiniLM-L6-v2 + FAISS]
                    |
                    v
Retrieval
     [Top-k = 5 similarity search]
                    |
                    v
Generation
     [LLM prompt with retrieved chunks + grounded answer/citations]
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
- I plan to use Copilot to Implement the Ingestion.py file that reads the files from the documents, chunks it and returns it for embedding. I plan on using the chunking strategy and diagram from the planning.md file. I expect it to produce a fully functioning class for chucking documents. I will verfiy the output matches my spec by asking it to generate 10 random chucks and seeing if what is generated natches my spec.

**Milestone 4 — Embedding and retrieval:**
- I plan to use Copilot to implement `Embeddings.py` that creates a persistent Chroma client (`chromadb.PersistentClient(path=...)`), configures `SentenceTransformerEmbeddingFunction(model_name='all-MiniLM-L6-v2')`, and exposes `get_collection()`, `embed_and_store(chunks)`, and `retrieve(query, n_results)`. It should persist `metadata` (`file_name`, `chunk_index`, `start_token`, `end_token`) and include a small CLI/snippet to bulk-embed flattened chunks from `ingest_documents()`. I will verify this by running a script in the project venv that ingests documents, calls `embed_and_store(...)`, asserts `get_collection().count() > 0`, calls `retrieve(test_query, n_results=4)` and inspects returned items.


**Milestone 5 — Generation and interface:**
- I plan to use Copilot to implement `generation.py`, `query.py`, and `app.py`. `generation.py` will implement a strict grounding `SYSTEM_PROMPT`, `format_context(chunks)`, and `generate_answer(query, chunks)` that calls the LLM client. `query.py` will glue ingestion→embedding→retrieval→generation with `ensure_indexed()` and return `{answer, sources}` where `sources` are derived programmatically from retrieved chunk metadata. `app.py` will be a Gradio UI that accepts a question, calls `query.ask()`, and displays the answer and deduplicated source filenames. I will verify by installing dependencies in the venv, confirm in-scope queries return grounded answers and out-of-scope queries return "I don't have enough information on that.", and launching the Gradio app to manually exercise the UI.

