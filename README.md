<h1 align="center">RAG Document Assistant</h1>

<p align="center">
  <strong>AI-powered document ingestion, conversational RAG, and interview booking backend.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue" alt="Python 3.12">
  <img src="https://img.shields.io/badge/FastAPI-Backend-green" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-Database-blue" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Redis-Memory-red" alt="Redis">
  <img src="https://img.shields.io/badge/Weaviate-Vector%20DB-orange" alt="Weaviate">
  <img src="https://img.shields.io/badge/Groq-LLM-purple" alt="Groq">
</p>

<hr>

<h2>📌 Overview</h2>

<p>
RAG Document Assistant is a modular backend application built with
<strong>FastAPI</strong>. It provides document ingestion, custom
Retrieval-Augmented Generation (RAG), conversational memory, and
LLM-powered interview booking.
</p>

<p>
The project was designed to satisfy the requirements of an AI/ML backend
assignment while following clean architecture, type-safe Python, explicit
RAG implementation, and modular service boundaries.
</p>

<h2>🚀 Features</h2>

<ul>
  <li>📄 Upload and process <code>.pdf</code> and <code>.txt</code> documents</li>
  <li>✂️ Two selectable document chunking strategies</li>
  <li>🧠 Generate embeddings for document chunks</li>
  <li>🔎 Semantic vector search using Weaviate Cloud</li>
  <li>💬 Custom RAG pipeline without <code>RetrievalQAChain</code></li>
  <li>🧠 Multi-turn conversational memory using Redis</li>
  <li>🎯 LLM-based intent detection</li>
  <li>📅 Multi-turn interview booking</li>
  <li>📋 LLM-based extraction of booking details</li>
  <li>🗄️ PostgreSQL persistence for documents and bookings</li>
  <li>📚 Source attribution for RAG responses</li>
  <li>🔐 Environment-based configuration</li>
</ul>

<h2>🏗️ Architecture</h2>

<pre>
                         ┌─────────────────┐
                         │     Client      │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     FastAPI     │
                         └────────┬────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             Document Ingestion            Chat API
                    │                           │
                    ▼                           ▼
             Text Extraction             Intent Detection
                    │                    ┌──────┴──────┐
                    ▼                    │             │
                Chunking                RAG         Booking
                    │                    │             │
                    ▼                    ▼             ▼
               Embeddings           Retrieval     Extraction
                    │                    │             │
                    ▼                    ▼             ▼
                Weaviate             Weaviate       Redis
                    │                                  │
                    ▼                                  ▼
               PostgreSQL                         PostgreSQL
</pre>

<h2>🧰 Technology Stack</h2>

<table>
  <thead>
    <tr>
      <th>Component</th>
      <th>Technology</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Backend</td>
      <td>FastAPI</td>
      <td>REST API</td>
    </tr>
    <tr>
      <td>Language</td>
      <td>Python 3.12</td>
      <td>Application development</td>
    </tr>
    <tr>
      <td>LLM</td>
      <td>Groq</td>
      <td>Generation, intent detection and extraction</td>
    </tr>
    <tr>
      <td>Embeddings</td>
      <td>Local embedding model</td>
      <td>Semantic representation</td>
    </tr>
    <tr>
      <td>Vector Database</td>
      <td>Weaviate Cloud</td>
      <td>Semantic document retrieval</td>
    </tr>
    <tr>
      <td>Database</td>
      <td>PostgreSQL</td>
      <td>Persistent application data</td>
    </tr>
    <tr>
      <td>ORM</td>
      <td>SQLAlchemy</td>
      <td>Database access</td>
    </tr>
    <tr>
      <td>Memory</td>
      <td>Redis</td>
      <td>Conversation history</td>
    </tr>
    <tr>
      <td>Validation</td>
      <td>Pydantic</td>
      <td>Request and structured output validation</td>
    </tr>
  </tbody>
</table>

<h2>📁 Project Structure</h2>

<pre>
Rag-document-asssistant/
│
├── src/
│   ├── config.py
│   ├── main.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   ├── init_db.py
│   │   └── models.py
│   │
│   ├── routers/
│   │   ├── chat.py
│   │   └── ingestion.py
│   │
│   └── services/
│       ├── booking.py
│       ├── booking_service.py
│       ├── chunking.py
│       ├── embeddings.py
│       ├── extractor.py
│       ├── intent.py
│       ├── llm.py
│       ├── memory.py
│       ├── rag.py
│       ├── retriever.py
│       └── vector_store.py
│
├── pyproject.toml
├── uv.lock
└── README.md
</pre>

