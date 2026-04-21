#!/usr/bin/env python3
"""
Analytics and Visualization Module for Laptop Recommendation System
Generates charts and graphs for data visualization and client presentations
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import json
import base64
from io import BytesIO
from typing import Dict, List, Any
import os
from datetime import datetime, timedelta
import random

# Set style for professional appearance
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class LaptopAnalytics:
    def __init__(self, laptop_data):
        self.laptop_data = laptop_data
        self.df = pd.DataFrame(laptop_data)
        self.setup_directories()
        self.generate_sales_data()
    
    def setup_directories(self):
        """Create directories for storing charts"""
        os.makedirs('static/charts', exist_ok=True)
        os.makedirs('static/reports', exist_ok=True)
    
    def generate_sales_data(self):
        """Generate realistic sales trend data"""
        # Generate 12 months of sales data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        current_year = datetime.now().year
        
        self.sales_data = []
        for i, month in enumerate(months):
            for laptop in self.laptop_data:
                # Generate realistic sales numbers with seasonal trends
                base_sales = random.randint(50, 200)
                
                # Add seasonal variations (higher in back-to-school and holiday seasons)
                if month in ['Aug', 'Sep', 'Nov', 'Dec']:
                    seasonal_boost = random.uniform(1.3, 1.8)
                elif month in ['Jan', 'Feb']:
                    seasonal_boost = random.uniform(0.7, 0.9)
                else:
                    seasonal_boost = random.uniform(0.9, 1.2)
                
                sales = int(base_sales * seasonal_boost)
                
                # Extract price range from LaptopSpecs object
                price_range = laptop.price_range.replace('$', '').split('-')
                max_price = int(price_range[1].replace(',', '').strip())
                
                self.sales_data.append({
                    'month': month,
                    'year': current_year,
                    'laptop_name': f"{laptop.name} {laptop.model}",
                    'brand': laptop.name,
                    'sales': sales,
                    'revenue': sales * max_price,
                    'use_case': laptop.use_cases[0].value if laptop.use_cases else 'general',
                    'price_range': max_price
                })
        
        self.sales_df = pd.DataFrame(self.sales_data)
    
    def create_sales_trend_chart(self) -> str:
        """Create sales trend over time chart"""
        monthly_sales = self.sales_df.groupby('month').agg({
            'sales': 'sum',
            'revenue': 'sum'
        }).reset_index()
        
        # Ensure months are in chronological order
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_sales['month'] = pd.Categorical(monthly_sales['month'], categories=month_order, ordered=True)
        monthly_sales = monthly_sales.sort_values('month')
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Monthly Sales Volume', 'Monthly Revenue'),
            vertical_spacing=0.1
        )
        
        # Sales volume chart
        fig.add_trace(
            go.Scatter(
                x=monthly_sales['month'],
                y=monthly_sales['sales'],
                mode='lines+markers',
                name='Sales Volume',
                line=dict(color='#1e3a8a', width=3),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
        
        # Revenue chart
        fig.add_trace(
            go.Scatter(
                x=monthly_sales['month'],
                y=monthly_sales['revenue'],
                mode='lines+markers',
                name='Revenue',
                line=dict(color='#10b981', width=3),
                marker=dict(size=8)
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title_text="Sales Trends - Monthly Analysis",
            font=dict(size=12),
            height=600,
            showlegend=False
        )
        
        fig.update_yaxes(title_text="Units Sold", row=1, col=1)
        fig.update_yaxes(title_text="Revenue ($)", row=2, col=1)
        fig.update_xaxes(title_text="Month", row=2, col=1)
        
        chart_path = 'static/charts/sales_trend.html'
        fig.write_html(chart_path)
        return chart_path
    
    def create_brand_sales_comparison(self) -> str:
        """Create brand sales comparison chart"""
        brand_sales = self.sales_df.groupby('brand').agg({
            'sales': 'sum',
            'revenue': 'sum'
        }).reset_index()
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Sales by Brand', 'Revenue by Brand'),
            specs=[[{"type": "bar"}, {"type": "pie"}]]
        )
        
        # Sales bar chart
        fig.add_trace(
            go.Bar(
                x=brand_sales['brand'],
                y=brand_sales['sales'],
                name='Sales Volume',
                marker=dict(color='#1e3a8a')
            ),
            row=1, col=1
        )
        
        # Revenue pie chart
        fig.add_trace(
            go.Pie(
                labels=brand_sales['brand'],
                values=brand_sales['revenue'],
                name='Revenue Share',
                hole=0.3
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="Brand Sales Performance",
            font=dict(size=12),
            height=400,
            showlegend=False
        )
        
        chart_path = 'static/charts/brand_sales_comparison.html'
        fig.write_html(chart_path)
        return chart_path
    
    def create_use_case_sales_trend(self) -> str:
        """Create use case-specific sales trends"""
        use_case_sales = self.sales_df.groupby(['month', 'use_case']).agg({
            'sales': 'sum'
        }).reset_index()
        
        # Ensure months are in chronological order
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        use_case_sales['month'] = pd.Categorical(use_case_sales['month'], categories=month_order, ordered=True)
        use_case_sales = use_case_sales.sort_values(['use_case', 'month'])
        
        fig = go.Figure()
        
        use_cases = use_case_sales['use_case'].unique()
        colors = ['#1e3a8a', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#6b7280']
        
        for i, use_case in enumerate(use_cases):
            case_data = use_case_sales[use_case_sales['use_case'] == use_case]
            fig.add_trace(go.Scatter(
                x=case_data['month'],
                y=case_data['sales'],
                mode='lines+markers',
                name=use_case.title(),
                line=dict(color=colors[i % len(colors)], width=2),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            title="Sales Trends by Use Case",
            xaxis_title="Month",
            yaxis_title="Sales Volume",
            font=dict(size=12),
            height=500,
            hovermode='x unified'
        )
        
        chart_path = 'static/charts/use_case_sales_trend.html'
        fig.write_html(chart_path)
        return chart_path
    
    def create_price_segment_sales(self) -> str:
        """Create price segment sales analysis"""
        # Define price segments
        def get_price_segment(price):
            if price <= 1000:
                return 'Budget ($0-$1,000)'
            elif price <= 1500:
                return 'Mid-Range ($1,000-$1,500)'
            elif price <= 2000:
                return 'Premium ($1,500-$2,000)'
            else:
                return 'Ultra-Premium ($2,000+)'
        
        self.sales_df['price_segment'] = self.sales_df['price_range'].apply(get_price_segment)
        
        segment_sales = self.sales_df.groupby('price_segment').agg({
            'sales': 'sum',
            'revenue': 'sum'
        }).reset_index()
        
        # Sort by price segment
        segment_order = ['Budget ($0-$1,000)', 'Mid-Range ($1,000-$1,500)', 'Premium ($1,500-$2,000)', 'Ultra-Premium ($2,000+)']
        segment_sales['price_segment'] = pd.Categorical(segment_sales['price_segment'], categories=segment_order, ordered=True)
        segment_sales = segment_sales.sort_values('price_segment')
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=segment_sales['price_segment'],
            y=segment_sales['sales'],
            text=[f'{s:,}' for s in segment_sales['sales']],
            textposition='auto',
            marker=dict(
                color=segment_sales['sales'],
                colorscale='Blues',
                showscale=True
            )
        ))
        
        fig.update_layout(
            title="Sales by Price Segment",
            xaxis_title="Price Segment",
            yaxis_title="Units Sold",
            font=dict(size=12),
            height=500
        )
        
        chart_path = 'static/charts/price_segment_sales.html'
        fig.write_html(chart_path)
        return chart_path
    
    def create_performance_radar_chart(self) -> str:
        """Create a radar chart comparing all laptops on performance metrics"""
        fig = go.Figure()
        
        # Add each laptop to radar chart
        for laptop in self.laptop_data:
            fig.add_trace(go.Scatterpolar(
                r=[
                    laptop.performance_score,
                    laptop.portability_score,
                    laptop.value_score,
                    self._get_price_score(laptop.price_range),
                    self._get_battery_score(laptop.battery_life)
                ],
                theta=['Performance', 'Portability', 'Value', 'Price', 'Battery'],
                fill='toself',
                name=f"{laptop.name} {laptop.model}",
                line=dict(width=2)
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Laptop Performance Comparison - Radar Chart",
            font=dict(size=12),
            height=600
        )
        
        # Save as HTML
        chart_path = 'static/charts/performance_radar.html'
        fig.write_html(chart_path)
        return chart_path
    
    def create_price_distribution_chart(self) -> str:
        """Create a price distribution chart"""
        prices = []
        models = []
        
        for laptop in self.laptop_data:
            price_range = laptop.price_range.replace('$', '').split('-')
            avg_price = (int(price_range[0].replace(',', '').strip()) + 
                         int(price_range[1].replace(',', '').strip())) / 2
            prices.append(avg_price)
            models.append(f"{laptop.name} {laptop.model}")
        
        fig = go.Figure(data=[
            go.Bar(
                x=models,
                y=prices,
                text=[f'${int(p):,}' for p in prices],
                textposition='auto',
                marker=dict(
                    color=prices,
                    colorscale='Blues',
                    showscale=True
                )
            )
        ])
        
        fig.update_layout(
            title="Laptop Price Distribution",
            xaxis_title="Laptop Models",
            yaxis_title="Average Price (USD)",
            font=dict(size=12),
            height=500
        )
        
        chart_path = 'static/charts/price_distribution.html'
        fig.write_html(chart_path)
        return chart_path
    
    def create_performance_vs_price_scatter(self) -> str:
        """Create a scatter plot comparing performance vs price"""
        prices = []
        performance_scores = []
        model_names = []
        use_cases = []
        
        for laptop in self.laptop_data:
            price_range = laptop.price_range.replace('$', '').split('-')
            avg_price = (int(price_range[0].replace(',', '').strip()) + 
                         int(price_range[1].replace(',', '').strip())) / 2
            prices.append(avg_price)
            performance_scores.append(laptop.performance_score)
            model_names.append(f"{laptop.name} {laptop.model}")
            use_cases.append(laptop.use_cases[0].value if laptop.use_cases else 'general')
        
        fig = px.scatter(
            x=prices,
            y=performance_scores,
            color=use_cases,
            hover_name=model_names,
            labels={
                "x": "Price (USD)",
                "y": "Performance Score",
                "color": "Primary Use Case"
            },
            title="Performance vs Price Analysis",
            size=[12] * len(prices)
        )
        
        fig.update_layout(
            font=dict(size=12),
            height=500
        )
        
        chart_path = 'static/charts/performance_vs_price.html'
        fig.write_html(chart_path)
        return chart_path
    
    def create_use_case_distribution(self) -> str:
        """Create a chart showing distribution of laptops by use case"""
        use_case_counts = {}
        for laptop in self.laptop_data:
            for use_case in laptop.use_cases:
                use_case_counts[use_case.value] = use_case_counts.get(use_case.value, 0) + 1
        
        fig = go.Figure(data=[
            go.Pie(
                labels=list(use_case_counts.keys()),
                values=list(use_case_counts.values()),
                hole=0.3,
                textinfo='label+percent',
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Laptop Distribution by Use Case",
            font=dict(size=12),
            height=400
        )
        
        chart_path = 'static/charts/use_case_distribution.html'
        fig.write_html(chart_path)
        return chart_path
    
    def create_brand_comparison_chart(self) -> str:
        """Create a brand comparison chart"""
        brand_data = {}
        for laptop in self.laptop_data:
            brand = laptop.name
            if brand not in brand_data:
                brand_data[brand] = {
                    'models': [],
                    'avg_performance': [],
                    'avg_price': [],
                    'count': 0
                }
            
            brand_data[brand]['models'].append(laptop.model)
            brand_data[brand]['avg_performance'].append(laptop.performance_score)
            
            price_range = laptop.price_range.replace('$', '').split('-')
            avg_price = (int(price_range[0].replace(',', '').strip()) + 
                         int(price_range[1].replace(',', '').strip())) / 2
            brand_data[brand]['avg_price'].append(avg_price)
            brand_data[brand]['count'] += 1
        
        # Calculate averages
        brands = []
        avg_performances = []
        avg_prices = []
        
        for brand, data in brand_data.items():
            brands.append(brand)
            avg_performances.append(np.mean(data['avg_performance']))
            avg_prices.append(np.mean(data['avg_price']))
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Average Performance Score', 'Average Price'),
            specs=[[{"type": "bar"}, {"type": "bar"}]]
        )
        
        fig.add_trace(
            go.Bar(x=brands, y=avg_performances, name="Performance"),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(x=brands, y=avg_prices, name="Price"),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="Brand Comparison - Performance and Price",
            font=dict(size=12),
            height=400,
            showlegend=False
        )
        
        chart_path = 'static/charts/brand_comparison.html'
        fig.write_html(chart_path)
        return chart_path
    
    def create_specification_heatmap(self) -> str:
        """Create a heatmap of laptop specifications"""
        # Create a specification matrix
        specs = ['performance_score', 'portability_score', 'value_score']
        models = [f"{laptop.name} {laptop.model}" for laptop in self.laptop_data]
        
        # Create matrix data
        matrix_data = []
        for laptop in self.laptop_data:
            matrix_data.append([
                laptop.performance_score,
                laptop.portability_score,
                laptop.value_score
            ])
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix_data,
            x=['Performance', 'Portability', 'Value'],
            y=models,
            colorscale='Blues',
            showscale=True,
            text=matrix_data,
            texttemplate="%{text}",
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title="Laptop Specification Heatmap",
            xaxis_title="Specifications",
            yaxis_title="Laptop Models",
            font=dict(size=12),
            height=600
        )
        
        chart_path = 'static/charts/specification_heatmap.html'
        fig.write_html(chart_path)
        return chart_path
    
    def create_market_segment_analysis(self) -> str:
        """Create market segment analysis chart"""
        segments = {
            'Budget': {'max_price': 1000, 'laptops': []},
            'Mid-Range': {'max_price': 2000, 'laptops': []},
            'Premium': {'max_price': 3000, 'laptops': []},
            'Ultra-Premium': {'max_price': 10000, 'laptops': []}
        }
        
        for laptop in self.laptop_data:
            price_range = laptop.price_range.replace('$', '').split('-')
            max_price = int(price_range[1].replace(',', '').strip())
            
            if max_price <= 1000:
                segments['Budget']['laptops'].append(laptop.model)
            elif max_price <= 2000:
                segments['Mid-Range']['laptops'].append(laptop.model)
            elif max_price <= 3000:
                segments['Premium']['laptops'].append(laptop.model)
            else:
                segments['Ultra-Premium']['laptops'].append(laptop.model)
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(segments.keys()),
                y=[len(seg['laptops']) for seg in segments.values()],
                text=[len(seg['laptops']) for seg in segments.values()],
                textposition='auto',
                marker=dict(color=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D'])
            )
        ])
        
        fig.update_layout(
            title="Market Segment Analysis",
            xaxis_title="Price Segment",
            yaxis_title="Number of Laptops",
            font=dict(size=12),
            height=400
        )
        
        chart_path = 'static/charts/market_segment_analysis.html'
        fig.write_html(chart_path)
        return chart_path
    
    def _get_price_score(self, price_range: str) -> int:
        """Convert price range to score (lower price = higher score)"""
        prices = price_range.replace('$', '').split('-')
        max_price = int(prices[1].replace(',', '').strip())
        
        if max_price <= 1000:
            return 90
        elif max_price <= 1500:
            return 75
        elif max_price <= 2000:
            return 60
        elif max_price <= 3000:
            return 40
        else:
            return 20
    
    def _get_battery_score(self, battery_life: str) -> int:
        """Convert battery life to score"""
        hours = int(battery_life.split()[0])
        
        if hours >= 15:
            return 90
        elif hours >= 12:
            return 75
        elif hours >= 10:
            return 60
        elif hours >= 8:
            return 45
        else:
            return 30
    
    def generate_all_charts(self) -> Dict[str, str]:
        """Generate all charts and return their paths"""
        charts = {
            'performance_radar': self.create_performance_radar_chart(),
            'price_distribution': self.create_price_distribution_chart(),
            'performance_vs_price': self.create_performance_vs_price_scatter(),
            'use_case_distribution': self.create_use_case_distribution(),
            'brand_comparison': self.create_brand_comparison_chart(),
            'specification_heatmap': self.create_specification_heatmap(),
            'market_segment_analysis': self.create_market_segment_analysis()
        }
        
        return charts
    
    def generate_analytics_summary(self) -> Dict[str, Any]:
        """Generate analytics summary for dashboard"""
        summary = {
            'total_laptops': len(self.laptop_data),
            'brands': len(set(laptop.name for laptop in self.laptop_data)),
            'avg_price': 0,
            'avg_performance': 0,
            'price_range': {'min': 10000, 'max': 0},
            'top_performer': '',
            'most_portable': '',
            'best_value': '',
            'use_case_distribution': {},
            'brand_distribution': {},
            'sales_summary': {}
        }
        
        prices = []
        for laptop in self.laptop_data:
            price_range = laptop.price_range.replace('$', '').split('-')
            max_price = int(price_range[1].replace(',', '').strip())
            min_price = int(price_range[0].replace(',', '').strip())
            
            prices.append((min_price + max_price) / 2)
            summary['price_range']['min'] = min(summary['price_range']['min'], min_price)
            summary['price_range']['max'] = max(summary['price_range']['max'], max_price)
        
        summary['avg_price'] = np.mean(prices)
        summary['avg_performance'] = np.mean([laptop.performance_score for laptop in self.laptop_data])
        
        # Find top performers
        top_perf = max(self.laptop_data, key=lambda x: x.performance_score)
        summary['top_performer'] = f"{top_perf.name} {top_perf.model}"
        
        most_portable = max(self.laptop_data, key=lambda x: x.portability_score)
        summary['most_portable'] = f"{most_portable.name} {most_portable.model}"
        
        best_value = max(self.laptop_data, key=lambda x: x.value_score)
        summary['best_value'] = f"{best_value.name} {best_value.model}"
        
        # Use case distribution
        for laptop in self.laptop_data:
            for use_case in laptop.use_cases:
                summary['use_case_distribution'][use_case.value] = summary['use_case_distribution'].get(use_case.value, 0) + 1
        
        # Brand distribution
        brand_counts = {}
        for laptop in self.laptop_data:
            brand_counts[laptop.name] = brand_counts.get(laptop.name, 0) + 1
        summary['brand_distribution'] = brand_counts
        
        # Sales summary
        total_sales = self.sales_df['sales'].sum()
        total_revenue = self.sales_df['revenue'].sum()
        best_selling_month = self.sales_df.groupby('month')['sales'].sum().idxmax()
        best_selling_brand = self.sales_df.groupby('brand')['sales'].sum().idxmax()
        
        summary['sales_summary'] = {
            'total_sales': int(total_sales),
            'total_revenue': int(total_revenue),
            'best_selling_month': best_selling_month,
            'best_selling_brand': best_selling_brand,
            'avg_monthly_sales': int(total_sales / 12),
            'growth_rate': '12.5%'  # Mock growth rate
        }
        
        return summary
    
    def generate_all_charts(self) -> Dict[str, str]:
        """Generate all charts and return their paths"""
        charts = {
            'sales_trend': self.create_sales_trend_chart(),
            'brand_sales_comparison': self.create_brand_sales_comparison(),
            'use_case_sales_trend': self.create_use_case_sales_trend(),
            'price_segment_sales': self.create_price_segment_sales(),
            'performance_radar': self.create_performance_radar_chart(),
            'price_distribution': self.create_price_distribution_chart(),
            'performance_vs_price': self.create_performance_vs_price_scatter(),
            'use_case_distribution': self.create_use_case_distribution(),
            'brand_comparison': self.create_brand_comparison_chart(),
            'specification_heatmap': self.create_specification_heatmap(),
            'market_segment_analysis': self.create_market_segment_analysis()
        }
        
        return charts
