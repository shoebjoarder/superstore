# Dash & Plotly Superstore Application

A web application built with Dash and Plotly to analyze the Superstore dataset  ([link here](https://datawonders.atlassian.net/wiki/spaces/TABLEAU/blog/2022/10/26/1953431553/Where+Can+I+Find+Superstore+Sales)). The app has three pages: Dashboard, Data Table, and Insights. Some features of the application includes:

- Get insights of the recent (past four months) sales and profit ratio
- Add new data to the dataset
- Filter the dataset with preview
- Provide interactive visualizations with various filters
- Navigate pages using sidebar
- Applied Responsive Design

## Live Demo

Link: [Live Demo](https://shoeb-superstore.onrender.com/)

## 🚀 Getting Started

### Prerequisites

- Install [Python](https://www.python.org/downloads/release/python-31012/) (v3.10.12)
- A code editor such as [IntelliJ Ultimate](https://www.jetbrains.com/idea/download) or [Visual Studio Code](https://code.visualstudio.com/download)
- [GitHub Desktop](https://desktop.github.com/) (optional, for cloning the repository)

### Installation Steps

1. Open a terminal and clone the repository

   ```
   git clone https://github.com/shoebjoarder/superstore.git
   ```

2. Create a Python virtual environment in the project directory

   ```bash
   cd superstore
   python -m venv venv
   ```

3. Activate the environment

   ```bash
   source ./venv/bin/activate
   ```

4. Install the Python packages

   ```bash
   pip install -r requirements.txt
   ```

5. Start the Dash server

   ```bash
   python src/app.py
   ```

7. Open the application in your browser:

   ```
   http://127.0.0.1:8050
   ```