<p>
Note: there is no automated <code>tests/</code> suite or <code>.env.example</code>
yet — required environment variables are listed under "Configure Environment"
below.
</p>

<h2>🔄 RAG Pipeline</h2>

<pre>
User Question
      │
      ▼
Query Embedding
      │
      ▼
Weaviate Vector Search
      │
      ▼
Top-K Relevant Chunks
      │
      ▼
Context Construction
      │
      ▼
Groq LLM
      │
      ▼
Answer + Sources
</pre>

<p>
The RAG pipeline is implemented explicitly rather than relying on
high-level retrieval chains.
</p>

<p>
The LLM receives the retrieved document context and is instructed to answer
only from that context. This reduces unsupported or hallucinated responses.
</p>

<h2>📄 Document Ingestion</h2>

<pre>
Upload File
    │
    ▼
Validate File
    │
    ▼
Extract Text
    │
    ▼
Select Chunking Strategy
    │
    ▼
Generate Embeddings
    │
    ▼
Store Chunks → Weaviate
    │
    ▼
Store Metadata → PostgreSQL
</pre>

<p><strong>Supported formats:</strong></p>

<ul>
  <li><code>.pdf</code></li>
  <li><code>.txt</code></li>
</ul>

<p>Document chunks contain metadata such as:</p>

<pre>
document_id
filename
section
chunk_index
text
</pre>

<p>
<code>document_id</code>, <code>chunking_strategy</code>, <code>chunk_index</code>,
and <code>section</code> are also persisted in PostgreSQL (see the Database
Design section below), linked to each chunk's Weaviate object id — so chunk
metadata can be queried from SQL without going back to the vector store.
</p>

<h2>🧠 Conversational Memory</h2>

<p>
Redis is used to maintain multi-turn conversation history.
</p>

<pre>
chat:history:&lt;conversation_id&gt;
</pre>

<p>Example message:</p>

<pre>
{
  "role": "user",
  "content": "What technologies does the company use?"
}
</pre>

<p>
The system retains recent messages so that follow-up questions can be
understood within the conversation.
</p>

<h2>🎯 Intent Detection</h2>

<p>The application currently supports two main intents:</p>

<table>
  <tr>
    <th>Intent</th>
    <th>Example</th>
  </tr>
  <tr>
    <td><code>RAG</code></td>
    <td>What technologies does the company use?</td>
  </tr>
  <tr>
    <td><code>RAG</code></td>
    <td>Tell me about the architecture.</td>
  </tr>
  <tr>
    <td><code>BOOKING</code></td>
    <td>I want to schedule an interview.</td>
  </tr>
  <tr>
    <td><code>BOOKING</code></td>
    <td>Can I book an interview?</td>
  </tr>
</table>

<h2>📅 Interview Booking</h2>

<p>
Interview booking is implemented as a multi-turn conversational workflow.
The LLM extracts structured booking information from natural language.
</p>

<h3>Required Information</h3>

<ul>
  <li>Name</li>
  <li>Email</li>
  <li>Interview date</li>
  <li>Interview time</li>
</ul>

<h3>Example Conversation</h3>

<pre>
User:
I want to schedule an interview.

Assistant:
Sure! What is your name?

User:
My name is Sandip.

Assistant:
Thanks, Sandip. What is your email?

User:
My email is sandip@example.com.

Assistant:
What date would you prefer for the interview?

User:
August 20.

Assistant:
What time would you prefer for the interview?

User:
10 AM.
</pre>

<p>
Once all required fields are available, the booking is validated and stored
in PostgreSQL.
</p>

<h2>🗄️ Database Design</h2>

<h3>Documents</h3>

<pre>
documents
├── id
├── filename
├── content_type
├── source
├── chunking_strategy
├── chunk_count
└── created_at
</pre>

<h3>Document Chunks</h3>

<p>
Each chunk stored in Weaviate has a matching row here, so a document's
metadata can be cross-referenced between PostgreSQL and the vector store.
</p>

