"""Visual-aware RAG with attribute integration - v2.4.5."""

import json
import time
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class VisualAttributeFilter:
    """Filter products based on visual attributes from v2.1."""
    
    def __init__(self, attributes_df: Any = None):
        """
        Initialize attribute filter.
        
        Args:
            attributes_df: DataFrame with product attributes (product_id, attribute, confidence)
        """
        self.attributes_df = attributes_df
        self._build_attribute_index()
    
    def _build_attribute_index(self):
        """Build index for fast attribute lookup."""
        self.product_attributes = {}
        
        if self.attributes_df is not None and not self.attributes_df.empty:
            for _, row in self.attributes_df.iterrows():
                product_id = row.get('product_id')
                attribute = row.get('attribute')
                confidence = row.get('confidence', 1.0)
                
                if product_id not in self.product_attributes:
                    self.product_attributes[product_id] = []
                
                self.product_attributes[product_id].append({
                    "attribute": attribute,
                    "confidence": confidence
                })
    
    def get_attributes(self, product_id: int) -> List[Dict]:
        """Get attributes for a product."""
        return self.product_attributes.get(product_id, [])
    
    def filter_by_attributes(self, results: List[Any], target_attributes: List[str],
                            confidence_threshold: float = 0.3) -> List[Any]:
        """
        Filter results by target attributes.
        
        Args:
            results: List of retrieval results
            target_attributes: List of desired attributes
            confidence_threshold: Minimum confidence score
        
        Returns:
            Filtered results
        """
        if not target_attributes:
            return results
        
        filtered = []
        for result in results:
            product_id = result.product_id
            product_attrs = self.get_attributes(product_id)
            
            # Check if product has any target attributes
            matching = 0
            for attr in product_attrs:
                if attr["attribute"] in target_attributes and attr["confidence"] >= confidence_threshold:
                    matching += 1
            
            if matching > 0:
                filtered.append(result)
        
        return filtered
    
    def extract_visual_keywords(self, product_id: int, top_k: int = 5) -> List[str]:
        """Extract top visual keywords for a product."""
        attrs = self.get_attributes(product_id)
        
        # Sort by confidence
        sorted_attrs = sorted(attrs, key=lambda x: x["confidence"], reverse=True)
        
        # Return top keywords
        keywords = [attr["attribute"] for attr in sorted_attrs[:top_k]]
        return keywords


