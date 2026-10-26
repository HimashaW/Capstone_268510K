# Telecom Traffic Forecasting and Proactive Capacity Risk Detection System

## Project Overview
This project aims to forecast Internet activity using historical telecom traffic data and identify potential high-demand periods through scenario-based capacity-risk indicators.

## Dataset
The project uses the Milan subset of the Telecom Italia Big Data Challenge dataset, covering November 2013 to January 2014 at 10-minute intervals.

**Source:** https://www.nature.com/articles/sdata201555

## Planned Workflow
1. Data preparation and quality checks
2. Exploratory data analysis
3. Temporal feature engineering
4. Candidate forecasting models
5. Forecast evaluation and comparison
6. Capacity-risk detection
7. Explainability, where suitable
8. Visualisation and dashboard development

## Project Status
Initial setup and data inspection.

## Reproducibility
Environment dependencies, preprocessing decisions, model configurations, and evaluation procedures will be documented as the project develops.

## Initial Dataset Inspection

The initial inspection used a single-day Telecom Italia text file to assess the data structure before processing the complete dataset. The file is approximately 171 MB and contains 2,459,324 records across eight tab-separated columns without a header row. The records use 10-minute timestamps and include geographical identifiers, country codes, and telecom activity measurements.

Missing values were observed in several activity columns. Their meaning will be investigated before selecting a cleaning or aggregation strategy. The file naming also suggests that this may be the Trentino subset, so the geographical scope will be verified before proceeding with the main Milan-based analysis.
