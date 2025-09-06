"""
Risk Analysis Module - Fixed Version
Handles all stock data fetching and risk calculations with improved formatting
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
        """Format risk metrics into display string with better formatting"""
        color_map = {
            "high": "[color=#FF5252]",    # Red
            "medium": "[color=#FFC107]",  # Amber
            "low": "[color=#4CAF50]",     # Green
        }
        color_tag = color_map.get(metrics.risk_color, "")
        end_tag = "[/color]" if color_tag else ""
        return f"""ANALYSIS RESULTS FOR {metrics.ticker}

Current Price: ${metrics.current_price:.2f}

RISK METRICS:
• Annual Volatility: {metrics.volatility:.1%}
• Value at Risk (95%): {metrics.var_95:.2%} daily
• Value at Risk (99%): {metrics.var_99:.2%} daily
• Maximum Drawdown: {metrics.max_drawdown:.1%}
• Sharpe Ratio: {metrics.sharpe_ratio:.2f}

Risk Level: {color_tag}{metrics.risk_level}{end_tag}"""

    def format_results_detailed(self, metrics: RiskMetrics) -> str:
        """Format risk metrics with detailed explanations"""
        explanations = {
            'volatility': "Measures how much the stock price fluctuates",
            'var_95': "Maximum expected daily loss 95% of the time",
            'var_99': "Maximum expected daily loss 99% of the time", 
            'max_drawdown': "Largest peak-to-trough decline",
            'sharpe_ratio': "Risk-adjusted return (higher is better)"
        }
        
        return f"""DETAILED ANALYSIS FOR {metrics.ticker}

Current Price: ${metrics.current_price:.2f}

🔍 RISK METRICS EXPLAINED:

Annual Volatility: {metrics.volatility:.1%}
   {explanations['volatility']}

Value at Risk (95%): {metrics.var_95:.2%} daily
   {explanations['var_95']}

Value at Risk (99%): {metrics.var_99:.2%} daily
   {explanations['var_99']}

Maximum Drawdown: {metrics.max_drawdown:.1%}
   {explanations['max_drawdown']}

Sharpe Ratio: {metrics.sharpe_ratio:.2f}
   {explanations['sharpe_ratio']}

Risk Level: {metrics.risk_level}

{self._get_risk_interpretation(metrics.risk_level)}"""

    def _get_risk_interpretation(self, risk_level: str) -> str:
        """Get risk level interpretation"""
        interpretations = {
            "LOW": "This stock has relatively low volatility and is considered less risky.",
            "MEDIUM": "This stock has moderate volatility. Consider your risk tolerance.",
            "HIGH": "This stock is highly volatile and risky. Only suitable for risk-tolerant investors."
        }
        return interpretations.get(risk_level, "Risk level assessment unavailable.")


# Convenience functions for easy usage
def analyze_stock_risk(ticker: str) -> Optional[RiskMetrics]:
    """Quick function to analyze stock risk"""
    analyzer = StockRiskAnalyzer()
    return analyzer.analyze_stock(ticker)


def get_formatted_analysis(ticker: str, detailed: bool = False) -> str:
    """Get formatted analysis results"""
    try:
        analyzer = StockRiskAnalyzer()
        metrics = analyzer.analyze_stock(ticker)
        
        if detailed:
            return analyzer.format_results_detailed(metrics)
        else:
            return analyzer.format_results(metrics)
    except Exception as e:
        return f"ERROR ANALYZING {ticker.upper()}\n\n{str(e)}\n\nPlease check the ticker symbol and try again."


def get_risk_summary(ticker: str) -> str:
    """Get a quick risk summary"""
    try:
        analyzer = StockRiskAnalyzer()
        metrics = analyzer.analyze_stock(ticker)
        
        return f"""Quick Summary for {metrics.ticker}:
Price: ${metrics.current_price:.2f}
Volatility: {metrics.volatility:.1%}
Risk: {metrics.risk_level}"""
    except Exception as e:
        return f"Unable to analyze {ticker}: {str(e)}"