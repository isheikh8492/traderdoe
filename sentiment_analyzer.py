import re
from typing import Dict, List

class SentimentAnalyzer:
    def __init__(self):
        self.bullish_keywords = [
            "bullish", "buy", "long", "pump", "moon", "rocket", "gains", 
            "breakout", "rally", "surge", "bull run", "to the moon", 
            "diamond hands", "hodl", "calls", "green"
        ]
        
        self.bearish_keywords = [
            "bearish", "sell", "short", "dump", "crash", "drop", "fall",
            "bear", "puts", "red", "dip", "correction", "bubble", 
            "overvalued", "panic", "blood"
        ]
        
        self.neutral_keywords = [
            "sideways", "flat", "consolidation", "range", "support", 
            "resistance", "hold", "wait", "watch"
        ]
    
    def analyze_text(self, text: str) -> float:
        text_lower = text.lower()
        
        bullish_count = sum(1 for keyword in self.bullish_keywords if keyword in text_lower)
        bearish_count = sum(1 for keyword in self.bearish_keywords if keyword in text_lower)
        neutral_count = sum(1 for keyword in self.neutral_keywords if keyword in text_lower)
        
        total_keywords = bullish_count + bearish_count + neutral_count
        
        if total_keywords == 0:
            return 0.0
        
        sentiment_score = (bullish_count - bearish_count) / total_keywords
        
        return max(-1.0, min(1.0, sentiment_score))
    
    def get_sentiment_label(self, score: float) -> str:
        if score > 0.2:
            return "Bullish"
        elif score < -0.2:
            return "Bearish"
        else:
            return "Neutral"
    
    def analyze_batch(self, texts: List[str]) -> Dict[str, float]:
        results = {}
        for i, text in enumerate(texts):
            score = self.analyze_text(text)
            results[f"text_{i}"] = {
                "score": score,
                "label": self.get_sentiment_label(score)
            }
        return results