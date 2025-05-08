from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Supported languages for MyMemory (must specify source)
LANGUAGES = {
    'en': 'English 🇺🇸',
    'es': 'Spanish 🇪🇸',
    'fr': 'French 🇫🇷',
    'de': 'German 🇩🇪',
    'it': 'Italian 🇮🇹',
    'pt': 'Portuguese 🇧🇷',
    'ru': 'Russian 🇷🇺',
    'zh': 'Chinese 🇨🇳',
    'ja': 'Japanese 🇯🇵',
    'hi': 'Hindi 🇮🇳',
    'ar': 'Arabic 🇸🇦',
    'ko': 'Korean 🇰🇷'
}

USER_EMAIL = "rushikyadav3@gmail.com"  # Required by MyMemory

def detect_language(text):
    """Simple language detection (fallback to English)"""
    # Check for non-Latin characters as hint
    if any(ord(c) > 127 for c in text[:10]):  # Sample first 10 chars
        return 'auto'  # Will let MyMemory handle it
    return 'en'  # Default to English

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ''
    
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        target_lang = request.form.get('language', 'en')
        
        if not text:
            translated_text = "⚠️ Please enter text"
        else:
            try:
                # First detect source language
                source_lang = detect_language(text)
                
                response = requests.get(
                    'https://api.mymemory.translated.net/get',
                    params={
                        'q': text,
                        'langpair': f'{source_lang}|{target_lang}',
                        'de': USER_EMAIL
                    },
                    timeout=5
                )
                
                data = response.json()
                
                if response.status_code == 200:
                    translated_text = data.get('responseData', {}).get('translatedText', '')
                    if not translated_text:
                        translated_text = "⚠️ No translation available"
                else:
                    translated_text = f"⚠️ Error {response.status_code}"

            except requests.Timeout:
                translated_text = "⚠️ Translation timed out"
            except Exception as e:
                translated_text = f"⚠️ Error: {str(e)}"

    return render_template('index.html',
                        languages=LANGUAGES,
                        translated_text=translated_text)

if __name__ == '__main__':
    app.run(debug=True)