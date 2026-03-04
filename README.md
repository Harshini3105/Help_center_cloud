# Help Center Cloud Project ☁️ 🤖

Hey there! Welcome to my cloud project. I built this AI Support Center as a modern help center portal for an e-commerce/product-based company. The idea is to connect a clean, professional frontend UI with an Azure Cloud Function backend that processes what the customer is asking and guesses their intent.

---

## 🌟 What it does

* **Clean UI:** I put together a dashboard that looks like a real support portal. I went with a darker Navy Blue (`#0A192F`) and Maroon (`#800000`) theme because it feels a lot more professional than bright, flashy colors.
* **Working Chatbot:** There's a built-in chat (`Nexus AI Assistant`) that talks to an Azure function I set up.
* **Intent Detection:** The AI figures out what the user wants to do, covering stuff like:
  * 📦 Checking where their order is
  * 💸 Asking for a refund or return
  * 🚚 Delivery questions
  * ❌ Canceling an order
* **Smart Buttons:** When the bot figures out the intent, it actually spawns clickable action buttons (like checking real orders or starting a return).

## 🛠️ How it's built

* **Frontend:** Just plain HTML, CSS, and JS in a single file so it's super fast.
* **Backend Scripts:** A few Python scripts I wrote for the database side (`proxy_server.py`, `add_products.py`, `update_script.py`).
* **Cloud Service:** An Azure Serverless Function handles the intent confidence scoring. 
* **Database:** SQLite (`chat_history.db`) to keep track of stuff locally.

## 🚀 Running it locally

If you want to test it out yourself on your own machine:

1. **Clone it**
   ```bash
   git clone https://github.com/Harshini3105/Help_center_cloud.git
   cd Help_center_cloud
   ```

2. **Start a server**
   Since it's just HTML/JS, running a simple python server works perfectly:
   ```bash
   python3 -m http.server 8000
   ```

3. **Try the chat**
   Open `localhost:8000` in your browser. Type something like:
   * *"Where is my package?"*
   * *"I need a refund."*
   
---
*Built by Harshini*
