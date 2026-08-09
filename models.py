from extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='seeker')  # 'seeker' or 'provider'
    full_name = db.Column(db.String(100))
    profile_image = db.Column(db.String(200))
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    listings = db.relationship('Listing', backref='owner', lazy=True)
    services = db.relationship('Service', backref='provider', lazy=True)


class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(50))
    brand = db.Column(db.String(100))          # brand / type / model-year value used across filters
    clothing_type = db.Column(db.String(100))  # used by fashion/kids & fashion/preloved filters
    condition = db.Column(db.String(20), default='used')
    location = db.Column(db.String(100), nullable=False)
    images = db.Column(db.JSON)  # List of image URLs
    is_sold = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)  # gym, massage, tutoring
    subcategory = db.Column(db.String(50))
    brand = db.Column(db.String(100))  # e.g. "Automatic Transmission", used by auto-repair/tutoring filters
    service_type = db.Column(db.String(20), default='hourly')  # hourly, fixed, package
    hourly_rate = db.Column(db.Float)
    fixed_price = db.Column(db.Float)
    package_details = db.Column(db.JSON)
    availability = db.Column(db.JSON)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    seeker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    duration_hours = db.Column(db.Float, default=1.0)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    service = db.relationship('Service', backref='bookings')
    seeker = db.relationship('User', foreign_keys=[seeker_id])