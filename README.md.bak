# Management Tools Analysis Dashboard

An interactive Dash application for analyzing management tools data with AI-powered insights. This dashboard provides comprehensive statistical analysis, bilingual support, and real-time data visualization for management research.

## 🎯 System Overview

```mermaid
graph LR
    A[User Interface] --> B[Dash Application]
    B --> C[Data Sources]
    B --> D[Analysis Engine]
    B --> E[AI Services]
    B --> F[Database Layer]
    
    C --> C1[Google Trends]
    C --> C2[Google Books]
    C --> C3[Bain Survey]
    C --> C4[Crossref]
    
    D --> D1[Statistical Analysis]
    D --> D2[Time Series]
    D --> D3[PCA Analysis]
    D --> D4[Correlation]
    
    E --> E1[Key Findings]
    E --> E2[Data Insights]
    E --> E3[Recommendations]
    
    F --> F1[SQLite Database]
    F --> F2[Cache Management]
    F --> F3[Metadata Storage]
```

## 🏗️ Architecture Flow

```mermaid
flowchart TB
    subgraph "Data Layer"
        A1[CSV Files] --> A2[Database Manager]
        A2 --> A3[SQLite DB]
    end
    
    subgraph "Processing Layer"
        B1[Data Aggregator] --> B2[Statistical Engine]
        B2 --> B3[AI Service]
    end
    
    subgraph "Presentation Layer"
        C1[Dash Components] --> C2[Interactive Charts]
        C2 --> C3[User Interface]
    end
    
    A3 --> B1
    B3 --> C1
```

## 🌟 Features

### Core Functionality
- **Interactive Data Visualization**: Multi-source data analysis with real-time updates
- **Bilingual Support**: Complete Spanish/English language switching
- **AI-Powered Insights**: Automated key findings generation using multiple AI services
- **Advanced Statistical Analysis**: PCA, regression, time series, Fourier analysis
- **Responsive Design**: Mobile-friendly interface with Bootstrap components

### Data Sources
- **Google Trends**: Real-time search interest data
- **Google Books Ngrams**: Historical book publication frequency
- **Bain Management Tools Survey**: Usage and satisfaction metrics
- **Crossref**: Academic publication and citation data

### Analysis Tools
- **Temporal Analysis**: 2D and 3D time series visualization
- **Seasonal Decomposition**: Trend and seasonal pattern analysis
- **Correlation Analysis**: Heatmap visualization of relationships
- **Principal Component Analysis**: Dimension reduction and pattern discovery
- **Regression Analysis**: Linear and non-linear modeling
- **Fourier Analysis**: Frequency domain analysis and periodograms

## 🧠 Concept Map

```mermaid
mindmap
  root((Management Tools Analysis))
    Data Sources
      Google Trends
        Search Interest
        Regional Data
        Time Series
      Google Books
        Ngrams Analysis
        Historical Trends
        Publication Frequency
      Bain Survey
        Usage Metrics
        Satisfaction Scores
        Industry Benchmarks
      Crossref
        Academic Citations
        Publication Impact
        Research Trends
    Analysis Methods
      Statistical Analysis
        Descriptive Stats
        Hypothesis Testing
        Confidence Intervals
      Time Series
        Trend Analysis
        Seasonal Decomposition
        Forecasting
      Multivariate
        PCA
        Factor Analysis
        Cluster Analysis
      Frequency Domain
        Fourier Transform
        Periodograms
        Spectral Analysis
    AI Integration
      Key Findings
        Pattern Recognition
        Anomaly Detection
        Insight Generation
      Natural Language
        Report Generation
        Summary Creation
        Recommendation Engine
    User Interface
      Interactive Charts
        2D Visualizations
        3D Plots
        Heatmaps
      Controls
        Tool Selection
        Source Filtering
        Time Range
        Language Switch
      Export Options
        Data Downloads
        Chart Images
        Report Generation

```

## 🔄 Data Processing Pipeline

