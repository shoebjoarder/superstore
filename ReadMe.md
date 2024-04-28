# Dash & Plotly Superstore Application

This web application is developed using Dash and Plotly, designed to provide a comprehensive analysis of the Superstore dataset. The application is structured into three main sections: Dashboard, Data Table, and Insights, each crafted to deliver specific functionalities efficiently.

### ✅ Key Features

- **Dynamic Insights**: Analyze recent trends in sales and profit ratios.
- **Data Management**: Seamlessly add new entries to update and expand the dataset.
- **Advanced Filtering**: Utilize powerful filters to refine data searches; includes a real-time preview feature.
- **Interactive Visualizations**: Explore data through engaging and customizable visual graphics, adjustable with various filters to pinpoint precise information.
- **User-Friendly Navigation**: Easily move between different sections using a responsive sidebar.
- **Responsive Design**: Enjoy a consistent user experience across various devices and screen sizes, ensuring accessibility and ease of use.

### 💡 Benefits

This application aims to empower users to make data-driven decisions by offering detailed and intuitive analyses of sales and profitability metrics. Whether you are looking to identify trends, assess performance, or enhance operational strategies, this tool provides essential functionalities to navigate and interpret complex datasets.

## Live Demo

Link: [Live Demo](https://shoeb-superstore.onrender.com/)

## Dataset

Link to the Superstore [dataset](https://datawonders.atlassian.net/wiki/spaces/TABLEAU/blog/2022/10/26/1953431553/Where+Can+I+Find+Superstore+Sales).

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
   # Move to the directory
   cd superstore 

   # Create a virtual environment
   python -m venv venv
   ```

3. Activate the environment

   ```bash
   # Command for Linux
   source ./venv/bin/activate
   
   # Command for Windows
   ./venv/Scripts/activate
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
