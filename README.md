# Nexus Enterprise - AI Support Center

## What This Project Is

Nexus Enterprise is a cloud-powered customer support portal built for enterprise e-commerce environments. The core idea was straightforward but ambitious: instead of customers waiting in a queue to get answers to basic questions like "where is my order?", an AI system should be able to understand what they are asking, identify their intent, and respond instantly with the right information and actionable next steps.

This project brings that idea to life. It is a complete, working support system with a polished frontend dashboard wired up to a live serverless AI backend hosted on Microsoft Azure. Customers get real answers, not canned scripts, and the interface adapts to what they actually need.

---

## The Problem It Solves

Traditional customer support portals force users to scroll through FAQ pages or wait for a live agent. This project treats that as a solvable engineering problem. By running intent classification on every message through a cloud function, the system can instantly understand what a customer is trying to do and respond with a specific, helpful reply and relevant action options, without any human agent involvement for common request types.

---

## How It Works

When a customer types a message into the chat interface, the following happens behind the scenes:

1. The frontend sends the message to a local Python proxy server running on port 8082.
2. The proxy server forwards the request to an Azure Cloud Function endpoint (`/api/ProcessQuery`) hosted in Central India.
3. The Azure function runs the machine learning model, classifies the intent of the message, and returns a structured JSON response with the predicted category and a confidence score.
4. The proxy receives the response and relays it back to the frontend.
5. The frontend parses the intent and confidence score, then renders a human-readable reply along with context-aware action buttons specific to that intent.
6. Every message, along with its category and confidence score, is logged to a local SQLite database (`chat_history.db`) for persistence across sessions.

A live cloud activity log on the right side of the UI shows exactly what is happening at the system level, in real time, as each message is processed.

---

## Key Features

**An AI Chatbot That Understands Context**
The Nexus AI Assistant does not keyword-match. It uses a trained intent classification model to understand what the customer actually needs, even when the same question is phrased differently each time. Supported intents include:

- Order tracking and status updates
- Refund and return requests
- Delivery timelines and shipping queries
- Order cancellation requests

**Confidence-Driven Responses**
Every AI response is backed by a floating-point confidence score. The UI surfaces this score in the cloud log panel, making it easy to evaluate the reliability of each classification and understand where the model is highly certain versus where it might be less sure.

**Automated Action Buttons**
After every AI response, the UI renders one or more action buttons based on what the system believes the customer wants to do next. For example, if the intent is order tracking, the bot surfaces a "Track My Order" button directly inside the conversation. This removes friction from the support experience.

**Multilingual Support**
The chat interface includes a language selector supporting English, Spanish, French, and Hindi, making it accessible to a broader customer base without any additional backend changes.

**Voice Input**
Customers can speak their query using the microphone button, which uses the Web Speech API to transcribe and submit the message. Useful for mobile or accessibility scenarios.

**Real-Time Cloud Activity Log**
A dedicated panel on the right side logs every Azure function call with the raw request payload, the classified intent, and the confidence score. This makes the system fully transparent and straightforward to demo or debug during development.

**Persistent Chat History**
All conversations are stored in a local SQLite database via the proxy server so sessions are preserved across page refreshes without requiring any external database setup.

**Order and Product Panels**
The sidebar gives quick access to a product catalog and an order history panel, giving the support experience the feel of a complete, enterprise customer portal rather than just a standalone chatbot.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3 (Vanilla), JavaScript (Vanilla) |
| Fonts | Inter via Google Fonts |
| Backend Proxy | Python 3 (`proxy_server.py`) using `http.server` and `socketserver` |
| AI / Cloud | Microsoft Azure Serverless Function (Python) |
| Database | SQLite (`chat_history.db`) via Python `sqlite3` |
| Utility Scripts | `add_products.py`, `update_script.py` |

---

## Project Structure

```
Help_center_cloud/
├── index.html          # The complete frontend application (single-page, self-contained)
├── proxy_server.py     # Local HTTP server on port 8082, proxies requests to Azure
├── add_products.py     # Utility script for populating the product catalog
├── update_script.py    # Utility script for maintaining and updating data records
└── chat_history.db     # SQLite database storing all chat session records
```

---

## Getting Started

You only need Python 3 installed to run this locally. There are no additional dependencies to install.

**Step 1 - Clone the repository**

```bash
git clone https://github.com/Harshini3105/Help_center_cloud.git
cd Help_center_cloud
```

**Step 2 - Start the proxy server**

The proxy server handles all communication between the frontend and the Azure AI backend. It needs to be running before you open the app.

```bash
python3 proxy_server.py
```

Once running, you will see:

```
Server running on http://localhost:8082
Azure Proxy is enabled for POST /api/ProcessQuery
SQLite Chat History is enabled for GET/POST /api/messages
```

**Step 3 - Open the application**

Open `index.html` directly in your browser, or serve it from the same directory using Python's built-in HTTP server:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000` in your browser.

**Step 4 - Try the chatbot**

Type any of the following into the chat input to see the AI intent classification in action:

- "Where is my package?"
- "I want to request a refund for my last order."
- "How long will my delivery take to arrive?"
- "Can I cancel my order?"

Watch the right-side cloud log panel update in real time as each query is sent to Azure, classified, and returned with a confidence score.

---

## API Endpoints (Local Proxy)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/messages` | Retrieves the full chat history from SQLite |
| POST | `/api/messages` | Saves a new message entry to SQLite |
| POST | `/api/ProcessQuery` | Proxies an AI classification query to the Azure Cloud Function |

---

## Notes on the Azure Backend

The Azure Cloud Function endpoint used in this project:

```
https://helpcenterfunction3-fdangsh0f0fcc0f4.centralindia-01.azurewebsites.net/api/ProcessQuery
```

This is a serverless Python function deployed on Azure App Service in the Central India region. It accepts a JSON payload containing the customer query and returns a structured JSON response with the predicted intent category and a floating-point confidence score. The local proxy in `proxy_server.py` handles Azure HTTP errors gracefully and forwards them back to the frontend with the correct status code.

---

## Why This Architecture

Keeping the frontend as a single self-contained HTML file and routing AI calls through a local Python proxy was a deliberate design decision. It keeps the setup minimal, meaning anyone can clone this and run it with a single command, while still connecting to a real, production-grade AI backend on Azure. There is no build step, no package manager, and no environment to configure beyond having Python 3 available.

---

*Built by Harshini as part of an enterprise-scale cloud and AI support systems project.*
