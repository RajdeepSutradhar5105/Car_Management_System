# 🚗 Car Management System

A comprehensive, multi-user car dealership management application built with Streamlit, MySQL, and scikit-learn. This system provides distinct interfaces for managers, sellers, and buyers, along with an AI-powered price prediction tool.

## ✨ Features

This application is divided into three user roles, each with a specific set of features:

### 👑 Manager
- **Dashboard:** Get a high-level overview of the entire system.
- **Analytics:** View key metrics like total cars, available cars, total revenue, and number of transactions.
- **Data Visualization:** Interactive charts show the distribution of cars by make and status (available vs. sold).
- **Inventory Management:** View a complete list of all cars in the system, regardless of seller.
- **Transaction Monitoring:** Access a detailed log of all sales transactions across the platform.

### 🏪 Seller
- **Personalized Dashboard:** Track your own inventory and sales performance.
- **Inventory Management:** Add new cars to the system for sale.
- **View Listings:** See a clear list of all cars you have listed, including their status.
- **Sales History:** Review a complete history of your own sales transactions.

### 🛒 Buyer
- **Advanced Search:** Browse and filter available cars by make, model, and price range.
- **Interactive Car Cards:** View car details in a clean, card-based layout.
- **Seamless Purchasing:** Purchase any available car with a single click.

### 🤖 AI Price Estimator
- **Machine Learning Powered:** Utilizes a Linear Regression model trained on the existing car data.
- **Accurate Predictions:** Enter a car's make, model, and year to get an estimated market value.
- **Data-Driven:** The model continuously improves as more car data is added to the system.

## 🛠️ Technologies Used

- **Backend & Frontend:** [Streamlit](https://streamlit.io/)
- **Database:** [MySQL](https://www.mysql.com/)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
- **Machine Learning:** [Scikit-learn](https://scikit-learn.org/)
- **Data Visualization:** [Plotly](https://plotly.com/)

## 🚀 Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Prerequisites
- Python 3.8+
- MySQL Server

### 2. Clone the Repository
```bash
git clone [https://github.com/RajdeepSutradhar5105/car-management-system.git](https://github.com/RajdeepSutradhar5105/car-management-system.git)
cd car-management-system
```

### 3. Set Up the Database
1.  Start your MySQL server.
2.  Log in to your MySQL client (e.g., MySQL Workbench, `mysql` command line).
3.  Create the database:
    ```sql
    CREATE DATABASE car_management_system;
    ```
4.  Run the provided SQL script to create the tables and insert initial data:
    ```bash
    mysql -u root -p car_management_system < setup.sql
    ```

### 4. Update Database Credentials
Open the `app.py` file and update the database connection details in the `get_db_connection` function with your own credentials:

```python
# in app.py
def get_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # <-- UPDATE THIS
            password="your_password", # <-- UPDATE THIS
            database="car_management_system"
        )
        return connection
    # ...
```

### 5. Install Dependencies
Install the required Python packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 6. Run the Application
Launch the Streamlit application from your terminal:
```bash
streamlit run app.py
```
The application will open in your default web browser.

## 🧑‍💻 How to Use

The application provides separate login portals for each user role. Use the following credentials (defined in `setup.sql`) to explore the different views:

-   **Manager:**
    -   **Username:** `manager1`
    -   **Password:** `managerpass`
-   **Seller:**
    -   **Username:** `seller1`
    -   **Password:** `sellerpass`
-   **Buyer:**
    -   **Username:** `buyer1`
    -   **Password:** `buyerpass`

You can also create new Seller or Buyer accounts directly from the user interface.

## Workflow

```mermaid
graph TD
    A[Start Application] --> B{User Logged In?};

    subgraph "Authentication"
        B -- No --> C[Display Login/Signup Page];
        C --> D{Choose Action};
        D -- Login --> E[Select Role: Manager, Seller, or Buyer];
        E --> F[Enter Credentials & Submit];
        F --> G[Login User];
        G --> H{Credentials Valid?};
        H -- Yes --> I[Set Session State & Rerun];
        H -- No --> J[Show Error Message];
        J --> C;

        D -- Signup --> K[Fill Signup Form for Buyer or Seller];
        K --> L[Create User];
        L --> M{Username Exists?};
        M -- No --> N[Create User in DB & Show Success];
        M -- Yes --> O[Show Error Message];
        N --> C;
        O --> K;
    end

    B -- Yes --> P[Display Main App];
    I --> P;

    subgraph "Main Application"
        P --> Q[Show Sidebar with User Info & Navigation];
        Q --> R{Select Navigation};
        R -- Dashboard --> S{Check User Role};
        R -- Price Estimator --> T[Price Estimator View];
        T --> U[Enter Car Details];
        U --> V[Predict Price with ML Model];
        V --> W[Display Estimated Price];
        W --> Q;

        S -- Manager --> X[Manager View];
        X --> X1[View Metrics, Charts, All Cars, All Transactions];
        X1 --> Q;

        S -- Seller --> Y[Seller View];
        Y --> Y1{Select Menu};
        Y1 -- Add Car --> Y2[Show Add Car Form];
        Y1 -- My Cars --> Y3[Show Seller's Cars];
        Y1 -- My Transactions --> Y4[Show Seller's Sales];
        Y2 --> Q;
        Y3 --> Q;
        Y4 --> Q;

        S -- Buyer --> Z[Buyer View];
        Z --> Z1[Filter & Search for Cars];
        Z1 --> Z2[Display Available Cars];
        Z2 --> Z3{Purchase Car?};
        Z3 -- Yes --> Z4[Purchase Car];
        Z4 --> Z5[Update DB & Show Success];
        Z5 --> Z1;
        Z3 -- No --> Q;
    end

    Q -- Logout --> AA[Clear Session State & Rerun];
    AA --> B;
