# 📊 KAI Voice Assistant - Benchmark Evaluation Report

**Date:** 2026-11-11 23:19:02  
**Evaluation Mode:** LIVE (Google Gemini 3.1 Flash-Lite)  
**Test Suite Size:** 155 curated queries across 5 functional domains  

## 1. Executive Summary & Resume Metrics

- **Overall Intent Accuracy:** `98.71%`
- **Macro F1-Score:** `98.71%`
- **Slot Error Rate (SER):** `1.85%`
- **Inference Latency (P50 / Median):** `3912.2 ms`
- **Inference Latency (P90):** `20167.5 ms`

## 2. Intent Classification Breakdown

| Functional Domain | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| **WhatsApp (Msg/Call)** | 100.0% | 96.7% | **98.3%** | 30 |
| **Web Navigation** | 100.0% | 96.7% | **98.3%** | 30 |
| **Spotify Music** | 97.2% | 100.0% | **98.6%** | 35 |
| **System OS Controls** | 100.0% | 100.0% | **100.0%** | 30 |
| **Conversational Chat** | 96.8% | 100.0% | **98.4%** | 30 |
| **Macro Average** | - | - | **98.7%** | 155 |

## 3. Resume Bullet Points (Copy & Paste)

> * "Engineered an offline-first hybrid voice assistant leveraging Google Gemini 3.1 Flash-Lite and Faster-Whisper, achieving **98.7% intent classification accuracy** and **98.7% macro F1-score** across 5 functional domains with a **1.9% slot error rate**."

> * "Benchmarked and optimized end-to-end NLU inference latency to **3912ms (P50)** and **20167ms (P90)** using structured JSON schemas and robust regex boundary matching."

> * "Implemented dynamic background acoustic suppression via Windows Core Audio session monitoring, preventing false trigger cascades during multi-turn audio playback."
