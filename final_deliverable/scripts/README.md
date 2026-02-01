# CSD Dataset Analysis Scripts Setup

## Overview
This directory contains modular Python scripts for comprehensive analysis of the Saudi Arabian CSD (Carbonated Soft Drink) dataset.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation:**
   ```bash
   python -c "import pandas, numpy, matplotlib, seaborn; print('All dependencies installed successfully!')"
   ```

## Available Modules

### Core Analysis Modules

1. **`data_loader.py`** - Data loading and preprocessing
   - Excel file processing
   - Data cleaning and validation
   - Feature engineering
   - Dataset summary generation

2. **`eda_analysis.py`** - Exploratory Data Analysis
   - Descriptive statistics
   - Distribution analysis
   - Correlation analysis
   - Comprehensive insights generation

3. **`geographic_analysis.py`** - Geographic Intelligence
   - Regional performance analysis
   - Province-level deep dive
   - Precision area hotspot analysis
   - Seasonal geographic patterns

4. **`time_series_analysis.py`** - Temporal Analysis
   - Seasonal decomposition
   - Trend analysis
   - Ramadan impact assessment
   - Growth momentum tracking

5. **`strategic_insights.py`** - Strategic Intelligence
   - Distribution gap analysis
   - White space opportunities
   - Competitive vulnerability assessment
   - Emerging trend identification

## Usage Examples

### Basic Analysis Pipeline

```python
# Example usage
from data_loader import CSDDatasetLoader
from eda_analysis import CSDExploratoryAnalysis
from geographic_analysis import CSDGeographicAnalysis
from strategic_insights import CSDStrategicAnalysis

# 1. Load and prepare data
loader = CSDDatasetLoader()
loader.load_data()
loader.convert_to_long_format()
loader.clean_data()
loader.create_derived_features()

# 2. Run comprehensive analysis
df = loader.df_long

# 3. Exploratory analysis
eda = CSDExploratoryAnalysis(df)
insights = eda.generate_insights()

# 4. Geographic analysis
geo = CSDGeographicAnalysis(df)
geo_intelligence = geo.generate_geographic_intelligence()

# 5. Strategic analysis
strategic = CSDStrategicAnalysis(df)
recommendations = strategic.generate_strategic_recommendations()
```

### Individual Module Usage

```python
# Run specific analysis modules
from time_series_analysis import CSDTimeSeriesAnalysis

ts = CSDTimeSeriesAnalysis(df)
temporal_intelligence = ts.generate_temporal_intelligence()
```

## Data Requirements

The scripts expect the dataset in the following format:
- Excel file (.xlsx) with monthly sales data
- Columns for geographic hierarchy (Region, Province, Precision Area, Market)
- Product dimensions (Manufacturer, Brand, Flavor, Pack Type, Pack Size)
- Monthly sales columns with format 'MMMYY' (e.g., 'Jan24', 'Feb24')

## Output Features

Each module provides:
- **Console Output**: Detailed analysis results with formatted summaries
- **Return Values**: Structured data for further processing
- **Visualizations**: Charts and plots where applicable
- **Insights**: Actionable business intelligence

## Configuration

### File Paths
Default Excel file: `"DUMMY DATA FOR PRECISION AREAS.xlsx"`
Default sheet: `'Sheet6'`

Modify these parameters in the `CSDDatasetLoader` initialization:
```python
loader = CSDDatasetLoader(
    file_path="your_file.xlsx", 
    sheet_name="your_sheet_name"
)
```

### Customization Options

Each analysis class can be customized with:
- Specific time periods
- Geographic filters
- Product category focus
- Analysis parameters

## Error Handling

The modules include comprehensive error handling for:
- Missing data files
- Invalid data formats
- Insufficient data for analysis
- Calculation errors

## Performance Considerations

- Large datasets may require additional memory
- Complex analyses may take several minutes
- Consider using data sampling for exploratory work

## Integration

The modules are designed to work together:
1. Use `data_loader.py` for data preparation
2. Pass the processed DataFrame to analysis modules
3. Combine insights from multiple modules
4. Generate comprehensive reports

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **File Not Found**: Check file paths and permissions
3. **Memory Issues**: Use data sampling or increase available memory
4. **Data Format Issues**: Verify Excel file structure

### Support

For issues or questions:
1. Check the console output for error messages
2. Verify input data format matches expectations
3. Ensure all dependencies are properly installed

## Extensions

The modular design allows for:
- Additional analysis modules
- Custom visualization functions
- Integration with external databases
- Automated reporting pipelines

## Version History

- **v1.0**: Initial release with core analysis modules
- Compatible with Python 3.8+
- Supports pandas 1.5.0+ and related dependencies