# Laptop Recommendation System - Web Application

A full-stack web application that provides intelligent laptop recommendations with a modern, responsive user interface and powerful backend API.

## 🚀 Features

### Frontend
- **Modern UI**: Clean, responsive design using Tailwind CSS
- **Interactive Interface**: Real-time recommendations with smooth animations
- **Mobile Responsive**: Works perfectly on all device sizes
- **User-Friendly Forms**: Intuitive input for use case, budget, and preferences
- **Visual Results**: Beautiful cards displaying laptop recommendations
- **Comparison Summary**: At-a-glance comparison of top picks
- **JSON Export**: Copy-ready JSON output for developers

### Backend API
- **RESTful Endpoints**: Clean API design for recommendations
- **Smart Algorithm**: Weighted scoring based on user requirements
- **Multiple Use Cases**: Gaming, Business, Student, Creative, Programming, General
- **Budget Filtering**: Optional price range constraints
- **Portability Options**: Prioritize lightweight laptops
- **CORS Support**: Full cross-origin resource sharing

## 🏗️ Architecture

```
Frontend (HTML/CSS/JS) ←→ Flask Backend API ←→ Laptop Database
       ↓                        ↓                      ↓
   Tailwind CSS           Recommendation Engine    8 Laptop Models
   Font Awesome           Scoring Algorithm        Detailed Specs
   Vanilla JS            JSON API Endpoints       Price Ranges
```

## 📋 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open Your Browser
Navigate to `http://localhost:5000`

## 🎯 How to Use

1. **Select Your Use Case**: Choose from Gaming, Business, Student, Creative, Programming, or General
2. **Set Your Budget** (Optional): Enter maximum price in USD
3. **Prioritize Portability** (Optional): Check if you need a lightweight laptop
4. **Get Recommendations**: Click the button to see your personalized recommendations
5. **Review Results**: Browse through the top 3-5 laptop recommendations
6. **Compare Models**: View the comparison summary
7. **Export Data**: Copy the JSON output for integration

## 🔧 API Endpoints

### GET `/api/use-cases`
Returns available use cases:
```json
["gaming", "business", "student", "creative", "programming", "general"]
```

### POST `/api/recommend`
Get personalized recommendations:
```json
{
  "use_case": "gaming",
  "max_price": 1500,
  "prioritize_portability": false
}
```

Response:
```json
{
  "use_case": "gaming",
  "recommendations": [
    {
      "rank": 1,
      "name": "ASUS",
      "model": "ROG Strix G15",
      "specs": {...},
      "price_range": "$1,200-$1,500",
      "pros": [...],
      "cons": [...],
      "fit_explanation": "..."
    }
  ],
  "comparison_summary": {
    "best_performance": "ROG Strix G15",
    "most_portable": "MacBook Air M2",
    "best_value": "Swift 3",
    "price_range_comparison": {...}
  }
}
```

### GET `/api/laptops`
Get all laptop data:
```json
[
  {
    "name": "Dell",
    "model": "XPS 15",
    "processor": "Intel Core i7-13700H",
    "ram": "16GB DDR5",
    "storage": "512GB SSD",
    "graphics": "NVIDIA RTX 4050",
    "display": "15.6\" FHD+ (1920x1200)",
    "battery_life": "8 hours",
    "weight": "4.2 lbs",
    "price_range": "$1,500-$2,000",
    "pros": [...],
    "cons": [...],
    "use_cases": ["business", "creative", "programming"],
    "performance_score": 85,
    "portability_score": 75,
    "value_score": 80
  }
]
```

## 🎨 UI Components

### Recommendation Cards
- **Rank Badge**: Clear visual hierarchy
- **Laptop Details**: Name, model, price
- **Performance Indicators**: Visual scores and badges
- **Specifications**: Complete hardware specs
- **Pros & Cons**: Balanced analysis
- **Fit Explanation**: Personalized reasoning

### Comparison Summary
- **Best Performance**: Top-performing model
- **Most Portable**: Lightest option
- **Best Value**: Best price-to-performance ratio
- **Price Comparison**: Side-by-side pricing

