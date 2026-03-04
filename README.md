# Nexus Enterprise - AI Support Center ☁️ 🤖

Welcome to the **Nexus AI Support Center**, a dynamic, full-fledged cloud-based support portal designed for enterprise e-commerce customers. This project provides a robust frontend UI linked to a powerful backend system (Azure Cloud Functions) that uses AI to analyze intent and automate responses for common customer inquiries.

---

## 🌟 Key Features

* **Professional Enterprise UI/UX:** A stunning, modern dashboard layout that feels like a premium support environment using a tailored Navy Blue (`#0A192F`) and Maroon (`#800000`) color palette.
* **Integrated Live AI Chatbot:** A fully interactive chatbot interface (`Nexus AI Assistant`) that analyzes real-time customer queries using Azure cloud functions.
* **Dynamic Intent Resolution:** The AI system instantly recognizes user intents, such as:
  * 📦 Tracking & Order Management
  * 💸 Refunds & Returns Processing
  * 🚚 Delivery & Shipping Timelines
  * ❌ Order Cancellations  
* **Automated Action Items:** Based on the predicted intent and confidence scores, the bot instantly offers context-aware UI action buttons (e.g., "Start my return", "Track Order").

## 🛠️ Technology Stack

* **Frontend:** HTML5, CSS3 (Vanilla), JavaScript (Vanilla)
* **Backend:** Python scripts (`proxy_server.py`, `add_products.py`, `update_script.py`)
* **Cloud & AI Integration:** Serverless functions deployed on **Microsoft Azure** (`https://helpcenterfunction3-*.azurewebsites.net`) to process and return machine-learning confidence scores.
* **Database:** Local SQLite configuration (`chat_history.db`)

## 🚀 Getting Started

To run this application locally on your machine:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Harshini3105/Help_center_cloud.git
   cd Help_center_cloud
   ```

2. **Serve the Application**
   You can run a local HTTP server to host the `index.html` file using Python:
   ```bash
   python3 -m http.server 8000
   ```

3. **Explore the AI Features**
   Navigate to `localhost:8000` in your web browser. Type a sample phrase into the chat input like: 
   * *"Where is my package?"*
   * *"I want to request a refund."*

---
*Created by Harshini for Enterprise Support Scale Projects.*
