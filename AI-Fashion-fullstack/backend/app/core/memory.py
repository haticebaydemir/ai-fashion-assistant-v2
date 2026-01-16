"""Conversation memory system with sliding window and auto-summarization."""

from collections import deque
from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime


@dataclass
class Turn:
    """Single conversation turn."""
    query: str
    response: str
    tool_used: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert turn to dictionary."""
        return {
            "query": self.query,
            "response": self.response,
            "tool_used": self.tool_used,
            "timestamp": self.timestamp.isoformat()
        }


class ConversationMemory:
    """Sliding window conversation memory with auto-summarization."""
    
    def __init__(self, max_turns: int = 10, summarize_threshold: int = 5):
        """
        Initialize conversation memory.
        
        Args:
            max_turns: Maximum turns to keep in memory (sliding window)
            summarize_threshold: Auto-summarize after N turns
        """
        self.turns: deque = deque(maxlen=max_turns)
        self.max_turns = max_turns
        self.summarize_threshold = summarize_threshold
        self.summary: Optional[str] = None
        self.all_turns: List[Turn] = []  # Full history
    
    def add_turn(self, query: str, response: str, tool_used: Optional[str] = None) -> None:
        """Add a new turn to memory."""
        turn = Turn(query=query, response=response, tool_used=tool_used)
        self.turns.append(turn)
        self.all_turns.append(turn)
        
        # Auto-summarize if threshold reached
        if len(self.all_turns) > 0 and len(self.all_turns) % self.summarize_threshold == 0:
            self._auto_summarize()
    
    def get_context(self, include_summary: bool = True) -> str:
        """Get formatted context for LLM injection."""
        context_parts = []
        
        # Add summary if available
        if include_summary and self.summary:
            context_parts.append(f"Previous Conversation Summary:\n{self.summary}\n")
        
        # Add recent turns
        if self.turns:
            context_parts.append("Recent Conversation:")
            for i, turn in enumerate(self.turns, 1):
                tool_info = f" [used: {turn.tool_used}]" if turn.tool_used else ""
                context_parts.append(f"  Turn {i}: Q: {turn.query}\n    A: {turn.response}{tool_info}")
        
        return "\n".join(context_parts)
    
    def _auto_summarize(self) -> None:
        """Generate summary of conversation (basic version)."""
        if not self.all_turns:
            return
        
        # Extract key topics from queries
        queries = [t.query for t in self.all_turns]
        tools_used = [t.tool_used for t in self.all_turns if t.tool_used]
        
        # Simple summary generation
        unique_tools = set(tools_used)
        self.summary = f"User has asked {len(queries)} questions about fashion products. "
        self.summary += f"Topics covered: {', '.join(queries[:3])}... "
        self.summary += f"Tools used: {', '.join(unique_tools) if unique_tools else 'General search'}."
    
    def clear(self) -> None:
        """Clear memory."""
        self.turns.clear()
        self.all_turns.clear()
        self.summary = None
    
    def get_stats(self) -> Dict:
        """Get memory statistics."""
        tools_used = [t.tool_used for t in self.all_turns if t.tool_used]
        return {
            "total_turns": len(self.all_turns),
            "current_window": len(self.turns),
            "max_window": self.max_turns,
            "tools_used": dict(zip(set(tools_used), [tools_used.count(t) for t in set(tools_used)])),
            "has_summary": self.summary is not None,
            "memory_efficiency": (len(self.turns) / self.max_turns * 100) if self.max_turns > 0 else 0
        }
