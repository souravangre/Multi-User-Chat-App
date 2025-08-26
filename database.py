from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import bcrypt

# Create base class for models
Base = declarative_base()

class User(Base):
    """User model for the chat application"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    def __repr__(self):
        return f"<User(username='{self.username}')>"

class DatabaseHandler:
    def __init__(self, db_path="sqlite:///chat_users.db"):
        """Initialize database with SQLAlchemy"""
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        
        # Create session factory
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        print("✅ Database initialized with SQLAlchemy")
    
    def register_user(self, username, password):
        """Register a new user with hashed password"""
        try:
            # Validate input
            if not username or not password:
                return False, "Username and password cannot be empty"
            
            if len(username) < 3:
                return False, "Username must be at least 3 characters long"
            
            if len(password) < 6:
                return False, "Password must be at least 6 characters long"
            
            # Check if user already exists
            existing_user = self.session.query(User).filter_by(username=username).first()
            if existing_user:
                return False, "Username already exists"
            
            # Hash the password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Create new user
            new_user = User(
                username=username,
                password_hash=password_hash
            )
            
            # Add and commit to database
            self.session.add(new_user)
            self.session.commit()
            
            print(f"✅ User '{username}' registered successfully")
            return True, "Registration successful"
            
        except Exception as e:
            self.session.rollback()
            print(f"❌ Registration error: {e}")
            return False, "Registration failed"
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        try:
            # Find user by username
            user = self.session.query(User).filter_by(username=username).first()
            
            if not user:
                return False, "Username not found"
            
            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
                # Update last login
                user.last_login = datetime.utcnow()
                self.session.commit()
                
                print(f"✅ User '{username}' authenticated successfully")
                return True, "Login successful"
            else:
                return False, "Invalid password"
                
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False, "Authentication failed"
    
    def user_exists(self, username):
        """Check if username exists"""
        try:
            user = self.session.query(User).filter_by(username=username).first()
            return user is not None
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False
    
    def get_user_stats(self):
        """Get basic user statistics"""
        try:
            total_users = self.session.query(User).count()
            
            # Get recent registrations (last 7 days)
            week_ago = datetime.utcnow().replace(day=datetime.utcnow().day - 7)
            recent_users = self.session.query(User).filter(
                User.created_at >= week_ago
            ).count()
            
            return {
                "total_users": total_users,
                "recent_users": recent_users
            }
            
        except Exception as e:
            print(f"❌ Stats error: {e}")
            return {"total_users": 0, "recent_users": 0}
    
    def get_all_users(self):
        """Get all users (for admin purposes)"""
        try:
            users = self.session.query(User).all()
            return [(user.username, user.created_at) for user in users]
        except Exception as e:
            print(f"❌ Error fetching users: {e}")
            return []
    
    def close(self):
        """Close database session"""
        if self.session:
            self.session.close()
            print("🔒 Database session closed")

# Test the database functionality
if __name__ == "__main__":
    # Test the database handler
    db = DatabaseHandler()
    
    print("🧪 Testing SQLAlchemy Database Handler...")
    
    # Test registration
    success, msg = db.register_user("testuser", "password123")
    print(f"Registration: {success} - {msg}")
    
    # Test duplicate registration
    success, msg = db.register_user("testuser", "password456")
    print(f"Duplicate registration: {success} - {msg}")
    
    # Test authentication
    success, msg = db.authenticate_user("testuser", "password123")
    print(f"Correct login: {success} - {msg}")
    
    # Test wrong password
    success, msg = db.authenticate_user("testuser", "wrongpassword")
    print(f"Wrong password: {success} - {msg}")
    
    # Test stats
    stats = db.get_user_stats()
    print(f"Stats: {stats}")
    
    # Test getting all users
    users = db.get_all_users()
    print(f"All users: {users}")
    
    # Close database
    db.close()
    
    print("✅ SQLAlchemy database tests completed!")