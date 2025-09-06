"""
Risk Analysis Module
Handles all stock data fetching and risk calculations
"""

import yfinance as yf
import numpy as np
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class RiskMetrics:
    """Data class to store risk analysis results"""
    ticker: str
    current_price: float
    volatility: float
    var_95: float
    var_99: float
    max_drawdown: float
    sharpe_ratio: float
    risk_level: str
    risk_color: str


class StockRiskAnalyzer:
    """Main class for stock risk analysis"""
    
    def __init__(self):
        self.risk_thresholds = {
            'high': 0.3,
            'medium': 0.15
        }
    
    def analyze_stock(self, ticker: str, period: str = "1y") -> Optional[RiskMetrics]:
        """
        Analyze stock risk metrics for given ticker
        
        Args:
            ticker (str): Stock ticker symbol
            period (str): Time period for analysis (default: 1y)
            
        Returns:
            RiskMetrics: Analysis results or None if error
            
        Raises:
            ValueError: If ticker is invalid or insufficient data
            Exception: For other data fetching errors
        """
        try:
            # Download stock data
            data = self._fetch_stock_data(ticker, period)
            
            # Calculate returns
            returns = self._calculate_returns(data)
            
            # Calculate risk metrics
            metrics = self._calculate_risk_metrics(ticker, data, returns)
            
            return metrics
            
        except Exception as e:
            raise Exception(f"Analysis failed: {str(e)}")
    
    def _fetch_stock_data(self, ticker: str, period: str) -> Any:
        """Fetch stock data from Yahoo Finance"""
        data = yf.download(ticker, period=period, progress=False)
        
        if data.empty:
            raise ValueError("No data found for this ticker")
            
        return data
    
    def _calculate_returns(self, data: Any) -> np.ndarray:
        """Calculate daily returns from price data"""
        returns = data["Close"].pct_change().dropna()
        
        if len(returns) < 30:
            raise ValueError("Insufficient data for analysis (need at least 30 days)")
            
        return returns
    
    def _calculate_risk_metrics(self, ticker: str, data: Any, returns: np.ndarray) -> RiskMetrics:
        """Calculate all risk metrics"""
        # Basic metrics
        current_price = float(data["Close"].iloc[-1])
        volatility = float(returns.std() * np.sqrt(252))  # Annualized
        
        # Value at Risk calculations
        var_95 = float(np.percentile(returns, 5))  # 5th percentile
        var_99 = float(np.percentile(returns, 1))  # 1st percentile
        
        # Maximum drawdown
        cumulative_returns = (returns + 1).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (peak - cumulative_returns) / peak
        max_drawdown = float(drawdown.max())
        
        # Sharpe ratio (assuming risk-free rate of 0)
        annual_return = float(returns.mean() * 252)
        annual_volatility = float(returns.std() * np.sqrt(252))
        sharpe_ratio = annual_return / annual_volatility if annual_volatility != 0 else 0
        
        # Determine risk level
        risk_level, risk_color = self._determine_risk_level(volatility)
        
        return RiskMetrics(
            ticker=ticker.upper(),
            current_price=current_price,
            volatility=volatility,
            var_95=var_95,
            var_99=var_99,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            risk_level=risk_level,
            risk_color=risk_color
        )
    
    def _determine_risk_level(self, volatility: float) -> tuple[str, str]:
        """Determine risk level based on volatility"""
        if volatility > self.risk_thresholds['high']:
            return "HIGH", "high"
        elif volatility > self.risk_thresholds['medium']:
            return "MEDIUM", "medium"
        else:
            return "LOW", "low"
    
    def format_results(self, metrics: RiskMetrics) -> str:
        """Format risk metrics into display string"""
        return f"""ANALYSIS RESULTS FOR {metrics.ticker}
            
Current Price: ${metrics.current_price:.2f}

RISK METRICS:
• Annual Volatility: {metrics.volatility:.1%}
• Value at Risk (95%): {metrics.var_95:.2%} daily
• Value at Risk (99%): {metrics.var_99:.2%} daily
• Maximum Drawdown: {metrics.max_drawdown:.1%}
• Sharpe Ratio: {metrics.sharpe_ratio:.2f}

Risk Level: {metrics.risk_level}"""


# Convenience functions for easy usage
def analyze_stock_risk(ticker: str) -> Optional[RiskMetrics]:
    """Quick function to analyze stock risk"""
    analyzer = StockRiskAnalyzer()
    return analyzer.analyze_stock(ticker)


def get_formatted_analysis(ticker: str) -> str:
    """Get formatted analysis results"""
    try:
        analyzer = StockRiskAnalyzer()
        metrics = analyzer.analyze_stock(ticker)
        return analyzer.format_results(metrics)
    except Exception as e:
        return f"ERROR ANALYZING {ticker.upper()}\n\n{str(e)}\n\nPlease check the ticker symbol and try again."