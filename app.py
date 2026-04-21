#!/usr/bin/env python3
"""
Flask Backend API for Laptop Recommendation System
Provides RESTful endpoints for laptop recommendations
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
from analytics import LaptopAnalytics

app = Flask(__name__)
CORS(app)

class UseCase(Enum):
    GAMING = "gaming"
    BUSINESS = "business"
    STUDENT = "student"
    CREATIVE = "creative"
    PROGRAMMING = "programming"
    GENERAL = "general"

@dataclass
class LaptopSpecs:
    name: str
    model: str
    processor: str
    ram: str
    storage: str
    graphics: str
    display: str
    battery_life: str
    weight: str
    price_range: str
    pros: List[str]
    cons: List[str]
    use_cases: List[UseCase]
    performance_score: int
    portability_score: int
    value_score: int

class LaptopDatabase:
    def __init__(self):
        self.laptops = self._initialize_laptops()
    
    def _initialize_laptops(self) -> List[LaptopSpecs]:
        return [
            LaptopSpecs(
                name="Dell",
                model="XPS 15",
                processor="Intel Core i7-13700H",
                ram="16GB DDR5",
                storage="512GB SSD",
                graphics="NVIDIA RTX 4050",
                display="15.6\" FHD+ (1920x1200)",
                battery_life="8 hours",
                weight="4.2 lbs",
                price_range="$1,500-$2,000",
                pros=["Premium build quality", "Excellent display", "Strong performance", "Good keyboard"],
                cons=["Limited port selection", "Can run warm under load", "Premium price"],
                use_cases=[UseCase.BUSINESS, UseCase.CREATIVE, UseCase.PROGRAMMING],
                performance_score=85,
                portability_score=75,
                value_score=80
            ),
            LaptopSpecs(
                name="Apple",
                model="MacBook Air M2",
                processor="Apple M2",
                ram="8GB unified",
                storage="256GB SSD",
                graphics="Integrated 8-core GPU",
                display="13.6\" Liquid Retina (2560x1664)",
                battery_life="18 hours",
                weight="2.7 lbs",
                price_range="$1,100-$1,400",
                pros=["Incredible battery life", "Silent operation", "Premium design", "Excellent display"],
                cons=["Limited ports", "Not ideal for gaming", "Fixed RAM", "Premium pricing"],
                use_cases=[UseCase.STUDENT, UseCase.BUSINESS, UseCase.GENERAL],
                performance_score=75,
                portability_score=95,
                value_score=85
            ),
            LaptopSpecs(
                name="Lenovo",
                model="ThinkPad X1 Carbon",
                processor="Intel Core i7-1365U",
                ram="16GB LPDDR5",
                storage="1TB SSD",
                graphics="Intel Iris Xe",
                display="14\" FHD (1920x1200)",
                battery_life="15 hours",
                weight="2.8 lbs",
                price_range="$1,600-$2,200",
                pros=["Exceptional keyboard", "Business-class durability", "Great battery life", "Lightweight"],
                cons=["Average display", "Limited graphics performance", "High price"],
                use_cases=[UseCase.BUSINESS, UseCase.STUDENT, UseCase.PROGRAMMING],
                performance_score=70,
                portability_score=90,
                value_score=75
            ),
            LaptopSpecs(
                name="ASUS",
                model="ROG Strix G15",
                processor="AMD Ryzen 7 7735HS",
                ram="16GB DDR5",
                storage="1TB SSD",
                graphics="NVIDIA RTX 4060",
                display="15.6\" FHD 144Hz",
                battery_life="6 hours",
                weight="5.3 lbs",
                price_range="$1,200-$1,500",
                pros=["Excellent gaming performance", "High refresh rate display", "Good value", "RGB keyboard"],
                cons=["Heavy and bulky", "Short battery life", "Loud fans under load"],
                use_cases=[UseCase.GAMING, UseCase.PROGRAMMING],
                performance_score=90,
                portability_score=50,
                value_score=85
            ),
            LaptopSpecs(
                name="HP",
                model="Spectre x360 14",
                processor="Intel Core i7-1355U",
                ram="16GB LPDDR5",
                storage="512GB SSD",
                graphics="Intel Iris Xe",
                display="14\" 2.8K OLED (2880x1800)",
                battery_life="12 hours",
                weight="3.0 lbs",
                price_range="$1,300-$1,700",
                pros=["Stunning OLED display", "2-in-1 versatility", "Premium design", "Good performance"],
                cons=["Can run warm", "Limited gaming capability", "Reflective screen"],
                use_cases=[UseCase.CREATIVE, UseCase.BUSINESS, UseCase.STUDENT],
                performance_score=75,
                portability_score=85,
                value_score=80
            ),
            LaptopSpecs(
                name="Acer",
                model="Swift 3",
                processor="AMD Ryzen 5 7530U",
                ram="8GB LPDDR5",
                storage="512GB SSD",
                graphics="AMD Radeon Graphics",
                display="14\" FHD (1920x1080)",
                battery_life="11 hours",
                weight="2.8 lbs",
                price_range="$700-$900",
                pros=["Great value", "Lightweight", "Good battery life", "Solid performance"],
                cons=["Average display quality", "Limited storage options", "Basic build quality"],
                use_cases=[UseCase.STUDENT, UseCase.GENERAL, UseCase.BUSINESS],
                performance_score=65,
                portability_score=85,
                value_score=95
            ),
            LaptopSpecs(
                name="Razer",
                model="Blade 15",
                processor="Intel Core i7-13800H",
                ram="16GB DDR5",
                storage="1TB SSD",
                graphics="NVIDIA RTX 4070",
                display="15.6\" QHD 240Hz",
                battery_life="5 hours",
                weight="4.4 lbs",
                price_range="$2,500-$3,000",
                pros=["Premium gaming performance", "Excellent display", "CNC aluminum build", "RGB keyboard"],
                cons=["Very expensive", "Poor battery life", "Can get hot", "Heavy"],
                use_cases=[UseCase.GAMING, UseCase.CREATIVE, UseCase.PROGRAMMING],
                performance_score=95,
                portability_score=60,
                value_score=70
            ),
            LaptopSpecs(
                name="Microsoft",
                model="Surface Laptop 5",
                processor="Intel Core i7-1255U",
                ram="16GB LPDDR5x",
                storage="512GB SSD",
                graphics="Intel Iris Xe",
                display="13.5\" PixelSense (2256x1504)",
                battery_life="18 hours",
                weight="2.8 lbs",
                price_range="$1,600-$2,000",
                pros=["Excellent touchscreen", "Premium build", "Great battery life", "Silent operation"],
                cons=["Limited ports", "Not for gaming", "High price", "Fixed configuration"],
                use_cases=[UseCase.BUSINESS, UseCase.STUDENT, UseCase.CREATIVE],
                performance_score=70,
                portability_score=90,
                value_score=75
            )
        ]

class LaptopRecommender:
    def __init__(self):
        self.db = LaptopDatabase()
    
    def recommend_laptops(self, use_case: UseCase, max_price: int = None, 
                         min_performance: int = None, prioritize_portability: bool = False) -> List[LaptopSpecs]:
        candidates = [laptop for laptop in self.db.laptops if use_case in laptop.use_cases]
        
        if max_price:
            candidates = [l for l in candidates if self._parse_price_range(l.price_range)[1] <= max_price]
        
        if min_performance:
            candidates = [l for l in candidates if l.performance_score >= min_performance]
        
        scored_laptops = []
        for laptop in candidates:
            score = self._calculate_relevance_score(laptop, use_case, prioritize_portability)
            scored_laptops.append((laptop, score))
        
        scored_laptops.sort(key=lambda x: x[1], reverse=True)
        return [laptop for laptop, score in scored_laptops[:5]]
    
    def _calculate_relevance_score(self, laptop: LaptopSpecs, use_case: UseCase, 
                                 prioritize_portability: bool) -> float:
        base_score = 0.0
        
        if use_case in laptop.use_cases:
            base_score += 30
        
        if use_case == UseCase.GAMING:
            base_score += laptop.performance_score * 0.5
            base_score -= (5.3 - float(laptop.weight.split()[0])) * 2
        elif use_case == UseCase.BUSINESS:
            base_score += laptop.performance_score * 0.3
            base_score += laptop.portability_score * 0.4
            base_score += laptop.value_score * 0.3
        elif use_case == UseCase.STUDENT:
            base_score += laptop.performance_score * 0.3
            base_score += laptop.portability_score * 0.4
            base_score += laptop.value_score * 0.5
        elif use_case == UseCase.CREATIVE:
            base_score += laptop.performance_score * 0.4
            base_score += laptop.portability_score * 0.2
            base_score += laptop.value_score * 0.2
        elif use_case == UseCase.PROGRAMMING:
            base_score += laptop.performance_score * 0.4
            base_score += laptop.portability_score * 0.3
            base_score += laptop.value_score * 0.2
        else:
            base_score += laptop.performance_score * 0.3
            base_score += laptop.portability_score * 0.3
            base_score += laptop.value_score * 0.4
        
        if prioritize_portability:
            base_score += laptop.portability_score * 0.2
        
        return base_score
    
    def _parse_price_range(self, price_range: str) -> Tuple[int, int]:
        prices = price_range.replace('$', '').split('-')
        min_price = int(prices[0].replace(',', '').strip())
        max_price = int(prices[1].replace(',', '').strip())
        return (min_price, max_price)
    
    def generate_recommendation_output(self, recommendations: List[LaptopSpecs], use_case: UseCase) -> Dict:
        json_output = {
            "use_case": use_case.value,
            "recommendations": [],
            "comparison_summary": {}
        }
        
        for i, laptop in enumerate(recommendations, 1):
            laptop_json = {
                "rank": i,
                "name": laptop.name,
                "model": laptop.model,
                "specs": {
                    "processor": laptop.processor,
                    "ram": laptop.ram,
                    "storage": laptop.storage,
                    "graphics": laptop.graphics,
                    "display": laptop.display,
                    "battery_life": laptop.battery_life,
                    "weight": laptop.weight
                },
                "price_range": laptop.price_range,
                "pros": laptop.pros,
                "cons": laptop.cons,
                "fit_explanation": self._generate_fit_explanation(laptop, use_case)
            }
            json_output["recommendations"].append(laptop_json)
        
        json_output["comparison_summary"] = self._generate_comparison_summary(recommendations)
        return json_output
    
    def _generate_fit_explanation(self, laptop: LaptopSpecs, use_case: UseCase) -> str:
        explanations = {
            UseCase.GAMING: f"The {laptop.name} {laptop.model} excels at gaming with its {laptop.graphics} graphics and {laptop.processor} processor. The {laptop.display} provides smooth gameplay, making it ideal for both casual and competitive gaming.",
            UseCase.BUSINESS: f"The {laptop.name} {laptop.model} is perfect for business use with its professional design, reliable {laptop.processor} processor, and excellent portability at {laptop.weight}. The {laptop.battery_life} battery life ensures you can work through long meetings.",
            UseCase.STUDENT: f"The {laptop.name} {laptop.model} is ideal for students with its balance of performance and portability. At {laptop.weight}, it's easy to carry between classes, and the {laptop.battery_life} battery life will last through multiple lectures.",
            UseCase.CREATIVE: f"The {laptop.name} {laptop.model} supports creative work with its powerful {laptop.processor} processor and {laptop.graphics} graphics. The {laptop.display} provides excellent color accuracy for photo and video editing.",
            UseCase.PROGRAMMING: f"The {laptop.name} {laptop.model} handles programming tasks well with its {laptop.ram} RAM and {laptop.processor} processor. The comfortable keyboard and good performance make it suitable for long coding sessions.",
            UseCase.GENERAL: f"The {laptop.name} {laptop.model} offers great all-around performance for everyday tasks. With its {laptop.processor} processor and {laptop.battery_life} battery life, it's perfect for web browsing, email, and light productivity work."
        }
        return explanations.get(use_case, f"The {laptop.name} {laptop.model} offers a good balance of features for your needs.")
    
    def _generate_comparison_summary(self, recommendations: List[LaptopSpecs]) -> Dict:
        return {
            "best_performance": max(recommendations, key=lambda x: x.performance_score).model,
            "most_portable": min(recommendations, key=lambda x: float(x.weight.split()[0])).model,
            "best_value": max(recommendations, key=lambda x: x.value_score).model,
            "price_range_comparison": {
                laptop.model: laptop.price_range for laptop in recommendations
            }
        }

# Initialize recommender and analytics
recommender = LaptopRecommender()
analytics = LaptopAnalytics(recommender.db.laptops)

@app.route('/')
def index():
    return render_template('enhanced_index.html')

@app.route('/basic')
def basic():
    return render_template('index.html')

@app.route('/api/use-cases')
def get_use_cases():
    return jsonify([use_case.value for use_case in UseCase])

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        
        use_case_str = data.get('use_case', 'general')
        max_price = data.get('max_price')
        prioritize_portability = data.get('prioritize_portability', False)
        
        use_case = UseCase(use_case_str)
        
        recommendations = recommender.recommend_laptops(
            use_case=use_case,
            max_price=max_price,
            prioritize_portability=prioritize_portability
        )
        
        if not recommendations:
            return jsonify({"error": "No laptops found matching your criteria"}), 404
        
        output = recommender.generate_recommendation_output(recommendations, use_case)
        return jsonify(output)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/laptops')
def get_all_laptops():
    laptops_data = []
    for laptop in recommender.db.laptops:
        laptop_dict = {
            "name": laptop.name,
            "model": laptop.model,
            "processor": laptop.processor,
            "ram": laptop.ram,
            "storage": laptop.storage,
            "graphics": laptop.graphics,
            "display": laptop.display,
            "battery_life": laptop.battery_life,
            "weight": laptop.weight,
            "price_range": laptop.price_range,
            "pros": laptop.pros,
            "cons": laptop.cons,
            "use_cases": [uc.value for uc in laptop.use_cases],
            "performance_score": laptop.performance_score,
            "portability_score": laptop.portability_score,
            "value_score": laptop.value_score
        }
        laptops_data.append(laptop_dict)
    
    return jsonify(laptops_data)

@app.route('/api/analytics/summary')
def get_analytics_summary():
    """Get analytics summary for dashboard"""
    return jsonify(analytics.generate_analytics_summary())

@app.route('/api/analytics/charts')
def get_analytics_charts():
    """Get all chart paths"""
    charts = analytics.generate_all_charts()
    return jsonify(charts)

@app.route('/analytics')
def analytics_dashboard():
    """Analytics dashboard page"""
    return render_template('analytics.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