class VisualAwareRAG:
    """RAG system with visual attribute awareness."""
    
    def __init__(self, rag_pipeline: Any, attribute_filter: VisualAttributeFilter = None):
        """
        Initialize visual-aware RAG.
        
        Args:
            rag_pipeline: Base RAGPipeline from v2.2
            attribute_filter: VisualAttributeFilter for attribute integration
        """
        self.rag_pipeline = rag_pipeline
        self.attribute_filter = attribute_filter or VisualAttributeFilter()
    
    def _build_visual_context(self, products: List[Dict]) -> str:
        """Build context with visual attributes."""
        context_parts = ["Here are the recommended fashion items with visual details:\n"]
        
        for i, product in enumerate(products[:5], 1):  # Top 5 for context
            product_id = product.get('product_id')
            name = product.get('name', 'Unknown')
            category = product.get('category', 'Unknown')
            color = product.get('color', 'Unknown')
            
            # Get visual keywords
            visual_keywords = self.attribute_filter.extract_visual_keywords(product_id, top_k=3)
            keywords_str = ", ".join(visual_keywords) if visual_keywords else "classic style"
            
            context_parts.append(
                f"{i}. {name} ({category}) - {color} | Style: {keywords_str}"
            )
        
        return "\n".join(context_parts)
    
    def query_with_visual_awareness(self, query: str, products: List[Dict],
                                   use_cache: bool = True) -> Dict[str, Any]:
        """
        Generate RAG response with visual awareness.
        
        Args:
            query: User query
            products: Retrieved products
            use_cache: Whether to use caching
        
        Returns:
            Response with visual awareness
        """
        start_time = time.time()
        
        # Build visual context
        visual_context = self._build_visual_context(products)
        
        # Enhance prompt with visual awareness
        enhanced_query = f"{query}\n\n[Visual Context]\n{visual_context}"
        
        # Query RAG pipeline with enhanced context
        try:
            response = self.rag_pipeline.query(enhanced_query, products=products, use_cache=use_cache)
        except Exception as e:
            logger.error(f"Error in RAG query: {e}")
            response = {
                "answer": "I couldn't generate a response at this time.",
                "products": products,
                "response_time": time.time() - start_time,
                "cached": False
            }
        
        # Extract visual keywords from response
        visual_keywords_in_response = 0
        if self.attribute_filter:
            response_lower = response.get("answer", "").lower()
            for product in products[:5]:
                product_id = product.get('product_id')
                keywords = self.attribute_filter.extract_visual_keywords(product_id, top_k=3)
                for kw in keywords:
                    if kw.lower() in response_lower:
                        visual_keywords_in_response += 1
        
        response["visual_awareness"] = {
            "visual_keywords_count": visual_keywords_in_response,
            "visual_context_length": len(visual_context)
        }
        
        response["response_time"] = time.time() - start_time
        
        return response
    
    def query_with_attribute_filtering(self, query: str, products: List[Dict],
                                      target_attributes: List[str] = None,
                                      use_cache: bool = True) -> Dict[str, Any]:
        """
        Query with attribute-based filtering.
        
        Args:
            query: User query
            products: Retrieved products
            target_attributes: Attributes to filter by
            use_cache: Whether to use caching
        
        Returns:
            Response with filtered products
        """
        # Filter products by attributes
        if target_attributes and self.attribute_filter:
            products = self.attribute_filter.filter_by_attributes(products, target_attributes)
        
        # Generate response with visual awareness
        return self.query_with_visual_awareness(query, products, use_cache=use_cache)
    
    def get_visual_summary(self, products: List[Dict]) -> Dict[str, Any]:
        """Get visual summary of products."""
        visual_summary = {
            "total_products": len(products),
            "products_with_attributes": 0,
            "average_keywords_per_product": 0,
            "all_keywords": {}
        }
        
        if not self.attribute_filter:
            return visual_summary
        
        total_keywords = 0
        for product in products:
            product_id = product.get('product_id')
            keywords = self.attribute_filter.extract_visual_keywords(product_id, top_k=5)
            
            if keywords:
                visual_summary["products_with_attributes"] += 1
                total_keywords += len(keywords)
                
                for kw in keywords:
                    visual_summary["all_keywords"][kw] = visual_summary["all_keywords"].get(kw, 0) + 1
        
        if visual_summary["products_with_attributes"] > 0:
            visual_summary["average_keywords_per_product"] = (
                total_keywords / visual_summary["products_with_attributes"]
            )
        
        return visual_summary
    
    def save_visual_rag_results(self, results: List[Dict], output_dir: Path):
        """Save visual RAG results to file."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON results
        output_file = output_dir / "visual_rag_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Saved visual RAG results to {output_file}")
        
        return output_file


class AttributeEnhancedResponse:
    """Response with visual attribute enhancements."""
    
    def __init__(self, base_response: str, visual_attributes: Dict):
        """
        Initialize attribute-enhanced response.
        
        Args:
            base_response: Base LLM response
            visual_attributes: Visual attributes to inject
        """
        self.base_response = base_response
        self.visual_attributes = visual_attributes
    
    def enhance_with_attributes(self) -> str:
        """Enhance response with visual attributes."""
        enhanced = self.base_response
        
        # Add attribute insights
        if self.visual_attributes.get("all_keywords"):
            keywords = self.visual_attributes["all_keywords"]
            top_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:3]
            
            if top_keywords:
                keyword_str = ", ".join([kw for kw, _ in top_keywords])
                enhanced += f"\n\nKey visual styles: {keyword_str}"
        
        return enhanced
    
    def get_visual_summary(self) -> str:
        """Get summary of visual attributes."""
        summary = f"Visual Summary: "
        summary += f"{self.visual_attributes.get('total_products', 0)} products, "
        summary += f"{self.visual_attributes.get('average_keywords_per_product', 0):.1f} visual keywords avg"
        
        return summary
