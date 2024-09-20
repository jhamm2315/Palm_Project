# PALM Dashboards for Financial Data Analysis

## Overview

This project is an interactive dashboard application built using Python's Dash framework. It integrates various data sources, machine learning models, and advanced user interactions to provide comprehensive financial analysis. The app is designed to be easily adaptable for other users, who can simply replace the data sources with their own.

## Features

1. **Dynamic Dashboards**: The app showcases multiple financial dashboards, including Accounts Receivable, Payments, Invoices, Budget, Cash Flow, and more, which can change based on user-selected filters.
2. **Chart Annotations**: Highlight significant data points and trends within the charts for better data visualization.
3. **Drill-Down Capabilities**: Enable drill-down functionality on charts, allowing users to explore deeper levels of data by clicking on specific points.
4. **Data Export Options**: Users can export data from the dashboards into CSV format directly from the application.
5. **Sortable and Searchable Tables**: Integrated `dash-table` with sorting, filtering, and editable cells for a more interactive experience.
6. **Machine Learning Models**: Predictive analytics and machine learning models provide trend forecasting and data-driven recommendations.
7. **Natural Language Processing (NLP) Search**: Users can search and filter data using natural language queries.
8. **Third-Party API Integration**: Fetch data from external APIs to enhance the application's functionality.

## Project Structure

- `main.py`: The main Python script that runs the Dash application.
- `your_model.pkl`: The trained machine learning model used for predictions. Ensure this file is saved in the appropriate directory as defined in the `main.py` script.
- `requirements.txt`: Contains the required libraries and dependencies for the project.
- `index.html`, `styles.css`: HTML and CSS files used for hosting and styling the application.

## Installation

### Prerequisites

Ensure you have the following installed on your machine:
- Python 3.10 or higher
- PostgreSQL Database
- Git
- Required Python libraries (see `requirements.txt`)

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/interactive-dashboards.git
   cd interactive-dashboards
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration**:
   - Ensure your PostgreSQL database is running.
   - Modify the database connection string in `main.py` to match your PostgreSQL credentials and database details.

5. **Run the Application**:
   ```bash
   python main.py
   ```
   Open your browser and navigate to `http://127.0.0.1:8050/` to view the app.

## Using the App

- **Navigating Dashboards**: Click on tabs to switch between different financial dashboards such as Accounts Receivable, Expenses, Assets, and more.
- **Exporting Data**: Use the "Download Data" button to export the current data displayed in the dashboard.
- **Editable Tables**: Edit table cells directly to update backend data and see the changes reflected in the dashboards.
- **Machine Learning Predictions**: Enter parameters into the provided input box to receive predictions from the integrated ML model.
- **NLP Search**: Use the search box to filter data using natural language queries, enhancing user interaction with data.
- **API Data Fetching**: Fetch external data using the provided button, integrating real-time data into your dashboards.

## Hosting the App with GitHub Pages

To host the app on GitHub Pages, follow these steps:

1. **Create GitHub Repository**:
   - Go to GitHub and create a new public repository.
   - Upload your project files (`main.py`, `requirements.txt`, HTML, CSS files) to the repository.

2. **Enable GitHub Pages**:
   - Go to the **Settings** of your repository.
   - Scroll to the **GitHub Pages** section.
   - Select the main branch as the source and save.

3. **Access Your Web App**:
   - After a few moments, your app will be live at:
     ```
     https://your-username.github.io/interactive-dashboards/
     ```

## Customizing the Project

- **Updating Data**: Replace the current SQL queries in `main.py` with your database tables and columns.
- **ML Model**: Replace `your_model.pkl` with your trained machine learning model to enable prediction features.
- **Styling**: Modify `styles.css` to change the look and feel of the dashboards.

## Troubleshooting

- **Connection Issues**: Verify your database connection string and ensure PostgreSQL is running.
- **Missing Dependencies**: Run `pip install -r requirements.txt` to ensure all libraries are installed.
- **Model Loading Errors**: Check the path to your machine learning model file and ensure it matches the file location defined in `main.py`.

## Contributing

Feel free to fork this repository and contribute by submitting pull requests. Any improvements, bug fixes, or new features are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please open an issue on the GitHub repository or contact me at [jhamm2315@gmail.com](mailto:jhamm2315@gmail.com).
