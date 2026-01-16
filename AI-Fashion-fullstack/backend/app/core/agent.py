"""ReAct Agent implementation with LangChain tool calling."""

from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import re
import numpy as np

from app.core.memory import ConversationMemory
from app.services.search_engine import FashionSearchEngine
import logging

logger = logging.getLogger(__name__)


class ActionType(Enum):
    """Tool action types."""
    SEARCH_PRODUCTS = "SearchProducts"
    RECOMMEND_SIMILAR = "RecommendSimilar"
    GET_PRODUCT_DETAILS = "GetProductDetails"
    FINAL_ANSWER = "FinalAnswer"


@dataclass
class AgentAction:
    """Represents an action the agent decides to take."""
    tool: ActionType
    input: Dict[str, Any]
    thought: str


@dataclass
class AgentResponse:
    """Final agent response with metadata."""
    response: str
    actions_taken: List[AgentAction]
    final_answer: str
    reasoning: str
    used_memory: bool = False
    response_time: float = 0.0


class FashionAgent:
    """ReAct-based fashion assistant agent with tool calling and memory."""
    
    def __init__(
        self,
        search_engine: FashionSearchEngine,
        products_df: Any,
        max_iterations: int = 5,
        memory: Optional[ConversationMemory] = None
    ):
        """
        Initialize agent.
        
        Args:
            search_engine: FashionSearchEngine instance
            products_df: Products DataFrame with metadata
            max_iterations: Max ReAct loop iterations
            memory: Conversation memory (optional)
        """
        self.search_engine = search_engine
        self.products_df = products_df
        self.max_iterations = max_iterations
        self.memory = memory or ConversationMemory()
        self.iterations = 0
        
        # Initialize tool registry
        self._init_tools()
    
    def _init_tools(self) -> None:
        """Initialize available tools."""
        self.tools = {
            "SearchProducts": self._search_products_tool,
            "RecommendSimilar": self._recommend_similar_tool,
            "GetProductDetails": self._get_product_details_tool,
        }
    
    def _search_products_tool(self, query: str, k: int = 5) -> List[Dict]:
        """Search products by query."""
        try:
            results = self.search_engine.search(query=query, k=k, mode="text")
            products = []
            for result in results[:k]:
                prod_data = self.products_df[self.products_df['product_id'] == result.product_id].iloc[0]
                products.append({
                    "product_id": result.product_id,
                    "name": prod_data.get('product_name', 'Unknown'),
                    "category": prod_data.get('category', 'Unknown'),
                    "color": prod_data.get('color', 'Unknown'),
                    "price": prod_data.get('price', 'N/A'),
                    "gender": prod_data.get('gender', 'Unisex'),
                    "score": float(result.score)
                })
            return products
        except Exception as e:
            logger.error(f"Search tool error: {e}")
            return []
    
    def _recommend_similar_tool(self, product_id: int, k: int = 3) -> List[Dict]:
        """Get similar products to a given product ID."""
        try:
            # Find product in embeddings
            if product_id not in self.products_df['product_id'].values:
                return []
            
            # Use image search for similarity
            results = self.search_engine.search(query=str(product_id), k=k+1, mode="image")
            similar = []
            for result in results:
                if result.product_id != product_id:  # Exclude input product
                    prod_data = self.products_df[self.products_df['product_id'] == result.product_id].iloc[0]
                    similar.append({
                        "product_id": result.product_id,
                        "name": prod_data.get('product_name', 'Unknown'),
                        "category": prod_data.get('category', 'Unknown'),
                        "color": prod_data.get('color', 'Unknown'),
                        "similarity_score": float(result.score)
                    })
            return similar[:k]
        except Exception as e:
            logger.error(f"Recommend tool error: {e}")
            return []
    
    def _get_product_details_tool(self, product_id: int) -> Optional[Dict]:
        """Get full details for a product."""
        try:
            if product_id not in self.products_df['product_id'].values:
                return None
            
            prod_data = self.products_df[self.products_df['product_id'] == product_id].iloc[0]
            return {
                "product_id": product_id,
                "name": prod_data.get('product_name', 'Unknown'),
                "category": prod_data.get('category', 'Unknown'),
                "color": prod_data.get('color', 'Unknown'),
                "gender": prod_data.get('gender', 'Unisex'),
                "price": prod_data.get('price', 'N/A'),
                "material": prod_data.get('material', 'N/A'),
                "description": prod_data.get('description', 'N/A'),
                "in_stock": prod_data.get('in_stock', True)
            }
        except Exception as e:
            logger.error(f"Details tool error: {e}")
            return None
    
    def _parse_action(self, text: str) -> Optional[AgentAction]:
        """Parse LLM thought output to extract action."""
        # Look for action patterns
        action_patterns = {
            "SearchProducts": r"(SearchProducts|Search)\[(.+?)\]",
            "RecommendSimilar": r"(RecommendSimilar|Recommend)\[(\d+)\]",
            "GetProductDetails": r"(GetProductDetails|Details)\[(\d+)\]",
        }
        
        for tool_name, pattern in action_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if tool_name == "SearchProducts":
                    return AgentAction(
                        tool=ActionType.SEARCH_PRODUCTS,
                        input={"query": match.group(2), "k": 5},
                        thought=text
                    )
                elif tool_name == "RecommendSimilar":
                    return AgentAction(
                        tool=ActionType.RECOMMEND_SIMILAR,
                        input={"product_id": int(match.group(2)), "k": 3},
                        thought=text
                    )
                elif tool_name == "GetProductDetails":
                    return AgentAction(
                        tool=ActionType.GET_PRODUCT_DETAILS,
                        input={"product_id": int(match.group(2))},
                        thought=text
                    )
        
        # Check for final answer
        if "Final Answer:" in text or "final answer:" in text.lower():
            return AgentAction(
                tool=ActionType.FINAL_ANSWER,
                input={"answer": text},
                thought=text
            )
        
        return None
    
    def _execute_action(self, action: AgentAction) -> str:
        """Execute a tool action and return observation."""
        tool_name = action.tool.value
        
        if action.tool == ActionType.SEARCH_PRODUCTS:
            results = self._search_products_tool(**action.input)
            return f"Found {len(results)} products: {results[:3]}"
        
        elif action.tool == ActionType.RECOMMEND_SIMILAR:
            results = self._recommend_similar_tool(**action.input)
            return f"Similar products: {results}"
        
        elif action.tool == ActionType.GET_PRODUCT_DETAILS:
            result = self._get_product_details_tool(**action.input)
            return f"Product details: {result}" if result else "Product not found"
        
        elif action.tool == ActionType.FINAL_ANSWER:
            return action.input.get("answer", "No answer provided")
        
        return f"Unknown action: {tool_name}"
    
    def run(self, query: str, use_memory: bool = True) -> AgentResponse:
        """Run ReAct agent loop."""
        import time
        start_time = time.time()
        
        actions_taken: List[AgentAction] = []
        context = self.memory.get_context() if use_memory else ""
        
        # Prepare initial thought
        full_query = f"{context}\n\nUser Query: {query}" if context else f"Query: {query}"
        thought = f"I need to help the user with: {query}. Let me search for relevant products."
        
        # ReAct loop
        for iteration in range(self.max_iterations):
            self.iterations += 1
            
            # Parse action from thought
            action = self._parse_action(thought)
            if not action:
                # Default to search if no action parsed
                action = AgentAction(
                    tool=ActionType.SEARCH_PRODUCTS,
                    input={"query": query, "k": 5},
                    thought=thought
                )
            
            actions_taken.append(action)
            
            # Execute action
            observation = self._execute_action(action)
            
            # Check if final answer reached
            if action.tool == ActionType.FINAL_ANSWER:
                break
            
            # Generate next thought based on observation
            thought = f"Based on the observation: {observation[:100]}..., "
            
            if iteration < self.max_iterations - 1:
                thought += "I should search for more specific products or get details."
            else:
                thought += "Final Answer: I've found relevant products for your request."
        
        # Generate final response
        final_answer = "\n".join([
            f"Based on your search for '{query}':",
            f"I found {len(actions_taken)} relevant product(s) for you.",
            f"Tools used: {', '.join([a.tool.value for a in actions_taken if a.tool != ActionType.FINAL_ANSWER])}"
        ])
        
        # Add to memory
        tools_str = ", ".join(set([a.tool.value for a in actions_taken if a.tool != ActionType.FINAL_ANSWER]))
        self.memory.add_turn(query, final_answer, tool_used=tools_str if tools_str else None)
        
        response_time = time.time() - start_time
        
        return AgentResponse(
            response=final_answer,
            actions_taken=actions_taken,
            final_answer=final_answer,
            reasoning=thought,
            used_memory=use_memory and bool(context),
            response_time=response_time
        )
    
    def get_memory_stats(self) -> Dict:
        """Get conversation memory statistics."""
        return self.memory.get_stats()
    
    def clear_memory(self) -> None:
        """Clear conversation memory."""
        self.memory.clear()
