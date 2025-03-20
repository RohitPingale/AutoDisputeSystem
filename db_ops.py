import sqlite3

def init_database(name):
        conn = sqlite3.connect(f'{name}.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS disputes (
            reference_number TEXT UNIQUE,
            transaction_id TEXT,
            customer_id TEXT,
            amount REAL,
            description TEXT,
            account_age_years INTEGER,
            previous_disputes INTEGER,
            is_premium_customer INTEGER,
            account_balance REAL,
            category TEXT,
            priority TEXT,
            assigned_team TEXT,
            recommendation TEXT
            )
        ''')
    
        conn.commit()
        return conn

def dispute_to_db(conn, dispute_data,category,  priority, team, unique_ref, recommendation):
    """Save dispute data to the database"""
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO disputes (
            reference_number, transaction_id, customer_id, amount, description,
            account_age_years, previous_disputes, is_premium_customer, account_balance,
            category, assigned_team, recommendation,
            priority
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        unique_ref,
        dispute_data.transaction_id,
        dispute_data.customer_id,
        dispute_data.amount,
        dispute_data.description,
        dispute_data.acc_opened_years,
        dispute_data.previous_disputes,
        1 if dispute_data.is_premium else 0, 
        dispute_data.acc_balance,
        
        category,
        team,
        recommendation,
        priority
    ))
    
    conn.commit()
    return cursor.lastrowid