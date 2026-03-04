import re

with open('index.html', 'r') as f:
    html = f.read()

new_script = """
        const chatMessages = document.getElementById('chatMessages');
        const chatInput = document.getElementById('chatInput');
        const typingIndicator = document.getElementById('typingIndicator');
        const actionSuggestions = document.getElementById('actionSuggestions');
        const cloudLogs = document.getElementById('cloudLogs');
        const langSelect = document.getElementById('langSelect');
        const micBtn = document.getElementById('micBtn');
        const ttsIcon = document.getElementById('ttsIcon');

        let isTTSOn = true;
        let isRecording = false;
        let recognition = null;

        // Initialize Speech Recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRec();
            recognition.continuous = false;
            recognition.interimResults = false;
            
            recognition.onstart = function() {
                isRecording = true;
                micBtn.classList.add('recording');
                chatInput.placeholder = "Listening...";
            };
            
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                chatInput.value = transcript;
            };
            
            recognition.onend = function() {
                isRecording = false;
                micBtn.classList.remove('recording');
                chatInput.placeholder = "Describe your issue or ask a question...";
                if (chatInput.value.trim() !== "") {
                    sendMessage();
                }
            };
            
            recognition.onerror = function(e) {
                console.error("Speech recognition error", e);
                isRecording = false;
                micBtn.classList.remove('recording');
                chatInput.placeholder = "Describe your issue or ask a question...";
            };
        }

        // Load History from SQLite DB on startup
        window.addEventListener('load', async () => {
            try {
                const res = await fetch('/api/messages');
                const messages = await res.json();
                if (messages.length > 0) {
                    addCloudLog("Database Connected", `Found ${messages.length} previous messages loaded from SQLite table!`, false);
                    
                    // Clear placeholder defaults
                    chatMessages.innerHTML = ''; 
                    chatMessages.appendChild(typingIndicator);
                    
                    messages.forEach(msg => {
                        if (msg.sender === 'user') {
                            appendUserMessageUI(msg.text, msg.timestamp);
                        } else {
                            const botReplyHTML = generateBotResponseHTML(msg.category, msg.confidenceScore, msg.text);
                            appendBotMessageUI(botReplyHTML, msg.category, msg.confidenceScore, msg.timestamp);
                        }
                    });
                }
            } catch (e) { console.error("Could not load from DB", e); }
        });

        function toggleDictation() {
            if (!recognition) {
                alert("Speech Recognition is not supported in this browser.");
                return;
            }
            if (isRecording) {
                recognition.stop();
            } else {
                recognition.lang = langSelect.value;
                recognition.start();
            }
        }

        function toggleTTS() {
            isTTSOn = !isTTSOn;
            if (isTTSOn) {
                ttsIcon.parentElement.style.color = "#10B981";
                ttsIcon.innerHTML = `<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>`;
            } else {
                ttsIcon.parentElement.style.color = "#94A3B8";
                ttsIcon.innerHTML = `<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><line x1="23" y1="9" x2="17" y2="15"></line><line x1="17" y1="9" x2="23" y2="15"></line>`;
            }
        }

        function speakText(text) {
            if (!isTTSOn || !window.speechSynthesis) return;
            // Clean HTML tags and markdown before reading
            const cleanText = text.replace(/<[^>]*>?/gm, '').replace(/\\*\\*/g, '');
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.lang = langSelect.value;
            window.speechSynthesis.speak(utterance);
        }

        // Translation utility via Google Translate unofficial API
        async function translateText(text, targetLang) {
            if (targetLang === 'en') return text;
            try {
                const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${targetLang}&dt=t&q=${encodeURI(text)}`;
                const res = await fetch(url);
                const data = await res.json();
                return data[0].map(item => item[0]).join("");
            } catch(e) {
                console.error("Translation error", e);
                return text;
            }
        }

        chatInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendMessage();
            }
        });

        function fillAndSend(text) {
            chatInput.value = text;
            sendMessage();
        }

        function addCloudLog(title, jsonStr, isError = false) {
            const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            const logClass = isError ? 'error' : '';
            const statusText = isError ? 'FAILED' : '200 OK';

            const html = `
                <div class="log-entry">
                    <div class="log-title">
                        <span>${title}</span>
                        <span class="log-status ${logClass}">${statusText}</span>
                    </div>
                    <div class="log-code">${jsonStr}</div>
                </div>
            `;
            cloudLogs.insertAdjacentHTML('afterbegin', html);
        }

        async function saveMessageToDB(sender, text, category, confidenceScore, timestamp) {
            try {
                await fetch('/api/messages', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({sender, text, category, confidenceScore, timestamp})
                });
            } catch(e) {}
        }

        async function sendMessage() {
            const originalText = chatInput.value.trim();
            if (!originalText) return;

            chatInput.value = '';
            actionSuggestions.style.display = 'none';

            const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            appendUserMessageUI(originalText, timeStr);
            saveMessageToDB('user', originalText, null, null, timeStr);

            showTyping();

            // 1. Translate user input to English (if needed)
            const sourceLang = langSelect.value;
            let englishText = originalText;
            
            if (sourceLang !== 'en') {
                englishText = await translateText(originalText, 'en');
                addCloudLog("Azure Translator API", `Translated to English:\\n"${englishText}"`);
            }

            const requestPayload = { text: englishText };
            addCloudLog("Outgoing POST Request", JSON.stringify(requestPayload, null, 2));
            const startTime = Date.now();

            try {
                // 2. Proxied Call to Azure
                const response = await fetch("/api/ProcessQuery", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(requestPayload)
                });

                if (!response.ok) throw new Error("Network Error");

                const data = await response.json();
                const latency = Date.now() - startTime;
                addCloudLog(`Azure Response (${latency}ms)`, JSON.stringify(data, null, 2));

                // 3. Generate internal english intent mapping
                const { responseText, actionsHTML } = generateBotResponseTextAndActions(data.category, data.confidenceScore);
                
                // 4. Translate bot answer back to user's native tongue
                let localizedResponse = responseText;
                if (sourceLang !== 'en') {
                    localizedResponse = await translateText(responseText, sourceLang);
                }

                const botReplyHTML = localizedResponse + actionsHTML;
                const botTimeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                hideTyping();
                appendBotMessageUI(botReplyHTML, data.category, data.confidenceScore, botTimeStr);
                
                // 5. Save output to internal SQLite DB
                saveMessageToDB('bot', localizedResponse, data.category, data.confidenceScore, botTimeStr);

                // 6. Speak translation/native via Browser TTS
                speakText(localizedResponse);

            } catch (error) {
                console.error("Error:", error);
                const latency = Date.now() - startTime;
                addCloudLog(`Azure Error (${latency}ms)`, error.message || "Connection refused", true);
                hideTyping();
                
                let errorMsg = "I am currently experiencing connection issues to the support database. Please try again later.";
                if (sourceLang !== 'en') errorMsg = await translateText(errorMsg, sourceLang);
                
                const botTimeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                appendBotMessageUI(errorMsg, "Error", 0, botTimeStr);
                speakText(errorMsg);
            }
        }

        function appendUserMessageUI(text, timeStr) {
            const html = `
                <div class="message-row user">
                    <div class="message-content">
                        <div class="message-bubble">${escapeHTML(text)}</div>
                        <div class="message-meta">${timeStr}</div>
                    </div>
                </div>
            `;
            const div = document.createElement('div');
            div.innerHTML = html;
            chatMessages.insertBefore(div.firstElementChild, typingIndicator);
            scrollToBottom();
        }

        function appendBotMessageUI(contentHTML, category, confidence, timeStr) {
            let badgeHTML = '';
            if (category && category !== 'Error' && category !== null) {
                const confPercent = confidence ? (confidence * 100).toFixed(0) + '%' : '';
                badgeHTML = `
                    <div class="intent-badge">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        Intent: ${category} ${confPercent}
                    </div>
                `;
            }

            const html = `
                <div class="message-row bot">
                    <div class="message-avatar">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
                    </div>
                    <div class="message-content">
                        <div class="message-bubble">${contentHTML}</div>
                        <div class="message-meta">
                            Nexus AI &bull; ${timeStr} 
                            ${badgeHTML}
                        </div>
                    </div>
                </div>
            `;
            const div = document.createElement('div');
            div.innerHTML = html;
            chatMessages.insertBefore(div.firstElementChild, typingIndicator);
            scrollToBottom();
        }
        
        function generateBotResponseHTML(category, confidence, historicText=null) {
            if (historicText) {
                const result = generateBotResponseTextAndActions(category, confidence);
                return historicText + result.actionsHTML;
            }
            const result = generateBotResponseTextAndActions(category, confidence);
            return result.responseText + result.actionsHTML;
        }

        function generateBotResponseTextAndActions(category, confidence) {
            const intent = (category || "").toLowerCase();
            let responseText = "";
            let actionsHTML = "";

            if (intent.includes("order") || intent.includes("track")) {
                responseText = "I see you are inquiring about an order's status. To fetch the most accurate tracking details, please provide your **9-digit Order ID (e.g., ORD-123456789)**.";
                actionsHTML = `
                    <div class="msg-actions">
                        <button class="msg-action-btn" onclick="alert('Navigating to Recent Orders...')">View Recent Orders</button>
                    </div>
                `;
            }
            else if (intent.includes("refund") || intent.includes("return")) {
                responseText = "It looks like you need help with a refund or return. Our policy allows returns within 30 days of the delivery date. Would you like me to initiate the automated return process for your last order?";
                actions of intent
                actionsHTML = `
                    <div class="msg-actions">
                        <button class="msg-action-btn" onclick="fillAndSend('Yes, start my return')">Yes, start my return</button>
                    </div>
                `;
            }
            else if (intent.includes("cancel")) {
                responseText = "I understand you wish to cancel an order. If your items haven't shipped yet, we can usually process a cancellation immediately. What is the Order ID you wish to cancel?";
            }
            else if (intent.includes("deliver") || intent.includes("shipping")) {
                responseText = "Standard delivery times range from 3-5 business days depending on your region. Expedited shipping takes 1-2 days. Did you have a specific shipment you wanted me to look up?";
            }
            else {
                responseText = `I have categorized your request under **${category || "General"}**. I can try to find relevant articles for this, or connect you with a live human agent.`;
            }

            return { responseText, actionsHTML };
        }

        function showTyping() {
            typingIndicator.style.display = 'flex';
            scrollToBottom();
        }

        function hideTyping() {
            typingIndicator.style.display = 'none';
        }

        function scrollToBottom() {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Utility to prevent XSS in chat
        function escapeHTML(str) {
            return str.replace(/[&<>'"]/g,
                tag => ({
                    '&': '&amp;',
                    '<': '&lt;',
                    '>': '&gt;',
                    "'": '&#39;',
                    '"': '&quot;'
                }[tag])
            );
        }
"""

html = re.sub(r'<script>.*?</script>', '<script>\n' + new_script + '\n    </script>', html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
