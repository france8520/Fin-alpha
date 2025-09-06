import yfinance as yf
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label


class StockRiskApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical", padding=15, spacing=15)

        # Input field
        self.ticker_input = TextInput(
            hint_text="Enter stock ticker (e.g. AAPL, PTTEP.BK)", 
            size_hint=(1, 0.15), 
            multiline=False
        )

        # Button
        btn = Button(
            text="Calculate Risk", 
            size_hint=(1, 0.15),
            background_color=(0.1, 0.5, 0.8, 1)  # bluish
        )
        btn.bind(on_press=self.calculate_risk)

        # Result label
        self.result_label = Label(
            text="Result will be displayed here",
            size_hint=(1, 0.7)
        )

        # Add widgets
        self.layout.add_widget(self.ticker_input)
        self.layout.add_widget(btn)
        self.layout.add_widget(self.result_label)

        return self.layout

    def calculate_risk(self, instance):
        ticker = self.ticker_input.text.strip()
        if not ticker:
            self.result_label.text = "Please enter a ticker symbol"
            return

        try:
            data = yf.download(ticker, period="1y")
            data["Returns"] = data["Close"].pct_change().dropna()

            returns = data["Returns"].dropna()
            volatility = returns.std() * np.sqrt(252)  # Annualized
            var_95 = np.percentile(returns, 5)  # 5th percentile

            result = (
                f"Stock: {ticker}\n"
                f"Volatility: {volatility:.2%} per year\n"
                f"Value at Risk (95%): {var_95:.2%} per day"
            )
            self.result_label.text = result

        except Exception as e:
            self.result_label.text = f"Error: {e}"


if __name__ == "__main__":
    StockRiskApp().run()