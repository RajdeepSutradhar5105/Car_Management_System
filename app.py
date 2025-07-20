import streamlit as st
import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.exceptions import NotFittedError
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(
    page_title="Car Management System", 
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Modern Styling ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Card Styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    /* Login Card Styling */
    .login-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border: 1px solid #e5e7eb;
    }
    
    .role-header {
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f3f4f6;
    }
    
    .role-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    
    /* Table Styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 8px;
        padding: 1rem;
        color: white;
    }
    
    .stError {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        border-radius: 8px;
        padding: 1rem;
        color: white;
    }
    
    /* Form Styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Price Estimator Styling */
    .price-result {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
    }
    
    .price-amount {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    /* Car Card Styling */
    .car-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .car-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .car-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .car-price {
        font-size: 1.8rem;
        font-weight: 700;
        color: #10b981;
        margin-bottom: 1rem;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    .status-available {
        background: #dcfce7;
        color: #166534;
    }
    
    .status-sold {
        background: #fee2e2;
        color: #991b1b;
    }
</style>
""", unsafe_allow_html=True)

# --- Database Connection (Your existing function) ---
def get_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="car_management_system"
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error connecting to database: {err}")
        return None

# --- Machine Learning Model (Your existing function) ---
@st.cache_resource
def train_price_prediction_model():
    """
    Fetches car data, trains a price prediction model, and caches it.
    Returns the trained model pipeline.
    """
    conn = get_db_connection()
    if not conn:
        return None
    query = "SELECT make, model, year, price FROM cars"
    df = pd.read_sql(query, conn)
    conn.close()
    if len(df) < 5:
        return None
    X = df[['make', 'model', 'year']]
    y = df['price']
    categorical_features = ['make', 'model']
    numerical_features = ['year']
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough'
    )
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])
    model.fit(X, y)
    return model

# --- User Authentication Functions (Your existing functions) ---
def login_user(username, password, role):
    """
    Authenticates a user by checking the specific table for their role.
    Returns user details.
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    table_map = {'manager': 'managers', 'seller': 'sellers', 'buyer': 'buyers'}
    if role not in table_map:
        return None
        
    table_name = table_map[role]
    
    cursor = conn.cursor(dictionary=True)
    query = f"SELECT *, '{role}' as role FROM {table_name} WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return user

def create_user(username, password, role):
    """Creates a new user in the appropriate table (sellers or buyers)."""
    conn = get_db_connection()
    if not conn:
        return False
    
    table_map = {'seller': 'sellers', 'buyer': 'buyers'}
    if role not in table_map:
        st.error("Invalid role specified for account creation.")
        return False
        
    table_name = table_map[role]
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username FROM managers WHERE username = %s UNION SELECT username FROM sellers WHERE username = %s UNION SELECT username FROM buyers WHERE username = %s", (username, username, username))
        if cursor.fetchone():
            st.error("Username already exists. Please choose a different one.")
            return False
        
        cursor.execute(
            f"INSERT INTO {table_name} (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        st.success("Account created successfully! You can now log in.")
        return True
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# --- Manager Functions (Your existing functions) ---
def view_all_cars():
    """Fetches all cars, joining with the sellers table."""
    conn = get_db_connection()
    if conn:
        query = """
            SELECT c.id, c.make, c.model, c.year, c.price, c.status, s.username as seller
            FROM cars c
            LEFT JOIN sellers s ON c.seller_id = s.id
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    return pd.DataFrame()

def view_all_transactions():
    """Fetches all transactions, joining with sellers and buyers tables."""
    conn = get_db_connection()
    if conn:
        query = """
            SELECT t.id, c.make, c.model, b.username as buyer, s.username as seller, t.sale_price, t.transaction_date
            FROM transactions t
            LEFT JOIN cars c ON t.car_id = c.id
            LEFT JOIN buyers b ON t.buyer_id = b.id
            LEFT JOIN sellers s ON t.seller_id = s.id
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    return pd.DataFrame()

# --- Seller Functions (Your existing functions) ---
def add_car(make, model, year, price, seller_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cars (make, model, year, price, seller_id) VALUES (%s, %s, %s, %s, %s)",
            (make, model, year, price, seller_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        st.success("🎉 Car added successfully!")

def view_seller_cars(seller_id):
    conn = get_db_connection()
    if conn:
        query = "SELECT id, make, model, year, price, status FROM cars WHERE seller_id = %s"
        df = pd.read_sql(query, conn, params=(seller_id,))
        conn.close()
        return df
    return pd.DataFrame()

def view_seller_transactions(seller_id):
    """Fetches seller transactions, joining with the buyers table."""
    conn = get_db_connection()
    if conn:
        query = """
            SELECT t.id, c.make, c.model, b.username as buyer, t.sale_price, t.transaction_date
            FROM transactions t
            LEFT JOIN cars c ON t.car_id = c.id
            LEFT JOIN buyers b ON t.buyer_id = b.id
            WHERE t.seller_id = %s
        """
        df = pd.read_sql(query, conn, params=(seller_id,))
        conn.close()
        return df
    return pd.DataFrame()

# --- Buyer Functions (Your existing functions) ---
def search_available_cars(make="", model="", min_price=0, max_price=9999999):
    conn = get_db_connection()
    if conn:
        query = "SELECT id, make, model, year, price FROM cars WHERE status = 'available' AND make LIKE %s AND model LIKE %s AND price BETWEEN %s AND %s"
        df = pd.read_sql(query, conn, params=(f"%{make}%", f"%{model}%", min_price, max_price))
        conn.close()
        return df
    return pd.DataFrame()

def purchase_car(car_id, buyer_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cars WHERE id = %s AND status = 'available'", (car_id,))
        car = cursor.fetchone()
        if car:
            cursor.execute("UPDATE cars SET status = 'sold' WHERE id = %s", (car_id,))
            cursor.execute(
                "INSERT INTO transactions (car_id, buyer_id, seller_id, sale_price) VALUES (%s, %s, %s, %s)",
                (car['id'], buyer_id, car['seller_id'], car['price'])
            )
            conn.commit()
            st.success("🎉 Purchase successful! The car is now yours.")
        else:
            st.error("❌ Car is not available for purchase or does not exist.")
        cursor.close()
        conn.close()

# --- Enhanced UI Functions ---
def create_metric_card(value, label, icon="📊"):
    st.markdown(f"""
    <div class="metric-card">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 2rem; margin-right: 1rem;">{icon}</span>
            <div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_car_card(car_data, show_purchase_button=False, buyer_id=None):
    status_class = "status-available" if car_data.get('status', 'available') == 'available' else "status-sold"
    status_text = car_data.get('status', 'available').title()
    
    card_html = f"""
    <div class="car-card">
        <div class="car-title">🚗 {car_data['make']} {car_data['model']}</div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div class="car-price">${car_data['price']:,.2f}</div>
            <span class="status-badge {status_class}">{status_text}</span>
        </div>
        <div style="color: #6b7280; margin-bottom: 1rem;">
            📅 Year: {car_data['year']}
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    if show_purchase_button and car_data.get('status', 'available') == 'available':
        if st.button(f"🛒 Purchase Car ID: {car_data['id']}", key=f"buy_{car_data['id']}"):
            purchase_car(car_data['id'], buyer_id)
            st.rerun()

# --- Main Application ---
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚗 Car Management System</h1>
        <p>Manage your automotive business with modern elegance</p>
    </div>
    """, unsafe_allow_html=True)

    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        # Login/Signup Interface
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("## 🔐 Login to Your Account")
            
            # Manager Login
            with st.expander("👑 Manager Login", expanded=False):
                st.markdown('<div class="role-header"><div class="role-icon">👑</div><h3>Manager Portal</h3><p>Complete system oversight and management</p></div>', unsafe_allow_html=True)
                manager_user = st.text_input("Manager Username", key="manager_user", placeholder="Enter your username")
                manager_pass = st.text_input("Manager Password", type="password", key="manager_pass", placeholder="Enter your password")
                if st.button("🚀 Login as Manager", key="manager_login"):
                    user = login_user(manager_user, manager_pass, "manager")
                    if user:
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("❌ Invalid manager credentials.")

            # Seller Login
            with st.expander("🏪 Seller Login", expanded=False):
                st.markdown('<div class="role-header"><div class="role-icon">🏪</div><h3>Seller Portal</h3><p>Manage your car inventory and sales</p></div>', unsafe_allow_html=True)
                seller_user = st.text_input("Seller Username", key="seller_user", placeholder="Enter your username")
                seller_pass = st.text_input("Seller Password", type="password", key="seller_pass", placeholder="Enter your password")
                if st.button("🚀 Login as Seller", key="seller_login"):
                    user = login_user(seller_user, seller_pass, "seller")
                    if user:
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("❌ Invalid seller credentials.")

            # Buyer Login
            with st.expander("🛒 Buyer Login", expanded=False):
                st.markdown('<div class="role-header"><div class="role-icon">🛒</div><h3>Buyer Portal</h3><p>Find and purchase your perfect car</p></div>', unsafe_allow_html=True)
                buyer_user = st.text_input("Buyer Username", key="buyer_user", placeholder="Enter your username")
                buyer_pass = st.text_input("Buyer Password", type="password", key="buyer_pass", placeholder="Enter your password")
                if st.button("🚀 Login as Buyer", key="buyer_login"):
                    user = login_user(buyer_user, buyer_pass, "buyer")
                    if user:
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("❌ Invalid buyer credentials.")

        with col2:
            st.markdown("## 📝 Create New Account")
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            
            with st.form("signup_form"):
                st.markdown("### Join Our Platform")
                new_username = st.text_input("Choose a Username", placeholder="Enter a unique username")
                new_password = st.text_input("Choose a Password", type="password", placeholder="Create a secure password")
                role = st.selectbox("I am a:", ["Buyer", "Seller"], key="role_select")
                submitted = st.form_submit_button("✨ Create Account")
                
                if submitted:
                    if new_username and new_password and role:
                        create_user(new_username, new_password, role.lower())
                    else:
                        st.warning("⚠️ Please fill in all fields.")
            
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        user = st.session_state.user
        
        # Sidebar
        with st.sidebar:
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); border-radius: 15px; margin-bottom: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">
                    {'👑' if user['role'] == 'manager' else '🏪' if user['role'] == 'seller' else '🛒'}
                </div>
                <h2 style="color: white; margin-bottom: 0.5rem;">Welcome!</h2>
                <h3 style="color: rgba(255,255,255,0.9); margin-bottom: 0.5rem;">{user['username']}</h3>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">{user['role'].title()}</p>
            </div>
            """, unsafe_allow_html=True)
            
            page = st.radio("🧭 Navigation", ["📊 Dashboard", "💰 Price Estimator"], label_visibility="collapsed")
            
            st.markdown("---")
            if st.button("🚪 Logout", key="logout_btn"):
                st.session_state.user = None
                st.rerun()

        # Main Content
        if "Dashboard" in page:
            if user['role'] == 'manager':
                manager_view()
            elif user['role'] == 'seller':
                seller_view(user['id'])
            elif user['role'] == 'buyer':
                buyer_view(user['id'])
        elif "Price Estimator" in page:
            price_estimator_view()

def price_estimator_view():
    st.markdown("## 🤖 AI-Powered Car Price Estimator")
    st.markdown("Get accurate market price estimates using machine learning")
    
    model = train_price_prediction_model()
    if model is None:
        st.warning("⚠️ The price estimator is not yet available. More car data is needed in the system to train the model.")
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Enter Car Details")
        with st.form("estimator_form"):
            make = st.text_input("🏭 Make", placeholder="e.g., Toyota")
            model_input = st.text_input("🚗 Model", placeholder="e.g., Camry")
            year = st.number_input("📅 Year", min_value=1980, max_value=2025, step=1, value=2020)
            submitted = st.form_submit_button("🔮 Predict Price")
            
            if submitted:
                if make and model_input and year:
                    input_data = pd.DataFrame({'make': [make], 'model': [model_input], 'year': [year]})
                    try:
                        predicted_price = model.predict(input_data)[0]
                        st.session_state.predicted_price = predicted_price
                        st.session_state.predicted_car = f"{year} {make} {model_input}"
                    except NotFittedError:
                        st.error("❌ Model is not fitted yet. Please add more data.")
                    except Exception as e:
                        st.error(f"❌ An error occurred during prediction: {e}")
                else:
                    st.warning("⚠️ Please fill in all fields to get a prediction.")
    
    with col2:
        st.markdown("### 💰 Price Estimate")
        if hasattr(st.session_state, 'predicted_price'):
            st.markdown(f"""
            <div class="price-result">
                <div class="price-amount">${st.session_state.predicted_price:,.2f}</div>
                <p>Estimated market value for</p>
                <h4>{st.session_state.predicted_car}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("💡 This estimate is based on market data and machine learning models. Actual prices may vary based on condition, mileage, and local market factors.")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: #6b7280;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🔮</div>
                <p>Enter car details and click "Predict Price" to get an AI-powered estimate</p>
            </div>
            """, unsafe_allow_html=True)

def manager_view():
    st.markdown("## 👑 Manager Dashboard")
    st.markdown("Complete system overview and analytics")
    
    # Get data
    cars_df = view_all_cars()
    transactions_df = view_all_transactions()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card(len(cars_df), "Total Cars", "🚗")
    
    with col2:
        available_cars = len(cars_df[cars_df['status'] == 'available']) if not cars_df.empty else 0
        create_metric_card(available_cars, "Available Cars", "✅")
    
    with col3:
        total_revenue = transactions_df['sale_price'].sum() if not transactions_df.empty else 0
        create_metric_card(f"${total_revenue:,.0f}", "Total Revenue", "💰")
    
    with col4:
        create_metric_card(len(transactions_df), "Transactions", "📊")
    
    # Charts
    if not cars_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Cars by Status")
            status_counts = cars_df['status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index, 
                        color_discrete_sequence=['#10b981', '#ef4444'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🏭 Cars by Make")
            make_counts = cars_df['make'].value_counts().head(10)
            fig = px.bar(x=make_counts.values, y=make_counts.index, orientation='h',
                        color_discrete_sequence=['#667eea'])
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
    
    # Tables
    st.markdown("### 🚗 All Cars")
    if not cars_df.empty:
        st.dataframe(cars_df, use_container_width=True)
    else:
        st.info("No cars found in the system.")
    
    st.markdown("### 💳 All Transactions")
    if not transactions_df.empty:
        st.dataframe(transactions_df, use_container_width=True)
    else:
        st.info("No transactions found in the system.")

def seller_view(seller_id):
    st.markdown("## 🏪 Seller Dashboard")
    st.markdown("Manage your inventory and track your sales")
    
    # Get seller data
    seller_cars_df = view_seller_cars(seller_id)
    seller_transactions_df = view_seller_transactions(seller_id)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_metric_card(len(seller_cars_df), "My Cars", "🚗")
    
    with col2:
        available = len(seller_cars_df[seller_cars_df['status'] == 'available']) if not seller_cars_df.empty else 0
        create_metric_card(available, "Available", "✅")
    
    with col3:
        revenue = seller_transactions_df['sale_price'].sum() if not seller_transactions_df.empty else 0
        create_metric_card(f"${revenue:,.0f}", "Revenue", "💰")
    
    # Menu
    menu = st.selectbox("📋 Menu", ["➕ Add Car", "🚗 My Cars", "💳 My Transactions"])
    
    if menu == "➕ Add Car":
        st.markdown("### ➕ Add a New Car for Sale")
        with st.form("add_car_form"):
            col1, col2 = st.columns(2)
            with col1:
                make = st.text_input("🏭 Make", placeholder="e.g., Toyota")
                year = st.number_input("📅 Year", min_value=1900, max_value=2025, step=1, value=2020)
            with col2:
                model = st.text_input("🚗 Model", placeholder="e.g., Camry")
                price = st.number_input("💰 Price ($)", min_value=0.0, format="%.2f", value=25000.0)
            
            submitted = st.form_submit_button("✨ Add Car to Inventory")
            if submitted:
                if make and model and year and price > 0:
                    add_car(make, model, year, price, seller_id)
                    st.rerun()
                else:
                    st.warning("⚠️ Please fill in all fields.")
    
    elif menu == "🚗 My Cars":
        st.markdown("### 🚗 My Car Inventory")
        if not seller_cars_df.empty:
            st.dataframe(seller_cars_df, use_container_width=True)
        else:
            st.info("You haven't added any cars yet. Use the 'Add Car' section to list your first car!")
    
    elif menu == "💳 My Transactions":
        st.markdown("### 💳 My Sales History")
        if not seller_transactions_df.empty:
            st.dataframe(seller_transactions_df, use_container_width=True)
        else:
            st.info("No sales yet. Keep promoting your cars!")

def buyer_view(buyer_id):
    st.markdown("## 🛒 Buyer Dashboard")
    st.markdown("Find and purchase your perfect car")
    
    # Search Filters
    st.markdown("### 🔍 Search Filters")
    with st.expander("🎛️ Filter Options", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            make_search = st.text_input("🏭 Filter by Make", placeholder="e.g., Toyota")
        with col2:
            model_search = st.text_input("🚗 Filter by Model", placeholder="e.g., Camry")
        with col3:
            min_price_search = st.number_input("💰 Min Price", min_value=0, value=0)
        with col4:
            max_price_search = st.number_input("💰 Max Price", min_value=0, value=1000000)
    
    # Search for cars
    available_cars_df = search_available_cars(make_search, model_search, min_price_search, max_price_search)
    
    st.markdown(f"### 🚗 Available Cars ({len(available_cars_df)} found)")
    
    if not available_cars_df.empty:
        # Display cars in a grid
        for i in range(0, len(available_cars_df), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(available_cars_df):
                    car = available_cars_df.iloc[i + j]
                    with col:
                        create_car_card(car.to_dict(), show_purchase_button=True, buyer_id=buyer_id)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #6b7280;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🔍</div>
            <h3>No cars found matching your criteria</h3>
            <p>Try adjusting your search filters to find more options</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
