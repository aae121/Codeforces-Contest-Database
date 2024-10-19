# Codeforces-Contest-Database

## Overview
This project is a database application built to gather, store, and analyze data from **Codeforces** contests. It aims to provide more flexible filtering, ranking, and aggregation features beyond what is available on the Codeforces platform. Users can log in to view their contest participation, problem attempts, and analyze trends in competitive programming.

## Project Milestones
1. **Milestone I: Database Design and Implementation** (Uploaded)
   - Designed the database schema and Entity-Relationship Diagram (ERD).
   - Created the database and tables in MySQL for storing contest, problem set, and user data.
   
2. **Milestone II: Web Crawling and Data Population** (Upcoming)
   - Develop a Python-based web crawler using libraries like Scrapy, Selenium, and BeautifulSoup to extract data from Codeforces.
   - Populate the MySQL database with the crawled data, including details on contests, problem sets, and user activities.

3. **Milestone III: Application Layer** (Upcoming)
   - Build a client application capable of connecting to the MySQL database.
   - Implement features for users to view contest history, problem attempts, and perform data analysis such as ranking users by problems solved, organizations by ratings, etc.

## Project Features
- **User Login**: Users can log in with their Codeforces screen name to view their contest history and problem attempts.
- **Contest and Problem Set Data**: 
  - Stores information on contests (Division 1 and Division 2), including contest names, dates, writers, and standings.
  - Tracks all problem sets, with details like tags, time/memory limits, users' attempts, and contest usage.
- **User and Team Insights**:
  - Top users ranked by problems solved, contest participation, and activity streaks.
  - Top programming languages by speed and memory efficiency in problem-solving.
  - Top 5 organizations by user ratings in contests.
  - Specific analysis of AUC users' contest performance.
  - Most attempted problem sets by users from Egypt.

## Technologies Used
- **Database**: MySQL is used to store all contest, problem set, and user-related data.
- **Web Crawling**: Python is used to develop a web crawler for extracting data from Codeforces.
  - **Libraries**: 
    - `Scrapy`: For web crawling and scraping data.
    - `Selenium`: For dynamic page handling.
    - `BeautifulSoup`: For HTML parsing and data extraction.
- **Backend Application**: Python is used for building the backend to handle database operations and data retrieval.

## Database Design
The database schema includes tables for:
- **Contests**: Stores contest details like name, division, date, and writers.
- **Problem Sets**: Contains information about problem sets such as tags, time limits, and contests used.
- **Users**: Records user details such as screen name, country, and organization.
- **Attempts**: Tracks user attempts on problem sets, including verdict, language, time, and memory usage.
- **Standings**: Keeps standings for users in contests.

## Future Improvements
- Enhance filtering capabilities to allow users more flexibility in data analysis.
- Implement additional statistical insights and data visualizations.
- Potentially build a front-end interface for easier interaction.

## Tools & Libraries
- **MySQL**: Database management system for storing contest, problem, and user data.
- **Python**: Programming language used for both web crawling and backend logic.
  - **Scrapy**: Web scraping framework to extract contest and problem data.
  - **Selenium**: To handle dynamic elements on the website during scraping.
  - **BeautifulSoup**: For parsing and extracting relevant data from HTML pages.
- **Pycharm**: Integrated Development Environment (IDE) used for development.

## Acknowledgments
This project is part of the AUC Fundementals of Database Systems Course, focusing on data aggregation, web crawling, and database management using Codeforces data, under the supervision of Prof. Mohamed Alhalaby.
