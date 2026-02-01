# 🛠️ Dashboard Technical Specifications

## System Architecture

### 🏗️ High-Level Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend UI   │◄──►│   API Gateway   │◄──►│   Data Sources  │
│   (React.js)    │    │  (FastAPI)      │    │   (Excel/DB)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Cache Layer   │    │  Business Logic │    │  Processing    │
│   (Redis)       │    │   (Python)      │    │  (Pandas/NumPy) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 🔄 Data Flow Architecture
```
Excel Files → ETL Pipeline → Data Warehouse → API Layer → Frontend Dashboard
     │              │              │             │              │
     ▼              ▼              ▼             ▼              ▼
Daily Refresh   Data Validation   PostgreSQL    FastAPI      React.js
Real-time      Quality Checks   Analytics     RESTful      Interactive
Processing     Error Handling   Storage       Endpoints    Visualizations
```

---

## 🖥️ Frontend Technology Stack

### Core Technologies
```json
{
  "framework": "React.js 18+",
  "language": "TypeScript",
  "bundler": "Vite",
  "styling": "Tailwind CSS + Headless UI",
  "state_management": "Zustand + React Query",
  "routing": "React Router v6",
  "charts": "Plotly.js + D3.js",
  "maps": "Leaflet + Mapbox GL",
  "testing": "Vitest + React Testing Library"
}
```

### UI Component Library
```typescript
// Custom Component Structure
interface DashboardComponent {
  data: DataSource[];
  config: ChartConfig;
  loading: boolean;
  error: Error | null;
  filters: FilterState;
  onExport: () => void;
  onRefresh: () => void;
}
```

### Responsive Design System
```css
/* Breakpoint System */
@media (max-width: 640px)  { /* Mobile */ }
@media (min-width: 641px) and (max-width: 1024px) { /* Tablet */ }
@media (min-width: 1025px) and (max-width: 1440px) { /* Desktop */ }
@media (min-width: 1441px) { /* Large Desktop */ }
```

---

## 🔧 Backend Technology Stack

