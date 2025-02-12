import streamlit as st
import pandas as pd
import hashlib

# Load customer data from the CSV file
@st.cache_data
def load_data():
    # Load customer data from 'customer.csv'
    df = pd.read_csv('customer.csv')  # Read from CSV file
    return df

# Save updated customer data to the CSV file
def save_data(df):
    df.to_csv('customer.csv', index=False)  # Save as CSV

# Hash password function for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Authenticate user login
def authenticate_user(customer_id, password, df):
    # Check if customer_id exists in the data and validate password
    if customer_id in df['Customer_ID'].values:
        stored_password = df[df['Customer_ID'] == customer_id]['Password'].values[0]
        if stored_password == hash_password(password):
            return True
    return False

# Add a new customer (Sign Up)
def add_new_customer(customer_id, password, name, age, tenure, current_plan, df):
    new_data = {
        'Customer_ID': customer_id,
        'Password': hash_password(password),
        'Name': name,
        'Age': age,
        'Tenure': tenure,
        'Current_Plan': current_plan
    }
    df = df.append(new_data, ignore_index=True)
    save_data(df)

# Recommendation based on Age
def recommend_plan(age):
    if age < 30:
        return "Youth Plan"
    elif 30 <= age < 50:
        return "Family Plan"
    else:
        return "Senior Plan"

# Main function to render the Streamlit app
def main():
    # Set the title of the web app
    st.title("Customer Insurance Management App")
    
    # Load customer data from CSV
    df = load_data()

    # Login Page
    login = st.sidebar.selectbox("Select an option", ["Login", "Sign Up"])
    
    if login == "Login":
        st.subheader("Login to Your Account")
        customer_id = st.text_input("Customer ID")
        password = st.text_input("Password", type='password')
        
        if st.button("Login"):
            if authenticate_user(customer_id, password, df):
                st.success(f"Logged in successfully as Customer ID: {customer_id}")
                
                # Fetch customer details after login
                customer_data = df[df['Customer_ID'] == customer_id].iloc[0]
                
                st.subheader("Customer Profile")
                st.write(f"Name: {customer_data['Name']}")
                st.write(f"Age: {customer_data['Age']}")
                st.write(f"Tenure: {customer_data['Tenure']} years")
                st.write(f"Current Insurance Plan: {customer_data['Current_Plan']}")
                
                # Insurance Plan Recommendation
                recommended_plan = recommend_plan(customer_data['Age'])
                st.write(f"Recommended Insurance Plan: {recommended_plan}")
                
                # Feedback Page
                feedback = st.text_area("Provide your feedback here")
                if st.button("Submit Feedback"):
                    st.write("Feedback submitted successfully!")
                    # You can save the feedback to the database or file
                
                # Customer Care Page
                st.subheader("Customer Care")
                st.write("For any issues, please reach out to our support team at support@insurance.com.")
                
                # Current Running Plan
                st.subheader("Current Running Plan")
                st.write(f"Your current running plan is: {customer_data['Current_Plan']}")
                
            else:
                st.error("Invalid Customer ID or Password")
    
    elif login == "Sign Up":
        st.subheader("Sign Up to Create a New Account")
        
        customer_id = st.text_input("Enter a new Customer ID")
        if customer_id in df['Customer_ID'].values:
            st.error("Customer ID already exists. Please choose a different ID.")
        else:
            name = st.text_input("Name")
            password = st.text_input("Choose a Password", type='password')
            confirm_password = st.text_input("Confirm Password", type='password')
            age = st.number_input("Age", min_value=18)
            tenure = st.number_input("Tenure (in years)", min_value=0)
            current_plan = st.selectbox("Select Insurance Plan", ["Basic", "Premium", "Standard"])

            if password == confirm_password:
                if st.button("Sign Up"):
                    # Add the new customer to the database
                    add_new_customer(customer_id, password, name, age, tenure, current_plan, df)
                    st.success("Account created successfully! You can now log in.")
            else:
                st.error("Passwords do not match.")
    
# Run the app
if __name__ == "__main__":
    main()
