# Causal Modeling of Intensive Longitudinal Data

This repository contains Python code for processing, analyzing, and conducting causal modeling on intensive longitudinal data (ILD) collected through survey methods. The codebase is designed to handle both individual participant data and aggregated group-level analyses.
ILD, such as the data from repeated surveys, offers rich insights into dynamic experiences. This project provides a structured approach to:
1.	**Data Cleaning**: Handling raw CSV files from ILD surveys.
2.	**Data Processing**: Preparing the data for causal modeling.
3.	**Causal Modeling**: Applying algorithms to infer potential causal relationships within the longitudinal data.
4.	**Resampling**: Employing jackknifing methods to assess the stability of the causal modeling results.
5.	**Individual and Group Analysis**: Supporting both within-person (individual participant) and group-level analyses.

## Installation

Dependencies include:  
- Python 3 (3.11 used)
- Python dependencies:
    - See requirements.txt
    - Install with 
    > pip install -r requirements.txt

Note: Multiple code files included in this repository require first cloning the py-tetrad [1] repository, then editing files to fit your current project. See https://github.com/cmu-phil/py-tetrad for more details and instructions. The following files require py-tetrad:  
- run_search_boss.py
- jackknifing.py
- run_search_boss_group.py
- jackknifing_group.py

Clone the repository  
> git clone https://github.com/keyfalbo/ILD-Causal-Modeling.git

## Data Format

Intensive longitudinal data for this project were provided as CSV files. Each row represented a single time point for a specific participant, and columns represented measured variables. This specific project included four CSV files containing raw data from each of the four ILD surveys, where CSV files were titled Morning.csv, Afternoon.csv, Evening.csv, and Pain.csv. See sample data for example files with dummy data.  

This project also included a fifth CSV file containing weather data for each participant downloaded from the Open-Meteo Weather Application Programming Interface [2], where the CSV file was titled EMAXX_Weather.csv, where “XX” represented the participant ID number. This weather data file included weather data from any traveling that the participant completed over the study protocol period, combined into a single file.

Note: Causal modeling requires sufficient data to detect effects. Sample data in this repository contains only 15 observations per participant; therefore, causal modeling code will produce singularity errors with sample data.

## Configuration

Prior to running the analysis, you will need to configure parameters such as:  
- File paths where your CSV files are located
- Variable names in your CSV files
- Causal modeling parameters
- Jackknifing parameters  

## Usage

### Individualized data processing and analysis

1.	Run ild_processing_part1.py  
    - Outputs from this code:  
        - Number of missing values for each variable as a CSV file
        - Partially processed data for the identified participant as a CSV file

2.	Open the saved CSV file with the partially processed data and impute any remaining missing values, if necessary

3.	Run ild_processing_part2.py
    - Outputs from this code:
        - Fully processed data for the identified participant as a CSV file before standardization of variables
        - Fully processed data for the identified participant as a CSV file after standardization of variables

4.	Run create_knowledge.py
    - Outputs from this code:
        - Knowledge data for the identified participant as a text file

5.	Run run_search_boss.py
    - Outputs from this code:
        - Completed partially directed acyclic graph (CPDAG) as text file
        - Directed acyclic graph (DAG) as text file
        - Graph in lavaan format as text file
        - Edge estimates as CSV file
        - Edge estimates specific to outcome variables as CSV file
        - Model fit statistics as CSV file

6.	Run jackknifing.py
    - Outputs from this code:
        - Jackknifing results as text file
        - Jackknifing results as CSV file
        - Jackknifing results specific to outcome variables as CSV file

### Group data processing and analysis

Note: Prior to processing and analyzing group data, complete at least steps 1-3 on individualized data processing and analysis.  
1.	Run combine_group_data.py
    - Outputs from this code:
        - Number of missing values for each variable as a CSV file
        - Data grouped from all individual participants as a CSV file

2.	Run run_search_boss_group.py
    - Outputs from this code:
        - Completed partially directed acyclic graph (CPDAG) as text file

3.	Run group_estimates.py
    - Outputs from this code:
        - Edge estimates as CSV file
        - Model fit statistics as CSV file

4.	Run jackknifing_group.py
    - Outputs from this code:
        - Jackknifing results as text files (number of files depends on specified value of “reps” within the file)

5.	Run jackknifing_group_summarize.py
    - Outputs from this code:
        - Jackknifing results as CSV files (number of files depends on specified value of “reps” within the file from the previous step)
        - All edges found in group jackknifing results as single CSV file
        - Group jackknifing results for unique edges as a single CSV file

## References

[1] Ramsey, J., & Andrews, B. (2023, November). Py-Tetrad and RPy-Tetrad: A New Python Interface 
with R Support for Tetrad Causal Search. In Causal Analysis Workshop Series (pp. 40-51). PMLR.  
[2] Zippenfenig P. Open-Meteo.com Weather API 2024. https://doi.org/10.5281/ZENODO.7970649.