<pre>
document_chunks
├── id
├── document_id   (→ documents.id)
├── weaviate_id   (→ Weaviate object id)
├── chunk_index
└── section
</pre>

<h3>Bookings</h3>

<pre>
bookings
├── id
├── name
├── email
├── booking_date
├── booking_time
└── created_at
</pre>

<h2>🔴 Redis Memory</h2>

<p>Conversation history is stored using:</p>

<pre>
chat:history:&lt;conversation_id&gt;
</pre>

<p>
Only the most recent messages are retained to prevent unlimited conversation
growth.
</p>

<h2>⚙️ Installation</h2>

<h3>Requirements</h3>

<ul>
  <li>Python 3.12+</li>
  <li>uv</li>
  <li>PostgreSQL</li>
  <li>Redis</li>
  <li>Weaviate Cloud</li>
  <li>Groq API key</li>
</ul>

<h3>1. Clone Repository</h3>

<pre>
git clone https://github.com/sanshre-sandip/Rag-document-asssistant.git
cd Rag-document-asssistant
</pre>

<h3>2. Install Dependencies</h3>

<pre>
uv sync
</pre>

<h3>3. Configure Environment</h3>

<p>Create a <code>.env</code> file:</p>

<pre>
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost/DATABASE

WEAVIATE_CLUSTER_URL=https://YOUR-CLUSTER.weaviate.network
WEAVIATE_API_KEY=YOUR_WEAVIATE_API_KEY

GROQ_API=YOUR_GROQ_API_KEY
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=YOUR_GROQ_MODEL

REDIS_URL=redis://localhost:6379/0
</pre>

<p>
<strong>Do not commit real API keys or database credentials.</strong>
</p>

<h3>4. Initialize Database</h3>

<pre>
uv run python -m src.db.init_db
</pre>

<h3>5. Start Redis</h3>

<pre>
sudo systemctl enable --now redis-server
</pre>

<p>Verify Redis:</p>

<pre>
redis-cli ping
</pre>

<p>Expected:</p>

<pre>
PONG
</pre>

<h3>6. Start FastAPI</h3>

<pre>
uv run uvicorn src.main:app --reload
</pre>

<p>
API:
<code>http://127.0.0.1:8000</code>
</p>

<p>
Interactive API documentation:
<code>http://127.0.0.1:8000/docs</code>
</p>

<h2>🔌 API Endpoints</h2>

<h3>Health Check</h3>

<pre>
GET /api/v1/chat/health
</pre>

<h3>Conversational RAG</h3>

<pre>
POST /api/v1/chat
</pre>

<p>Request:</p>

<pre>
{
  "conversation_id": "demo-001",
  "message": "What technologies does the company use?",
  "limit": 3
}
</pre>

<p>Example response:</p>

<pre>
{
  "answer": "The company uses Python, FastAPI, PostgreSQL, Redis, and Weaviate Cloud.",
  "sources": [
    {
      "document_id": "...",
      "filename": "sample.txt",
      "section": "Technology",
      "chunk_index": 1
    }
  ]
}
</pre>

<h2>🧪 Testing & Verification</h2>

<p>Python compilation:</p>

<pre>
uv run python -m py_compile src/routers/chat.py
</pre>

<p>Redis:</p>

<pre>
uv run python -c 'import redis; r=redis.from_url("redis://localhost:6379/0"); print(r.ping())'
</pre>

<p>Database initialization:</p>

<pre>
uv run python -m src.db.init_db
</pre>

<h2>✅ Assignment Requirements</h2>

