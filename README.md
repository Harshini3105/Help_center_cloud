# Nexus Enterprise - AI Support Center

## What This Project Is

Nexus Enterprise is a cloud-powered customer support portal built for enterprise e-commerce environments. The idea behind it was simple but ambitious: instead of customers waiting in a queue to ask a basic question like "where is my order?", an AI system should be able to understand what they are asking, figure out the intent, and respond with the right information and actionable options, instantly.

This project brings that idea to life with a full frontend dashboard connected to a live serverless backend hosted on Microsoft Azure. The AI layer processes customer queries in real time, classifies the intent, and returns confidence-scored responses that drive the UI to show meaningful action buttons, not just generic text.

---

## How It Works

When a customer types a message into the chat interface, the following happens behind the scenes:

1. The frontend sends the message to a local Python proxy server running on port 8082.
2. The proxy server forwards the request to an Azure Cloud Function endpoint (`/api/ProcessQuery`) hosted in Central India.
3. The Azure function runs the machine learning model, classifies the intent of the message, and returns a structured JSON response with the predicted category and a confidence score.
4. The proxy receives the response and relays it back to the frontend.
5. The frontend parses the intent and confidence score, then renders a human-readable reply along with context-aware action buttons specific to that intent.
6. Every message, along with its category and confidence score, is logged to a local SQLite database (`chat_history.db`) for persistence across sessions.

The right panel in the UI also surfaces a live cloud activity log so you can watch exactly what is happening at the system level as you interact with the chatbot.

---

## Key Features

**An AI Chatbot That Understands Context**
The Nexus AI Assistant does not just keyword-match. It uses a trained intent classification model to understand what the customer actually needs, even when it is phrased differently each time. Supported intents include:

- Order tracking and status updates
- Refund and return requests
- Delivery timelines and shipping queries
- Order cancellation requests

**Automated Action Buttons**
After every AI response, the UI renders one or more action buttons based on what the system believes the customer wants to do next. For example, if the intent is "order tracking", the bot might surface a "Track My Order" button. This removes friction from the support experience.

**Multilingual Support**
The chat interface includes a language selector supporting English, Spanish, French, and Hindi, making it accessible to a broader customer base.

**Voice Input**
Customers can also speak their query using the microphone button, which uses the Web Speech API to transcribe and submit the message.

**Real-Time Cloud Activity Log**
A dedicated panel on the right side of the UI logs every Azure function call, showing the raw request payload, the returned intent category, and the confidence score. This makes the system fully transparent and easy to debug or demo.

**Persistent Chat History**
All conversations are stored in a local SQLite database through the proxy server, so sessions are not lost between page refreshes.

**Order and Product Modals**
The sidebar includes quick access to a product catalog and an order history panel, giving the support experience a complete customer portal feel.

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
├── index.html          # The entire frontend application (single-page, self-contained)
├── proxy_server.py     # Local HTTP server on port 8082, proxies requests to Azure
├── add_products.py     # Utility script for populating the product catalog
├── update_script.py    # Utility script for maintaining/updating data records
└── chat_history.db     # SQLite database storing all chat session records
```

---

## Getting Started

To run this project on your local machine, you need Python 3 installed.

**Step 1 - Clone the repository**

```bash
git clone https://github.com/Harshini3105/Help_center_cloud.git
cd Help_center_cloud
```

**Step 2 - Start the proxy server**

The proxy server handles all communication between the frontend and the Azure AI backend. Start it before opening the app.

```bash
python3 proxy_server.py
```

Once running, you should see:

```
Server running on http://localhost:8082
Azure Proxy is enabled for POST /api/ProcessQuery
SQLite Chat History is enabled for GET/POST /api/messages
```

**Step 3 - Open the application**

Open `index.html` directly in your browser, or serve it from the same directory using Python's built-in HTTP server on a different port:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000` in your browser.

**Step 4 - Try the chatbot**

Type any of the following into the chat input to see the AI intent system in action:

- "Where is my package?"
- "I want to request a refund for my last order."
- "How long will it take for my delivery to arrive?"
- "Can I cancel my order?"

Watch the right-side cloud log panel update in real time as each query is processed and classified by Azure.

---

## API Endpoints (Local Proxy)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/messages` | Retrieves full chat history from SQLite |
| POST | `/api/messages` | Saves a new message to SQLite |
| POST | `/api/ProcessQuery` | Proxies an AI query to the Azure Cloud Function |

---

## Notes on the Azure Backend

The Azure function endpoint used in this project is:

```
https://helpcenterfunction3-fdangsh0f0fcc0f4.centralindia-01.azurewebsites.net/api/ProcessQuery
```

This is a serverless Python function deployed on Azure App Service in the Central India region. It accepts a JSON payload with the customer query and returns a structured response containing the predicted intent category and a floating-point confidence score. The proxy layer in `proxy_server.py` handles errors from Azure gracefully and passes them back to the frontend with the appropriate HTTP status code.

---

*Built by Harshini as part of an enterprise-scale cloud and AI support systems project.*
