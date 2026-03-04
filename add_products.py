import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the Dashboard link
html = html.replace(
    '<a href="#" class="menu-item">\n                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"\n                    stroke-linejoin="round">\n                    <rect x="3" y="3" width="7" height="7"></rect>',
    '<a href="#" class="menu-item" onclick="openProductsModal()">\n                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"\n                    stroke-linejoin="round">\n                    <rect x="3" y="3" width="7" height="7"></rect>'
)

html = html.replace(
    'Dashboard\n            </a>',
    'Shop Products\n            </a>', 1
)

# 2. Update the My Orders link
html = html.replace(
    '<a href="#" class="menu-item">\n                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"\n                    stroke-linejoin="round">\n                    <circle cx="9" cy="21" r="1"></circle>',
    '<a href="#" class="menu-item" onclick="openModal()">\n                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"\n                    stroke-linejoin="round">\n                    <circle cx="9" cy="21" r="1"></circle>'
)

# 3. Add ordersList wrapper
html = html.replace(
    '<button class="close-btn" onclick="closeModal()">×</button>\n                </div>\n\n                <!-- Ongoing Order -->',
    '<button class="close-btn" onclick="closeModal()">×</button>\n                </div>\n\n                <div id="ordersList">\n                <!-- Ongoing Order -->'
)

html = html.replace(
    '<span class="status-badge status-past">Delivered</span>\n                    </div>\n                </div>\n            </div>\n        </div>\n    </main>',
    '<span class="status-badge status-past">Delivered</span>\n                    </div>\n                </div>\n                </div>\n            </div>\n        </div>\n    </main>'
)

# 4. Inject Products Modal
products_modal = """
        <!-- Products Modal Prototype -->
        <div class="modal-overlay" id="productsModal">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="modal-title">Shop Products</div>
                    <button class="close-btn" onclick="closeProductsModal()">×</button>
                </div>
                
                <div class="order-card">
                    <div class="order-info">
                        <h3>iPhone 15 Pro Max - Titanium</h3>
                        <p>$1,199.00</p>
                    </div>
                    <div style="text-align:right;">
                        <button class="btn-select" onclick="buyProduct('iPhone 15 Pro Max', '$1,199.00')">Buy Now</button>
                    </div>
                </div>

                <div class="order-card">
                    <div class="order-info">
                        <h3>Sony WH-1000XM5 Headphones</h3>
                        <p>$348.00</p>
                    </div>
                    <div style="text-align:right;">
                        <button class="btn-select" onclick="buyProduct('Sony WH-1000XM5 Headphones', '$348.00')">Buy Now</button>
                    </div>
                </div>

                <div class="order-card">
                    <div class="order-info">
                        <h3>Samsung Neo QLED 4K TV (65")</h3>
                        <p>$1,899.00</p>
                    </div>
                    <div style="text-align:right;">
                        <button class="btn-select" onclick="buyProduct('Samsung Neo QLED 8K TV', '$1,899.00')">Buy Now</button>
                    </div>
                </div>
            </div>
        </div>
    </main>"""

html = html.replace('</main>', products_modal)

# 5. Inject JS functions
js_functions = """
        const productsModal = document.getElementById('productsModal');
        function openProductsModal() {
            productsModal.classList.add('active');
        }
        function closeProductsModal() {
            productsModal.classList.remove('active');
        }

        function buyProduct(itemName, itemPrice) {
            closeProductsModal();
            const orderId = 'ORD-' + Math.floor(100000 + Math.random() * 900000); // Generate Random Order ID
            const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            // User intention mock
            const userIntent = `I just placed an order for ${itemName}.`;
            appendUserMessageUI(userIntent, timeStr);
            saveMessageToDB('user', userIntent, null, null, timeStr);

            showTyping();
            setTimeout(() => {
                hideTyping();
                
                // Add order to modal instantly
                const orderHTML = `
                <div class="order-card">
                    <div class="order-info">
                        <h3>${itemName}</h3>
                        <p>Order ID: ${orderId} • Placed: Just Now</p>
                    </div>
                    <div style="text-align:right;">
                        <span id="badge-${orderId}" class="status-badge status-ongoing" style="display:block; margin-bottom:8px;">Processing</span>
                        <button class="btn-select" onclick="selectOrder('${orderId}', 'track')">Track</button>
                        <button id="btn-cancel-${orderId}" class="btn-select" onclick="selectOrder('${orderId}', 'cancel')"
                            style="background:#EF4444; margin-left:4px;">Cancel</button>
                    </div>
                </div>`;
                
                const ordersList = document.getElementById('ordersList');
                if (ordersList) {
                    ordersList.insertAdjacentHTML('afterbegin', orderHTML);
                }

                // Bot Success Response
                const reply = `Thank you for your purchase! Your order for **${itemName}** (${itemPrice}) has been successfully placed. Your Order ID is **${orderId}**.`;
                const botTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                
                appendBotMessageUI(reply, "Purchase_Success", 0.99, botTime);
                saveMessageToDB('bot', reply, "Purchase_Success", 0.99, botTime);
                speakText(`Thank you for your purchase. Your order for ${itemName} has been confirmed.`);
            }, 1200);
        }

        function showTyping() {"""

html = html.replace('function showTyping() {', js_functions)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
