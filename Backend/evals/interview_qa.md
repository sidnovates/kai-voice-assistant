# 🎯 KAI Voice Assistant - Evaluation & Technical Interview Guide

A concise reference to confidently explain and defend the NLU benchmark, metrics, and architecture during technical interviews.

---

### Q1: Why did you report Macro F1 and Slot Error Rate (SER) instead of just raw accuracy?
- **Answer:**
  - **Class Imbalance Defense:** Raw accuracy can mask systematic underperformance in smaller or harder categories. **Macro F1** treats all 5 functional domains equally ($F_1 = \frac{2 \cdot P \cdot R}{P + R}$ averaged unweighted across classes), proving the model didn't sacrifice edge domains to inflate overall scores.
  - **Task-Oriented Dialog Standard:** Accuracy only measures *intent classification* (e.g., Category 3: Spotify). However, voice assistants fail if they misextract entities (e.g., missing the song title or artist). **Slot Error Rate (SER)** measures entity-level mistakes:
    $$\text{SER} = \frac{\text{Substitutions} + \text{Deletions} + \text{Insertions}}{\text{Total Reference Slots}}$$
  - Demonstrating a **98.7% Macro F1** alongside a low **1.85% SER** confirms both routing correctness and payload precision.

---

### Q2: How did you construct the 155-query evaluation dataset, and how do you guard against data contamination?
- **Answer:**
  - **Dataset Composition:** 155 curated test cases partitioned across 5 real-world domains (WhatsApp messaging/calls, Web navigation, Spotify playback, OS automation, and open-domain chat).
  - **Real-World Edge Cases:** Includes phonetically tricky titles, multi-word entities, colloquialisms (*"put on some Punjabi music"*, *"yo Kai what's up"*), and code-mixed inputs (*"play ghungroo song"*).
  - **Contamination Prevention:** Because Gemini is evaluated in a zero-shot/few-shot in-context framework rather than fine-tuned on this data, contamination is prevented by strictly excluding test queries from system prompt demonstrations.

---

### Q3: Your P50 latency is ~3.9s, but P90 reached ~20s. What caused this tail latency, and how would you optimize it for production?
- **Answer:**
  - **Root Cause:** The benchmark ran over the public internet against Google's API under strict free-tier rate limits. P90 spikes were driven by network jitter and programmatic exponential backoff when handling rate-limit quotas (HTTP 429).
  - **Production Optimization Roadmap:**
    1. **Single-Pass Structured Extraction:** Combine intent routing and slot filling into a single JSON schema call (`llm.with_structured_output`), cutting LLM round-trips in half (~1.5s saved).
    2. **Local Edge Fast-Path:** Deploy a lightweight local classifier (e.g., a fine-tuned ONNX/SetFit model or regex trie) for deterministic OS commands (volume, scrolling, screenshots) to resolve them in **<5ms at 0 API cost**.
    3. **Token Streaming & Speculative Execution:** Stream output tokens from Gemini and pre-warm execution handlers (e.g., pre-resolving Spotify API tokens while generating).

---

### Q4: What caused the 1.3% failure cases in the benchmark?
- **Answer:**
  - **Semantic Boundary Ambiguity:** The failed queries involved ambiguous verbs without explicit service keywords (e.g., queries like *"put on music"* or searching for video clips without specifying "browser" vs "spotify").
  - **Resolution:** Tightened system prompt instructions to prioritize music playback over browser navigation when audio/song intent is inferred, eliminating the classification conflict.

---

### Q5: How does the system prevent acoustic feedback / self-triggering while audio or music is playing?
- **Answer:**
  - **Acoustic Session Tracking:** Integrated Windows Core Audio APIs via `pycaw` to check background audio sessions before processing microphone input.
  - **Stateful Audio Management:** The system automatically pauses background Spotify playback upon wake-word detection, records the query in a quiet acoustic environment, and restores previous playback status upon turn completion.

---

### Q6: Why did you choose a hybrid edge-cloud architecture (Porcupine + Faster-Whisper + Gemini) over an end-to-end cloud voice API?
- **Answer:**
  - **Privacy & Bandwidth:** Continuous microphone listening is handled 100% offline. Porcupine triggers wake-word detection on CPU in **<15ms** without streaming user audio to external servers.
  - **Efficient STT:** Local `faster-whisper` (CTranslate2 INT8 quantization) converts voice to text on-device in **~300ms**.
  - **Cost & Intelligence Separation:** Cloud API calls are only dispatched for high-level reasoning on transcribed text, drastically cutting token overhead, bandwidth, and API bills compared to continuous cloud audio streams.

