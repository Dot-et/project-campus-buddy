# modules/dictionary.py - SUPER SIMPLE VERSION
import requests

def define(word):
    """Get word definition - simple version"""
    try:
        # Call free dictionary API
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            return f"❌ '{word}' not found"
        
        data = response.json()
        first_meaning = data[0]['meanings'][0]
        definition = first_meaning['definitions'][0]['definition']
        
        return f"📚 {word}:\n{definition}"
        
    except:
        return f"❌ Error getting '{word}'"