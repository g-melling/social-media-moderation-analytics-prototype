# 🛡️ Social Media Moderation Analytics

A Python-based desktop analytics platform designed to support social media moderation teams through data cleaning, reporting, statistical analysis, and visualisation of user engagement and moderation activity.

Built with **Python**, **Tkinter**, **Pandas**, **SQLite**, and **Matplotlib**, the application provides an interactive graphical interface for exploring moderation datasets and identifying content moderation trends.

---

## 📖 Overview

Social media platforms generate large volumes of user-generated content and moderation events every day. This project demonstrates how data analytics can be used to support moderation teams by identifying patterns in reports, user behaviour, engagement metrics, and moderation actions.

The system provides:

* Data loading and validation
* Data cleaning and preprocessing
* Moderation trend analysis
* User engagement analytics
* Correlation analysis
* Statistical summaries
* Interactive visualisations
* Audit logging
* Backup and recovery functionality

The application is designed as a proof-of-concept moderation analytics tool that supports human decision-making rather than replacing human moderators.

---

## ✨ Features

### 📂 Data Management

* Load multiple social media datasets
* Validate required files
* Clean and preprocess records
* Remove duplicate entries
* Handle missing values
* Exclude bot accounts from behavioural analysis
* Save and restore backups

### 📊 Analytics

* Report pattern analysis
* Topic and moderation-level analysis
* Posting activity heatmaps
* User behaviour analysis
* Engagement statistics
* Correlation visualisation

### 📈 Visualisations

* Embedded charts within the application
* Bar charts
* Heatmaps
* Correlation matrices
* Interactive chart navigation tools

### 📝 Audit Logging

* Automatic activity logging
* Action history tracking
* Transparency and accountability support

### 💾 Backup System

* JSON backup storage
* SQLite database backups
* Automatic restoration on startup

---

## 🖥️ User Interface

The application is built using Tkinter and includes:

* File selection tools
* Data management controls
* Interactive analytics dashboard
* Tabbed results viewer
* Embedded chart visualisations
* Audit log viewer
* Status notifications

The interface allows users to perform data operations and analytics without requiring programming knowledge.

---

## 📊 Datasets

The application processes four core datasets:

| Dataset          | Description                                   |
| ---------------- | --------------------------------------------- |
| USERS.csv        | User account information                      |
| POSTS.csv        | Social media post data                        |
| INTERACTIONS.csv | Likes, comments, shares and reports           |
| TOPICS.csv       | Content categories and moderation information |

---

## 🧹 Data Cleaning Pipeline

The system automatically performs several preprocessing tasks:

### Duplicate Removal

* Removes duplicate users
* Removes duplicate posts
* Removes duplicate interactions
* Removes duplicate topic records

### Missing Value Handling

Default values are applied where appropriate:

| Field        | Default Value           |
| ------------ | ----------------------- |
| verified     | False                   |
| account_type | personal                |
| has_media    | False                   |
| content_type | unknown                 |
| description  | No description provided |

### Data Integrity Checks

* Removes invalid records
* Validates foreign key relationships
* Ensures posts belong to valid users
* Ensures interactions belong to valid posts

### Bot Filtering

Bot accounts are excluded from behavioural analysis to improve the accuracy of human engagement metrics.

---

## 📈 Analytics Modules

### 1. Report Pattern Analysis

Examines relationships between:

* Content categories
* Moderation levels
* User reports

Outputs:

* Summary tables
* Bar chart visualisations

---

### 2. Posting Activity Analysis

Analyses posting behaviour by:

* Time of day
* Content category

Outputs:

* Activity heatmaps
* Posting trend analysis

---

### 3. Categorical Analysis

Cross-tabulation of:

* User verification status
* Content type
* Moderation level

Provides insight into relationships between user characteristics and moderation outcomes.

---

### 4. Engagement Statistics

Calculates:

* Mean
* Median
* Mode

For metrics including:

* Likes per post
* Comments per post
* Shares per post
* Reports per post
* Total engagements per post

---

### 5. Correlation Analysis

Investigates relationships between:

* Moderation severity
* Report counts
* Report rates

Outputs:

* Correlation matrix
* Heatmap visualisation

---

## 📊 Example Insights

The platform can help answer questions such as:

* Which content categories generate the most reports?
* What times of day see the highest posting activity?
* Are verified users moderated differently?
* How strongly do moderation levels correlate with report frequency?
* Which posts generate the highest engagement?

---

## 🏗️ System Architecture

```text
CSV Datasets
      │
      ▼
 Data Loading
      │
      ▼
 Data Cleaning
      │
      ▼
 Data Validation
      │
      ▼
 Analytics Engine
      │
 ┌────┼────┐
 ▼    ▼    ▼
Stats Charts Reports
      │
      ▼
 Tkinter Dashboard
```

---

## 🛠 Technologies Used

### Programming Language

* Python

### Data Processing

* Pandas

### Statistical Analysis

* NumPy

### Visualisation

* Matplotlib

### User Interface

* Tkinter

### Database Storage

* SQLite

### Data Formats

* CSV
* JSON
* SQLite

---

## 📂 Project Structure

```text
social-media-moderation-analytics/
│
├── gui.py
├── backend.py
├── database_structure_dump.sql
│
├── USERS.csv
├── POSTS.csv
├── INTERACTIONS.csv
├── TOPICS.csv
│
├── backup.json
├── backup.db
├── audit_log.txt
│
└── README.md
```

---

## 🚀 Installation

### Prerequisites

* Python 3.9+
* pip

### Install Dependencies

```bash
pip install pandas matplotlib
```

### Run the Application

```bash
python gui.py
```

---

## 📄 License

This project is licensed under the MIT License.

---
