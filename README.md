# Bias in AI: Analyzing ChatGPT's University Ranking Tendencies

## Authors
- Marvin John Wiedenkeller
- David Jonas Scherrer
- Jan Marc Lüthi
- Simon Moser

## Course
Social Computing, FS 2024

## Overview
This repository contains the code and data for the project "Bias in AI: Analyzing ChatGPT's University Ranking Tendencies." The project investigates potential biases in ChatGPT's evaluations of academic papers based on the country and university affiliations of the authors.

## Table of Contents
- [Introduction](#introduction)
- [Related Work](#related-work)
- [Data Collection](#data-collection)
- [Statistical Analysis](#statistical-analysis)
- [Discussion and Visualization of Results](#discussion-and-visualization-of-results)
- [Future Work](#future-work)
- [Conclusion](#conclusion)
- [References](#references)
- [Interactive Visualizations](#interactive-visualizations)
- [How to Use](#how-to-use)
- [License](#license)

## Introduction
In recent years, concerns have been raised about biases in AI systems. This project aims to analyze how ChatGPT evaluates research papers from universities around the world, potentially showing bias towards or against certain institutions based on their ranking.

## Related Work
The study builds on existing literature about biases in AI, the use of ChatGPT in academic contexts, and the influence of university rankings. It seeks to fill a gap by examining the intersection of these areas.

## Data Collection
Data was collected from Arxiv.org using their API, focusing on recent research articles in five fields: Computer Science, Mathematics, Quantitative Finance, Statistics, and Economics. Each paper was preprocessed to remove institutional affiliations to ensure unbiased evaluation.

## Statistical Analysis
The collected data was analyzed using various statistical methods, including MANOVA and ANOVA, to detect biases in ChatGPT's ratings based on country and university affiliations.

## Discussion and Visualization of Results
Results indicate significant biases in ChatGPT's ratings, especially when limited context is provided. Interactive visualizations were created to explore these biases in detail.

## Future Work
Future research should address the limited generalizability of these findings by increasing the sample size and variety. Different AI models and prompting approaches could also be explored.

## Conclusion
The study reveals that ChatGPT's evaluations can perpetuate biases inherent in university rankings, affecting academic assessments and societal perceptions.

## References
A comprehensive list of references used in this study is provided in the report. Key references include:
- UZH opting out of the Times Higher Education World University Ranking.
- The impact of AI tools like Iris.ai and Moonhub.ai on academic and recruitment processes.
- Detailed methodologies for measuring biases in large language models.

## Interactive Visualizations
Interactive visualizations and tools developed during this project are available in the `visualization` folder. These include bar charts and parallel coordinates plots that help in understanding the biases detected in the analysis.

## How to Use
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/SC_final.git
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the data exploration tool:
    ```bash
    python visualization/data_exploration_tool.py
    ```
4. Explore the interactive visualizations available in the `visualization` folder.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