```mermaid
flowchart TD
    A[Raw Data Sources] --> B[Data Validation]
    B --> C[Data Cleaning]
    C --> D[Normalization]
    D --> E[Interpolation]
    E --> F[Database Storage]
    
    F --> G[User Request]
    G --> H[Data Retrieval]
    H --> I[Statistical Analysis]
    I --> J[Visualization]
    J --> K[User Display]
    
    subgraph "AI Processing"
        L[Data Aggregation] --> M[Pattern Analysis]
        M --> N[Insight Generation]
        N --> O[Report Creation]
    end
    
    I --> L
    O --> K
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- `uv` package manager (recommended) or `pip`
- Git

### Installation Process Flow

```mermaid
flowchart TD
    A[Clone Repository] --> B[Choose Installation Method]
    B --> C[UV Method]
    B --> D[Pip Method]
    B --> E[Script Method]
    
    C --> F[uv sync]
    D --> G[pip install -r requirements.txt]
    E --> H[./run_dashboard.sh]
    
    F --> I[Run Application]
    G --> I
    H --> I
    
    I --> J[Access Dashboard]
    J --> K[http://127.0.0.1:8050]
```

### Installation

#### Method 1: Using UV (Recommended)
```bash
# Clone the repository
git clone https://github.com/Wise-Connex/management-tools-analysis-dashboard.git
cd management-tools-analysis-dashboard

# Navigate to dashboard app
cd dashboard_app

# Install dependencies
uv sync

# Run the application
uv run python app.py
```

**⚠️ IMPORTANT: Always use `uv run python` to ensure environment variables and dependencies are properly loaded.**

#### Method 2: Using Pip
```bash
# Clone the repository
git clone https://github.com/Wise-Connex/management-tools-analysis-dashboard.git
cd management-tools-analysis-dashboard

# Navigate to dashboard app
cd dashboard_app

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

#### Method 3: Using Convenience Script
```bash
# Clone and run from project root
git clone https://github.com/Wise-Connex/management-tools-analysis-dashboard.git
cd management-tools-analysis-dashboard
./run_dashboard.sh
```

### Access the Application

Open your web browser and navigate to:
- **Local**: http://127.0.0.1:8050
- **Network**: http://your-local-ip:8050

## 🔑 API Configuration

### Groq API Key Setup

The dashboard uses Groq API for AI-powered key findings generation. To enable this feature:

**⚠️ IMPORTANT: Always use `uv run python` commands to ensure the python-dotenv package loads your API key from the .env file.**

1. **Get your Groq API key** from [Groq Console](https://console.groq.com/)
2. **Create .env file** in the project root:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Add your Groq API key
   echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
   ```

3. **Verify API key loading**:
   ```bash
   # Check if key is loaded
   python3 -c "import os; print('API Key loaded:', 'GROQ_API_KEY' in os.environ)"
   ```

### Key Findings Database-First Architecture

The dashboard implements a **database-first strategy** for AI analysis:

- **Pre-computed Database**: 1,302 tool-source-language combinations stored in SQLite
- **Performance**: Sub-2ms query time vs 5-15s live AI generation
- **Fallback**: Live AI generation only for missing combinations
- **Coverage**: All 21 management tools × 5 data sources × 2 languages

```mermaid
flowchart TD
    A[User Request] --> B{Check Database}
    B -->|Found| C[Return Cached Analysis]
    B -->|Not Found| D[Generate Live AI]
    C --> E[Display Results]
    D --> F[Store in Database]
    F --> E
    
    style C fill:#e8f5e8
    style D fill:#fff3e0
```

### Environment Variables

Key environment variables for AI services:

```bash
# Required for AI analysis
GROQ_API_KEY=your_groq_api_key_here

# Optional fallback service
OPENROUTER_API_KEY=your_openrouter_key_here

# Database configuration
DATABASE_PATH=/path/to/precomputed_findings.db
```

### Database-First Benefits

- **Speed**: 5,213x faster than live AI queries
- **Cost**: Eliminates API costs for cached analyses
- **Reliability**: No dependency on external services for cached data
- **Consistency**: Identical results across all requests
- **Scalability**: Unlimited concurrent users with database backend

## 📊 Usage Guide

### User Workflow Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Dashboard UI
    participant DB as Database
    participant AI as AI Service
    participant Viz as Visualization Engine
    
    U->>UI: Select Management Tool
    UI->>DB: Query Available Data
    DB-->>UI: Return Data Sources
    UI->>U: Display Source Options
    
    U->>UI: Choose Data Sources
    U->>UI: Configure Analysis Parameters
    UI->>DB: Retrieve Filtered Data
    DB-->>UI: Return Dataset
    
    U->>UI: Request Analysis Type
    UI->>Viz: Generate Visualizations
    Viz-->>UI: Return Charts
    
    U->>UI: Request AI Insights
    UI->>AI: Send Data for Analysis
    AI-->>UI: Return Key Findings
    UI->>U: Display Results
```

### Basic Workflow

1. **Select a Management Tool**: Choose from dropdown menu (e.g., "Benchmarking", "Calidad Total", "Cuadro de Mando Integral")
2. **Choose Data Sources**: Select which data sources to include in analysis
3. **Configure Analysis**: 
   - Select time range (5, 10, 15, 20 years or custom)
   - Choose data frequency (monthly/annual)
   - Configure visualization options
4. **View Results**: Explore different analysis tabs:
   - **Temporal Analysis**: Time series plots and trends
   - **Statistical Analysis**: Correlations, PCA, regression
   - **AI Insights**: Automated key findings and recommendations
   - **Data Table**: Raw data export and filtering

### Analysis Types Flowchart

```mermaid
flowchart LR
    A[Data Selection] --> B{Analysis Type}
    
    B -->|Temporal| C[Time Series Analysis]
    C --> C1[2D Line Charts]
    C --> C2[3D Surface Plots]
    C --> C3[Trend Analysis]
    
    B -->|Statistical| D[Statistical Methods]
    D --> D1[Correlation Matrix]
    D --> D2[PCA Analysis]
    D --> D3[Regression Models]
    
    B -->|Frequency| E[Fourier Analysis]
    E --> E1[Periodograms]
    E --> E2[Spectral Density]
    E --> E3[Frequency Components]
    
    B -->|AI Insights| F[AI Processing]
    F --> F1[Pattern Recognition]
    F --> F2[Anomaly Detection]
    F --> F3[Recommendation Engine]
    
    C1 --> G[Visualization Dashboard]
    C2 --> G
    C3 --> G
    D1 --> G
    D2 --> G
    D3 --> G
    E1 --> G
    E2 --> G
    E3 --> G
    F1 --> G
    F2 --> G
    F3 --> G
```

### Advanced Features

#### AI-Powered Key Findings
- Click the "🔍 Generate Key Findings" button for AI analysis
- Supports multiple AI providers (Groq, OpenRouter)
- Provides actionable insights based on data patterns
- Includes confidence scores and source attribution

#### Data Export
- Export charts as PNG/SVG
- Download data as CSV
- Generate comprehensive reports

#### Custom Configuration
- Environment-based configuration
- Docker deployment support
- Custom interpolation profiles
- Database backup and restore

## 🛠️ Configuration

### Configuration Architecture

```mermaid
graph LR
    A[Environment Variables] --> D[Configuration Manager]
    B[JSON Config Files] --> D
    C[Default Values] --> D
    
    D --> E[Database Config]
    D --> F[Server Config]
    D --> G[Path Config]
    D --> H[AI Service Config]
    
    E --> I[SQLite Settings]
    E --> J[Connection Pool]
    
    F --> K[Host/Port]
    F --> L[Debug Mode]
    
    G --> M[Data Sources]
    G --> N[Asset Paths]
    
    H --> O[API Keys]
    H --> P[Service URLs]
```

### Environment Variables
Create a `.env` file in project root:

```bash
# Database Configuration
DASHBOARD_DATABASE_PATH=dashboard_app/data.db

# Server Configuration  
DASHBOARD_HOST=127.0.0.1
DASHBOARD_PORT=8050
DASHBOARD_DEBUG=true

# AI Services (Optional)
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Data Paths
DASHBOARD_DATA_SOURCES=dbase
DASHBOARD_CONFIG_DIR=config
```

### Configuration Files
The application uses JSON configuration files in `config/` directory:

- `database.json`: Database schema and connection settings
- `server.json`: Server and deployment configuration  
- `paths.json`: File paths and directory structure

### Configuration Priority

```mermaid
flowchart LR
    A[Default Values] --> B[JSON Config Files]
    B --> C[Environment Variables]
    C --> D[Runtime Configuration]
    
    style A fill:#f9f9f9
    style B fill:#e3f2fd
    style C fill:#fff3e0
    style D fill:#e8f5e8
```

## 🐳 Docker Deployment

### Build and Run
```bash
# Build the Docker image
docker build -t management-tools-dashboard .

# Run the container
docker run -p 8050:8050 -v $(pwd)/data:/app/data management-tools-dashboard
```

### Docker Compose
```bash
# Using docker-compose
docker-compose up -d
```

## 📁 Project Structure

```
management-tools-analysis-dashboard/
├── dashboard_app/                 # Main application directory
│   ├── app.py                   # Dash application entry point
│   ├── tools.py                 # Tool definitions and mappings
│   ├── translations.py           # Bilingual support
│   ├── config.py                # Configuration management
│   ├── database.py              # Database operations
│   ├── key_findings/            # AI analysis modules
│   │   ├── ai_service.py        # AI service integration
│   │   ├── database_manager.py  # Findings database
│   │   └── key_findings_service.py # Analysis service
│   ├── assets/                  # Static assets (images, icons)
│   ├── data/                    # SQLite databases:
│   ├── requirements.txt          # Python dependencies
│   └── pyproject.toml          # UV project configuration
├── config/                      # Configuration files
├── dbase/                       # Data source files
├── run_dashboard.sh            # Convenience script
├── AGENTS.md                   # AI agent guidelines
└── README.md                   # This file
```

## 🔧 Development

### Code Style
- Follow PEP 8 for Python code formatting
- Use type hints for all functions
- Implement comprehensive error handling
- Write docstrings for all public methods
- See `AGENTS.md` for detailed coding guidelines

### Testing
```bash
# Run tests (when implemented)
python -m pytest tests/

# Test application manually
cd dashboard_app && python app.py
```

### Code Quality Tools
```bash
# Install development dependencies
uv sync --dev

# Run linting (when configured)
ruff check .
black .

# Type checking (when configured)
mypy .
```

## 📚 API Reference

### Database Manager
```python
from database import get_database_manager

db = get_database_manager()
data, sources = db.get_data_for_keyword("Benchmarking", [1, 2, 3])
```

### Configuration
```python
from config import get_config

config = get_config()
db_path = config.database_path
server_config = config.get_server_config()
```

### Translations
```python
from translations import get_text

text = get_text('select_tool', 'en')  # English
text = get_text('select_tool', 'es')  # Spanish
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m "Add feature description"`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

### Development Guidelines
- Follow the coding standards in `AGENTS.md`
- Add tests for new features
- Update documentation as needed
- Ensure all existing tests pass
- Use descriptive commit messages

## 🐛 Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
uv sync  # or pip install -r requirements.txt

# Check database permissions
ls -la dashboard_app/data.db
```

#### Database Connection Issues
```bash
# Recreate database schema
cd dashboard_app
python -c "from database import get_database_manager; get_database_manager().create_schema()"
```

#### AI Services Not Working
```bash
# Check API keys
echo $GROQ_API_KEY
echo $OPENROUTER_API_KEY

# Verify .env file exists
ls -la .env

# Test API key loading
python3 -c "import os; print('GROQ_API_KEY loaded:', 'GROQ_API_KEY' in os.environ)"

# Check database-first mode (works without API key)
python3 -c "
from database_implementation.precomputed_findings_db import get_precomputed_db_manager
db = get_precomputed_db_manager()
stats = db.get_statistics()
print('Database combinations:', stats.get('total_combinations', 0))
"
```

#### Port Already in Use
```bash
# Kill existing process
lsof -ti:8050 | xargs kill -9

# Or use different port
DASHBOARD_PORT=8051 python app.py
```

### Performance Optimization

- Use SSD storage for databases
- Increase memory allocation for large datasets
- Enable database WAL mode for better concurrency
- Use Redis for caching in production

## 📄 License

This project is part of doctoral research on management tools analysis. See LICENSE file for details.

## 🙏 Acknowledgments

- **Principal Investigator**: Diomar Añez (ORCID: 0000-0002-7925-5078)
- **Academic Tutor**: Dra. Elizabeth Pereira (ULAC)
- **Institution**: Solidum Consulting / Wise Connex
- **Data Sources**: Google Trends, Google Books, Bain & Company, Crossref

## 📞 Support

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: See `AGENTS.md` for development guidelines
- **Data**: Available through Harvard Dataverse and NLM Dataset Catalog

## 🔗 Related Links

- **Harvard Dataverse**: [Management Fads Dataset](https://dataverse.harvard.edu/dataverse/management-fads)
- **NLM Publication**: [Dataset Catalog](https://datasetcatalog.nlm.nih.gov/searchResults?filters=agent%3AAnez%252C%2520Diomar)
- **Zenodo**: [Research Data](https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22Anez%2C%20Diomar%22)
- **OpenAIRE**: [Research Output](https://explore.openaire.eu/search/advanced/research-outcomes?f0=resultauthor&fv0=Diomar%2520Anez)
- **GitHub Reports**: [Analysis Reports](https://github.com/Wise-Connex/Management-Tools-Analysis/tree/main/Informes)

---

**© 2024-2025 Diomar Añez - Dimar Añez. All rights reserved.**
