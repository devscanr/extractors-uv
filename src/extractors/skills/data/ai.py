from ..tag import Company, Skill, Tech, Topic
from ..utils import dis_incontext, dis_namelike, dis_nounlike
from ...xpatterns import ver1

SKILLS: list[Skill] = [
    # AI CORE & LLM ORCHESTRATION >
    Topic("LLM", ["llm(s)", "large=language=model(s)", "generative=ai", "gen=ai", "foundation=model(s)", "llm=integration"]),
    Topic("Prompting", ["prompting", "prompt=engineering", "prompt=design", "chain=of=thought", "prompt=optimization", "system=prompt(s)"]),
    Topic("Agents", ["agent(s)", "autonomous=agent(s)", "multi-agent=system(s)", "agentic=workflow(s)", "agent=orchestration", "agentic=ai"]),
    Topic("MCP", ["model=tools", "llm=tools", "api=calling=llm", "mcp=server", "mcp"]),
    Topic("Multimodal", [
        "multimodal",
        "image=2=text", "speech=2=text", "audio=2=text", "video=2=text",
        "image=to=text", "speech=to=text", "audio=to=text", "video=to=text",
        "text=2=image", "text=2=speech", "text=2=audio", "text=2=video",
        "text=to=image", "text=to=speech", "text=to=audio", "text=to=video",
        "vlm",
    ]),

    # DATA & RETRIEVAL (RAG) >
    Topic("RAG", ["rag", "retrieval=augmented=generation", "context=injection", "knowledge=retrieval", "graph-rag"]),
    Topic("Vector-Search", ["vector=search", "semantic=search", "similarity=search", "hybrid=search", "vector=indexing"]),
    Topic("Embeddings", ["embedding(s)", "vectorization", "vector(s)", "text=embeddings", "image=embeddings", "vector=representation"]),
    Topic("Chunking", ["chunking", "data=chunking", "semantic=chunking", "text=splitting", "context=window=management"]),

    # VOICE & AUDIO >
    Topic("Speech-to-Text", ["stt", "speech=to=text", "asr", "automatic=speech=recognition", "transcription", "audio=to=text"]),
    Topic("Text-to-Speech", ["tts", "text=to=speech", "speech=synthesis", "voice=cloning", "voice=synthesis"]),
    Topic("Audio-Intelligence", ["voice=activity=detection", "vad", "speaker=diarization", "audio=analysis"]),

    # AI-ASSISTED DEVELOPMENT (AI4SE) >
    Topic("AI-Coding-Assistants", ["coding=assistant(s)", "ai-powered=ide", "automated=refactoring", "ai=pair=programming", "copilot=integration"]),
    Topic("AI-Code-Review", ["ai=code=review", "automated=pr=summarization", "vulnerability=detection=ai", "static=analysis=llm"]),
    Topic("AI-Test-Generation", ["automated=test=generation", "ai=unit=testing", "synthetic=test=data", "automated=qa=agents"]),
    Topic("AI-Documentation", ["automated=documentation", "code=explanation=models", "docstring=generation", "readme=automation"]),

    # AI OPERATIONS & RELIABILITY >
    Topic("AI-Observability", ["ai=observability", "llm=observability", "tracing", "llm=monitoring", "model=tracing", "langsmith", "langfuse"]),
    Topic("AI-Evaluation", ["ai=evaluation", "llm=evaluation", "llm=benchmarking", "ai=benchmarking", "model=evaluation", "model=benchmarking", "hallucination=detection"]),
    Topic("AI-Validation", ["ai=validation", "llm-validation", "output=validation", "structured=output(s)", "schema=enforcement", "json=mode"]),
    Topic("Cost-Optimization", ["token=budgeting", "cost-aware=routing", "llm=financial=ops", "finops=for=ai", "token=usage=analytics"]),
    Topic("Semantic-Caching", ["semantic=caching", "llm=caching", "prompt=caching", "response=caching"]),

    # FRONTEND & AI-UX >
    Topic("AI-Streaming", ["ai=streaming", "llm=streaming", "real=time=generation"]),
    Topic("Generative-UI", ["generative=ui", "gen-ui", "dynamic=ui", "adaptive=interface", "ai-native=ux"]),
    Topic("Human-In-The-Loop", ["hitl", "human=oversight", "supervised=automation", "human=checkpoint(s)", "approval=workflows"]),

    # INFRASTRUCTURE & ADVANCED >
    Topic("Fine-Tuning", ["fine=tuning", "model=tuning", "llm=tuning", "lora", "peft", "transfer=learning"]),
    Topic("Model-Serving", ["model=serving", "inference=optimization", "self-hosted=llm", "quantization", "vllm"]),
    Topic("AI-Security", ["ai=security", "prompt=injection"]),
    Topic("Edge-AI", ["edge=ai", "on-device=inference", "webgpu", "local=llm"]),

    # ==========================================
    # TOP 100 AI TECH FOR FULLSTACK ENGINEERS
    # ==========================================

    # 1. FOUNDATION MODELS & PROVIDERS (1-10)
    Tech("Claude", [ver1("claude")], "High-reasoning AI models"),
    Tech("Chat-GPT", ["chat=gpt", ver1("gpt")]),
    Tech("Mistral", ["mistral", "mixtral", "codestral"], "Performance-optimized open models"),
    Tech("DeepSeek", ["deepseek"], "Efficiency-focused reasoning models"),
    Tech("Cohere", ["cohere"], "Enterprise-focused LLM & Rerank"),
    Tech("Perplexity", ["perplexity"], "Real-time search-enabled LLM"),

    # 2. ORCHESTRATION & AGENT FRAMEWORKS (11-20)
    Tech("LangChain", ["langchain"], "Universal LLM orchestration"),
    Tech("LangGraph", ["langgraph"], "Cyclic multi-agent workflows"),
    Tech("CrewAI", ["crewai"], "Role-based autonomous agents"),
    Tech("AutoGPT", ["autogpt"], "Autonomous agent loops"),
    Tech("Pydantic-AI", ["pydantic=ai"], "Type-safe Python AI agents"),
    Tech("LlamaIndex", ["llama=index"], "Data-centric RAG orchestration"),
    Tech("Semantic-Kernel", ["semantic=kernel"], "Microsoft's agent orchestration"),
    Tech("Haystack", ["haystack"], "NLP pipeline framework"),
    Tech("Flowise", ["flowise"], "No-code LLM flow builder"),
    Tech("n8n", ["n8n"], "Workflow automation with AI nodes"),

    # 3. VECTOR DATABASES & RETRIEVAL (21-30)
    Tech("Pinecone", ["pinecone"], "Managed serverless vector DB"),
    Tech("Pgvector", ["pg=vector"], "Vector search for PostgreSQL"),
    Tech("Weaviate", ["weaviate"], "Object-vector database"),
    Tech("Milvus", ["milvus", "zilliz"], "Large-scale vector data store"),
    Tech("Qdrant", ["qdrant"], "Rust-based vector search engine"),
    Tech("ChromaDB", ["chroma=db", "chroma"], "Embedded open-source vector store"),
    Tech("Elasticsearch", ["elasticsearch", "elk"], "Hybrid keyword/vector search"),
    Tech("Redis-VL", ["redis=vl", "redis=vector"], "In-memory vector caching"),
    Tech("MongoDB-Vector", ["mongodb=vector", "mongodb=atlas", "mongo=vector", "mongo=atlas"], "Vector search for NoSQL"),
    Tech("Faiss", ["faiss"], "Meta's efficient similarity search"),

    # 4. AI-ASSISTED DEVELOPMENT TOOLS (31-40)
    # Tech("Cursor", ["cursor=ide", "cursor"], "AI-first fork of VS Code"),
    Tech("GitHub-Copilot", ["github=copilot", "copilot"], "Standard AI pair programmer"),
    Tech("Windsurf", ["windsurf"], "Agentic IDE for multi-file tasks"),
    Tech("Tabnine", ["tabnine"], "Privacy-focused code completion"),
    Tech("Claude-Code", ["claude=code"], "Terminal-based coding agent"),
    Tech("Replit-Agent", ["replit=agent"], "End-to-end app generation"),
    Tech("Qodo", ["qodo", "codium=ai"], "AI-powered testing & review"),
    Tech("Sourcegraph-Cody", ["cody", "sourcegraph"], "Codebase-aware AI assistant"),
    Tech("Devin", ["devin"], "Autonomous AI software engineer"),
    Tech("Supermaven", ["supermaven"], "Ultra-low latency code completion"),

    # 5. VOICE, AUDIO & VISION (41-50)
    Tech("Whisper", ["whisper", "openai-whisper"], "Speech-to-text transcription"),
    Tech("ElevenLabs", ["elevenlabs"], "Professional voice synthesis"),
    Tech("Deepgram", ["deepgram"], "Real-time streaming transcription"),
    Tech("Vapi", ["vapi"], "Voice AI agent platform"),
    Tech("AssemblyAI", ["assemblyai"], "Speech-to-text with audio intelligence"),
    Tech("PlayHT", ["playht"], "Real-time conversational voice"),
    Tech("DALL-E", ["dall=e"], "Image generation API"),
    Tech("Stable-Diffusion", ["stable=diffusion"], "Open-source image gen"),
    Tech("Runway", ["runway"], "AI video generation"),
    Tech("Tesseract", ["tesseract"], "Open-source OCR engine"),

    # 6. BACKEND & SERVING (51-60)
    Tech("Ollama", ["ollama"], "Local LLM runner"),
    Tech("vLLM", ["vllm"], "High-throughput serving engine"),
    Tech("FastChat", ["fastchat"], "Open platform for training/serving"),
    Tech("BentoML", ["bentoml"], "Model deployment framework"),
    Tech("Ray-Serve", ["ray=serve"], "Scalable model serving"),
    # Tech("TRT-LLM", ["tensorrt-llm"], "NVIDIA optimized inference"),
    Tech("Triton-Inference-Server", ["triton"], "Multi-framework model server"),
    Tech("Modal", ["modal.com"], "Serverless GPU computing"),
    Tech("RunPod", ["runpod"], "On-demand GPU cloud"),

    # 7. FRONTEND & UI (61-70)
    Tech("Shadcn-UI", ["shadcn=ui", "shadcn"], "Modern accessible UI components"),
    Tech("Framer-Motion", ["framer-motion"], "Animations for streaming UI"),
    Tech("Streamlit", ["streamlit"], "Rapid AI dashboarding"),
    Tech("Gradio", ["gradio"], "Machine learning web interfaces"),
    Tech("Lucide-React", ["lucide"], "Icon set for AI interfaces"),
    Tech("TanStack-Query", ["tanstack=query", "react=query"], "Managing async AI data"),
    Tech("TanStack-Start", ["react=query"], "Managing async AI data"),

    # 8. OBSERVABILITY & LLMOPS (71-80)
    Tech("LangSmith", ["langsmith"], "Testing and tracing for LLMs"),
    Tech("Langfuse", ["langfuse"], "Open-source AI observability"),
    Tech("Weights-and-Biases", ["wandb"], "Experiment tracking & MLOps"),
    Tech("Arize-Phoenix", ["phoenix", "arize"], "RAG & LLM evaluation"),
    Tech("Promptfoo", ["promptfoo"], "CLI for prompt testing"),
    Tech("PromptLayer", ["promptlayer"], "CMS for prompt management"),
    Tech("Helicone", ["helicone"], "LLM cost & usage analytics"),
    Tech("EvidentlyAI", ["evidently"], "Model monitoring and drift"),
    Tech("MLflow", ["mlflow"], "End-to-end ML lifecycle"),
    Tech("Kubeflow", ["kubeflow"], "Cloud-native ML workflows"),

    # 9. DATA ENGINEERING & PIPELINES (81-90)
    Tech("Unstructured", ["unstructured.io"], "Parsing messy data for RAG"),
    Tech("Airbyte", ["airbyte"], "Data integration for AI context"),
    Tech("Dovetail", ["dovetail"], "Qualitative data analysis AI"),
    Tech("Firecrawl", ["firecrawl"], "Web scraping for LLM context"),
    Tech("Crawl4AI", ["crawl4ai"], "Async web crawling for agents"),

    # 10. INFRA & SECURITY (91-100)
    Tech("NeMo-Guardrails", ["nemo-guardrails"], "Safety & security for LLMs"),
    Tech("Snyk", ["snyk"], "Scanning AI code for vulnerabilities"),
]
