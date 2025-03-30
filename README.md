# Repo Insights Data Analysis

This repository is part of an assignment on *Functional Style and Data Analysis*. The goal is to apply principles of functional programming—such as purity, immutability, and higher-order functions—to analyze data extracted from GitHub. The data (retrieved via the GitHub API or downloaded from the [RepoInsights](https://repo-insights.hsborges.dev) tool) includes user information such as followers count, following count, and account creation date.

## Purpose

The assignment proposes two deliverables:

1. **Metrics Script:**
   - **Objective:** Extract and analyze user metrics (`followers_count`, `following_count`, and `account_age`).
   - **Calculations:** For each metric, the script computes the minimum, maximum, average, median, and standard deviation.
   - **Output:** A CSV output where each row represents a metric and the columns display the calculated statistics.

2. **Locations Script (Bonus):**
   - **Objective:** Process the location data of users.
   - **Processing:** Locations are normalized (converted to lowercase and trimmed) and their occurrences are counted.
   - **Output:** A CSV output with two columns: the location and the number of occurrences, sorted in descending order.

In addition, the repository includes unit tests to ensure the correctness of the functions.

## How to Run the Scripts

### Metrics Script

- **Preparation:**
  - Ensure the `dados.json` file (containing the user data) is located in the `src` directory.

- **Execution:**
  1. Open a terminal.
  2. Navigate to the `src` directory:
     ```bash
     cd src
     ```
  3. Run the metrics script:
     ```bash
     python3 metrics.py
     ```
  4. The script will read the data, calculate the statistics for each metric, and print the CSV output to the terminal.

### Locations Script

- **Preparation:**
  - Ensure the `dados.json` file is located in the `src` directory.

- **Execution:**
  1. Open a terminal.
  2. Navigate to the `src` directory:
     ```bash
     cd src
     ```
  3. Run the locations script:
     ```bash
     python3 locations.py
     ```
  4. The script will process user locations by normalizing and counting them, then print the CSV output to the terminal.

## How to Run Unit Tests

All unit tests are consolidated in a single file (`test_*.py`) located in the `src` directory.

- **Steps to Run Tests:**
  1. **Install pytest (if not already installed):**
     ```bash
     pip install pytest
     ```
  2. **Run the tests:**
     1. Open a terminal.
     2. Navigate to the `src` directory:
        ```bash
        cd src
        ```
     3. Execute:
        ```bash
        pytest
        ```
  3. Pytest will automatically discover and execute all tests in the `test_*.py` file.

## Additional Notes

- **Calculated Metrics:**
  - **min:** The minimum value found.
  - **max:** The maximum value found.
  - **avg:** The average of the values.
  - **median:** The median value.
  - **std:** The standard deviation of the values.

- **Location Processing:**
  The script converts all location entries to lowercase and trims extra spaces, ensuring that similar entries (e.g., "Brazil" and " brazil ") are unified.

- **Functional Programming Principles:**
  The project is developed following functional programming principles by using pure functions, immutability, and higher-order functions (e.g., `map`, `filter`, and `reduce`).

- **Data:**
  The data is read from a JSON file (`dados.json`), which contains user information retrieved from the GitHub API or downloaded from the RepoInsights tool.

## Repository Structure

```plaintext
src/
├── metrics.py            # Script for computing metrics and generating the statistics CSV.
├── locations.py          # Script for processing user locations and generating the locations CSV.
├── test_*.py             # File containing unit tests for functions in both scripts.
├── dados.json            # Example JSON file containing user data.
└── README.md             # This file.
