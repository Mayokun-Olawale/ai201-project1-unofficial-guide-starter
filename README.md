# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Tips and tricks for solo traveling. Helpful because there is alot if information online that can be overwhelming to go through.
      -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 100

**Overlap:** 25

**Why these choices fit your documents:** My documents are a collections of articles and short reddit posts, which means the chunk need to be small enough to accomodate the reddit posts but also large enough to contain semantic chunks from the articles. Started with 200, realized the chunks were way too large and reduced by half.

**Final chunk count:** 147

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** 
all-MiniLM-L6-v2
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
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
"You are a solo travel assistant.

You must answer using only the provided context.
Do not use outside knowledge.
Do not guess, infer facts not present, or invent details.

If the context does not contain enough information to answer the question, you must respond with exactly:
I don't have enough information on that.

Return only the answer text. Each Answer must include at least 1 source citation in the answer.
"""


**How source attribution is surfaced in the response:**
The UI has a section for where the information is derived and each sentence also has in line citations.
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

-### Question 1
- Question: How should I chose where to travel
- Expected answer: Pick based on interests, timeframe, budget; list places by interest
- System response: When choosing where to travel, consider your interests and personal attributes, as well as your timeframe and budget (r_solotravel's Introduction to Basic Trip Planning.txt). You can also look to popular guidebook series like Lonely Planet, the Rough Guide, and Rick Steves' Europe for recommended itineraries (r_solotravel's Introduction to Basic Trip Planning.txt). Additionally, consider your hobbies, skills you'd like to learn, historical events or cultural practices you're interested in, and cuisine you'd like to try (r_solotravel's Introduction to Basic Trip Planning.txt). It's also a good idea to be conservative with your first trip and consider the safety of the area, as the author of Solo travel - Zimbabwe & Zambia.txt advises against visiting certain areas alone. (Sources: `r_solotravel's Introduction to Basic Trip Planning.txt`, `Solo travel - Zimbabwe & Zambia.txt`)
- Retrieval quality: Relevant
- Response accuracy: Partially accurate

-### Question 2
- Question: What are some things I can do in Japan?
- Expected answer: Include visiting spots mentioned in the articles (e.g., Shibuya, Shinjuku)
- System response: In Japan, some things you can do include visiting spots like Shibuya, Shinjuku, and Ikebukuro, as mentioned in [Source: 17 Best Solo Travel Destinations Worldwide.txt]. Additionally, you can try the local cuisine, explore the efficient transportation system, and experience the respectful and polite culture, as noted in the same source. However, for more specific and unusual activities, the provided documents do not offer detailed information about Japan. (Source: `17 Best Solo Travel Destinations Worldwide.txt`)
- Retrieval quality: Relevant
- Response accuracy: Partially accurate

-### Question 3
- Question: What cities can I visit in Europe and what can I do in those cities?
- Expected answer: Provide a list of ~10 cities and activities
- System response: You can visit Bratislava, Budapest, and Lisbon in Europe. In Bratislava, you can take the Post Communist Tour with Authentic Slovakia, which is highly recommended [1]. Budapest is another interesting and safe Eastern European city to visit, where you can walk across the Széchenyi Chain Bridge, visit Memento Park, and explore ruin bars like Szimpla Kert [2]. In Lisbon, you can join a free walking tour to get familiar with the city, explore its stunning architecture, and visit charming neighborhoods [3]. (Source: `17 Best Solo Travel Destinations Worldwide.txt`)
- Retrieval quality: Relevant
- Response accuracy: Partially accurate

-### Question 4
- Question: Could you give me an itinerary for navigating Ghana for the first time?
- Expected answer: Should refuse or give an incorrect answer
- System response: I don't have enough information on that.
- Retrieval quality: Off-target
- Response accuracy: Accurate

-### Question 5
- Question: Can I do a solo trip while traveling with someone?
- Expected answer: Yes — mention the article about "Solo Travel, Together"
- System response: I don't have enough information on that.
- Retrieval quality: Off-target
- Response accuracy: Inaccurate


**Question that failed:** Can I do a solo trip while traveling with someone?

**What the system returned:** I don't have enough information on that.

**Root cause (tied to a specific pipeline stage):** There are two likely causes. First, the documents contains very little explicit content about "solo travel while traveling with someone," so retrieval had few or no high-relevance chunks to surface. Second, the semantic relationship between the query and the available document (`"Solo Travel, Together"`) was not captured strongly enough by the embedding/retrieval stage.

**What you would change to fix it:** Add more targeted documents and forum posts that discuss doing "solo" activities while traveling with others (so the index contains direct matches), and upgrade or experiment with a stronger embedding model.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The spec helped with implementation because i was able to get the LLM to produce the code without having to reprompt many times. Also when I decided to change my mind about the implementation method. I could just make the LLM refer to the changes in the spec
**One way your implementation diverged from the spec, and why:**
I noticed that for the implementation of the embedding.py, the spec wasn't very specific so I had to do alot of debugging to figure out what was wrong. Eventually, I used the starter code from the tinker lab to help guide the LLM in the right direction

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* My `planning.md` file and my documents folder, and examples of how I wanted the AI Tool Plan written.
- *What it produced:* It helped gave me a more specific chunking plan for the solo travel corpus.
- *What I changed or overrode:* I made the document paths consistent and readjusted the formatting.

**Instance 2**

- *What I gave the AI:* My chunking spec from `planning.md` and the sample document set, along with the requirement to implement `Ingestion.py`.
- *What it produced:* It produced an ingestion pipeline that reads the documents, tokenizes them, splits them into overlapping chunks, and returns chunk data that can be embedded later.
- *What I changed or overrode:* I kept the basic ingestion flow but refined the output shape and chunk metadata so it fit my project better, and I asked for smaller chunks with overlap after seeing that the original chunking was mixing multiple topics together.
