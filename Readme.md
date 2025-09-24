# 🍽 Local Food Wastage Management System

A comprehensive web application built with Streamlit for managing food waste reduction by connecting food providers with receivers. The system helps track food donations, manage claims, and analyze food distribution patterns to minimize waste in local communities.

## 🌟 Features

- **📊 Data Management**: View, add, update, and delete food listings
- **🏢 Provider & Receiver Management**: Track food providers (restaurants, supermarkets, etc.) and receivers (NGOs, shelters, charities, individuals) across different cities
- **📋 Claims Processing**: Handle food claims with comprehensive status tracking (Pending, Completed, Cancelled)
- **📈 Analytics & Reporting**: 15+ comprehensive analytical queries including:
  - Provider and receiver distribution by city
  - Food type and meal type analysis
  - Claims statistics and trends
  - Provider performance metrics
  - Expiry date monitoring
  - Daily claims patterns

## 🛠 Technology Stack

- **Frontend**: Streamlit (Interactive web interface)
- **Backend**: Python with SQLAlchemy ORM
- **Database**: MySQL
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Environment Management**: python-dotenv

## 📁 Project Structure

```
local_food_wastage_system/
├── app.py                    # Main Streamlit application
├── db_setup.py              # Database schema creation and setup
├── load_data.py             # CSV data loading utilities
├── queries.py               # Analytical queries and database functions
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in repo)
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
├── data/                   # Sample CSV data files
│   ├── providers_data.csv   # Food provider information
│   ├── receivers_data.csv   # Food receiver information
│   ├── food_listings_data.csv # Available food items
│   └── claims_data.csv      # Food claim records
├── utils/                  # Utility modules
│   ├── __pycache__/
│   └── db.py               # Database connection utilities
├── output_q*.csv           # Generated analytical query results (auto-generated)
├── __pycache__/            # Python cache files
└── video/                  # Demo videos (if any)
```

## ⚡ Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7+ or 8.0+
- Git

### 2. Clone & Setup

```bash
git clone <your-repository-url>
cd local_food_wastage_system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Configuration

1. Create a MySQL database for the project
2. Create a `.env` file in the root directory with your database credentials:

```env
DB_USER=your_mysql_username
DB_PASS=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=food_wastage
```

### 4. Initialize Database

```bash
# Set up database schema
python db_setup.py

# Load sample data
python load_data.py
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🗄️ Database Schema

### Core Tables

1. **providers**: Food providers (restaurants, supermarkets, grocery stores, catering services)
   - Provider_ID, Name, Type, Address, City, Contact

2. **receivers**: Food receivers (shelters, NGOs, individuals, charities)  
   - Receiver_ID, Name, Type, City, Contact

3. **food_listings**: Available food items with details
   - Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type

4. **claims**: Food claim requests and status tracking
   - Claim_ID, Food_ID, Receiver_ID, Status, Timestamp

### Key Relationships

- `food_listings.Provider_ID` → `providers.Provider_ID`
- `claims.Food_ID` → `food_listings.Food_ID`  
- `claims.Receiver_ID` → `receivers.Receiver_ID`

## 📱 Usage Guide

### Navigation Menu

- **📋 View Data**: Browse and filter existing food listings with provider details
- **➕ Add Food**: Create new food listings with comprehensive details
- **✏️ Update Food**: Modify existing food listings
- **🗑️ Delete Food**: Remove food listings from the system
- **📊 Analysis & Queries**: Run 15+ predefined analytical queries

### 📊 Available Analytics

1. **Q1**: Provider and receiver distribution by city
2. **Q2**: Food provider type analysis  
3. **Q3**: Provider contact information by city
4. **Q4**: Top receivers by claims count
5. **Q5**: Total food quantity available
6. **Q6**: City with highest food listings
7. **Q7**: Most common food types
8. **Q8**: Food claims by item type
9. **Q9**: Provider with most successful claims
10. **Q10**: Claims distribution by status
11. **Q11**: Average quantity per receiver
12. **Q12**: Most claimed meal types
13. **Q13**: Total donations by provider
14. **Q14**: Items near expiry (next 3 days)
15. **Q15**: Daily claims trends (last 30 days)

All query results can be downloaded as CSV files for further analysis.

## 📊 Sample Data

The system includes sample data with:
- **1000 food providers** across various types and cities
- **900+ food receivers** including shelters, NGOs, charities, and individuals
- **1000+ food listings** with different food types and meal categories
- **1000+ claims** with various statuses and timestamps

## 🔧 Development

### Adding New Queries

1. Add your query to the `queries` dictionary in [`queries.py`](queries.py)
2. Follow the format: `"query_id": ("Description", "SQL_QUERY", optional_params)`
3. The system will automatically generate downloadable CSV outputs

### Extending the Database

1. Modify schema in [`db_setup.py`](db_setup.py)
2. Update data loading logic in [`load_data.py`](load_data.py)
3. Extend the Streamlit interface in [`app.py`](app.py)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -am 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Environment Variables

Required environment variables in `.env` file:

```env
DB_USER=your_database_username
DB_PASS=your_database_password
DB_HOST=your_database_host (default: localhost)
DB_PORT=your_database_port (default: 3306)
DB_NAME=your_database_name (default: food_wastage)
```

## 🚀 Deployment

For production deployment, consider:

1. **Database**: Use a managed MySQL service (AWS RDS, Google Cloud SQL)
2. **Hosting**: Deploy on Streamlit Cloud, Heroku, or AWS
3. **Security**: Use environment-specific `.env` files
4. **Monitoring**: Implement logging and error tracking

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Check existing documentation
- Review the code comments for implementation details

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for rapid web development
- Powered by [SQLAlchemy](https://www.sqlalchemy.org/) for robust database operations  
- Data processing with [Pandas](https://pandas.pydata.org/)
- Visualizations with [Plotly](https://plotly.com/)

---

**Made with ❤️ for reducing food waste and helping communities**