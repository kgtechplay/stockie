# 📈 Stockie - Streamlit Multi-Page Application

A comprehensive stock analysis dashboard built with Streamlit, featuring real-time data, interactive charts, and multi-page navigation.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Copy the `.env` file and add your credentials:
- Alpha Vantage API key
- Supabase database credentials

### 3. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
Stockie/
├── app.py                          # Main Streamlit application
├── pages/                          # Multi-page navigation
│   ├── 1_📊_Dashboard.py          # Stock analytics dashboard
│   ├── 2_🔍_Stock_Search.py       # Stock search and analysis
│   ├── 3_📋_Data_Import.py        # Data import and management
│   └── 4_⚙️_Settings.py           # Application settings
├── utils/                          # Shared utilities
│   ├── __init__.py
│   ├── config.py                   # Streamlit configuration
│   └── auth.py                     # Environment validation
├── assets/                         # Static assets
│   ├── css/
│   │   └── custom.css             # Custom styling
│   ├── images/                     # Images and icons
│   └── README.md                   # Assets documentation
├── .streamlit/                     # Streamlit configuration
│   └── config.toml                # App configuration
├── .env                           # Environment variables
├── requirements.txt               # Python dependencies
└── README_STREAMLIT.md           # This file
```

## 🎯 Features

### 📊 Dashboard
- Interactive stock price charts
- Performance analytics
- Volume analysis
- Multi-stock comparison
- Downloadable data

### 🔍 Stock Search
- Company name and ticker search
- Real-time stock information
- Detailed stock analysis
- Popular stocks showcase

### 📋 Data Import
- **Auto Import**: Fetch data via Alpha Vantage API
- **File Upload**: Import CSV files
- **Manual Entry**: Add individual data points
- Data validation and management

### ⚙️ Settings
- Environment configuration status
- API and database settings
- Application preferences
- Performance tuning options

## 🔧 Configuration

### Environment Variables
Required in `.env` file:
```env
ALPHA_VANTAGE_API_KEY=your_api_key
supabaseURL=your_supabase_url
supabaseKey=your_supabase_anon_key
supabaseServiceKey=your_supabase_service_key
SUPABASE_DB_URL=your_database_url
```

### Streamlit Configuration
Settings in `.streamlit/config.toml`:
- Server configuration
- Theme settings
- Performance options
- Security settings

## 🎨 Customization

### Adding New Pages
1. Create a new file in `pages/` directory
2. Follow the naming convention: `N_📋_Page_Name.py`
3. Import utilities from `utils/` directory
4. Use consistent page structure

### Custom Styling
- Edit `assets/css/custom.css` for global styles
- Use Streamlit's theming system
- Follow the existing design patterns

### Adding Features
1. Create utility functions in `utils/`
2. Add new components to existing pages
3. Update navigation in `app.py` if needed
4. Test with different data sources

## 📊 Data Integration

### Existing Python Scripts
The app integrates with existing Python scripts:
- `import_stock.py` - Data fetching
- `get_ticker.py` - Company lookup
- `supabase_connect.py` - Database connection
- `update_stock_table.py` - Data updates

### Database Schema
Expects Supabase tables:
- `Company_ticker_all` - Company information
- `stock_data` - Historical stock data

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py --server.port 8501
```

### Production Deployment
1. **Streamlit Cloud**: Connect GitHub repository
2. **Heroku**: Add `setup.sh` and `Procfile`
3. **Docker**: Create Dockerfile with Streamlit
4. **AWS/GCP**: Use container services

### Environment Setup
Ensure all environment variables are configured in your deployment platform.

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all packages are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**: Check `.env` file configuration
   - Verify all required variables are set
   - Check for typos in variable names

3. **Database Connection**: Validate Supabase credentials
   - Test with `test_db_conn.py`
   - Check network connectivity

4. **API Limits**: Monitor Alpha Vantage usage
   - Free tier: 5 calls/minute
   - Implement proper caching

### Debug Mode
Enable debug mode in Settings page for detailed error information.

## 📈 Performance Tips

1. **Caching**: Enable Streamlit caching for data operations
2. **Data Limits**: Limit large dataset queries
3. **API Usage**: Implement efficient API call patterns
4. **Browser Cache**: Use appropriate cache headers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is part of the Stockie stock analysis tool.

---

**Happy Analyzing! 📈✨**

