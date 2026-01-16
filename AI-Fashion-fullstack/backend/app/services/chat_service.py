from typing import List, Dict
from groq import Groq
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY) if settings.GROQ_API_KEY else None
        self.conversations = {}
    
    def chat(self, session_id: str, message: str, search_results: List[dict] = None) -> str:
        if not self.client:
            return "Chat service not configured. Please add GROQ_API_KEY."
        
        # Get conversation history
        history = self.conversations.get(session_id, [])
        
        # Add context if search results
        context = ""
        if search_results:
            context = "\nAvailable products:\n"
            for p in search_results[:5]:
                context += f"- {p['product_name']}\n"
        
        # Build messages
        messages = [{"role": "system", "content": "You are a helpful fashion shopping assistant."}]
        messages.extend(history)
        messages.append({"role": "user", "content": message + context})
        
        try:
            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            reply = response.choices[0].message.content
            
            # Update history
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": reply})
            if len(history) > 10:
                history = history[-10:]
            self.conversations[session_id] = history
            
            return reply
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return f"Error: {str(e)}"