<table>
  <thead>
    <tr>
      <th>Requirement</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>FastAPI backend</td><td>✅</td></tr>
    <tr><td>PDF upload</td><td>✅</td></tr>
    <tr><td>TXT upload</td><td>✅</td></tr>
    <tr><td>Text extraction</td><td>✅</td></tr>
    <tr><td>Two chunking strategies</td><td>✅</td></tr>
    <tr><td>Selectable chunking</td><td>✅</td></tr>
    <tr><td>Embeddings</td><td>✅</td></tr>
    <tr><td>Weaviate vector storage</td><td>✅</td></tr>
    <tr><td>SQL metadata storage</td><td>✅</td></tr>
    <tr><td>Custom RAG</td><td>✅</td></tr>
    <tr><td>Redis chat memory</td><td>✅</td></tr>
    <tr><td>Multi-turn queries</td><td>⚠️ Partial — see Known Limitations</td></tr>
    <tr><td>Interview booking</td><td>✅</td></tr>
    <tr><td>LLM booking extraction</td><td>✅</td></tr>
    <tr><td>Booking persistence</td><td>✅</td></tr>
    <tr><td>No FAISS</td><td>✅</td></tr>
    <tr><td>No Chroma</td><td>✅</td></tr>
    <tr><td>No RetrievalQAChain</td><td>✅</td></tr>
    <tr><td>No UI</td><td>✅</td></tr>
    <tr><td>Type annotations</td><td>✅</td></tr>
    <tr><td>Modular architecture</td><td>✅</td></tr>
  </tbody>
</table>

<h2>⚠️ Known Limitations</h2>

<p>
Documented here for transparency, based on internal review, rather than
left implicit in the checklist above.
</p>

<h3>Multi-turn intent routing</h3>

<p>
Conversation history is passed into RAG answer generation, so pronoun and
reference follow-ups ("What language are they built with?") are correctly
understood once the assistant is on the RAG path. However, intent
classification (<code>detect_intent</code>) currently looks only at the
current message, not the conversation history. A context-only follow-up
with no self-contained meaning of its own (e.g. "How many did you just
say there were?") can be misclassified as a booking request and routed to
the booking flow instead of being answered. Planned fix: pass conversation
history into the intent classifier's prompt.
</p>

<h3>Retrieval on pronoun-heavy follow-ups</h3>

<p>
Vector retrieval embeds the raw follow-up query as-is, without rewriting it
using prior conversation context. A pronoun-heavy follow-up can therefore
occasionally retrieve less relevant chunks even though the LLM correctly
resolves the pronoun during generation. A query-rewrite step before
retrieval would close this gap.
</p>

<h3>Booking date anchor</h3>

<p>
The interview-booking extraction prompt anchors relative dates ("next
Thursday", "tomorrow") to a fixed date string rather than computing the
current date at request time. This needs to be made dynamic so relative
dates keep resolving correctly.
</p>

<h3>Blocking I/O in async handlers</h3>

<p>
Redis, Weaviate, and local embedding calls are synchronous and are invoked
directly from <code>async def</code> route handlers without an executor.
This is not visible under light, single-request usage but can block the
event loop under concurrent load.
</p>

<h2>🔐 Engineering Practices</h2>

<ul>
  <li>Strong Python type annotations</li>
  <li>Pydantic request and response validation</li>
  <li>SQLAlchemy typed ORM models</li>
  <li>Async PostgreSQL access</li>
  <li>FastAPI dependency injection</li>
  <li>Environment-based configuration</li>
  <li>Explicit RAG pipeline</li>
  <li>Separated retrieval and generation services</li>
  <li>Redis conversation state</li>
  <li>Structured LLM output validation</li>
  <li>Modular service architecture</li>
</ul>

<h2>🚫 Constraints Followed</h2>

<ul>
  <li>❌ No FAISS</li>
  <li>❌ No Chroma</li>
  <li>❌ No RetrievalQAChain</li>
  <li>❌ No frontend/UI</li>
</ul>

<p>
The RAG pipeline is implemented explicitly using embeddings, vector
similarity search, context construction, and LLM generation.
</p>

<h2>🔮 Future Improvements</h2>

<ul>
  <li>Interview slot availability validation</li>
  <li>Duplicate booking prevention</li>
  <li>Booking cancellation and rescheduling</li>
  <li>Authentication and authorization</li>
  <li>Automated unit and integration tests</li>
  <li>Docker / Docker Compose</li>
  <li>Structured logging</li>
  <li>Rate limiting</li>
  <li>Application monitoring and metrics</li>
</ul>

<h2>👨‍💻 Author</h2>

<p>
<strong>Sandip</strong><br>
AI/ML Intern Candidate
</p>

<p>
<a href="https://github.com/sanshre-sandip/Rag-document-asssistant">
GitHub Repository
</a>
</p>

<hr>

<p align="center">
  <strong>Built with FastAPI • PostgreSQL • Redis • Weaviate • Groq</strong>
</p>
