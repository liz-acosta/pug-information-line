import sqlite3
from typing import Optional, Dict, Any
from config import settings

class CallDatabase:
    def __init__(self, db_path: str = "customer_calls.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the database schema and seed sample data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT UNIQUE NOT NULL,
                name TEXT,
                account_id TEXT,
                billing_info TEXT,
                support_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create call interactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS call_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                call_type TEXT NOT NULL,
                message TEXT,
                transcription TEXT,
                duration_seconds INTEGER,
                agent_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Seed sample customer data
        sample_customers = [
            ("15105550101", "Alice Johnson", "ACC001", 
             "Current plan: Premium, $49.99/month. Last payment: 2026-04-01",
             "Prefers email communication. Previously inquired about enterprise features."),
            ("14155550102", "Bob Smith", "ACC002",
             "Current plan: Standard, $19.99/month. Last payment: 2026-04-02",
             "New customer. Account created 2026-03-15. First-time user."),
            ("14155550103", "Carol White", "ACC003",
             "Current plan: Basic, $9.99/month. Last payment: 2026-04-03",
             "Loyal customer since 2025. Interested in API access."),
             (settings.your_phone_number, settings.your_name, "ACC004",
             "Current plan: Basic, $9.99/month. Last payment: 2026-04-03",
             "Loyal customer since 2025. Interested in API access.")
        ]
        
        for phone, name, account_id, billing, notes in sample_customers:
            cursor.execute('''
                INSERT OR IGNORE INTO customers 
                (phone_number, name, account_id, billing_info, support_notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (phone, name, account_id, billing, notes))
        
        conn.commit()
        conn.close()
    
    def get_customer_by_phone(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """Retrieve customer record by phone number."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM customers WHERE phone_number = ?
        ''', (phone_number,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def log_interaction(self, customer_id: int, call_type: str, 
                       message: str = None, transcription: str = None, 
                       agent_name: str = None, duration: int = 0) -> int:
        """Log a call interaction to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO call_interactions 
            (customer_id, call_type, message, transcription, agent_name, duration_seconds)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (customer_id, call_type, message, transcription, agent_name, duration))
        
        conn.commit()
        interaction_id = cursor.lastrowid
        conn.close()
        
        return interaction_id
    
    def get_customer_history(self, customer_id: int) -> list:
        """Retrieve call history for a customer."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM call_interactions 
            WHERE customer_id = ? 
            ORDER BY created_at DESC 
            LIMIT 10
        ''', (customer_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]

    def insert_customer_and_log_interaction(self, phone_number: str,
                                            call_type: str,
                                            name: str = None, 
                                            account_id: str = None, 
                                            billing_info: str = None, 
                                            support_notes: str = None,
                                            message: str = None, 
                                            transcription: str = None,
                                            agent_name: str = None, 
                                            duration: int = 0) -> Dict[str, Any]:
        """Insert a new customer and log their initial interaction."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert the customer
            cursor.execute('''
                INSERT INTO customers 
                (phone_number, name, account_id, billing_info, support_notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (phone_number, name, account_id, billing_info, support_notes))
            
            customer_id = cursor.lastrowid
            
            # Log the interaction
            cursor.execute('''
                INSERT INTO call_interactions 
                (customer_id, call_type, message, transcription, agent_name, duration_seconds)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (customer_id, call_type, message, transcription, agent_name, duration))
            
            interaction_id = cursor.lastrowid
            
            conn.commit()
            
            return {
                "customer_id": customer_id,
                "interaction_id": interaction_id,
                "phone_number": phone_number,
                "name": name
            }
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise ValueError(f"Failed to insert customer: {e}")
        finally:
            conn.close()

# Global database instance
db = CallDatabase()
