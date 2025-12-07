from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Store scraped content in memory (in production, use a database)
scraped_data = {}

def clean_text(text):
    """Clean and normalize text content"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()

def scrape_website(url):
    """Scrape content from a given URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Extract title
        title = soup.find('title')
        title_text = title.get_text() if title else "No title found"
        
        # Extract main content
        content_tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'article', 'section'])
        
        content_parts = []
        for tag in content_tags:
            text = tag.get_text()
            cleaned = clean_text(text)
            if cleaned and len(cleaned) > 20:  # Only include substantial content
                content_parts.append(cleaned)
        
        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            link_text = clean_text(link.get_text())
            if link_text:
                links.append({'text': link_text, 'url': full_url})
        
        return {
            'success': True,
            'url': url,
            'title': clean_text(title_text),
            'content': ' '.join(content_parts[:100]),  # Limit content
            'links': links[:20],  # Limit links
            'content_length': len(' '.join(content_parts))
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'Failed to scrape URL: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error processing content: {str(e)}'
        }

def find_relevant_content(query, content):
    """Find relevant content based on user query"""
    query_lower = query.lower()
    words = query_lower.split()
    
    # Split content into sentences
    sentences = re.split(r'[.!?]+', content)
    
    # Score sentences based on query word matches
    scored_sentences = []
    for sentence in sentences:
        sentence_lower = sentence.lower()
        score = sum(1 for word in words if word in sentence_lower)
        if score > 0:
            scored_sentences.append((score, sentence.strip()))
    
    # Sort by score and return top sentences
    scored_sentences.sort(reverse=True, key=lambda x: x[0])
    relevant = [s[1] for s in scored_sentences[:3]]
    
    return ' '.join(relevant) if relevant else content[:500]

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Web Scraping Chatbot API is running'})

@app.route('/scrape', methods=['POST'])
def scrape():
    """Scrape content from a URL"""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'success': False, 'error': 'URL is required'}), 400
    
    url = data['url']
    
    # Validate URL
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return jsonify({'success': False, 'error': 'Invalid URL format'}), 400
    except:
        return jsonify({'success': False, 'error': 'Invalid URL'}), 400
    
    # Scrape the website
    result = scrape_website(url)
    
    if result['success']:
        # Store scraped data
        scraped_data[url] = result
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and respond based on scraped content"""
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'success': False, 'error': 'Message is required'}), 400
    
    message = data['message']
    url = data.get('url', '')
    
    # Check if we have scraped data for this URL
    if url and url in scraped_data:
        scraped_info = scraped_data[url]
        
        # Find relevant content
        relevant_content = find_relevant_content(message, scraped_info['content'])
        
        # Generate response
        response = f"Based on the content from {scraped_info['title']}, here's what I found:\n\n{relevant_content}"
        
        # Add specific responses for common queries
        if any(word in message.lower() for word in ['title', 'name', 'called']):
            response = f"The page is titled: {scraped_info['title']}"
        elif any(word in message.lower() for word in ['link', 'url', 'website']):
            if scraped_info['links']:
                links_text = '\n'.join([f"- {link['text']}: {link['url']}" for link in scraped_info['links'][:5]])
                response = f"Here are some links from the page:\n{links_text}"
        elif any(word in message.lower() for word in ['summary', 'about', 'what']):
            response = f"Summary of {scraped_info['title']}:\n\n{scraped_info['content'][:300]}..."
        
        return jsonify({
            'success': True,
            'response': response,
            'source': url
        }), 200
    else:
        # No scraped data available
        return jsonify({
            'success': True,
            'response': "Please scrape a website first by entering a URL above. Once I have the content, I can answer your questions about it!",
            'source': None
        }), 200

@app.route('/clear', methods=['POST'])
def clear():
    """Clear scraped data"""
    data = request.get_json()
    url = data.get('url', '')
    
    if url and url in scraped_data:
        del scraped_data[url]
        return jsonify({'success': True, 'message': 'Data cleared'}), 200
    elif not url:
        scraped_data.clear()
        return jsonify({'success': True, 'message': 'All data cleared'}), 200
    else:
        return jsonify({'success': False, 'error': 'No data found for this URL'}), 404

# Serve frontend files
@app.route('/')
def serve_index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