### Interactive Elements
- **Loading States**: Smooth transitions
- **Error Handling**: User-friendly error messages
- **Copy to Clipboard**: One-click JSON export
- **Responsive Grid**: Adapts to screen size
- **Hover Effects**: Enhanced interactivity

## 📊 Laptop Database

The system includes 8 carefully selected laptop models:

| Model | Use Cases | Price Range | Performance |
|-------|-----------|-------------|-------------|
| Dell XPS 15 | Business, Creative, Programming | $1,500-$2,000 | 85/100 |
| Apple MacBook Air M2 | Student, Business, General | $1,100-$1,400 | 75/100 |
| Lenovo ThinkPad X1 Carbon | Business, Student, Programming | $1,600-$2,200 | 70/100 |
| ASUS ROG Strix G15 | Gaming, Programming | $1,200-$1,500 | 90/100 |
| HP Spectre x360 14 | Creative, Business, Student | $1,300-$1,700 | 75/100 |
| Acer Swift 3 | Student, General, Business | $700-$900 | 65/100 |
| Razer Blade 15 | Gaming, Creative, Programming | $2,500-$3,000 | 95/100 |
| Microsoft Surface Laptop 5 | Business, Student, Creative | $1,600-$2,000 | 70/100 |

## 🧠 Recommendation Algorithm

The system uses a sophisticated scoring algorithm:

### Base Scoring
- **Use Case Match**: +30 points for direct compatibility
- **Performance Score**: Weighted 20-50% based on use case
- **Portability Score**: Weighted 20-40% based on use case
- **Value Score**: Weighted 20-50% based on use case

### Use Case Weights
- **Gaming**: Performance 50%, Portability 20%
- **Business**: Performance 30%, Portability 40%, Value 30%
- **Student**: Performance 30%, Portability 40%, Value 50%
- **Creative**: Performance 40%, Portability 20%, Value 20%
- **Programming**: Performance 40%, Portability 30%, Value 20%
- **General**: Performance 30%, Portability 30%, Value 40%

### Portability Bonus
- Additional 20% weight if prioritized by user

## 🔧 Technical Stack

### Backend
- **Flask**: Lightweight Python web framework
- **Flask-CORS**: Cross-origin resource sharing
- **Python 3.7+**: Core programming language

### Frontend
- **HTML5**: Semantic markup
- **Tailwind CSS**: Utility-first CSS framework
- **Vanilla JavaScript**: No framework dependencies
- **Font Awesome**: Icon library

### Development
- **Responsive Design**: Mobile-first approach
- **REST API**: Clean endpoint design
- **JSON Format**: Standard data interchange
- **Error Handling**: Comprehensive error management

## 📁 Project Structure

```
Recommendation engine/
├── app.py                    # Flask backend application
├── requirements.txt          # Python dependencies
├── README_WEB.md            # Web app documentation
├── templates/
│   └── index.html           # Frontend HTML template
├── laptop_recommender.py    # Original CLI version
├── example_usage.py         # CLI examples
└── README.md               # CLI documentation
```

## 🚀 Deployment Options

### Local Development
```bash
python app.py
# Runs on http://localhost:5000
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🎯 Use Case Examples

### Gaming Setup
- **Use Case**: Gaming
- **Budget**: $1500
- **Portability**: Not prioritized
- **Result**: ASUS ROG Strix G15, Razer Blade 15

### Student Setup
- **Use Case**: Student
- **Budget**: $1000
- **Portability**: Prioritized
- **Result**: Acer Swift 3, MacBook Air M2

### Business Setup
- **Use Case**: Business
- **Budget**: $2000
- **Portability**: Prioritized
- **Result**: ThinkPad X1 Carbon, Surface Laptop 5

## 🔮 Future Enhancements

- **User Accounts**: Save preferences and history
- **Real-time Prices**: Integration with price APIs
- **Reviews Integration**: User ratings and reviews
- **More Laptops**: Expanded database
- **Machine Learning**: Improved recommendation accuracy
- **Mobile App**: Native mobile applications
- **Comparison Charts**: Visual performance graphs
- **Email Notifications**: Price drop alerts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

---

**🎉 Enjoy your personalized laptop recommendations!**
