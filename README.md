# Analysing Portfolio Returns

This project focuses on analyzing portfolio returns using Fama-French factors, comparing two distinct investment strategies: monthly investments throughout the year and investments excluding summer months. The analysis employs a Monte Carlo simulation to assess robustness over randomly selected 30-year investment periods. Key performance metrics, including Time-weighted rate of return and Sharpe ratio, are calculated to offer insights into the risk-adjusted portfolio performance.

The motivation behind this project stems from the hypothesis that individuals, particularly those in academic professions with summer breaks, might alter their investment behaviors during the summer months. By excluding these months from the investment strategy, we aim to explore whether there are discernible differences in portfolio returns. This investigation could provide valuable insights into the impact of seasonal variations, specifically related to the financial decisions of individuals during periods of reduced professional commitments.

## Repository Structure

- Monte_carlo_Fama.ipynb: Monte Carlo simualtions to compare investment return for 30 years span with and without summer months investment
- Portfolio_Returns.ipynb: Portfolio returns with and without summer months investment
- porfolio_returns.py: Python script containing all the required custom functions
- *_returns.npy: Saved outputs