### Core Framework
```python
# FastAPI Application Structure
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="CSD Analytics API",
    description="Saudi Arabian CSD Market Intelligence API",
    version="1.0.0"
)

# Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Database Configuration
```sql
-- PostgreSQL Schema Design
CREATE TABLE sales_data (
    id SERIAL PRIMARY KEY,
    region VARCHAR(50) NOT NULL,
    province VARCHAR(50) NOT NULL,
    precision_area VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(50) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    pack_type VARCHAR(50) NOT NULL,
    pack_size VARCHAR(50) NOT NULL,
    sales_date DATE NOT NULL,
    sales_amount DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_region_date (region, sales_date),
    INDEX idx_brand (brand),
    INDEX idx_date (sales_date)
);
```

### Data Processing Pipeline
```python
# ETL Pipeline Structure
class CSDETLProcessor:
    def __init__(self):
        self.source_path = "DUMMY DATA FOR PRECISION AREAS.xlsx"
        self.db_connection = self._get_db_connection()
        
    def extract_data(self) -> pd.DataFrame:
        """Extract data from Excel files"""
        
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform and clean data"""
        
    def load_data(self, df: pd.DataFrame) -> bool:
        """Load processed data to database"""
        
    def run_pipeline(self) -> bool:
        """Execute complete ETL process"""
```

---

## 📊 Data Integration Specifications

### Excel File Processing
```python
# Excel Processing Configuration
EXCEL_CONFIG = {
    "file_path": "DUMMY DATA FOR PRECISION AREAS.xlsx",
    "sheet_name": "Sheet6",
    "monthly_columns_pattern": "'24",
    "id_columns": [
        "Region", "Province", "Precision Area", "MARKET",
        "KEY MANU  & KINZA", "BRAND", "CSD Flavor Segment",
        "REG/DIET", "PACK TYPE", "PACK SIZE", "ITEM"
    ]
}
```

### Data Validation Rules
```python
VALIDATION_RULES = {
    "required_fields": [
        "Region", "Province", "Precision Area", 
        "Manufacturer", "Brand", "Sales"
    ],
    "data_types": {
        "Sales": "numeric",
        "Date": "datetime",
        "Region": "categorical"
    },
    "business_rules": {
        "sales_min": 0,
        "sales_max": 10000000,
        "date_range": ("2024-01-01", "2024-12-31")
    }
}
```

### Real-time Data Integration
```python
# WebSocket Configuration for Real-time Updates
class RealtimeDataHandler:
    def __init__(self):
        self.connections: Set[WebSocket] = set()
        
    async def handle_connection(self, websocket: WebSocket):
        """Handle new WebSocket connections"""
        
    async def broadcast_updates(self, data: dict):
        """Broadcast data updates to all connected clients"""
        
    async def monitor_data_changes(self):
        """Monitor database for real-time changes"""
```

---

## 🚀 Performance Requirements

### Response Time Targets
```json
{
  "dashboard_load": "<2.0 seconds",
  "chart_rendering": "<1.5 seconds",
  "data_refresh": "<3.0 seconds",
  "filter_application": "<0.5 seconds",
  "export_generation": "<5.0 seconds",
  "api_response": "<500ms"
}
```

### Scalability Specifications
```json
{
  "concurrent_users": "100+",
  "data_volume": "100MB+ monthly growth",
  "api_requests": "1000+ per minute",
  "cpu_usage": "<70%",
  "memory_usage": "<80%",
  "storage_growth": "10% quarterly"
}
```

### Caching Strategy
```python
# Redis Caching Configuration
CACHE_CONFIG = {
    "static_data": {"ttl": 86400, "key_prefix": "static:"},
    "dynamic_data": {"ttl": 900, "key_prefix": "dynamic:"},
    "user_sessions": {"ttl": 3600, "key_prefix": "session:"},
    "api_responses": {"ttl": 300, "key_prefix": "api:"},
    "chart_data": {"ttl": 1800, "key_prefix": "chart:"}
}
```

---

## 🔒 Security Specifications

### Authentication & Authorization
```python
# JWT Authentication Setup
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityManager:
    def create_access_token(self, data: dict) -> str:
        """Create JWT access token"""
        
    def verify_token(self, token: str) -> dict:
        """Verify and decode JWT token"""
        
    def get_password_hash(self, password: str) -> str:
        """Hash password for storage"""
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
```

### Data Protection
```python
# Encryption Configuration
from cryptography.fernet import Fernet

ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

class DataProtection:
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        
    def mask_pii_data(self, data: dict) -> dict:
        """Mask personally identifiable information"""
```

### API Security
```python
# Rate Limiting and Security Headers
from fastapi import HTTPException, status
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

@app.get("/api/sales")
@limiter.limit("100/minute")
async def get_sales_data(request: Request):
    """API endpoint with rate limiting"""
```

---

## 📱 Mobile & Responsive Specifications

### Mobile Optimization
```css
/* Mobile-First Design */
.mobile-dashboard {
  /* Touch-friendly interactions */
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  
  /* Optimized for small screens */
  font-size: 14px;
  line-height: 1.4;
  padding: 8px;
}

.mobile-chart {
  /* Responsive chart sizing */
  width: 100%;
  height: 300px;
  max-width: 100vw;
}
```

### Progressive Web App (PWA) Features
```json
{
  "manifest": {
    "name": "CSD Analytics Dashboard",
    "short_name": "CSD Analytics",
    "start_url": "/dashboard",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#2E86AB",
    "icons": [
      {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
      {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}
    ]
  },
  "service_worker": {
    "cache_strategies": ["networkFirst", "cacheFirst"],
    "offline_support": true
  }
}
```

---

## 🔄 Deployment Architecture

### Container Configuration
```dockerfile
# Dockerfile for Frontend
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```dockerfile
# Dockerfile for Backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Infrastructure as Code
```yaml
# docker-compose.yml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
      
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - database
      - redis
    environment:
      - DATABASE_URL=postgresql://user:pass@database:5432/csd_db
      - REDIS_URL=redis://redis:6379
      
  database:
    image: postgres:15
    environment:
      - POSTGRES_DB=csd_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

---

## 📊 Monitoring & Observability

### Application Monitoring
```python
# Performance Monitoring Setup
import time
import logging
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logging.info(f"{func.__name__} executed in {execution_time:.2f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logging.error(f"{func.__name__} failed after {execution_time:.2f}s: {e}")
            raise
    return wrapper
```

### Health Checks
```python
# System Health Monitoring
@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": await check_database_health(),
            "redis": await check_redis_health(),
            "data_processing": await check_processing_health()
        }
    }
    return health_status
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy Dashboard
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      - name: Run tests
        run: pytest
        
  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: |
          # Deployment commands
```

---

*This technical specification provides the foundation for building a scalable, secure, and performant business intelligence dashboard for the Saudi Arabian CSD market.*