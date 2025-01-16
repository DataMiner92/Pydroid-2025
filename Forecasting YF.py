import pandas as pd
import yfinance as yf
import math
import numpy as np

df = yf.download("AAP", start="2024-01-01", end="2024-04-01")
print(df.head())