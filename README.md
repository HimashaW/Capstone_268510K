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


Telecommunications
The Telecommunication datasets provide data about the telecommunication activity in the city of Milan and in the Province of Trentino. Specifically, we are releasing three different datasets, one for telecommunication activities and two for telecommunication interactions.

Telecommunications activity
This dataset [Data citations 4,5] serves as measure of the level of interaction between the users and the mobile phone network.

Square id: identification string of a given square of Milan/Trentino GRID;

Time Interval: start interval time expressed in milliseconds. The end interval time can be obtained by adding 600,000 milliseconds (10 min) to this value;

SMS-in activity: activity proportional to the amount of received SMSs inside a given Square id and during a given Time interval. The SMSs are sent from the nation identified by the Country code;

SMS-out activity: activity proportional to the amount of sent SMSs inside a given Square id during a given Time interval. The SMSs are received in the nation identified by the Country code;

Call-in activity: activity proportional to the amount of received calls inside the Square id during a given Time interval. The calls are issued from the nation identified by the Country code;

Call-out activity: activity proportional to the amount of issued calls inside a given Square id during a given Time interval. The calls are received in the nation identified by the Country code;

Internet traffic activity: number of CDRs generated inside a given Square id during a given Time interval. The Internet traffic is initiated from the nation identified by the Country code;

Country code: the phone country code of the nation.


###Extra
In this dataset, CDR count is specifically used for the Internet activity column. The SMS and call activities are represented by separate columns.

Column	What it measures
SMS-in	Received SMS activity
SMS-out	Sent SMS activity
Call-in	Received call activity
Call-out	Issued call activity
Internet activity	Number of Internet-related CDRs generated

Internet activity as the main forecasting target and potentially use the other four activity columns as additional features.


