// Configuration
const API_BASE_URL = window.location.origin;

// State
let currentUrl = '';
let isScraped = false;

// DOM Elements
const urlInput = document.getElementById('urlInput');
const scrapeBtn = document.getElementById('scrapeBtn');
const scrapeStatus = document.getElementById('scrapeStatus');
const scrapeResult = document.getElementById('scrapeResult');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkBackendHealth();
});

function setupEventListeners() {
    // Scrape button
    scrapeBtn.addEventListener('click', handleScrape);

    // Enter key for URL input
    urlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleScrape();
        }
    });

    // Send button
    sendBtn.addEventListener('click', handleSendMessage);

    // Enter key for chat input
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    });
}

// Check backend health
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            updateStatus('Backend connected successfully', 'success');
            setTimeout(() => {
                scrapeStatus.style.display = 'none';
            }, 3000);
        }
    } catch (error) {
        updateStatus('⚠️ Backend not connected. Please start the Flask server.', 'error');
    }
}

// Handle scraping
async function handleScrape() {
    const url = urlInput.value.trim();

    if (!url) {
        updateStatus('Please enter a URL', 'error');
        return;
    }

    // Validate URL format
    if (!isValidUrl(url)) {
        updateStatus('Please enter a valid URL (e.g., https://example.com)', 'error');
        return;
    }

    // Update UI
    scrapeBtn.classList.add('loading');
    scrapeBtn.querySelector('.btn-text').textContent = 'Scraping...';
    updateStatus('Scraping website...', 'loading');
    scrapeResult.classList.remove('show');

    try {
        const response = await fetch(`${API_BASE_URL}/scrape`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (data.success) {
            currentUrl = url;
            isScraped = true;
            updateStatus('✓ Website scraped successfully!', 'success');
            displayScrapeResult(data);

            // Clear welcome message and add bot greeting
            chatMessages.innerHTML = '';
            addBotMessage(`I've successfully scraped "${data.title}". Ask me anything about this website!`);
        } else {
            updateStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        updateStatus(`Failed to connect to backend: ${error.message}`, 'error');
    } finally {
        scrapeBtn.classList.remove('loading');
        scrapeBtn.querySelector('.btn-text').textContent = 'Scrape';
    }
}

// Handle sending chat message
async function handleSendMessage() {
    const message = chatInput.value.trim();

    if (!message) return;

    // Add user message to chat
    addUserMessage(message);
    chatInput.value = '';

    // Disable send button while processing
    sendBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message,
                url: currentUrl
            })
        });

        const data = await response.json();

        if (data.success) {
            addBotMessage(data.response);
        } else {
            addBotMessage('Sorry, I encountered an error processing your message.');
        }
    } catch (error) {
        addBotMessage('Failed to connect to the backend. Please make sure the server is running.');
    } finally {
        sendBtn.disabled = false;
    }
}

// Display scrape result
function displayScrapeResult(data) {
    const contentPreview = data.content.substring(0, 300) + (data.content.length > 300 ? '...' : '');

    scrapeResult.innerHTML = `
        <div class="result-item">
            <div class="result-label">Title</div>
            <div class="result-value">${escapeHtml(data.title)}</div>
        </div>
        <div class="result-item">
            <div class="result-label">URL</div>
            <div class="result-value">${escapeHtml(data.url)}</div>
        </div>
        <div class="result-item">
            <div class="result-label">Content Preview</div>
            <div class="result-value truncate">${escapeHtml(contentPreview)}</div>
        </div>
        <div class="result-item">
            <div class="result-label">Content Length</div>
            <div class="result-value">${data.content_length.toLocaleString()} characters</div>
        </div>
        <div class="result-item">
            <div class="result-label">Links Found</div>
            <div class="result-value">${data.links.length} links</div>
        </div>
    `;

    scrapeResult.classList.add('show');
}

// Add user message to chat
function addUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    messageDiv.innerHTML = `
        <div class="message-avatar">👤</div>
        <div class="message-content">${escapeHtml(text)}</div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add bot message to chat
function addBotMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">${escapeHtml(text)}</div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Update status message
function updateStatus(message, type) {
    scrapeStatus.textContent = message;
    scrapeStatus.className = `scrape-status ${type}`;
}

// Scroll chat to bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Validate URL
function isValidUrl(string) {
    try {
        const url = new URL(string);
        return url.protocol === 'http:' || url.protocol === 'https:';
    } catch (_) {
        return false;
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Format text with line breaks
function formatText(text) {
    return escapeHtml(text).replace(/\n/g, '<br>');
}
