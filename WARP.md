# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Fin-alpha is a **Stock Risk Analyzer** desktop application built with Python using the Kivy framework. It provides real-time stock risk analysis with beautiful animated UI components, fetching data from Yahoo Finance and calculating comprehensive risk metrics.

## Core Architecture

The application follows a **modular architecture** with clear separation of concerns:

### Main Components

- **`main.py`** - Application orchestrator and entry point
  - Contains `StockRiskApp` class that coordinates all modules
  - Handles application lifecycle (start, pause, resume, stop)
  - Manages error handling and user input validation
  - Coordinates between UI and analysis components

- **`risk.py`** - Financial analysis engine
  - `StockRiskAnalyzer` class performs all risk calculations
  - `RiskMetrics` dataclass structures analysis results
  - Calculates volatility, VaR, max drawdown, Sharpe ratio
  - Integrates with Yahoo Finance API via yfinance

- **`ui.py`** - UI components and styling
  - Custom widget classes with modern styling
  - `StockAnalyzerLayout` - main application layout
  - `ModernButton`, `ModernTextInput` - styled components
  - `ScrollableResultLabel` - formatted results display
  - Responsive design with markup support

- **`background.py`** - Animated background system
  - `BeautifulWaveWidget` - multi-layer wave animations
  - `SimpleWaveWidget` - performance-optimized single wave
  - `BackgroundWidget` - gradient background management
  - Real-time 60fps wave animations using Kivy graphics

### Key Design Patterns

1. **Separation of Concerns**: Each module has a distinct responsibility
2. **Asynchronous Processing**: UI updates and data fetching are decoupled using Kivy's Clock
3. **Error Handling Layers**: Validation at input level, analysis level, and display level
4. **Component-Based UI**: Reusable styled widgets with consistent theming
5. **Factory Pattern**: Background creation functions for different animation types

## Common Development Commands

### Running the Application
```powershell
# Run the main application
python main.py

# Alternative entry point
python -m main
```

### Environment Setup
```powershell
# Install required dependencies
pip install kivy yfinance numpy

# Install specific versions (if needed)
pip install kivy==2.3.1 yfinance==0.2.65 numpy==1.26.3

# Install additional Kivy dependencies for Windows
pip install kivy-deps.angle kivy-deps.glew kivy-deps.sdl2
```

### Development and Testing
```powershell
# Test individual modules
python -c "from risk import StockRiskAnalyzer; analyzer = StockRiskAnalyzer(); print(analyzer.analyze_stock('AAPL'))"

# Test UI components
python -c "from ui import create_main_ui; ui = create_main_ui(); print('UI created successfully')"

# Test background animations
python -c "from background import create_animated_background; bg = create_animated_background(); print('Background created successfully')"
```

### Code Quality
```powershell
# Check for Python syntax errors
python -m py_compile main.py
python -m py_compile risk.py
python -m py_compile ui.py
python -m py_compile background.py

# Run with verbose error output
python -u main.py
```

## Key Technical Details

### Dependencies
- **Kivy 2.3.1** - Cross-platform GUI framework
- **yfinance 0.2.65** - Yahoo Finance data fetching
- **numpy 1.26.3** - Numerical computations for risk metrics
- **KivyMD 1.2.0** - Additional material design components

### Risk Analysis Methodology
- Uses **1 year historical data** by default
- Calculates **annualized volatility** (252 trading days)
- **VaR calculations** at 95% and 99% confidence levels
- **Maximum drawdown** analysis using cumulative returns
- **Sharpe ratio** calculation (assumes 0% risk-free rate)
- **Risk categorization**: LOW (<15%), MEDIUM (15-30%), HIGH (>30%)

### UI Architecture
- **FloatLayout** base with responsive positioning
- **BoxLayout** containers for organized content flow
- **ScrollView** for results with automatic text wrapping
- **Custom styling** with consistent color schemes and typography
- **Animation system** with press effects and state management

### Performance Considerations
- **Asynchronous data fetching** prevents UI blocking
- **60fps animations** with efficient canvas drawing
- **Memory management** with proper cleanup on app close
- **Responsive design** adapts to different screen sizes

## Error Handling Strategy

1. **Input Validation**: Ticker format and length validation
2. **Data Fetching**: Network and API error handling
3. **Analysis Errors**: Mathematical computation safeguards
4. **UI State Management**: Loading states and user feedback
5. **Graceful Degradation**: Fallback messages for all failure modes

## Development Notes

- The application is designed for **Windows PowerShell** environment
- **Mobile compatibility** included with pause/resume lifecycle methods
- **Modular design** allows easy extension of new risk metrics
- **Custom widget system** enables consistent theming across components
- **Real-time animations** provide engaging user experience without blocking functionality

## Extending the Application

### Adding New Risk Metrics
1. Modify `RiskMetrics` dataclass in `risk.py`
2. Update calculation methods in `StockRiskAnalyzer`
3. Enhance formatting in `format_results()` methods

### UI Customization
1. Modify color schemes in `ui.py` component classes
2. Adjust animation parameters in `background.py`
3. Add new widget types following existing patterns

### Data Sources
1. Extend `_fetch_stock_data()` in `risk.py` for additional APIs
2. Add new analysis periods beyond the default 1-year
3. Implement caching for improved performance
