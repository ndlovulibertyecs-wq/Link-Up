from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from extensions import db
from models import User, Listing, Service, Booking
from sqlalchemy import or_

# ============ BLUEPRINTS DEFINITIONS ============
main_bp = Blueprint('main', __name__)
marketplace_bp = Blueprint('marketplace', __name__, url_prefix='/marketplace')
services_bp = Blueprint('services', __name__, url_prefix='/services')
hire_bp = Blueprint('hire', __name__, url_prefix='/hire')
farmers_bp = Blueprint('farmers', __name__, url_prefix='/farmers')
machinery_bp = Blueprint('machinery', __name__, url_prefix='/machinery')
construction_bp = Blueprint('construction', __name__, url_prefix='/construction')
housing_bp = Blueprint('housing', __name__, url_prefix='/housing')
listings_bp = Blueprint('listings', __name__, url_prefix='/listings')

# ============ LISTINGS BLUEPRINT ============
@listings_bp.route('/marketcenter')
def marketcenter():
    return render_template('listings.marketcenter.html')

@listings_bp.route('/servicehub')
def servicehub():
    return render_template('listings.servicehub.html')

@listings_bp.route('/hirezone')
def hirezone():
    return render_template('listings.hirezone.html')

@listings_bp.route('/housing')
def housing():
    return render_template('listings.housing.html')

@listings_bp.route('/farmersroom')
def farmersroom():
    return render_template('listings.farmersroom.html')

@listings_bp.route('/adverts')
def adverts():
    return render_template('listings.adverts.html')

@listings_bp.route('/jobsgigs')
def jobsgigs():
    return render_template('listings.jobsgigs.html')

@listings_bp.route('/events')
def events():
    return render_template('listings.events.html')

@listings_bp.route('/community')
def community():
    return render_template('listings.community.html')

# Adverts Hub Blueprints
adverts_bp = Blueprint('adverts', __name__, url_prefix='/adverts')
business_ads_bp = Blueprint('business_ads', __name__, url_prefix='/adverts/business-ads')
event_promotion_bp = Blueprint('event_promotion', __name__, url_prefix='/adverts/event-promotion')
product_launch_bp = Blueprint('product_launch', __name__, url_prefix='/adverts/product-launch')
sales_discounts_bp = Blueprint('sales_discounts', __name__, url_prefix='/adverts/sales-discounts')
food_beverage_bp = Blueprint('food_beverage', __name__, url_prefix='/adverts/food-beverage')

# Jobs, Events, Community Blueprints
jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')
events_bp = Blueprint('events', __name__, url_prefix='/events')
community_bp = Blueprint('community', __name__, url_prefix='/community')

# Concerts Blueprint (no url_prefix, routes start with /concerts)
concerts_bp = Blueprint('concerts', __name__)

# ============ AUTH ROUTES ============
@main_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    """Sign in page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        role = request.form.get('role')
        
        flash('Signed in successfully!')
        
        if role == 'host':
            return redirect(url_for('main.hostdashboard'))
        else:
            return redirect(url_for('main.dashboard'))

    return render_template('signin.html')


@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign up page"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        flash('Account created successfully! Please sign in.')
        return redirect(url_for('main.signin'))

    return render_template('signup.html')


@services_bp.route('/home-service')
def home_service():
    return render_template('home_service.html')


@main_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page"""
    if request.method == 'POST':
        email = request.form.get('email')
        flash('Password reset instructions sent to your email!')
        return redirect(url_for('main.signin'))

    return render_template('forgot_password.html')


@main_bp.route('/host/dashboard')
def hostdashboard():
    return render_template('host_dashboard.html')


@main_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('search_results.html', query='', listings=[], services=[])

    listings = Listing.query.filter(
        or_(
            Listing.title.ilike(f'%{query}%'),
            Listing.description.ilike(f'%{query}%'),
            Listing.category.ilike(f'%{query}%'),
            Listing.subcategory.ilike(f'%{query}%'),
            Listing.brand.ilike(f'%{query}%'),
            Listing.location.ilike(f'%{query}%')
        ),
        Listing.is_active == True
    ).limit(50).all()

    services = Service.query.filter(
        or_(
            Service.title.ilike(f'%{query}%'),
            Service.description.ilike(f'%{query}%'),
            Service.category.ilike(f'%{query}%'),
            Service.subcategory.ilike(f'%{query}%'),
            Service.location.ilike(f'%{query}%')
        ),
        Service.is_active == True
    ).limit(50).all()

    return render_template('search_results.html',
                           query=query,
                           listings=listings,
                           services=services)

@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ============ HIRE ZONE ROUTES ============
@hire_bp.route('/')
def hire_home():
    """Main hire zone page"""
    return render_template('hire.hire_home.html')


@hire_bp.route('/personnel-hiring')
def personnel_hiring():
    """Personnel hiring page"""
    return render_template('hire.personnel_hiring.html')

# ============ PERSONNEL HIRING – SUBCATEGORY ROUTES ============

@hire_bp.route('/admin-staff')
def admin_staff():
    selected_brand = request.args.get('brand', '')
    brands = ['Executive Assistant', 'Receptionist', 'Office Manager', 'Data Entry', 'Administrative Clerk']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Admin Staff',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('person.admin_staff.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@hire_bp.route('/customer-service')
def customer_service():
    selected_brand = request.args.get('brand', '')
    brands = ['Call Center', 'Customer Support Rep', 'Help Desk', 'Client Relations', 'Technical Support']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Customer Service',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('person.customer_service.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@hire_bp.route('/sales-marketing')
def sales_marketing():
    selected_brand = request.args.get('brand', '')
    brands = ['Sales Rep', 'Account Manager', 'Digital Marketer', 'SEO Specialist', 'Social Media Manager']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Sales & Marketing',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('person.sales_marketing.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@hire_bp.route('/accounting-finance')
def accounting_finance():
    selected_brand = request.args.get('brand', '')
    brands = ['Accountant', 'Bookkeeper', 'Financial Analyst', 'Tax Preparer', 'Auditor', 'Payroll Specialist']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Accounting & Finance',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('person.accounting_finance.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@hire_bp.route('/human-resources')
def human_resources():
    selected_brand = request.args.get('brand', '')
    brands = ['HR Generalist', 'Recruiter', 'Payroll Admin', 'Training Coordinator', 'HR Assistant']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Human Resources',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('person.human_resources.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@hire_bp.route('/skilled-trades')
def skilled_trades():
    selected_brand = request.args.get('brand', '')
    brands = ['Electrician', 'Plumber', 'Welder', 'Carpenter', 'Mechanic', 'HVAC Tech']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Skilled Trades',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('person.skilled_trades.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@hire_bp.route('/healthcare')
def healthcare():
    selected_brand = request.args.get('brand', '')
    brands = ['Nurse', 'Medical Assistant', 'Caregiver', 'Pharmacist', 'Therapist', 'Home Health Aide']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Healthcare',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('person.healthcare.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)

@hire_bp.route('/ittech')
def ittech():
    selected_brand = request.args.get('brand', '')
    brands = [
        # Hardware
        'Hardware Technician', 'PC Repair', 'Server Maintenance', 'Printer Support',
        # Software
        'Software Developer', 'Web Developer', 'Mobile App Developer', 'DevOps Engineer',
        'QA Tester', 'Database Administrator',
        # Cybersecurity
        'Cybersecurity Analyst', 'Penetration Tester', 'Security Engineer', 'Compliance Specialist',
        # Networking
        'Network Administrator', 'Network Engineer', 'IT Support Specialist', 'Help Desk',
        # Cloud
        'Cloud Architect', 'Cloud Engineer', 'AWS Specialist', 'Azure Specialist', 'Google Cloud',
        # Data
        'Data Scientist', 'Data Analyst', 'Business Intelligence', 'Machine Learning Engineer',
        # Other
        'IT Consultant', 'Systems Administrator', 'ERP Specialist', 'CRM Specialist'
    ]
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='IT & Tech',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('hire.ittech.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@hire_bp.route('/hospitality')
def hospitality():
    selected_brand = request.args.get('brand', '')
    brands = ['Chef', 'Waiter', 'Bartender', 'Hotel Receptionist', 'Housekeeper', 'Event Coordinator']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Hospitality',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('person.hospitality.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@hire_bp.route('/education')
def education():
    selected_brand = request.args.get('brand', '')
    brands = ['Teacher', 'Tutor', 'Instructor', 'Professor', 'Teaching Assistant', 'Curriculum Developer']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Education',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('person.education.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@hire_bp.route('/home-helpers')
def home_helpers():
    selected_brand = request.args.get('brand', '')
    brands = ['Cleaner', 'Nanny', 'Elderly Care', 'Pet Sitter', 'Gardener', 'Personal Assistant']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Home Helpers',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('person.home_helpers.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)

#========CAR HIRE==============
@hire_bp.route('/car-hire')
def car_hire():
    """Car hire page"""
    return render_template('hire.car_hire.html')

# ============ CAR HIRE SUBCATEGORIES ============

@hire_bp.route('/car-hire/economy')
def carhire_economy():
    selected_brand = request.args.get('brand', '')
    brands = ['Toyota', 'Honda', 'Hyundai', 'Kia', 'Nissan', 'Ford', 'Volkswagen']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Car Hire - Economy',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('car.economy.html',  # or whatever your template name is
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@hire_bp.route('/car-hire/commercial')
def carhire_commercial():
    selected_brand = request.args.get('brand', '')
    brands = ['Below 1 tonne ', '1-3 tonne', '5 tonne', '10 tonne', '15 tonne', '30 tonne & Above']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Car Hire - Commercial',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('car.trucks.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@hire_bp.route('/car-hire/caravans')
def carhire_caravans():
    selected_brand = request.args.get('brand', '')
    brands = []
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Car Hire - Caravans',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('car.caravans.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@hire_bp.route('/car-hire/luxury')
def carhire_luxury():
    selected_brand = request.args.get('brand', '')
    brands = ['BMW', 'Mercedes-Benz', 'Audi', 'Lexus', 'Jaguar', 'Porsche', 'Rolls-Royce', 'Bentley']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Car Hire - Luxury',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('car.luxury.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@hire_bp.route('/car-hire/sports')
def carhire_sports():
    selected_brand = request.args.get('brand', '')
    brands = []
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Hire Zone',
            subcategory='Car Hire - Sports',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('car.sport.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)

#=================MACHINERY =======================

@hire_bp.route('/machinery')
def machinery():
    """Machinery rental page"""
    return render_template('hire.machinery.html')

# ============ MACHINERY BLUEPRINT ROUTES (ENHANCED) ============
@services_bp.route('/construction-equipment')
def construction_equipment():
    selected_brand = request.args.get('brand', '')
    brands = [
        'Power Tools', 'Hand Tools', 'Heavy Equipment',
        'Safety Gear', 'Building Materials', 'Scaffolding',
        'Surveying', 'Generators', 'Plumbing', 'Electrical'
    ]
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Construction Equipment',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('construction_equipment.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)

#==================== CONSTRUCTION ====================
@hire_bp.route('/construction')
def construction():
    """Construction services page"""
    return render_template('hire.construction.html')


@hire_bp.route('/hire-now', methods=['GET', 'POST'])
def hire_now():
    """Hire now page for submitting hire requests"""
    if request.method == 'POST':
        service_type = request.form.get('service_type')
        details = request.form.get('details')
        location = request.form.get('location')
        date_needed = request.form.get('date_needed')

        flash('Your hire request has been submitted successfully!')
        return redirect(url_for('hire.hire_home'))

    return render_template('hire.hire_now.html')



# ============ FARMERS' ROOM ROUTES ============
@farmers_bp.route('/')
def farmers_home():

    return render_template('farmers.farmers_home.html')


@farmers_bp.route('/crops')
def crops():

    return render_template('farmers.crops.html')

#=================== CROPS ======================

@farmers_bp.route('/crops/fruits')
def fruits():
    selected_type = request.args.get('type', '')
    types = ['Mangoes', 'Bananas', 'Avocados', 'Oranges', 'Lemons', 'Pineapples', 'Apples', 'Peaches',
             'Strawberries', 'Blueberries', 'Litchis', 'Passion Fruit']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farmers',
                subcategory='Fruits',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('crops.fruits.html',   # <-- DOT here
                           types=types,
                           selected_type=selected_type,
                           listings=listings)

@farmers_bp.route('/crops/vegetables')
def vegetables():
    selected_type = request.args.get('type', '')
    types = ['Tomatoes', 'Cabbage', 'Onions', 'Carrots', 'Irish Potato', 'Butternut',
              'Cucumber', 'Green Beans', 'Peas', 'Leafy Vegetables', 'Okra', 'Pepper']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farmers',
                subcategory='Vegetables',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('crops.vegetables.html',   # <-- DOT
                           types=types,
                           selected_type=selected_type,
                           listings=listings)

@farmers_bp.route('/crops/grain')
def grain():
    selected_type = request.args.get('type', '')
    types = ['Maize', 'Wheat', 'Sorghum', 'Pearl Millet', 'Finger Millet',
             'Rice', 'Groundnuts', 'Sunflower', 'Sugar Beans', 'Soyabeans']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farmers',
                subcategory='Grains',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('crops.grain.html',   # <-- DOT
                           types=types,
                           selected_type=selected_type,
                           listings=listings)

@farmers_bp.route('/crops/herbs')
def herbs():
    selected_type = request.args.get('type', '')
    types = ['Garlic', 'Ginger', 'Turmeric', 'Parsley', 'Coriander',
             'Basil', 'Mint', 'Thyme', 'Rosemary', 'Chives', 'Dill', 'Fennel']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farmers',
                subcategory='Herbs',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('crops.herbs.html',   # <-- DOT
                           types=types,
                           selected_type=selected_type,
                           listings=listings)

@farmers_bp.route('/crops/organic')
def organic():
    selected_type = request.args.get('type', '')
    types = ['Organic Garlic', 'Organic Ginger', 'Organic Turmeric', 'Organic Cotton', 'Organic Pineapple', 'Organic Avocados',
             'Organic Blueberries', 'Organic Herbs', 'Organic Vegetables']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farmers',
                subcategory='Organic',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('crops.organic.html',   # <-- DOT
                           types=types,
                           selected_type=selected_type,
                           listings=listings)

@farmers_bp.route('/crops/seeds')
def seeds():
    selected_type = request.args.get('type', '')
    types = ['Vegetable Seeds', 'Flower Seeds', 'Herb Seeds', 'Grain Seeds', 'Heirloom', 'Hybrid', 'Organic', 'Bulk Seeds']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farmers',
                subcategory='Seeds',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('crops.seeds.html',   # <-- DOT
                           types=types,
                           selected_type=selected_type,
                           listings=listings)


# ================== LIVESTOCK ================
@farmers_bp.route('/livestock')
def livestock():
    """Livestock marketplace page"""
    return render_template('farmers.livestock.html')

# ============ LIVESTOCK SUBCATEGORIES ROUTES ============

@farmers_bp.route('/livestock/cattle')
def cattle():
    selected_type = request.args.get('type', '')
    types = ['Communal breed', 'Angus', 'Hereford', 'Holstein', 'Jersey', 'Brahman', 'Charolais', 'Simmental', 'Limousin', 'Shorthorn', 'Gelbvieh']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Livestock',
                subcategory='Cattle',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('livestock.cattle.html',
                           types=types,
                           selected_type=selected_type,
                           listings=listings)


@farmers_bp.route('/livestock/poultry')
def poultry():
    selected_type = request.args.get('type', '')
    types = ['Chickens', 'Turkeys', 'Ducks', 'Geese', 'Quail', 'Guinea Fowl', 'Broilers', 'Layers', 'Heritage Breeds']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Livestock',
                subcategory='Poultry',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('livestock.poultry.html',
                           types=types,
                           selected_type=selected_type,
                           listings=listings)


@farmers_bp.route('/livestock/goats')
def goats():
    selected_type = request.args.get('type', '')
    types = ['Boer', 'Nubian', 'Alpine', 'Saanen', 'LaMancha', 'Myotonic', 'Kiko', 'Pygmy', 'Nigerian Dwarf', 'Savanna', 'Merino', 'Suffolk', 'Hampshire', 'Dorset', 'Rambouillet', 'Katahdin', 'Cheviot', 'Southdown', 'Lamb', 'Wool Sheep']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Livestock',
                subcategory='Goats',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('livestock.goats.html',
                           types=types,
                           selected_type=selected_type,
                           listings=listings)



@farmers_bp.route('/livestock/pigs')
def pigs():
    selected_type = request.args.get('type', '')
    types = ['Duroc', 'Berkshire', 'Yorkshire', 'Hampshire', 'Landrace', 'Tamworth', 'Gloucestershire Old Spot', 'Pietrain']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Livestock',
                subcategory='Pigs',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('livestock.pigs.html',
                           types=types,
                           selected_type=selected_type,
                           listings=listings)



@farmers_bp.route('/livestock/rabbits')
def rabbits():
    selected_type = request.args.get('type', '')
    types = ['New Zealand White', 'Californian', 'Flemish Giant', 'Rex', 'Holland Lop', 'Mini Rex', 'Angora', 'Lionhead', 'Dutch', 'English Lop']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Livestock',
                subcategory='Rabbits',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('livestock.rabbits.html',
                           types=types,
                           selected_type=selected_type,
                           listings=listings)



@farmers_bp.route('/equipment')
def equipment():
    # List of equipment types (matches the buttons)
    equipment_types = [
        'Tractors',
        'Harvesters',
        'Plows & Tillers',
        'Irrigation',
        'Trailers & Wagons',
        'Hand Tools',
        'Milking Equipment'
    ]
    selected_type = request.args.get('type', '')
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farming Equipment',
                brand=selected_type,   # store equipment type in `brand` field
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except Exception:
            listings = []
    else:
        try:
            listings = Listing.query.filter_by(
                category='Farming Equipment',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except Exception:
            listings = []

    return render_template('farmers.equipment.html',
                           types=equipment_types,   # passed as `types`
                           selected_type=selected_type,
                           listings=listings)


# ======================== SUPPLIES ==========================
@farmers_bp.route('/supplies')
def supplies():
    return render_template('farmers.supplies.html')

# ============ FARM SUPPLIES SUBCATEGORY ROUTES (all under /fertilizer/) ============

@farmers_bp.route('/fertilizer/organic')
def organic_fertilizers():
    selected_type = request.args.get('type', '')
    types = ['Compost', 'Manure', 'Bone Meal', 'Blood Meal', 'Fish Emulsion', 'Kelp Meal', 'Worm Castings']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farm Supplies',
                subcategory='Organic Fertilizers',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('fertilizer.organic.html',
                           types=types,
                           selected_type=selected_type,
                           listings=listings)


@farmers_bp.route('/fertilizer/chemical')
def chemical_fertilizers():
    selected_type = request.args.get('type', '')
    types = ['NPK 20-20-20', 'Urea', 'Ammonium Nitrate', 'Potassium Chloride', 'Superphosphate', 'Sulfate of Potash', 'Calcium Nitrate']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farm Supplies',
                subcategory='Chemical Fertilizers',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('fertilizer.chemical.html',
                           types=types,
                           selected_type=selected_type,
                           listings=listings)


@farmers_bp.route('/fertilizer/vegetable')
def vegetable_seedlings():
    selected_type = request.args.get('type', '')
    types = ['Tomato', 'Pepper', 'Cucumber', 'Lettuce', 'Cabbage', 'Broccoli', 'Onion', 'Carrot', 'Spinach', 'Kale']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farm Supplies',
                subcategory='Vegetable Seedlings',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('fertilizer.vegetable.html',
                           types=types,
                           selected_type=selected_type,
                           listings=listings)


@farmers_bp.route('/fertilizer/grain')
def grain_seedlings():
    selected_type = request.args.get('type', '')
    types = ['Corn', 'Wheat', 'Rice', 'Barley', 'Oats', 'Sorghum', 'Millet', 'Quinoa']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farm Supplies',
                subcategory='Grain Seedlings',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('fertilizer.grain.html',
                           types=types,
                           selected_type=selected_type,
                           listings=listings)


@farmers_bp.route('/fertilizer/herbs-bulbs')
def herbs_bulbs_seedlings():
    selected_type = request.args.get('type', '')
    types = ['Basil', 'Mint', 'Thyme', 'Rosemary', 'Cilantro', 'Parsley', 'Garlic', 'Onion', 'Shallot', 'Chives']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farm Supplies',
                subcategory='Herbs & Bulbs Seedlings',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('fertilizer.herbs.html',
                           types=types,
                           selected_type=selected_type,
                           listings=listings)


@farmers_bp.route('/fertilizer/fruit')
def fruit_seedlings():
    selected_type = request.args.get('type', '')
    types = ['Apple', 'Strawberry', 'Blueberry', 'Raspberry', 'Peach', 'Plum', 'Cherry', 'Grape', 'Watermelon', 'Cantaloupe']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farm Supplies',
                subcategory='Fruit Seedlings',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('fertilizer.fruit.html',
                           types=types,
                           selected_type=selected_type,
                           listings=listings)


@farmers_bp.route('/fertilizer/pesticides')
def pesticides():
    selected_type = request.args.get('type', '')
    types = ['Herbicides', 'Fungicides', 'Insecticides', 'Neem Oil', 'Diatomaceous Earth', 'Pyrethrin', 'Spinosad']
    listings = []
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farm Supplies',
                subcategory='Pesticides',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('fertilizer.pesticides.html',
                           types=types,
                           selected_type=selected_type,
                           listings=listings)

@farmers_bp.route('/services')
def services():
    service_types = [
        'Veterinary',
        'Farm Labor',
        'Equipment Repair',
        'Transport',
        'Consulting',
        'Land Preparation',
        'Pest Control'
    ]
    selected_type = request.args.get('type', '')
    if selected_type:
        try:
            listings = Listing.query.filter_by(
                category='Farm Services',
                brand=selected_type,   # store service type in `brand` field
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except Exception:
            listings = []
    else:
        try:
            listings = Listing.query.filter_by(
                category='Farm Services',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except Exception:
            listings = []

    return render_template('farmers.services.html',
                           types=service_types,   # passed as `types`
                           selected_type=selected_type,
                           listings=listings)


@farmers_bp.route('/post-listing', methods=['GET', 'POST'])
def post_listing():
    """Post a farming listing or need"""
    if request.method == 'POST':
        listing_type = request.form.get('listing_type')
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        category = request.form.get('category')
        location = request.form.get('location')

        flash('Your farming listing has been posted successfully!')
        return redirect(url_for('farmers.farmers_home'))

    return render_template('farmers.post_listing.html')


# ============ HOUSING BLUEPRINT ROUTES (ENHANCED) ============

@housing_bp.route('/apartments')
def apartments():
    selected_brand = request.args.get('brand', '')
    brands = ['Studio', '1 Bedroom', '2 Bedroom', '3 Bedroom', 'Penthouse', 'Luxury']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Housing',
            subcategory='Apartments',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('housing.apartments.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@housing_bp.route('/houses')
def houses():
    selected_brand = request.args.get('brand', '')
    brands = ['Single Family', 'Townhouse', 'Duplex', 'Mansion', 'Modern', 'Traditional']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Housing',
            subcategory='Houses',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('housing.houses.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@housing_bp.route('/vacation-rentals')
def vacation_rentals():
    selected_brand = request.args.get('brand', '')
    brands = ['Hotels', 'Lodge', 'Cottage', 'City Apartment', 'Villa']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Housing',
            subcategory='Vacation Rentals',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('housing.vacation_rentals.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@housing_bp.route('/commercial')
def commercial():
    selected_brand = request.args.get('brand', '')
    brands = ['Stands', 'Office Space', 'Hall', 'Meeting Space', 'Retail', 'Farms', 'Plots',
              'Warehouse', 'Industrial', 'Co-working', 'Mixed Use']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Housing',
            subcategory='Commercial',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('housing.commercial.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@housing_bp.route('/roommates')
def roommates():
    selected_brand = request.args.get('brand', '')
    brands = ['Shared Room', 'Private Room', 'Master Bedroom', 'Couple Friendly', 'Students Only', 'Pet Friendly']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Housing',
            subcategory='Roommates',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('housing.roommates.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)

@housing_bp.route('/student')
def student():
    selected_brand = request.args.get('brand', '')
    brands = ['Studio', 'Shared Room', 'Private Room', 'Ensuite', 'Apartment', 'Residence Hall', 'Student Village']
    listings = []
    try:
        query = Listing.query.filter_by(
            category='Housing',
            subcategory='Student',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []
    return render_template('housing.student.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


# ============ MARKETPLACE ROUTES ============

@marketplace_bp.route('/')
def marketplace_home():
    try:
        listings = Listing.query.filter_by(is_active=True).limit(20).all()
    except:
        listings = []
    return render_template('marketplace.html', listings=listings)


@marketplace_bp.route('/create', methods=['GET', 'POST'])
def create_listing():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        location = request.form.get('location')

        new_listing = Listing(
            title=title,
            description=description,
            price=price,
            category=category,
            location=location,
            user_id=1
        )

        db.session.add(new_listing)
        db.session.commit()

        flash('Listing created successfully!')
        return redirect(url_for('marketplace.marketplace_home'))

    return render_template('create_listing.html')


@marketplace_bp.route('/<int:listing_id>')
def listing_detail(listing_id):
    try:
        listing = Listing.query.get_or_404(listing_id)
        listing.views += 1
        db.session.commit()
        return render_template('listing_detail.html', listing=listing)
    except:
        flash('Listing not found')
        return redirect(url_for('marketplace.marketplace_home'))


@marketplace_bp.route('/electronics')
def electronics():
    try:
        electronics_listings = Listing.query.filter_by(
            category='Electronics',
            is_active=True
        ).limit(8).all()
    except:
        electronics_listings = []
    return render_template('electronics.html', listings=electronics_listings)


# ============ ELECTRONICS SUBCATEGORIES ROUTES ============
@marketplace_bp.route('/smartphones')
def smartphones():
    selected_brand = request.args.get('brand', '')
    brands = ['Samsung', 'iPhone','Huawei', 'Xiaomi', 'Itel',
              'Google', 'Tecno', 'Infinix', 'Vivo', 'Honor', 'Oppo', 'ZTE', 'Lenovo', 'G-Tel', 'Hisense', 'Sony']

    # Sample listings per brand so every brand button has phones to browse.
    sample_listings = [
        # Samsung
        {'id': 1, 'brand': 'Samsung', 'title': 'Samsung Galaxy S23 Ultra', 'category': 'Smartphones',
         'price': '$820', 'status': 'available', 'likes': 42, 'location': 'Nairobi',
         'specs': '256GB storage · 12GB RAM · 200MP camera · S-Pen included',
         'description': 'Excellent condition with original box, charger and a free case.',
         'img_prompt': 'samsung galaxy s23 ultra smartphone product photo'},
        {'id': 2, 'brand': 'Samsung', 'title': 'Samsung Galaxy A54', 'category': 'Smartphones',
         'price': '$310', 'status': 'available', 'likes': 18, 'location': 'Mombasa',
         'specs': '128GB storage · 8GB RAM · 50MP OIS camera · Dual SIM',
         'description': 'Boxed and barely used, complete with accessories.',
         'img_prompt': 'samsung galaxy a54 smartphone product photo'},
        {'id': 3, 'brand': 'Samsung', 'title': 'Samsung Galaxy Z Flip 5', 'category': 'Smartphones',
         'price': '$650', 'status': 'sold', 'likes': 27, 'location': 'Kisumu',
         'specs': '256GB storage · 8GB RAM · Foldable AMOLED display',
         'description': 'Foldable flagship, minor scratch on the hinge.',
         'img_prompt': 'samsung galaxy z flip foldable phone product photo'},

        # iPhone
        {'id': 4, 'brand': 'iPhone', 'title': 'iPhone 15 Pro Max', 'category': 'Smartphones',
         'price': '$1,150', 'status': 'available', 'likes': 65, 'location': 'Nairobi',
         'specs': '256GB storage · A17 Pro · Titanium frame · Battery health 100%',
         'description': 'Sealed unit with warranty and original accessories.',
         'img_prompt': 'iphone 15 pro max smartphone product photo'},
        {'id': 5, 'brand': 'iPhone', 'title': 'iPhone 13', 'category': 'Smartphones',
         'price': '$540', 'status': 'available', 'likes': 40, 'location': 'Eldoret',
         'specs': '128GB storage · A15 Bionic · Face ID · Unlocked',
         'description': 'Clean device, comes with charger and cable.',
         'img_prompt': 'iphone 13 smartphone product photo'},
        {'id': 6, 'brand': 'iPhone', 'title': 'iPhone 12 mini', 'category': 'Smartphones',
         'price': '$380', 'status': 'available', 'likes': 22, 'location': 'Nakuru',
         'specs': '64GB storage · A14 Bionic · Compact 5.4" display · Battery 88%',
         'description': 'Neat and compact, no scratches on screen.',
         'img_prompt': 'iphone 12 mini smartphone product photo'},

        # Xiaomi
        {'id': 7, 'brand': 'Xiaomi', 'title': 'Xiaomi Redmi Note 12 Pro', 'category': 'Smartphones',
         'price': '$210', 'status': 'available', 'likes': 31, 'location': 'Thika',
         'specs': '128GB storage · 8GB RAM · AMOLED 120Hz display',
         'description': 'Great mid-range value, sealed box.',
         'img_prompt': 'xiaomi redmi note smartphone product photo'},
        {'id': 8, 'brand': 'Xiaomi', 'title': 'Xiaomi 13', 'category': 'Smartphones',
         'price': '$480', 'status': 'available', 'likes': 19, 'location': 'Nairobi',
         'specs': '256GB storage · 12GB RAM · Leica triple camera',
         'description': 'Flagship performance, sealed and unused.',
         'img_prompt': 'xiaomi 13 flagship smartphone product photo'},

        # Itel
        {'id': 9, 'brand': 'Itel', 'title': 'itel A60', 'category': 'Smartphones',
         'price': '$65', 'status': 'available', 'likes': 12, 'location': 'Machakos',
         'specs': '32GB storage · 2GB RAM · Android Go · Dual SIM',
         'description': 'Brand new budget phone, ideal for daily use.',
         'img_prompt': 'itel budget android smartphone product photo'},
        {'id': 10, 'brand': 'Itel', 'title': 'itel P40', 'category': 'Smartphones',
         'price': '$79', 'status': 'available', 'likes': 9, 'location': 'Meru',
         'specs': '64GB storage · 4GB RAM · 6000mAh battery',
         'description': 'Long battery life, perfect for travel.',
         'img_prompt': 'itel android smartphone big battery product photo'},

        # Tecno
        {'id': 11, 'brand': 'Tecno', 'title': 'Tecno Spark 10 Pro', 'category': 'Smartphones',
         'price': '$125', 'status': 'available', 'likes': 24, 'location': 'Nairobi',
         'specs': '128GB storage · 8GB RAM · 50MP camera · 90Hz display',
         'description': 'Stylish design with strong camera performance.',
         'img_prompt': 'tecno spark smartphone product photo'},
        {'id': 12, 'brand': 'Tecno', 'title': 'Tecno Camon 20', 'category': 'Smartphones',
         'price': '$170', 'status': 'available', 'likes': 15, 'location': 'Kakamega',
         'specs': '256GB storage · 8GB RAM · 64MP RGBW sensor',
         'description': 'Sleek and slim, great for photography.',
         'img_prompt': 'tecno camon smartphone product photo'},

        # Infinix
        {'id': 13, 'brand': 'Infinix', 'title': 'Infinix Hot 30', 'category': 'Smartphones',
         'price': '$120', 'status': 'available', 'likes': 17, 'location': 'Nairobi',
         'specs': '128GB storage · 8GB RAM · 90Hz display · 50MP camera',
         'description': 'Smooth daily driver at a friendly price.',
         'img_prompt': 'infinix hot smartphone product photo'},
        {'id': 14, 'brand': 'Infinix', 'title': 'Infinix Note 30', 'category': 'Smartphones',
         'price': '$185', 'status': 'available', 'likes': 21, 'location': 'Kisii',
         'specs': '256GB storage · 8GB RAM · 45W fast charging',
         'description': 'Big screen and fast charging for power users.',
         'img_prompt': 'infinix note smartphone product photo'},

        # Huawei
        {'id': 15, 'brand': 'Huawei', 'title': 'Huawei P60 Pro', 'category': 'Smartphones',
         'price': '$600', 'status': 'available', 'likes': 20, 'location': 'Nairobi',
         'specs': '256GB storage · 8GB RAM · XMAGE camera system',
         'description': 'Premium camera phone, sealed in box.',
         'img_prompt': 'huawei p60 pro smartphone product photo'},
        {'id': 16, 'brand': 'Huawei', 'title': 'Huawei Nova 11', 'category': 'Smartphones',
         'price': '$300', 'status': 'available', 'likes': 11, 'location': 'Nyeri',
         'specs': '128GB storage · 8GB RAM · 4G LTE · 66W charging',
         'description': 'Slim mid-ranger with fast charging.',
         'img_prompt': 'huawei nova smartphone product photo'},

        # Oppo
        {'id': 17, 'brand': 'Oppo', 'title': 'Oppo Reno 10', 'category': 'Smartphones',
         'price': '$390', 'status': 'available', 'likes': 16, 'location': 'Mombasa',
         'specs': '256GB storage · 8GB RAM · 67W SuperVOOC · AMOLED',
         'description': 'Elegant phone with excellent portrait camera.',
         'img_prompt': 'oppo reno smartphone product photo'},

        # Vivo
        {'id': 18, 'brand': 'Vivo', 'title': 'Vivo Y36', 'category': 'Smartphones',
         'price': '$175', 'status': 'available', 'likes': 10, 'location': 'Nairobi',
         'specs': '128GB storage · 8GB RAM · 90Hz display · 5000mAh',
         'description': 'Reliable all-rounder with a bright display.',
         'img_prompt': 'vivo y series smartphone product photo'},

        # Google
        {'id': 19, 'brand': 'Google', 'title': 'Google Pixel 8 Pro', 'category': 'Smartphones',
         'price': '$780', 'status': 'available', 'likes': 33, 'location': 'Nairobi',
         'specs': '128GB storage · Tensor G3 · 50MP triple camera',
         'description': 'Clean Android experience with class-leading camera.',
         'img_prompt': 'google pixel pro smartphone product photo'},

        # Honor
        {'id': 20, 'brand': 'Honor', 'title': 'Honor 90', 'category': 'Smartphones',
         'price': '$360', 'status': 'available', 'likes': 13, 'location': 'Nakuru',
         'specs': '256GB storage · 12GB RAM · 200MP camera · 66W charging',
         'description': 'Sharp display and a high-resolution main camera.',
         'img_prompt': 'honor smartphone product photo'},

        # Sony
        {'id': 21, 'brand': 'Sony', 'title': 'Sony Xperia 1 V', 'category': 'Smartphones',
         'price': '$950', 'status': 'available', 'likes': 8, 'location': 'Nairobi',
         'specs': '256GB storage · 12GB RAM · 4K OLED · Pro camera apps',
         'description': 'Flagship for creatives and mobile photographers.',
         'img_prompt': 'sony xperia smartphone product photo'},

        # ZTE
        {'id': 22, 'brand': 'ZTE', 'title': 'ZTE Blade A73', 'category': 'Smartphones',
         'price': '$110', 'status': 'available', 'likes': 6, 'location': 'Mombasa',
         'specs': '128GB storage · 6GB RAM · 50MP camera',
         'description': 'Budget pick with solid everyday performance.',
         'img_prompt': 'zte android smartphone product photo'},

        # Lenovo
        {'id': 23, 'brand': 'Lenovo', 'title': 'Lenovo K14 Plus', 'category': 'Smartphones',
         'price': '$95', 'status': 'available', 'likes': 5, 'location': 'Kisumu',
         'specs': '64GB storage · 4GB RAM · 5000mAh battery',
         'description': 'Affordable and dependable for basic tasks.',
         'img_prompt': 'lenovo k series smartphone product photo'},

        # G-Tel
        {'id': 24, 'brand': 'G-Tel', 'title': 'G-Tel F3', 'category': 'Smartphones',
         'price': '$45', 'status': 'available', 'likes': 4, 'location': 'Eldoret',
         'specs': '32GB storage · 2GB RAM · Entry-level Android',
         'description': 'Sealed entry-level phone, great as a backup.',
         'img_prompt': 'budget android smartphone product photo'},

        # Hisense
        {'id': 25, 'brand': 'Hisense', 'title': 'Hisense E60', 'category': 'Smartphones',
         'price': '$85', 'status': 'available', 'likes': 3, 'location': 'Nairobi',
         'specs': '128GB storage · 4GB RAM · 6.5" display · 5000mAh',
         'description': 'Large display and long battery life.',
         'img_prompt': 'hisense android smartphone product photo'},
    ]

    # Structured device specs shown in the client info modal (make = brand, city = location)
    _device_specs = {
        1: ('2023', '256GB', '12GB', 'Like New', '6 months'),
        2: ('2023', '128GB', '8GB', 'New', '1 year'),
        3: ('2023', '256GB', '8GB', 'Used', 'None'),
        4: ('2023', '256GB', '8GB', 'New', '1 year'),
        5: ('2021', '128GB', '4GB', 'Like New', '3 months'),
        6: ('2020', '64GB', '4GB', 'Used', 'None'),
        7: ('2023', '128GB', '8GB', 'New', '1 year'),
        8: ('2023', '256GB', '12GB', 'Like New', '6 months'),
        9: ('2024', '32GB', '2GB', 'New', '1 year'),
        10: ('2023', '64GB', '4GB', 'New', '1 year'),
        11: ('2023', '128GB', '8GB', 'New', '1 year'),
        12: ('2023', '256GB', '8GB', 'Like New', '6 months'),
        13: ('2023', '128GB', '8GB', 'New', '1 year'),
        14: ('2023', '256GB', '8GB', 'Like New', '6 months'),
        15: ('2023', '256GB', '8GB', 'New', '1 year'),
        16: ('2023', '128GB', '8GB', 'Like New', '6 months'),
        17: ('2023', '256GB', '8GB', 'New', '1 year'),
        18: ('2023', '128GB', '8GB', 'New', '1 year'),
        19: ('2023', '128GB', '12GB', 'Like New', '6 months'),
        20: ('2023', '256GB', '12GB', 'New', '1 year'),
        21: ('2023', '256GB', '12GB', 'Like New', '6 months'),
        22: ('2023', '128GB', '6GB', 'New', '1 year'),
        23: ('2022', '64GB', '4GB', 'Used', 'None'),
        24: ('2023', '32GB', '2GB', 'New', '1 year'),
        25: ('2022', '128GB', '4GB', 'Used', 'None'),
    }

    for listing in sample_listings:
        listing['section'] = 'Market-Center'
        listing['created'] = '2026-07-' + str((listing['id'] % 28) + 1).zfill(2)
        year, storage, ram, condition, warranty = _device_specs[listing['id']]
        listing['year'] = year
        listing['storage'] = storage
        listing['ram'] = ram
        listing['condition'] = condition
        listing['warranty'] = warranty
        listing.pop('specs', None)

    brand_counts = {b: sum(1 for l in sample_listings if l['brand'] == b) for b in brands}

    if selected_brand:
        listings = [l for l in sample_listings if l['brand'] == selected_brand]
    else:
        listings = sample_listings

    return render_template('smartphones.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings,
                           brand_counts=brand_counts,
                           total_count=len(sample_listings))


def _sample(brand, title, price, likes, location, description, prompt, **specs):
    """Build one sample marketplace listing (id/category/section added by _prepare)."""
    return {
        'brand': brand, 'title': title, 'price': price,
        'status': specs.pop('status', 'available'), 'likes': likes,
        'location': location, 'description': description, 'img_prompt': prompt,
        **specs,
    }


def _prepare(items, category):
    """Give a category's sample listings their id, category, section and created date."""
    for i, item in enumerate(items, start=1):
        item['id'] = i
        item['category'] = category
        item['section'] = 'Market-Center'
        item['created'] = '2026-07-' + str((i % 28) + 1).zfill(2)
    return items


def _render_category(template, brands, sample_listings):
    """Filter sample listings by the ?brand= query and render a category page."""
    selected_brand = request.args.get('brand', '')
    brand_counts = {b: sum(1 for l in sample_listings if l['brand'] == b) for b in brands}
    listings = [l for l in sample_listings if l['brand'] == selected_brand] if selected_brand else sample_listings
    return render_template(template,
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings,
                           brand_counts=brand_counts,
                           total_count=len(sample_listings))


@marketplace_bp.route('/laptops')
def laptops():
    brands = ['Dell', 'HP', 'Lenovo', 'Apple', 'Asus',
              'Acer', 'MSI', 'Huawei', 'Microsoft', 'Samsung', 'Avantis', 'LG', 'Toshiba']
    sample_listings = _prepare([
        _sample('Dell', 'Dell XPS 13 Plus', '$950', 28, 'Nairobi', 'Slim ultrabook with a superb display and all-day battery.', 'dell xps 13 laptop product photo', year='2023', storage='512GB SSD', ram='16GB', condition='Like New', warranty='6 months'),
        _sample('HP', 'HP Spectre x360 14', '$880', 22, 'Mombasa', 'Convertible touchscreen laptop with premium finish.', 'hp spectre x360 laptop product photo', year='2023', storage='1TB SSD', ram='16GB', condition='Like New', warranty='6 months'),
        _sample('Lenovo', 'Lenovo ThinkPad X1 Carbon', '$790', 19, 'Nairobi', 'Business-class ultrabook, lightweight and rugged.', 'lenovo thinkpad x1 carbon laptop product photo', year='2022', storage='512GB SSD', ram='16GB', condition='Used', warranty='None'),
        _sample('Apple', 'Apple MacBook Air M2', '$1,050', 34, 'Nairobi', 'Fanless M2 MacBook Air, sealed and unused.', 'apple macbook air m2 laptop product photo', year='2023', storage='256GB SSD', ram='8GB', condition='New', warranty='1 year'),
        _sample('Asus', 'Asus ROG Zephyrus G14', '$1,180', 26, 'Nakuru', 'Gaming laptop with RTX graphics and 165Hz screen.', 'asus rog zephyrus gaming laptop product photo', year='2023', storage='1TB SSD', ram='16GB', condition='Like New', warranty='6 months'),
        _sample('Acer', 'Acer Aspire 5', '$520', 12, 'Kisumu', 'Everyday laptop for study and office work.', 'acer aspire 5 laptop product photo', year='2022', storage='512GB SSD', ram='8GB', condition='Used', warranty='None'),
        _sample('MSI', 'MSI Katana 15', '$1,020', 15, 'Nairobi', 'Budget gaming machine with backlit keyboard.', 'msi katana gaming laptop product photo', year='2023', storage='512GB SSD', ram='16GB', condition='Like New', warranty='6 months'),
        _sample('Huawei', 'Huawei MateBook D15', '$560', 11, 'Eldoret', 'Thin metal body with a full-size display.', 'huawei matebook d15 laptop product photo', year='2022', storage='512GB SSD', ram='8GB', condition='Used', warranty='None'),
        _sample('Microsoft', 'Microsoft Surface Laptop 5', '$930', 20, 'Nairobi', 'Touchscreen laptop with a vivid PixelSense display.', 'microsoft surface laptop product photo', year='2023', storage='512GB SSD', ram='8GB', condition='Like New', warranty='6 months'),
        _sample('Samsung', 'Samsung Galaxy Book3', '$760', 14, 'Thika', 'Slim AMOLED laptop that pairs with Galaxy phones.', 'samsung galaxy book laptop product photo', year='2023', storage='512GB SSD', ram='8GB', condition='Like New', warranty='6 months'),
        _sample('Avantis', 'Avantis Student Laptop', '$310', 9, 'Machakos', 'Affordable laptop built for students.', 'affordable student laptop product photo', year='2023', storage='128GB SSD', ram='4GB', condition='New', warranty='1 year'),
        _sample('LG', 'LG Gram 16', '$1,120', 17, 'Nairobi', 'Ultra-light 16-inch laptop with long battery life.', 'lg gram 16 laptop product photo', year='2023', storage='1TB SSD', ram='16GB', condition='Like New', warranty='6 months'),
        _sample('Toshiba', 'Toshiba Dynabook Satellite Pro', '$400', 8, 'Meru', 'Dependable machine for everyday tasks.', 'toshiba dynabook laptop product photo', year='2021', storage='256GB SSD', ram='8GB', condition='Used', warranty='None'),
    ], 'Laptops')
    return _render_category('laptops.html', brands, sample_listings)


@marketplace_bp.route('/audio')
def audio():
    brands = ['Headphones', 'EarBuds', 'AirPods', 'Earphones', 'Speaker', 'SoundBars']
    sample_listings = _prepare([
        _sample('Headphones', 'Sony WH-1000XM5', '$280', 31, 'Nairobi', 'Class-leading noise cancelling over-ear headphones.', 'sony wh-1000xm5 headphones product photo', year='2023', type='Over-ear ANC', battery='30 hours', condition='Like New', warranty='6 months'),
        _sample('Headphones', 'Beats Studio Pro', '$220', 18, 'Mombasa', 'Punchy sound with spatial audio support.', 'beats studio pro headphones product photo', year='2023', type='Over-ear', battery='40 hours', condition='New', warranty='1 year'),
        _sample('EarBuds', 'Samsung Galaxy Buds2 Pro', '$140', 24, 'Mombasa', 'Compact ANC earbuds with 24-bit audio.', 'samsung galaxy buds2 pro earbuds product photo', year='2023', type='True wireless ANC', battery='5 hours', condition='New', warranty='1 year'),
        _sample('AirPods', 'Apple AirPods Pro 2', '$210', 44, 'Nairobi', 'Adaptive audio and ANC in a tiny package.', 'apple airpods pro 2 earbuds product photo', year='2023', type='True wireless ANC', battery='6 hours', condition='New', warranty='1 year'),
        _sample('Earphones', 'JBL Tune 310C', '$25', 7, 'Kisumu', 'Wired in-ear earphones with a USB-C plug.', 'jbl wired earphones product photo', year='2023', type='Wired in-ear', battery='N/A', condition='New', warranty='1 year'),
        _sample('Speaker', 'JBL Charge 5', '$150', 21, 'Nakuru', 'Portable Bluetooth speaker that also charges your phone.', 'jbl charge 5 bluetooth speaker product photo', year='2022', type='Portable Bluetooth', battery='20 hours', condition='Like New', warranty='6 months'),
        _sample('SoundBars', 'Sony HT-S2000', '$390', 13, 'Nairobi', 'Dolby Atmos soundbar with built-in subwoofers.', 'sony dolby atmos soundbar product photo', year='2023', type='3.1ch Dolby Atmos', battery='N/A', condition='Like New', warranty='6 months', status='sold'),
    ], 'Audio')
    return _render_category('audio.html', brands, sample_listings)


@marketplace_bp.route('/cameras')
def cameras():
    brands = ['Canon', 'Nikon', 'Sony', 'Fujifilm', 'GoPro', 'Panasonic', 'Olympus', 'Leica', 'Sigma', 'DJI']
    sample_listings = _prepare([
        _sample('Canon', 'Canon EOS R6', '$1,650', 27, 'Nairobi', 'Full-frame mirrorless with superb low-light autofocus.', 'canon eos r6 mirrorless camera product photo', year='2023', sensor='Full-frame CMOS 20MP', mount='Canon RF', condition='Like New', warranty='6 months'),
        _sample('Nikon', 'Nikon Z6 II', '$1,400', 22, 'Mombasa', 'Versatile full-frame body with dual card slots.', 'nikon z6 ii mirrorless camera product photo', year='2022', sensor='Full-frame CMOS 24MP', mount='Nikon Z', condition='Used', warranty='None'),
        _sample('Sony', 'Sony Alpha 7 IV', '$1,850', 35, 'Nairobi', 'Hybrid all-rounder with 4K60 video and 33MP stills.', 'sony alpha 7 iv mirrorless camera product photo', year='2023', sensor='Full-frame CMOS 33MP', mount='Sony E', condition='Like New', warranty='6 months'),
        _sample('Fujifilm', 'Fujifilm X-T5', '$1,300', 29, 'Kisumu', 'Retro-styled APS-C body with film simulations.', 'fujifilm xt5 camera product photo', year='2023', sensor='APS-C X-Trans 40MP', mount='Fujifilm X', condition='Like New', warranty='6 months'),
        _sample('GoPro', 'GoPro HERO11 Black', '$320', 26, 'Nairobi', 'Rugged action camera with 5.3K video.', 'gopro hero 11 action camera product photo', year='2023', sensor='1/1.9 inch CMOS', mount='Fixed lens', condition='New', warranty='1 year'),
        _sample('Panasonic', 'Panasonic Lumix GH6', '$1,250', 16, 'Nakuru', 'Video-first Micro Four Thirds powerhouse.', 'panasonic lumix gh6 camera product photo', year='2022', sensor='Micro Four Thirds 25MP', mount='Micro Four Thirds', condition='Like New', warranty='6 months'),
        _sample('Olympus', 'Olympus OM-D E-M10 Mark IV', '$640', 12, 'Eldoret', 'Lightweight travel camera with in-body stabilisation.', 'olympus om-d camera product photo', year='2021', sensor='Micro Four Thirds 20MP', mount='Micro Four Thirds', condition='Used', warranty='None'),
        _sample('Leica', 'Leica Q2', '$3,200', 19, 'Nairobi', 'Full-frame compact with a legendary fixed lens.', 'leica q2 compact camera product photo', year='2021', sensor='Full-frame CMOS 47MP', mount='Fixed 28mm', condition='Like New', warranty='3 months'),
        _sample('Sigma', 'Sigma fp L', '$1,500', 10, 'Thika', 'Tiny full-frame body with 61MP resolution.', 'sigma fp l camera product photo', year='2022', sensor='Full-frame BSI 61MP', mount='L-Mount', condition='Like New', warranty='6 months'),
        _sample('DJI', 'DJI Osmo Pocket 3', '$520', 23, 'Nairobi', 'Pocket gimbal camera with a 1-inch sensor.', 'dji osmo pocket 3 camera product photo', year='2023', sensor='1-inch CMOS', mount='Fixed lens', condition='New', warranty='1 year'),
    ], 'Cameras')
    return _render_category('cameras.html', brands, sample_listings)


@marketplace_bp.route('/gaming')
def gaming():
    brands = ['Sony', 'Microsoft', 'Nintendo', 'Razer', 'Logitech', 'SteelSeries', 'Corsair', 'ASUS', 'MSI', 'HyperX']
    sample_listings = _prepare([
        _sample('Sony', 'PlayStation 5 Slim', '$520', 46, 'Nairobi', 'Latest PS5 revision with a 1TB SSD and one controller.', 'playstation 5 slim console product photo', year='2023', platform='PlayStation 5', storage='1TB SSD', condition='Like New', warranty='6 months'),
        _sample('Microsoft', 'Xbox Series X', '$480', 33, 'Mombasa', '4K gaming console with a 1TB SSD.', 'xbox series x console product photo', year='2022', platform='Xbox Series X', storage='1TB SSD', condition='Like New', warranty='6 months'),
        _sample('Nintendo', 'Nintendo Switch OLED', '$310', 38, 'Nairobi', 'Handheld console with a vivid OLED screen.', 'nintendo switch oled console product photo', year='2023', platform='Nintendo Switch', storage='64GB', condition='New', warranty='1 year'),
        _sample('Razer', 'Razer BlackWidow V4', '$150', 14, 'Kisumu', 'Mechanical gaming keyboard with RGB lighting.', 'razer mechanical gaming keyboard product photo', year='2023', platform='PC', storage='N/A', condition='New', warranty='1 year'),
        _sample('Logitech', 'Logitech G Pro X Superlight 2', '$130', 25, 'Nakuru', 'Ultra-light wireless esports mouse.', 'logitech wireless gaming mouse product photo', year='2023', platform='PC', storage='N/A', condition='Like New', warranty='6 months'),
        _sample('SteelSeries', 'SteelSeries Arctis Nova Pro', '$300', 17, 'Nairobi', 'Premium gaming headset with active noise cancelling.', 'steelseries gaming headset product photo', year='2023', platform='PC / Console', storage='N/A', condition='Like New', warranty='6 months'),
        _sample('Corsair', 'Corsair K70 RGB Pro', '$140', 11, 'Thika', 'Aluminium mechanical keyboard with media controls.', 'corsair rgb mechanical keyboard product photo', year='2022', platform='PC', storage='N/A', condition='Used', warranty='None'),
        _sample('ASUS', 'ASUS ROG Ally', '$600', 21, 'Nairobi', 'Windows handheld gaming PC with a 120Hz screen.', 'asus rog ally handheld console product photo', year='2023', platform='Windows handheld', storage='512GB', condition='Like New', warranty='6 months'),
        _sample('MSI', 'MSI Claw', '$650', 13, 'Eldoret', 'Handheld PC with Intel Arc graphics.', 'msi claw handheld gaming pc product photo', year='2024', platform='Windows handheld', storage='512GB', condition='New', warranty='1 year'),
        _sample('HyperX', 'HyperX Cloud III', '$100', 9, 'Meru', 'Comfortable wired headset with clear mic.', 'hyperx gaming headset product photo', year='2023', platform='PC / Console', storage='N/A', condition='New', warranty='1 year', status='sold'),
    ], 'Gaming')
    return _render_category('gaming.html', brands, sample_listings)


@marketplace_bp.route('/accessories')
def accessories():
    brands = ['Phone Accessories', 'Laptop Accessories', 'Airpods', 'Earbuds/(pods)', 'Earphones', 'Headphones', 'Watches', 'Other']
    sample_listings = _prepare([
        _sample('Phone Accessories', 'Anker 20W USB-C Charger', '$18', 24, 'Nairobi', 'Fast compact charger with PowerIQ technology.', 'anker usb c fast charger product photo', year='2023', type='Wall charger', compatibility='iPhone & Android', condition='New', warranty='1 year'),
        _sample('Laptop Accessories', 'Ugreen Aluminium Laptop Stand', '$35', 15, 'Mombasa', 'Adjustable stand that keeps your laptop cool.', 'aluminium laptop stand product photo', year='2023', type='Laptop stand', compatibility='11 to 17 inch laptops', condition='New', warranty='1 year'),
        _sample('Airpods', 'Apple AirPods 3rd Gen', '$150', 29, 'Nairobi', 'Spatial audio with a comfortable open-fit design.', 'apple airpods 3rd generation product photo', year='2022', type='True wireless', compatibility='iPhone & iPad', condition='Like New', warranty='3 months'),
        _sample('Earbuds/(pods)', 'Xiaomi Redmi Buds 4', '$30', 18, 'Kisumu', 'Affordable ANC earbuds with a long battery.', 'xiaomi redmi buds earbuds product photo', year='2023', type='True wireless ANC', compatibility='Android & iOS', condition='New', warranty='1 year'),
        _sample('Earphones', 'Samsung AKG Wired Earphones', '$12', 8, 'Nakuru', 'Tangle-free wired earphones with a 3.5mm plug.', 'wired earphones with mic product photo', year='2023', type='Wired in-ear', compatibility='3.5mm devices', condition='New', warranty='6 months'),
        _sample('Headphones', 'Beats Solo3 Wireless', '$170', 20, 'Nairobi', 'On-ear wireless headphones with a 40-hour battery.', 'beats solo3 wireless headphones product photo', year='2022', type='On-ear wireless', compatibility='Bluetooth devices', condition='Like New', warranty='3 months'),
        _sample('Watches', 'Samsung Galaxy Watch6', '$260', 27, 'Thika', 'Health tracking smartwatch with a bright AMOLED display.', 'samsung galaxy watch smartwatch product photo', year='2023', type='Smartwatch', compatibility='Android', condition='New', warranty='1 year'),
        _sample('Other', 'Baseus 65W Power Bank 20000mAh', '$45', 13, 'Meru', 'Laptop-capable power bank with fast charging.', 'baseus power bank product photo', year='2023', type='Power bank', compatibility='USB-C devices', condition='New', warranty='1 year'),
    ], 'Accessories')
    return _render_category('accessories.html', brands, sample_listings)


@marketplace_bp.route('/tablets')
def tablets():
    brands = ['iPad', 'Samsung', 'Microsoft', 'Lenovo', 'Huawei', 'Amazon', 'Xiaomi', 'ASUS', 'Google', 'TCL']
    sample_listings = _prepare([
        _sample('iPad', 'Apple iPad Air 5', '$520', 32, 'Nairobi', 'M1-powered iPad Air with a 10.9-inch display.', 'apple ipad air tablet product photo', year='2022', storage='64GB', ram='8GB', condition='Like New', warranty='6 months'),
        _sample('Samsung', 'Samsung Galaxy Tab S9', '$700', 24, 'Mombasa', 'AMOLED tablet with an S-Pen in the box.', 'samsung galaxy tab tablet product photo', year='2023', storage='128GB', ram='8GB', condition='Like New', warranty='6 months'),
        _sample('Microsoft', 'Microsoft Surface Pro 9', '$880', 19, 'Nairobi', 'Tablet that works like a full laptop with a keyboard.', 'microsoft surface pro tablet product photo', year='2022', storage='256GB', ram='8GB', condition='Like New', warranty='6 months'),
        _sample('Lenovo', 'Lenovo Tab P11 Pro', '$380', 14, 'Kisumu', 'Big OLED display ideal for streaming.', 'lenovo tab p11 pro tablet product photo', year='2022', storage='128GB', ram='6GB', condition='Used', warranty='None'),
        _sample('Huawei', 'Huawei MatePad 11', '$330', 12, 'Nakuru', 'Smooth 120Hz tablet with quad speakers.', 'huawei matepad tablet product photo', year='2022', storage='128GB', ram='6GB', condition='Used', warranty='None'),
        _sample('Amazon', 'Amazon Fire HD 10', '$120', 21, 'Eldoret', 'Budget tablet perfect for reading and video.', 'amazon fire hd tablet product photo', year='2023', storage='32GB', ram='3GB', condition='New', warranty='1 year'),
        _sample('Xiaomi', 'Xiaomi Pad 6', '$300', 26, 'Thika', 'Snapdragon tablet with a 144Hz display.', 'xiaomi pad tablet product photo', year='2023', storage='128GB', ram='6GB', condition='New', warranty='1 year'),
        _sample('ASUS', 'ASUS Zenpad 8', '$160', 7, 'Meru', 'Compact 8-inch tablet for on-the-go use.', 'asus zenpad tablet product photo', year='2020', storage='32GB', ram='3GB', condition='Used', warranty='None'),
        _sample('Google', 'Google Pixel Tablet', '$450', 17, 'Nairobi', 'Android tablet that doubles as a smart display.', 'google pixel tablet product photo', year='2023', storage='128GB', ram='8GB', condition='Like New', warranty='6 months'),
        _sample('TCL', 'TCL NXTPAPER 11', '$220', 10, 'Mombasa', 'Paper-like display that is easy on the eyes.', 'tcl nxtpaper tablet product photo', year='2023', storage='128GB', ram='4GB', condition='New', warranty='1 year', status='sold'),
    ], 'Tablets')
    return _render_category('tablets.html', brands, sample_listings)


@marketplace_bp.route('/home-tech')
def home_tech():
    brands = ['Entertainment', 'Speakers', 'Soundbars', 'Climate', 'Security', 'Lighting', 'Kitchen', 'Cleaning', 'Power', 'Drones', 'Other']
    sample_listings = _prepare([
        _sample('Entertainment', 'Samsung 55" Crystal UHD 4K TV', '$520', 30, 'Nairobi', 'Smart 4K TV with a slim bezel and vivid colour.', 'samsung 55 inch 4k smart tv product photo', year='2023', type='4K Smart TV', power='120W', condition='Like New', warranty='6 months'),
        _sample('Speakers', 'JBL PartyBox 110', '$380', 22, 'Mombasa', 'Loud portable party speaker with light show.', 'jbl partybox bluetooth speaker product photo', year='2022', type='Party speaker', power='160W', condition='Like New', warranty='6 months'),
        _sample('Soundbars', 'LG S75Q Soundbar', '$420', 15, 'Nairobi', '3.1.2 channel soundbar with a wireless subwoofer.', 'lg soundbar with subwoofer product photo', year='2022', type='3.1.2ch soundbar', power='380W', condition='Used', warranty='None'),
        _sample('Climate', 'Xiaomi Smart Air Purifier 4', '$180', 18, 'Kisumu', 'Cleans the air and reports quality in real time.', 'xiaomi smart air purifier product photo', year='2023', type='Air purifier', power='33W', condition='New', warranty='1 year'),
        _sample('Security', 'Ring Video Doorbell 4', '$160', 12, 'Nakuru', 'See and speak to visitors from your phone.', 'smart video doorbell product photo', year='2022', type='Smart doorbell', power='Battery', condition='Like New', warranty='6 months'),
        _sample('Lighting', 'Philips Hue White & Colour Starter Kit', '$190', 20, 'Nairobi', 'Smart bulbs with millions of colours.', 'philips hue smart bulbs product photo', year='2023', type='Smart bulb kit', power='9W per bulb', condition='New', warranty='1 year'),
        _sample('Kitchen', 'Ninja Air Fryer 5.5L', '$170', 25, 'Thika', 'Crispy food with little to no oil.', 'ninja air fryer kitchen appliance product photo', year='2023', type='Air fryer', power='1750W', condition='New', warranty='1 year'),
        _sample('Cleaning', 'Roborock Q7 Robot Vacuum', '$340', 16, 'Eldoret', 'Maps your home and cleans without help.', 'robot vacuum cleaner product photo', year='2023', type='Robot vacuum', power='2400Pa suction', condition='Like New', warranty='6 months'),
        _sample('Power', 'EcoFlow River 2 Portable Power Station', '$290', 13, 'Meru', 'Backup power for outages and camping.', 'portable power station product photo', year='2023', type='Power station', power='300W output', condition='New', warranty='1 year'),
        _sample('Drones', 'DJI Mini 3', '$460', 21, 'Nairobi', 'Lightweight camera drone under 249g.', 'dji mini 3 camera drone product photo', year='2023', type='Camera drone', power='Battery', condition='Like New', warranty='6 months'),
        _sample('Other', 'Google Nest Hub 2nd Gen', '$95', 14, 'Mombasa', 'Smart display for your home controls.', 'google nest hub smart display product photo', year='2022', type='Smart display', power='15W', condition='Used', warranty='None'),
    ], 'Home Tech')
    return _render_category('home_tech.html', brands, sample_listings)


@marketplace_bp.route('/drones')
def drones():
    brands = ['DJI', 'Parrot', 'Autel', 'Holy Stone', 'Skydio', 'Yuneec', 'Hubsan', 'Ryze', 'PowerVision', 'Walkera']
    sample_listings = _prepare([
        _sample('DJI', 'DJI Air 3', '$980', 29, 'Nairobi', 'Dual-camera drone with a long flight time.', 'dji air 3 camera drone product photo', year='2023', camera='4K/60 HDR', flight_time='46 min', condition='Like New', warranty='6 months'),
        _sample('Parrot', 'Parrot Anafi USA', '$1,150', 11, 'Mombasa', 'Compact thermal-capable drone for professionals.', 'parrot anafi drone product photo', year='2022', camera='4K HDR', flight_time='32 min', condition='Used', warranty='None'),
        _sample('Autel', 'Autel EVO Lite+', '$1,020', 19, 'Nairobi', '1-inch sensor drone with adjustable aperture.', 'autel evo lite drone product photo', year='2023', camera='6K', flight_time='40 min', condition='Like New', warranty='6 months'),
        _sample('Holy Stone', 'Holy Stone HS720E', '$280', 13, 'Kisumu', 'Easy-to-fly GPS drone for beginners.', 'holy stone camera drone product photo', year='2022', camera='4K EIS', flight_time='26 min', condition='Used', warranty='None'),
        _sample('Skydio', 'Skydio 2+', '$1,300', 16, 'Nakuru', 'Autonomous drone that follows and films you.', 'skydio autonomous drone product photo', year='2022', camera='4K60', flight_time='27 min', condition='Like New', warranty='3 months'),
        _sample('Yuneec', 'Yuneec Typhoon H3', '$890', 8, 'Eldoret', 'Six-rotor drone with a retractable landing gear.', 'yuneec typhoon drone product photo', year='2020', camera='4K', flight_time='25 min', condition='Used', warranty='None'),
        _sample('Hubsan', 'Hubsan Zino Pro+', '$420', 12, 'Thika', 'Folding drone with a 4K gimbal camera.', 'hubsan zino drone product photo', year='2022', camera='4K', flight_time='43 min', condition='Like New', warranty='6 months'),
        _sample('Ryze', 'Ryze Tello', '$110', 22, 'Meru', 'Tiny drone perfect for learning to fly.', 'ryze tello mini drone product photo', year='2021', camera='720p', flight_time='13 min', condition='Used', warranty='None'),
        _sample('PowerVision', 'PowerVision PowerEgg X', '$640', 9, 'Mombasa', 'All-weather drone that doubles as a handheld camera.', 'powervision drone product photo', year='2021', camera='4K', flight_time='30 min', condition='Used', warranty='None'),
        _sample('Walkera', 'Walkera Vitus 320', '$700', 10, 'Nairobi', 'Portable folding drone with gesture control.', 'walkera vitus drone product photo', year='2021', camera='4K', flight_time='33 min', condition='Like New', warranty='3 months', status='sold'),
    ], 'Drones')
    return _render_category('drones.html', brands, sample_listings)

@marketplace_bp.route('/fashion')
def fashion():
    try:
        fashion_listings = Listing.query.filter_by(
            category='Fashion',
            is_active=True
        ).all()
    except:
        fashion_listings = []
    return render_template('fashion.html', listings=fashion_listings)



# ============ FASHION SUBCATEGORIES ROUTES ============

@marketplace_bp.route('/fashion/bags')
def bags():
    brands = ['Travelling Bags', 'Wallets', 'Sling Bags', 'Back Packs', 'Hand Bags', 'Other']
    sample_listings = _prepare([
        _sample('Travelling Bags', 'Hard-Shell Cabin Trolley 20"', '$85', 21, 'Nairobi', 'Lightweight cabin suitcase with spinner wheels and a TSA lock.', 'hard shell cabin trolley suitcase product photo', type='Hard-shell trolley', material='Polycarbonate', colour='Black', warranty='1 year', condition='New'),
        _sample('Back Packs', 'Water-Resistant Laptop Backpack', '$45', 18, 'Mombasa', 'Everyday backpack with a padded 15-inch laptop sleeve.', 'water resistant laptop backpack product photo', type='Laptop backpack', material='Nylon', colour='Grey', warranty='6 months', condition='New'),
        _sample('Hand Bags', 'Leather Tote Handbag', '$120', 27, 'Nairobi', 'Spacious genuine-leather tote for work and weekends.', 'leather tote handbag product photo', type='Tote', material='Genuine leather', colour='Tan', warranty='6 months', condition='Like New'),
        _sample('Wallets', 'Bifold Leather Wallet', '$25', 14, 'Kisumu', 'Slim bifold wallet with RFID-blocking card slots.', 'bifold leather wallet product photo', type='Bifold', material='Leather', colour='Brown', warranty='3 months', condition='New'),
        _sample('Sling Bags', 'Crossbody Sling Bag', '$32', 11, 'Nakuru', 'Compact sling bag that keeps essentials close.', 'crossbody sling bag product photo', type='Crossbody', material='Canvas', colour='Navy', warranty='3 months', condition='New'),
        _sample('Other', 'Travel Duffel Bag 45L', '$55', 16, 'Thika', 'Durable duffel with a separate shoe compartment.', 'travel duffel bag product photo', type='Duffel', material='Polyester', colour='Green', warranty='6 months', condition='Like New'),
        _sample('Travelling Bags', 'Soft-Shell Check-In Suitcase 28"', '$110', 13, 'Eldoret', 'Expandable check-in case with four spinner wheels.', 'soft shell check in suitcase product photo', type='Soft-shell trolley', material='Polyester', colour='Charcoal', warranty='1 year', condition='Used'),
        _sample('Back Packs', 'Anti-Theft Travel Backpack', '$60', 22, 'Nairobi', 'Hidden zips and a USB port for secure travel.', 'anti theft travel backpack product photo', type='Travel backpack', material='Polyester', colour='Black', warranty='6 months', condition='New', status='sold'),
        _sample('Hand Bags', 'Quilted Shoulder Bag', '$95', 19, 'Mombasa', 'Chain-strap shoulder bag with a quilted finish.', 'quilted shoulder bag product photo', type='Shoulder bag', material='Faux leather', colour='Beige', warranty='3 months', condition='Like New'),
    ], 'Bags')
    return _render_category('fashion.bags.html', brands, sample_listings)


@marketplace_bp.route('/fashion/clothing')
def clothing():
    brands = ['T-Shirts', 'Shirts', 'Jackets', 'Sweater', 'Hoody',
              'Scuffs', 'Blouses & tops', 'Dresses', 'Trousers', ' Jeans',
              'Pants', 'Shorts','Track-Suits', 'Pyjamas']
    sample_listings = _prepare([
        _sample('T-Shirts', 'Classic Cotton Crew Tee', '$15', 34, 'Nairobi', 'Soft combed-cotton tee that holds its shape.', 'classic cotton crew neck t shirt product photo', size='M', fit='Regular', colour='White', material='100% Cotton', condition='New'),
        _sample('Shirts', 'Oxford Button-Down Shirt', '$28', 21, 'Mombasa', 'Smart-casual oxford shirt for work or weekends.', 'oxford button down shirt product photo', size='L', fit='Slim', colour='Light Blue', material='Cotton', condition='New'),
        _sample('Jackets', 'Waterproof Windbreaker Jacket', '$65', 18, 'Kisumu', 'Light packable shell that blocks wind and rain.', 'waterproof windbreaker jacket product photo', size='XL', fit='Regular', colour='Olive', material='Polyester', condition='Like New'),
        _sample('Sweater', 'Merino Wool Sweater', '$48', 15, 'Nakuru', 'Warm breathable merino knit for cool evenings.', 'merino wool sweater product photo', size='M', fit='Regular', colour='Burgundy', material='Merino wool', condition='Like New'),
        _sample('Hoody', 'Fleece Pullover Hoodie', '$38', 29, 'Nairobi', 'Cosy fleece hoodie with a kangaroo pocket.', 'fleece pullover hoodie product photo', size='L', fit='Regular', colour='Charcoal', material='Cotton blend', condition='New'),
        _sample('Blouses & tops', 'Floral Chiffon Blouse', '$26', 12, 'Thika', 'Flowy chiffon blouse with a flattering drape.', 'floral chiffon blouse product photo', size='S', fit='Relaxed', colour='Floral', material='Chiffon', condition='New'),
        _sample('Dresses', 'Midi Wrap Dress', '$52', 24, 'Mombasa', 'Elegant wrap dress that flatters every shape.', 'midi wrap dress product photo', size='M', fit='Wrap', colour='Emerald', material='Viscose', condition='Like New'),
        _sample('Trousers', 'Tailored Chino Trousers', '$35', 16, 'Eldoret', 'Stretch chinos with a neat tailored cut.', 'tailored chino trousers product photo', size='32', fit='Slim', colour='Khaki', material='Cotton twill', condition='Used'),
        _sample(' Jeans', 'Straight-Cut Denim Jeans', '$40', 27, 'Nairobi', 'Classic straight-leg jeans in mid-wash denim.', 'straight cut denim jeans product photo', size='34', fit='Straight', colour='Mid Blue', material='Denim', condition='Like New'),
        _sample('Shorts', 'Cargo Casual Shorts', '$22', 9, 'Meru', 'Everyday cargo shorts with roomy pockets.', 'cargo casual shorts product photo', size='M', fit='Regular', colour='Stone', material='Cotton', condition='New', status='sold'),
        _sample('Track-Suits', 'Two-Piece Tracksuit', '$58', 20, 'Nairobi', 'Matching zip jacket and joggers for training.', 'two piece tracksuit product photo', size='L', fit='Athletic', colour='Navy', material='Polyester', condition='New'),
    ], 'Clothing')
    return _render_category('fashion.clothing.html', brands, sample_listings)


@marketplace_bp.route('/fashion/footwear')
def footwear():
    brands = ['Sneakers', 'Loafers',
              'Sandals', 'Boots',
              'Crocs', 'Slides', 'School Shoes', 'Slippers & flip-flops', 'Ballet flats', 'Heels & Wedges']
    sample_listings = _prepare([
        _sample('Sneakers', 'Retro Running Sneakers', '$70', 26, 'Nairobi', 'Cushioned retro trainers for all-day comfort.', 'retro running sneakers product photo', size='42', type='Low-top', colour='White', material='Mesh', condition='New'),
        _sample('Loafers', 'Suede Penny Loafers', '$85', 17, 'Mombasa', 'Classic suede loafers for smart-casual looks.', 'suede penny loafers product photo', size='43', type='Slip-on', colour='Brown', material='Suede', condition='Like New'),
        _sample('Sandals', 'Strappy Leather Sandals', '$40', 12, 'Kisumu', 'Handmade leather sandals with adjustable straps.', 'strappy leather sandals product photo', size='39', type='Open-toe', colour='Tan', material='Leather', condition='New'),
        _sample('Boots', 'Chelsea Ankle Boots', '$110', 23, 'Nairobi', 'Timeless Chelsea boots with elastic side panels.', 'chelsea ankle boots product photo', size='41', type='Ankle boot', colour='Black', material='Leather', condition='Like New'),
        _sample('Crocs', 'Classic Clogs', '$35', 30, 'Nakuru', 'Lightweight ventilated clogs for everyday wear.', 'classic clog shoes product photo', size='40', type='Clog', colour='Navy', material='EVA foam', condition='New'),
        _sample('Slides', 'Cushioned Pool Slides', '$20', 14, 'Thika', 'Soft slides ideal for the beach and gym.', 'cushioned pool slides product photo', size='44', type='Slide', colour='Black', material='Rubber', condition='New'),
        _sample('School Shoes', 'Durable School Shoes', '$30', 8, 'Meru', 'Scuff-resistant black shoes built for school days.', 'durable black school shoes product photo', size='38', type='Lace-up', colour='Black', material='Faux leather', condition='New'),
        _sample('Slippers & flip-flops', 'Beach Flip-Flops', '$12', 11, 'Eldoret', 'Quick-dry flip-flops with a grippy sole.', 'beach flip flops product photo', size='42', type='Flip-flop', colour='Blue', material='Rubber', condition='New', status='sold'),
        _sample('Ballet flats', 'Pointed Ballet Flats', '$45', 19, 'Nairobi', 'Simple ballet flats that pair with anything.', 'pointed ballet flats product photo', size='37', type='Flat', colour='Nude', material='Faux leather', condition='Like New'),
        _sample('Heels & Wedges', 'Block-Heel Pumps', '$65', 21, 'Mombasa', 'Comfortable block heels for long events.', 'block heel pumps product photo', size='38', type='Heel', colour='Red', material='Patent leather', condition='Like New'),
    ], 'Footwear')
    return _render_category('fashion.footwear.html', brands, sample_listings)


@marketplace_bp.route('/fashion/formal')
def formal_wear():
    brands = ['Hugo Boss', 'Armani', 'Calvin Klein', 'Ralph Lauren', 'Tom Ford', 'Brooks Brothers']
    sample_listings = _prepare([
        _sample('Hugo Boss', 'Hugo Boss Slim-Fit Suit', '$420', 24, 'Nairobi', 'Sharp two-piece suit in a breathable wool blend.', 'hugo boss slim fit suit product photo', size='40R', colour='Charcoal', material='Wool blend', warranty='6 months', condition='Like New'),
        _sample('Armani', 'Giorgio Armani Dress Shirt', '$180', 19, 'Mombasa', 'Crisp cotton dress shirt with mother-of-pearl buttons.', 'armani dress shirt product photo', size='16', colour='White', material='Cotton', warranty='3 months', condition='New'),
        _sample('Calvin Klein', 'Calvin Klein Silk Tie', '$60', 15, 'Nairobi', 'Pure silk tie with a subtle sheen.', 'calvin klein silk tie product photo', size='Standard', colour='Navy', material='Silk', warranty='None', condition='New'),
        _sample('Ralph Lauren', 'Ralph Lauren Blazer', '$260', 21, 'Kisumu', 'Single-breasted blazer for smart occasions.', 'ralph lauren blazer product photo', size='42R', colour='Navy', material='Wool', warranty='6 months', condition='Like New'),
        _sample('Tom Ford', 'Tom Ford Tuxedo Jacket', '$890', 17, 'Nairobi', 'Luxury satin-lapel tuxedo jacket for black-tie events.', 'tom ford tuxedo jacket product photo', size='40R', colour='Black', material='Wool silk', warranty='3 months', condition='Like New'),
        _sample('Brooks Brothers', 'Brooks Brothers Dress Trousers', '$140', 13, 'Nakuru', 'Classic wool dress trousers with a clean drape.', 'brooks brothers dress trousers product photo', size='34', colour='Grey', material='Wool', warranty='6 months', condition='New'),
        _sample('Hugo Boss', 'Hugo Boss Leather Belt', '$75', 10, 'Thika', 'Reversible leather belt with a brushed buckle.', 'hugo boss leather belt product photo', size='34', colour='Black', material='Leather', warranty='3 months', condition='Used'),
        _sample('Armani', 'Armani Wool Overcoat', '$520', 22, 'Eldoret', 'Tailored single-breasted overcoat for winter.', 'armani wool overcoat product photo', size='40R', colour='Camel', material='Wool', warranty='6 months', condition='Like New', status='sold'),
    ], 'Formal Wear')
    return _render_category('fashion.formal.html', brands, sample_listings)


@marketplace_bp.route('/fashion/jewellery')
def jewellery():
    brands = ['Necklace', 'Ear-rings', 'Bandles', 'Rings']
    sample_listings = _prepare([
        _sample('Necklace', 'Gold-Plated Pendant Necklace', '$55', 22, 'Nairobi', 'Delicate pendant necklace with an 18k gold plating.', 'gold plated pendant necklace product photo', type='Pendant', material='Gold-plated brass', stone='Cubic zirconia', warranty='3 months', condition='New'),
        _sample('Ear-rings', 'Diamond Stud Earrings', '$180', 27, 'Mombasa', 'Classic studs set with brilliant-cut stones.', 'diamond stud earrings product photo', type='Stud', material='Sterling silver', stone='Diamond', warranty='6 months', condition='New'),
        _sample('Bandles', 'Silver Charm Bangle', '$40', 14, 'Kisumu', 'Everyday bangle with a polished silver finish.', 'silver charm bangle product photo', type='Bangle', material='Sterling silver', stone='None', warranty='3 months', condition='New'),
        _sample('Rings', 'Rose Gold Solitaire Ring', '$320', 25, 'Nairobi', 'Elegant solitaire ring in rose gold vermeil.', 'rose gold solitaire ring product photo', type='Solitaire', material='Rose gold vermeil', stone='Moissanite', warranty='6 months', condition='Like New'),
        _sample('Necklace', 'Pearl Strand Necklace', '$75', 18, 'Nakuru', 'Timeless freshwater pearl necklace.', 'freshwater pearl necklace product photo', type='Strand', material='Sterling silver', stone='Freshwater pearl', warranty='3 months', condition='Like New'),
        _sample('Ear-rings', 'Gold Hoop Earrings', '$28', 20, 'Thika', 'Lightweight gold-tone hoops for daily wear.', 'gold hoop earrings product photo', type='Hoop', material='Gold-plated steel', stone='None', warranty='None', condition='New'),
        _sample('Bandles', 'Traditional Kada Bangle Set', '$32', 11, 'Meru', 'Traditional bangle set with intricate detailing.', 'traditional kada bangle set product photo', type='Bangle set', material='Brass', stone='None', warranty='None', condition='Used'),
        _sample('Rings', 'Titanium Wedding Band', '$90', 13, 'Eldoret', 'Brushed titanium band built to last.', 'brushed titanium ring band product photo', type='Band', material='Titanium', stone='None', warranty='1 year', condition='New', status='sold'),
    ], 'Jewellery')
    return _render_category('fashion.jewellery.html', brands, sample_listings)


@marketplace_bp.route('/fashion/kids')
def kids_fashion():
    brands = ['Socks', 'Jackets', 'Shirts', 'T‑Shirts', 'Tracksuits', 'Dresses', 'Shorts', 'Jeans', 'Pajamas', 'Hoodies']
    sample_listings = _prepare([
        _sample('Socks', 'Kids Cotton Socks (5-Pack)', '$10', 16, 'Nairobi', 'Soft cotton socks in fun colours for little feet.', 'kids cotton socks multi pack product photo', size='2-4Y', age='3-4 years', colour='Assorted', material='Cotton', condition='New'),
        _sample('Jackets', 'Kids Padded Puffer Jacket', '$35', 19, 'Mombasa', 'Warm padded jacket for chilly mornings.', 'kids padded puffer jacket product photo', size='4Y', age='4 years', colour='Blue', material='Polyester', condition='New'),
        _sample('Shirts', 'Kids Checked Shirt', '$18', 12, 'Kisumu', 'Smart checked shirt for family occasions.', 'kids checked shirt product photo', size='3Y', age='3 years', colour='Red', material='Cotton', condition='New'),
        _sample('T‑Shirts', 'Kids Graphic Tee', '$12', 22, 'Nairobi', 'Bright printed tee with a soft hand feel.', 'kids graphic t shirt product photo', size='4Y', age='4 years', colour='Yellow', material='Cotton', condition='New'),
        _sample('Tracksuits', 'Kids Tracksuit Set', '$28', 15, 'Nakuru', 'Comfy two-piece tracksuit for playtime.', 'kids tracksuit set product photo', size='3Y', age='3 years', colour='Grey', material='Cotton blend', condition='Like New'),
        _sample('Dresses', 'Kids Party Dress', '$30', 21, 'Thika', 'Twirl-worthy party dress with tulle layers.', 'kids party dress product photo', size='4Y', age='4 years', colour='Pink', material='Polyester', condition='Like New'),
        _sample('Shorts', 'Kids Denim Shorts', '$14', 9, 'Meru', 'Durable denim shorts with an adjustable waist.', 'kids denim shorts product photo', size='3Y', age='3 years', colour='Blue', material='Denim', condition='New', status='sold'),
        _sample('Jeans', 'Kids Stretch Jeans', '$20', 13, 'Eldoret', 'Soft stretch jeans that move with active kids.', 'kids stretch jeans product photo', size='4Y', age='4 years', colour='Dark Blue', material='Cotton denim', condition='New'),
        _sample('Pajamas', 'Kids Pyjama Set', '$16', 17, 'Nairobi', 'Cosy pyjamas with a friendly print.', 'kids pyjama set product photo', size='3Y', age='3 years', colour='Navy', material='Cotton', condition='New'),
        _sample('Hoodies', 'Kids Fleece Hoodie', '$22', 11, 'Mombasa', 'Warm fleece hoodie for cool days.', 'kids fleece hoodie product photo', size='4Y', age='4 years', colour='Green', material='Fleece', condition='Like New'),
    ], 'Kids Fashion')
    return _render_category('fashion.kids.html', brands, sample_listings)

@marketplace_bp.route('/fashion/preloved')
def preloved():
    brands = ['Socks', 'Jackets', 'Hoody', 'T‑Shirts', 'Shirts', 'Shoes', 'Sneakers', 'Jeans', 'Dresses', 'Shorts']
    sample_listings = _prepare([
        _sample('Socks', 'Preloved Ankle Socks (3-Pack)', '$5', 8, 'Nairobi', 'Gently worn ankle socks, freshly laundered.', 'preloved ankle socks product photo', size='Free', colour='White', warranty='None', condition='Used'),
        _sample('Jackets', 'Preloved Denim Jacket', '$25', 19, 'Mombasa', 'Vintage denim jacket with a lived-in fade.', 'vintage denim jacket product photo', size='L', colour='Blue', warranty='None', condition='Used'),
        _sample('Hoody', 'Preloved Fleece Hoodie', '$18', 14, 'Kisumu', 'Cosy preloved hoodie with plenty of life left.', 'preloved fleece hoodie product photo', size='M', colour='Grey', warranty='None', condition='Used'),
        _sample('T‑Shirts', 'Preloved Graphic Tee', '$8', 12, 'Nairobi', 'Soft graphic tee in great condition.', 'preloved graphic t shirt product photo', size='M', colour='Black', warranty='None', condition='Used'),
        _sample('Shirts', 'Preloved Oxford Shirt', '$14', 10, 'Nakuru', 'Button-down shirt with minimal wear.', 'preloved oxford shirt product photo', size='L', colour='Sky Blue', warranty='None', condition='Used'),
        _sample('Shoes', 'Preloved Leather Shoes', '$30', 15, 'Thika', 'Well-kept leather shoes with fresh soles.', 'preloved leather shoes product photo', size='42', colour='Brown', warranty='None', condition='Used'),
        _sample('Sneakers', 'Preloved Running Sneakers', '$35', 21, 'Eldoret', 'Clean preloved sneakers with plenty of tread.', 'preloved running sneakers product photo', size='43', colour='White', warranty='None', condition='Like New'),
        _sample('Jeans', 'Preloved Straight Jeans', '$16', 13, 'Meru', 'Classic straight jeans with a comfortable fit.', 'preloved straight jeans product photo', size='32', colour='Indigo', warranty='None', condition='Used', status='sold'),
        _sample('Dresses', 'Preloved Summer Dress', '$20', 17, 'Nairobi', 'Floral summer dress, worn once.', 'preloved summer dress product photo', size='S', colour='Floral', warranty='None', condition='Like New'),
        _sample('Shorts', 'Preloved Cargo Shorts', '$12', 9, 'Mombasa', 'Durable cargo shorts with roomy pockets.', 'preloved cargo shorts product photo', size='M', colour='Khaki', warranty='None', condition='Used'),
    ], 'Preloved')
    return _render_category('fashion.preloved.html', brands, sample_listings)


@marketplace_bp.route('/fashion/sports')
def activewear():
    brands = [
  "Soccer",  "Basketball",  "Tennis",  "Cricket",
  "Rugby",  "Running & Athletics",  "Swimming",  "Cycling",
  "Golf",  "Boxing & Martial Arts", "Baseball",  "Hockey",  "Volleyball",  "Gymnastics",
  "Skiing & Snowboarding",  "Field Hockey",  "Badminton",
  "Weightlifting & Crossfit",  "Netball"
]
    sample_listings = _prepare([
        _sample('Running & Athletics', 'Moisture-Wicking Running Tee', '$28', 24, 'Nairobi', 'Breathable running top that wicks sweat fast.', 'moisture wicking running t shirt product photo', sport='Running', size='M', colour='Neon Green', material='Polyester', condition='New'),
        _sample('Soccer', 'Soccer Training Kit', '$45', 19, 'Mombasa', 'Two-piece training kit with a breathable jersey.', 'soccer training kit product photo', sport='Football', size='L', colour='Blue', material='Polyester', condition='New'),
        _sample('Basketball', 'Basketball Jersey & Shorts', '$38', 22, 'Kisumu', 'Sleeveless jersey and shorts set for the court.', 'basketball jersey and shorts product photo', sport='Basketball', size='XL', colour='Red', material='Mesh polyester', condition='New'),
        _sample('Cycling', 'Padded Cycling Shorts', '$42', 16, 'Nakuru', 'Chamois-padded shorts for longer rides.', 'padded cycling shorts product photo', sport='Cycling', size='M', colour='Black', material='Spandex', condition='New'),
        _sample('Swimming', 'Competition Swim Suit', '$55', 14, 'Thika', 'Chlorine-resistant racing swimsuit.', 'competition swimsuit product photo', sport='Swimming', size='32', colour='Navy', material='Lycra', condition='New'),
        _sample('Tennis', 'Tennis Polo Shirt', '$32', 12, 'Nairobi', 'Classic tennis polo with sweat-wicking fabric.', 'tennis polo shirt product photo', sport='Tennis', size='M', colour='White', material='Cotton blend', condition='Like New'),
        _sample('Weightlifting & Crossfit', 'Crossfit Training Shorts', '$30', 18, 'Eldoret', 'Stretch shorts built for lifting and WODs.', 'crossfit training shorts product photo', sport='CrossFit', size='L', colour='Grey', material='Nylon spandex', condition='New'),
        _sample('Rugby', 'Rugby Training Jersey', '$40', 11, 'Meru', 'Reinforced rugby jersey for contact training.', 'rugby training jersey product photo', sport='Rugby', size='XL', colour='Green', material='Polyester', condition='Like New'),
        _sample('Golf', 'Golf Performance Polo', '$48', 15, 'Nairobi', 'Breathable polo with UV protection for the course.', 'golf performance polo product photo', sport='Golf', size='L', colour='Sky Blue', material='Polyester', condition='New'),
        _sample('Boxing & Martial Arts', 'Muay Thai Training Shorts', '$26', 13, 'Mombasa', 'Lightweight satin shorts for striking sports.', 'muay thai training shorts product photo', sport='Muay Thai', size='M', colour='Black', material='Satin', condition='New', status='sold'),
    ], 'Sportswear')
    return _render_category('fashion.sports.html', brands, sample_listings)

# ================== VEHICLES ====================
@marketplace_bp.route('/vehicles')
def vehicles():
    try:
        vehicles_listings = Listing.query.filter_by(
            category='Vehicles',
            is_active=True
        ).all()
    except:
        vehicles_listings = []
    return render_template('vehicles.html', listings=vehicles_listings)

# ============ VEHICLES SUBCATEGORIES ROUTES ============
@marketplace_bp.route('/vehicles/caravans')
def caravans():
    brands = ['Jurgens', 'Sprite', 'Bush Lapa', 'Conqueror', 'Afrispoor', 'Echo']
    sample_listings = _prepare([
        _sample('Jurgens', 'Jurgens Exclusive Deluxe', '$18,500', 16, 'Nairobi', 'Family caravan with a full bathroom and separate kids bunks.', 'jurgens exclusive caravan product photo', year='2021', berths='4 berths', length='6.5 m', condition='Used', warranty='6 months'),
        _sample('Sprite', 'Sprite Tourer SP', '$22,000', 21, 'Mombasa', 'Modern tow-behind caravan with an outdoor kitchen.', 'sprite tourer caravan product photo', year='2022', berths='4 berths', length='6.2 m', condition='Like New', warranty='1 year'),
        _sample('Bush Lapa', 'Bush Lapa Miskruier', '$28,500', 27, 'Nakuru', 'Rugged off-road caravan built for the bush.', 'bush lapa miskruier caravan product photo', year='2023', berths='2 berths', length='5.0 m', condition='New', warranty='2 years'),
        _sample('Conqueror', 'Conqueror UEV-490', '$31,000', 24, 'Nairobi', 'Hybrid off-road camper with an expandable hard shell.', 'conqueror uev off-road camper product photo', year='2023', berths='4 berths', length='4.9 m', condition='New', warranty='2 years'),
        _sample('Afrispoor', 'Afrispoor Cheetah', '$15,900', 13, 'Kisumu', 'Compact four-sleeper camper trailer for weekend trips.', 'afrispoor cheetah camper trailer product photo', year='2020', berths='4 berths', length='4.4 m', condition='Used', warranty='None'),
        _sample('Echo', 'Echo 4x4 Trailer', '$12,750', 11, 'Eldoret', 'Tough 4x4 trailer with a rooftop tent setup.', 'echo 4x4 off-road trailer product photo', year='2019', berths='2 berths', length='3.8 m', condition='Used', warranty='None'),
        _sample('Sprite', 'Sprite Splash 400', '$19,400', 15, 'Thika', 'Lightweight two-berth caravan that tows easily.', 'sprite splash caravan product photo', year='2022', berths='2 berths', length='5.4 m', condition='Like New', warranty='6 months'),
        _sample('Jurgens', 'Jurgens Safari Xplorer', '$24,900', 19, 'Nairobi', 'Off-road caravan with an independent suspension.', 'jurgens safari caravan product photo', year='2021', berths='4 berths', length='5.8 m', condition='Used', warranty='3 months', status='sold'),
    ], 'Caravans & Campers')
    return _render_category('vehicles.caravans.html', brands, sample_listings)


@marketplace_bp.route('/vehicles/cars')
def cars():
    brands = ['Vintage', 'Toyota', 'Volkswagen', 'BMW', 'Mercedes-Benz', 'Ford', 'Honda', 'Hyundai', 'Audi', 'Nissan', 'Mitsubishi']
    sample_listings = _prepare([
        _sample('Vintage', 'Classic VW Beetle', '$9,500', 18, 'Nairobi', 'Restored vintage Beetle with a rebuilt engine.', 'classic volkswagen beetle car product photo', year='1972', mileage='82,000 km', transmission='Manual', fuel='Petrol', condition='Used', warranty='None'),
        _sample('Toyota', 'Toyota Harrier 2020', '$12,500', 14, 'Nairobi', 'Clean SUV import with a spacious leather interior.', 'toyota harrier suv product photo', year='2020', mileage='45,000 km', transmission='Automatic', fuel='Petrol', condition='Used', warranty='6 months'),
        _sample('Volkswagen', 'Volkswagen Golf GTI', '$14,800', 23, 'Mombasa', 'Hot hatch with DSG gearbox and sport seats.', 'volkswagen golf gti car product photo', year='2019', mileage='58,000 km', transmission='Automatic', fuel='Petrol', condition='Like New', warranty='6 months'),
        _sample('BMW', 'BMW 3 Series 320i', '$21,900', 29, 'Nairobi', 'Executive sedan with a turbocharged petrol engine.', 'bmw 3 series sedan product photo', year='2021', mileage='36,000 km', transmission='Automatic', fuel='Petrol', condition='Like New', warranty='1 year'),
        _sample('Mercedes-Benz', 'Mercedes-Benz C200', '$24,500', 26, 'Nairobi', 'Luxury sedan with ambient lighting and a panoramic roof.', 'mercedes benz c200 sedan product photo', year='2020', mileage='41,000 km', transmission='Automatic', fuel='Petrol', condition='Like New', warranty='6 months'),
        _sample('Ford', 'Ford Ranger Wildtrak', '$18,300', 20, 'Nakuru', 'Double-cab pickup ready for both work and family.', 'ford ranger pickup product photo', year='2020', mileage='72,000 km', transmission='Automatic', fuel='Diesel', condition='Used', warranty='3 months'),
        _sample('Honda', 'Honda Civic RS', '$13,700', 17, 'Kisumu', 'Sporty sedan with a punchy turbo engine.', 'honda civic sedan product photo', year='2019', mileage='63,000 km', transmission='Automatic', fuel='Petrol', condition='Used', warranty='None'),
        _sample('Hyundai', 'Hyundai Tucson 2021', '$16,900', 15, 'Eldoret', 'Family SUV with a five-year warranty history.', 'hyundai tucson suv product photo', year='2021', mileage='38,000 km', transmission='Automatic', fuel='Petrol', condition='Like New', warranty='1 year'),
        _sample('Audi', 'Audi A4 40 TFSI', '$22,400', 19, 'Nairobi', 'Refined sedan with quattro all-wheel drive.', 'audi a4 sedan product photo', year='2020', mileage='49,000 km', transmission='Automatic', fuel='Petrol', condition='Like New', warranty='6 months'),
        _sample('Nissan', 'Nissan X-Trail 4WD', '$15,600', 12, 'Thika', 'Seven-seater SUV ideal for family road trips.', 'nissan xtrail suv product photo', year='2019', mileage='68,000 km', transmission='Automatic', fuel='Petrol', condition='Used', warranty='None'),
        _sample('Mitsubishi', 'Mitsubishi Outlander PHEV', '$17,800', 11, 'Meru', 'Plug-in hybrid SUV with low running costs.', 'mitsubishi outlander suv product photo', year='2020', mileage='52,000 km', transmission='Automatic', fuel='Hybrid', condition='Used', warranty='3 months', status='sold'),
    ], 'Cars')
    return _render_category('vehicles.cars.html', brands, sample_listings)


@marketplace_bp.route('/vehicles/commercial')
def vehicles_commercial():
    brands = ['Toyota', 'Mercedes-Benz', 'Volvo', 'Scania', 'MAN', 'Iveco', 'Tata', 'Hino']
    sample_listings = _prepare([
        _sample('Toyota', 'Toyota Hiace Van', '$21,000', 15, 'Nairobi', 'Reliable 14-seater commuter van in daily use.', 'toyota hiace commercial van product photo', year='2020', mileage='88,000 km', payload='1.2 tonnes', transmission='Manual', condition='Used', warranty='3 months'),
        _sample('Mercedes-Benz', 'Mercedes-Benz Sprinter 519', '$38,500', 19, 'Mombasa', 'Long-wheelbase panel van for freight delivery.', 'mercedes benz sprinter van product photo', year='2021', mileage='64,000 km', payload='2.5 tonnes', transmission='Automatic', condition='Like New', warranty='1 year'),
        _sample('Volvo', 'Volvo FH16 Tractor', '$95,000', 12, 'Nairobi', 'Line-haul tractor unit with a powerful 16-litre engine.', 'volvo fh16 truck tractor product photo', year='2019', mileage='420,000 km', payload='25 tonnes', transmission='Automatic', condition='Used', warranty='6 months'),
        _sample('Scania', 'Scania R450 Hauler', '$88,500', 14, 'Nakuru', 'Fuel-efficient R-series prime mover for long routes.', 'scania r450 truck product photo', year='2020', mileage='360,000 km', payload='24 tonnes', transmission='Automatic', condition='Used', warranty='3 months'),
        _sample('MAN', 'MAN TGS 26.440', '$79,900', 10, 'Eldoret', 'Rugged tipper chassis for construction haulage.', 'man tgs tipper truck product photo', year='2018', mileage='480,000 km', payload='18 tonnes', transmission='Manual', condition='Used', warranty='None'),
        _sample('Iveco', 'Iveco Daily 70C', '$30,200', 11, 'Kisumu', 'Cargo truck with a roomy refrigerated body option.', 'iveco daily cargo truck product photo', year='2021', mileage='92,000 km', payload='3.5 tonnes', transmission='Manual', condition='Like New', warranty='6 months'),
        _sample('Tata', 'Tata LPT 1613', '$42,000', 8, 'Thika', 'Affordable medium-duty truck built for tough roads.', 'tata lpt truck product photo', year='2020', mileage='150,000 km', payload='9 tonnes', transmission='Manual', condition='Used', warranty='3 months'),
        _sample('Hino', 'Hino 500 Series', '$55,700', 9, 'Meru', 'Dependable freight truck with a comfortable cab.', 'hino 500 truck product photo', year='2021', mileage='130,000 km', payload='11 tonnes', transmission='Manual', condition='Like New', warranty='1 year', status='sold'),
    ], 'Commercial Vehicles')
    return _render_category('vehicles.commercial.html', brands, sample_listings)


@marketplace_bp.route('/vehicles/motorcycles')
def motorcycles():
    brands = ['Harley-Davidson', 'Honda', 'Yamaha', 'Suzuki', 'Kawasaki', 'BMW', 'Ducati', 'Triumph']
    sample_listings = _prepare([
        _sample('Harley-Davidson', 'Harley-Davidson Fat Boy', '$19,500', 24, 'Nairobi', 'Iconic cruiser with a thumping Milwaukee-Eight engine.', 'harley davidson fat boy motorcycle product photo', year='2020', engine='1868cc V-twin', mileage='12,000 km', transmission='6-speed', condition='Like New', warranty='6 months'),
        _sample('Honda', 'Honda CB500X', '$7,900', 18, 'Mombasa', 'Versatile adventure bike that commutes and tours.', 'honda cb500x adventure motorcycle product photo', year='2021', engine='471cc twin', mileage='18,000 km', transmission='6-speed', condition='Like New', warranty='1 year'),
        _sample('Yamaha', 'Yamaha MT-07', '$8,400', 22, 'Nairobi', 'Naked street bike with a torquey crossplane twin.', 'yamaha mt-07 naked motorcycle product photo', year='2020', engine='689cc twin', mileage='21,000 km', transmission='6-speed', condition='Used', warranty='3 months'),
        _sample('Suzuki', 'Suzuki V-Strom 650', '$8,100', 16, 'Nakuru', 'Comfortable adventure tourer for long distances.', 'suzuki v-strom 650 motorcycle product photo', year='2019', engine='645cc V-twin', mileage='29,000 km', transmission='6-speed', condition='Used', warranty='None'),
        _sample('Kawasaki', 'Kawasaki Ninja 650', '$8,700', 20, 'Eldoret', 'Sporty middleweight with a relaxed riding position.', 'kawasaki ninja 650 motorcycle product photo', year='2021', engine='649cc twin', mileage='14,000 km', transmission='6-speed', condition='Like New', warranty='6 months'),
        _sample('BMW', 'BMW R 1250 GS', '$21,800', 27, 'Nairobi', 'Ultimate touring adventure bike with a boxer engine.', 'bmw r1250 gs adventure motorcycle product photo', year='2022', engine='1254cc boxer', mileage='9,000 km', transmission='6-speed', condition='New', warranty='2 years'),
        _sample('Ducati', 'Ducati Monster 821', '$11,500', 21, 'Kisumu', 'Italian naked bike with serious performance.', 'ducati monster motorcycle product photo', year='2019', engine='821cc L-twin', mileage='23,000 km', transmission='6-speed', condition='Used', warranty='3 months'),
        _sample('Triumph', 'Triumph Bonneville T120', '$12,900', 19, 'Thika', 'Classic-styled roadster with modern reliability.', 'triumph bonneville t120 motorcycle product photo', year='2021', engine='1200cc twin', mileage='11,000 km', transmission='6-speed', condition='Like New', warranty='1 year', status='sold'),
    ], 'Motorcycles')
    return _render_category('vehicles.motorcycles.html', brands, sample_listings)


@marketplace_bp.route('/vehicles/parts')
def parts():
    brands = ['Rims', 'Engine', 'Batteries', 'ATF', 'Engine Oil', 'Brake Fluid', 'Tyres', 'Shocks']
    sample_listings = _prepare([
        _sample('Rims', '18" Alloy Wheel Set', '$620', 17, 'Nairobi', 'Set of four staggered alloy rims with good tyres.', 'alloy wheel rims product photo', type='Alloy wheels', compatibility='Universal 5x114', condition='Like New', warranty='3 months'),
        _sample('Engine', 'Reconditioned 2.0L Engine', '$1,850', 10, 'Mombasa', 'Fully reconditioned petrol engine, ready to fit.', 'reconditioned car engine product photo', type='Complete engine', compatibility='Toyota 2.0L', condition='Used', warranty='6 months'),
        _sample('Batteries', 'Maintenance-Free Car Battery', '$95', 22, 'Nairobi', 'Reliable 12V battery with a two-year warranty.', 'car battery product photo', type='12V battery', compatibility='Most sedans & SUVs', condition='New', warranty='2 years'),
        _sample('ATF', 'Automatic Transmission Fluid 4L', '$38', 12, 'Nakuru', 'Genuine ATF for smooth shifting and long gearbox life.', 'automatic transmission fluid product photo', type='ATF fluid', compatibility='Toyota WS', condition='New', warranty='None'),
        _sample('Engine Oil', 'Fully Synthetic 5W-30 4L', '$42', 26, 'Kisumu', 'Fully synthetic engine oil for petrol and diesel engines.', 'synthetic engine oil product photo', type='Engine oil', compatibility='Petrol & diesel', condition='New', warranty='None'),
        _sample('Brake Fluid', 'DOT 4 Brake Fluid 500ml', '$14', 9, 'Eldoret', 'High boiling point brake fluid for responsive stopping.', 'dot4 brake fluid product photo', type='Brake fluid', compatibility='DOT 4 systems', condition='New', warranty='None'),
        _sample('Tyres', '265/65 R17 All-Terrain Tyre', '$150', 19, 'Thika', 'Durable all-terrain tyre for 4x4 and pickup use.', 'all terrain tyre product photo', type='All-terrain tyre', compatibility='17 inch rims', condition='New', warranty='1 year'),
        _sample('Shocks', 'Front Shock Absorber Pair', '$210', 11, 'Meru', 'Gas-charged shock absorbers for a firmer ride.', 'car shock absorber product photo', type='Shock absorbers', compatibility='Toyota Hilux', condition='New', warranty='1 year', status='sold'),
    ], 'Parts & Accessories')
    return _render_category('vehicles.parts.html', brands, sample_listings)


@marketplace_bp.route('/vehicles/trucks')
def trucks():
    brands = ['Below 1 Tonne', '1 tonne', '2 tonnes', '3 tonnes', '5 tonne', '7 tonne', '10 tonne', '15 tonne', '30 tonne']
    sample_listings = _prepare([
        _sample('Below 1 Tonne', 'Suzuki Carry Mini Truck', '$6,800', 12, 'Nairobi', 'Compact kei truck ideal for light urban deliveries.', 'suzuki carry mini truck product photo', year='2019', mileage='96,000 km', tonnage='750 kg', transmission='Manual', condition='Used', warranty='None'),
        _sample('1 tonne', 'Isuzu NKR Light Truck', '$14,500', 15, 'Mombasa', 'One-tonne workhorse with a reliable diesel engine.', 'isuzu nkr light truck product photo', year='2020', mileage='110,000 km', tonnage='1 tonne', transmission='Manual', condition='Used', warranty='3 months'),
        _sample('2 tonnes', 'Mitsubishi Fuso Canter', '$24,900', 17, 'Nairobi', 'Two-tonne truck with a durable cargo body.', 'mitsubishi fuso canter truck product photo', year='2021', mileage='88,000 km', tonnage='2 tonnes', transmission='Manual', condition='Like New', warranty='6 months'),
        _sample('3 tonnes', 'Toyota Dyna 300', '$27,400', 14, 'Nakuru', 'Three-tonne cab-over truck for general haulage.', 'toyota dyna truck product photo', year='2020', mileage='102,000 km', tonnage='3 tonnes', transmission='Manual', condition='Used', warranty='3 months'),
        _sample('5 tonne', 'Isuzu FRR 5-Tonne', '$39,800', 13, 'Eldoret', 'Medium-duty truck with a high payload body.', 'isuzu frr truck product photo', year='2021', mileage='94,000 km', tonnage='5 tonnes', transmission='Manual', condition='Like New', warranty='6 months'),
        _sample('7 tonne', 'Hino 300 Series 7-Tonne', '$52,500', 11, 'Kisumu', 'Heavy-duty hauler with a comfortable day cab.', 'hino 300 series truck product photo', year='2020', mileage='140,000 km', tonnage='7 tonnes', transmission='Manual', condition='Used', warranty='3 months'),
        _sample('10 tonne', 'Mercedes-Benz Actros 10-Tonne', '$78,900', 10, 'Nairobi', 'Distribution truck with advanced safety systems.', 'mercedes benz actros truck product photo', year='2021', mileage='165,000 km', tonnage='10 tonnes', transmission='Automatic', condition='Like New', warranty='1 year'),
        _sample('15 tonne', 'Volvo FM 15-Tonne', '$92,300', 8, 'Thika', 'Long-distance rigid truck with a spacious cab.', 'volvo fm truck product photo', year='2019', mileage='210,000 km', tonnage='15 tonnes', transmission='Automatic', condition='Used', warranty='6 months'),
        _sample('30 tonne', 'Scania G460 Prime Mover', '$118,000', 7, 'Nairobi', 'Heavy-haul tractor unit for the toughest routes.', 'scania g460 truck product photo', year='2019', mileage='320,000 km', tonnage='30 tonnes', transmission='Automatic', condition='Used', warranty='6 months', status='sold'),
    ], 'Trucks')
    return _render_category('vehicles.trucks.html', brands, sample_listings)

# ================= HOME & GARDEN ===========================
@marketplace_bp.route('/home-garden')
def home_garden():
    try:
        home_garden_listings = Listing.query.filter_by(
            category='Home & Garden',
            is_active=True
        ).all()
    except:
        home_garden_listings = []
    return render_template('home_garden.html', listings=home_garden_listings)


# ============ HOME & GARDEN SUBCATEGORIES ROUTES ============

@marketplace_bp.route('/home-garden/furniture')
def furniture():
    brands = ['Chairs', 'Table sets', 'Wardrobes', 'Cupboards', 'Stool', 'Desk', 'Furniture Sets', 'Couch', 'Coffy Tables']
    sample_listings = _prepare([
        _sample('Chairs', 'Ergonomic Mesh Office Chair', '$120', 18, 'Nairobi', 'Comfortable mesh office chair with lumbar support.', 'ergonomic mesh office chair product photo', material='Mesh & steel', dimensions='65 x 65 x 110 cm', colour='Black', condition='New', warranty='1 year'),
        _sample('Table sets', '6-Seater Dining Table Set', '$420', 15, 'Mombasa', 'Solid wood dining set that seats six comfortably.', '6 seater wooden dining table set product photo', material='Solid wood', dimensions='180 x 90 x 76 cm', colour='Walnut', condition='Like New', warranty='6 months'),
        _sample('Wardrobes', '3-Door Fitted Wardrobe', '$350', 11, 'Kisumu', 'Spacious wardrobe with hanging rails and shelves.', 'three door wardrobe product photo', material='Engineered wood', dimensions='120 x 55 x 200 cm', colour='White', condition='Like New', warranty='6 months'),
        _sample('Cupboards', 'Steel Filing Cupboard', '$180', 7, 'Nakuru', 'Lockable steel cupboard for office or home storage.', 'steel filing cupboard product photo', material='Powder-coated steel', dimensions='90 x 45 x 180 cm', colour='Grey', condition='Used', warranty='None'),
        _sample('Stool', 'Wooden Bar Stool', '$45', 12, 'Thika', 'Sleek bar stool with a padded seat.', 'wooden bar stool product photo', material='Rubberwood', dimensions='40 x 40 x 75 cm', colour='Natural', condition='New', warranty='6 months'),
        _sample('Desk', 'Compact Study Desk', '$95', 20, 'Nairobi', 'Space-saving desk with a drawer for study essentials.', 'compact study desk product photo', material='MDF board', dimensions='100 x 50 x 75 cm', colour='Oak', condition='New', warranty='1 year'),
        _sample('Furniture Sets', 'Living Room Furniture Set', '$690', 9, 'Eldoret', 'Complete sofa and table set for a modern living room.', 'living room furniture set product photo', material='Fabric & wood', dimensions='Sofa 3+2 seater', colour='Beige', condition='Like New', warranty='6 months'),
        _sample('Couch', '3-Seater Fabric Sofa', '$380', 22, 'Nairobi', 'Plush three-seater sofa with removable covers.', 'fabric three seater sofa product photo', material='Linen fabric', dimensions='210 x 90 x 85 cm', colour='Charcoal', condition='Like New', warranty='6 months'),
        _sample('Coffy Tables', 'Tempered Glass Coffee Table', '$130', 14, 'Meru', 'Tempered glass coffee table with wooden legs.', 'glass coffee table product photo', material='Tempered glass', dimensions='110 x 60 x 45 cm', colour='Clear', condition='New', warranty='6 months', status='sold'),
    ], 'Furniture')
    return _render_category('home.furniture.html', brands, sample_listings)


@marketplace_bp.route('/home-garden/home-decor')
def home_decor():
    brands = ['Wall Art', 'Kirkland', 'HomeGoods', 'Target', 'Walmart', 'Etsy']
    sample_listings = _prepare([
        _sample('Wall Art', 'Framed Abstract Wall Art', '$60', 21, 'Nairobi', 'Modern abstract print in a slim wooden frame.', 'framed abstract wall art product photo', type='Framed print', material='Canvas & wood', colour='Multicolour', style='Modern', condition='New'),
        _sample('Kirkland', 'Kirkland Scented Candle Set', '$35', 13, 'Mombasa', 'Set of three long-burning scented candles.', 'scented candle set product photo', type='Candle set', material='Soy wax', colour='Ivory', style='Minimalist', condition='New'),
        _sample('HomeGoods', 'Ceramic Vase Trio', '$42', 17, 'Kisumu', 'Set of three glazed ceramic vases.', 'ceramic vase set product photo', type='Vase set', material='Ceramic', colour='Sage', style='Contemporary', condition='Like New'),
        _sample('Target', 'Woven Storage Basket', '$28', 10, 'Nakuru', 'Handwoven basket that doubles as decor.', 'woven storage basket product photo', type='Decorative basket', material='Seagrass', colour='Natural', style='Boho', condition='New'),
        _sample('Walmart', 'Round Wall Mirror', '$55', 15, 'Thika', 'Round accent mirror with a rustic frame.', 'round wall mirror product photo', type='Wall mirror', material='Glass & metal', colour='Gold', style='Rustic', condition='New'),
        _sample('Etsy', 'Handmade Macrame Wall Hanging', '$38', 19, 'Nairobi', 'Hand-knotted macrame to warm up any wall.', 'macrame wall hanging product photo', type='Wall hanging', material='Cotton rope', colour='Cream', style='Bohemian', condition='Like New', status='sold'),
    ], 'Home Decor')
    return _render_category('home.homedeco.html', brands, sample_listings)


@marketplace_bp.route('/home-garden/kitchen-dining')
def kitchen_dining():
    brands = ['KitchenAid', 'Cuisinart', 'Instant Pot', 'Pyrex', 'Corningware', 'Hamilton Beach']
    sample_listings = _prepare([
        _sample('KitchenAid', 'KitchenAid Artisan Stand Mixer', '$320', 24, 'Nairobi', 'Powerful stand mixer for baking and dough.', 'kitchenaid stand mixer product photo', type='Stand mixer', material='Die-cast metal', capacity='4.8 L', condition='Like New', warranty='6 months'),
        _sample('Cuisinart', 'Cuisinart Food Processor', '$180', 16, 'Mombasa', 'Multi-purpose food processor with stainless blades.', 'cuisinart food processor product photo', type='Food processor', material='Stainless steel', capacity='2 L', condition='New', warranty='1 year'),
        _sample('Instant Pot', 'Instant Pot Duo 7-in-1', '$140', 29, 'Kisumu', 'Pressure cooker that also slow cooks and steams.', 'instant pot electric pressure cooker product photo', type='Pressure cooker', material='Stainless steel', capacity='5.7 L', condition='New', warranty='1 year'),
        _sample('Pyrex', 'Pyrex Glass Bakeware Set', '$55', 12, 'Nakuru', 'Oven-safe glass dishes in assorted sizes.', 'pyrex glass bakeware set product photo', type='Bakeware set', material='Borosilicate glass', capacity='8-piece set', condition='New', warranty='6 months'),
        _sample('Corningware', 'Corningware Casserole Dish', '$48', 9, 'Thika', 'Classic casserole dish for oven-to-table serving.', 'corningware casserole dish product photo', type='Casserole dish', material='Stoneware', capacity='3 L', condition='Like New', warranty='None'),
        _sample('Hamilton Beach', 'Hamilton Beach Countertop Blender', '$75', 18, 'Eldoret', '700W blender for smoothies and soups.', 'hamilton beach blender product photo', type='Countertop blender', material='Glass & plastic', capacity='1.5 L', condition='New', warranty='1 year', status='sold'),
    ], 'Kitchen & Dining')
    return _render_category('home.kitchen.html', brands, sample_listings)


@marketplace_bp.route('/home-garden/bedding-bath')
def bedding_bath():
    brands = ['Cannon', 'Fieldcrest', 'Martha Stewart', 'Laura Ashley', 'Tommy Hilfiger', 'Ralph Lauren']
    sample_listings = _prepare([
        _sample('Cannon', 'Cannon Cotton Towel Set', '$35', 20, 'Nairobi', 'Soft absorbent towel set for everyday use.', 'cotton bath towel set product photo', size='Bath & hand set', material='100% Cotton', colour='White', pieces='6-piece set', condition='New'),
        _sample('Fieldcrest', 'Fieldcrest Duvet Cover Set', '$110', 14, 'Mombasa', 'Plush duvet cover set with pillowcases.', 'duvet cover set product photo', size='Queen', material='Microfibre', colour='Grey', pieces='4-piece set', condition='Like New'),
        _sample('Martha Stewart', 'Martha Stewart Reversible Comforter', '$95', 17, 'Kisumu', 'Reversible comforter with a soft brushed finish.', 'reversible comforter bedding product photo', size='King', material='Cotton blend', colour='Blush', pieces='3-piece set', condition='New'),
        _sample('Laura Ashley', 'Laura Ashley Floral Sheet Set', '$65', 12, 'Nakuru', 'Floral cotton sheets with a crisp finish.', 'floral cotton sheet set product photo', size='Double', material='100% Cotton', colour='Floral Blue', pieces='4-piece set', condition='Like New'),
        _sample('Tommy Hilfiger', 'Tommy Hilfiger Cotton Bath Robe', '$55', 9, 'Thika', 'Cosy cotton bath robe with a classic stripe.', 'cotton bath robe product photo', size='Large', material='Cotton terry', colour='Navy', pieces='1 robe', condition='New'),
        _sample('Ralph Lauren', 'Ralph Lauren Bath Towels', '$48', 15, 'Nairobi', 'Premium cotton towels with a soft ribbed texture.', 'premium cotton bath towels product photo', size='Bath towel', material='Egyptian cotton', colour='Navy', pieces='4-piece set', condition='Like New', status='sold'),
    ], 'Bedding & Bath')
    return _render_category('home.bedding&bath.html', brands, sample_listings)


@marketplace_bp.route('/home-garden/lighting')
def lighting():
    brands = ['Philips', 'GE', 'IKEA', 'Westinghouse', 'Lithonia', 'Kichler']
    sample_listings = _prepare([
        _sample('Philips', 'Philips LED Bulb Pack', '$22', 25, 'Nairobi', 'Energy-saving LED bulbs with warm white light.', 'philips led light bulbs product photo', type='LED bulbs', wattage='9W', colour='Warm White', condition='New', warranty='1 year'),
        _sample('GE', 'GE Vintage Edison Bulb', '$15', 13, 'Mombasa', 'Retro filament bulb with a warm glow.', 'ge vintage edison bulb product photo', type='Filament bulb', wattage='60W', colour='Amber', condition='New', warranty='6 months'),
        _sample('IKEA', 'IKEA Adjustable Floor Lamp', '$45', 19, 'Kisumu', 'Minimal floor lamp with an adjustable shade.', 'ikea floor lamp product photo', type='Floor lamp', wattage='13W', colour='White', condition='Like New', warranty='6 months'),
        _sample('Westinghouse', 'Westinghouse Ceiling Light', '$60', 11, 'Nakuru', 'Flush-mount ceiling light for any room.', 'westinghouse ceiling light product photo', type='Ceiling light', wattage='18W', colour='Brushed Nickel', condition='New', warranty='1 year'),
        _sample('Lithonia', 'Lithonia LED Panel Light', '$70', 8, 'Thika', 'Slim LED panel light with even illumination.', 'led panel ceiling light product photo', type='LED panel', wattage='36W', colour='Cool White', condition='New', warranty='1 year'),
        _sample('Kichler', 'Kichler Outdoor Wall Sconce', '$85', 10, 'Nairobi', 'Weatherproof sconce for patios and entries.', 'outdoor wall sconce light product photo', type='Wall sconce', wattage='12W', colour='Black', condition='Like New', warranty='6 months', status='sold'),
    ], 'Lighting')
    return _render_category('home.lighting.html', brands, sample_listings)


@marketplace_bp.route('/home-garden/storage')
def storage():
    brands = ['Sterilite', 'ClosetMaid', 'Rubbermaid', 'IKEA', 'Simplehuman', 'Honey-Can-Do']
    sample_listings = _prepare([
        _sample('Sterilite', 'Sterilite Storage Bins', '$40', 27, 'Nairobi', 'Stackable plastic bins with latching lids.', 'sterilite plastic storage bins product photo', type='Storage bins', material='Plastic', capacity='50 L', condition='New', warranty='6 months'),
        _sample('ClosetMaid', 'ClosetMaid Stackable Shelves', '$65', 15, 'Mombasa', 'Modular shelving that stacks to fit your space.', 'closetmaid stackable shelves product photo', type='Shelving unit', material='Laminate', capacity='9 cubes', condition='Like New', warranty='6 months'),
        _sample('Rubbermaid', 'Rubbermaid Storage Tote', '$30', 18, 'Kisumu', 'Rugged tote for garage and closet storage.', 'rubbermaid storage tote product photo', type='Storage tote', material='Heavy-duty plastic', capacity='75 L', condition='New', warranty='1 year'),
        _sample('IKEA', 'IKEA Shoe Cabinet', '$90', 21, 'Nakuru', 'Slim cabinet that holds up to twelve pairs.', 'ikea shoe cabinet product photo', type='Shoe cabinet', material='Particle board', capacity='12 pairs', condition='Like New', warranty='6 months'),
        _sample('Simplehuman', 'Simplehuman Step Bin', '$110', 13, 'Thika', 'Fingerprint-proof step bin with a soft-close lid.', 'simplehuman step trash can product photo', type='Step bin', material='Stainless steel', capacity='45 L', condition='Like New', warranty='3 months'),
        _sample('Honey-Can-Do', 'Honey-Can-Do Organizer Rack', '$45', 9, 'Nairobi', 'Three-tier rack for the kitchen or utility room.', 'three tier storage rack product photo', type='Organizer rack', material='Chrome steel', capacity='3 tiers', condition='New', warranty='6 months', status='sold'),
    ], 'Storage & Organization')
    return _render_category('home.storage.html', brands, sample_listings)


@marketplace_bp.route('/home-garden/garden')
def garden():
    brands = ['Weber', 'Toro', 'Scotts', 'Miracle-Gro', 'Husqvarna', 'Suncast']
    sample_listings = _prepare([
        _sample('Weber', 'Weber Charcoal Kettle Grill', '$220', 23, 'Nairobi', 'Classic kettle grill for authentic barbecue flavour.', 'weber charcoal kettle grill product photo', type='Charcoal grill', material='Porcelain-enamel steel', size='57 cm', condition='Like New', warranty='1 year'),
        _sample('Toro', 'Toro Petrol Lawn Mower', '$310', 14, 'Mombasa', 'Petrol push mower with a mulching deck.', 'toro petrol lawn mower product photo', type='Push mower', material='Steel', size='21 inch deck', condition='Like New', warranty='6 months'),
        _sample('Scotts', 'Scotts Lawn Fertiliser', '$35', 12, 'Kisumu', 'Granular fertiliser for a greener lawn.', 'scotts lawn fertiliser product photo', type='Lawn fertiliser', material='Granular', size='15 kg bag', condition='New', warranty='None'),
        _sample('Miracle-Gro', 'Miracle-Gro Potting Mix', '$28', 17, 'Nakuru', 'Nutrient-rich potting mix for container plants.', 'miracle gro potting mix product photo', type='Potting mix', material='Peat & perlite', size='40 L bag', condition='New', warranty='None'),
        _sample('Husqvarna', 'Husqvarna Petrol Chainsaw', '$260', 11, 'Thika', 'Reliable petrol chainsaw for garden clearing.', 'husqvarna petrol chainsaw product photo', type='Chainsaw', material='Steel & plastic', size='18 inch bar', condition='Used', warranty='None'),
        _sample('Suncast', 'Suncast Garden Hose Reel', '$80', 8, 'Nairobi', 'Wall-mounted reel with a 30m hose.', 'garden hose reel product photo', type='Hose reel', material='Resin', size='30 m hose', condition='New', warranty='1 year', status='sold'),
    ], 'Garden & Outdoor')
    return _render_category('home.garden.html', brands, sample_listings)


@marketplace_bp.route('/home-garden/smart-home')
def smart_home():
    brands = ['Amazon', 'Google', 'Philips Hue', 'Ring', 'Nest', 'Samsung SmartThings']
    sample_listings = _prepare([
        _sample('Amazon', 'Amazon Echo Dot (5th Gen)', '$60', 32, 'Nairobi', 'Compact smart speaker with a built-in voice assistant.', 'amazon echo dot smart speaker product photo', type='Smart speaker', connectivity='Wi-Fi & Bluetooth', compatibility='Alexa', condition='New', warranty='1 year'),
        _sample('Google', 'Google Nest Mini', '$50', 24, 'Mombasa', 'Wall-friendly smart speaker with rich sound.', 'google nest mini smart speaker product photo', type='Smart speaker', connectivity='Wi-Fi', compatibility='Google Assistant', condition='Like New', warranty='6 months'),
        _sample('Philips Hue', 'Philips Hue Smart Bulb Kit', '$130', 21, 'Kisumu', 'Colour-changing smart bulbs with a bridge.', 'philips hue smart bulb starter kit product photo', type='Smart lighting', connectivity='Zigbee', compatibility='Alexa & Google', condition='New', warranty='1 year'),
        _sample('Ring', 'Ring Video Doorbell', '$150', 18, 'Nakuru', 'See and answer your door from anywhere.', 'ring video doorbell product photo', type='Video doorbell', connectivity='Wi-Fi', compatibility='Alexa', condition='Like New', warranty='6 months'),
        _sample('Nest', 'Google Nest Learning Thermostat', '$180', 14, 'Thika', 'Learning thermostat that saves on energy bills.', 'google nest thermostat product photo', type='Smart thermostat', connectivity='Wi-Fi', compatibility='Google Home', condition='New', warranty='1 year'),
        _sample('Samsung SmartThings', 'Samsung SmartThings Hub', '$95', 10, 'Nairobi', 'Central hub that connects your smart devices.', 'smart home hub device product photo', type='Smart hub', connectivity='Zigbee & Z-Wave', compatibility='SmartThings', condition='Like New', warranty='6 months', status='sold'),
    ], 'Smart Home')
    return _render_category('home.smarthome.html', brands, sample_listings)


@marketplace_bp.route('/home-garden/baby-kids')
def baby_kids():
    brands = ['Graco', 'Fisher-Price', 'Chicco', 'Evenflo', 'Summer Infant', 'Safety 1st']
    sample_listings = _prepare([
        _sample('Graco', 'Graco Baby Stroller', '$220', 27, 'Nairobi', 'Lightweight stroller with a compact fold.', 'graco baby stroller product photo', age='0-3 years', material='Aluminium & fabric', colour='Grey', safety='5-point harness', condition='Like New', warranty='6 months'),
        _sample('Fisher-Price', 'Fisher-Price Baby Swing', '$130', 20, 'Mombasa', 'Soothing swing with multiple speed settings.', 'fisher price baby swing product photo', age='0-12 months', material='Plastic & fabric', colour='Blue', safety='Secure harness', condition='Like New', warranty='6 months'),
        _sample('Chicco', 'Chicco Convertible Car Seat', '$190', 16, 'Kisumu', 'Rear and forward-facing car seat with side impact protection.', 'chicco convertible car seat product photo', age='0-7 years', material='Moulded plastic', colour='Black', safety='Side-impact protection', condition='New', warranty='1 year'),
        _sample('Evenflo', 'Evenflo High Chair', '$95', 12, 'Nakuru', 'Adjustable high chair that grows with your child.', 'evenflo baby high chair product photo', age='6 months-3 years', material='Plastic', colour='Grey', safety='3-point harness', condition='New', warranty='6 months'),
        _sample('Summer Infant', 'Summer Infant Baby Monitor', '$110', 14, 'Thika', 'Video baby monitor with night vision.', 'baby video monitor product photo', age='All ages', material='Plastic', colour='White', safety='Secure wireless', condition='New', warranty='1 year'),
        _sample('Safety 1st', 'Safety 1st Baby Gate', '$55', 11, 'Nairobi', 'Pressure-mounted gate to keep little ones safe.', 'baby safety gate product photo', age='6-24 months', material='Metal', colour='White', safety='Pressure mount', condition='Like New', warranty='6 months', status='sold'),
    ], 'Baby & Kids')
    return _render_category('home.baby&kids.html', brands, sample_listings)


@marketplace_bp.route('/home-garden/pet-supplies')
def pet_supplies():
    brands = ['Purina', 'Pedigree', "Hill's", 'Royal Canin', 'KONG', 'PetSafe']
    sample_listings = _prepare([
        _sample('Purina', 'Purina Dog Food 15kg', '$55', 30, 'Nairobi', 'Complete dry food for adult dogs.', 'purina dry dog food bag product photo', type='Dry food', pet='Dog', material='Chicken & rice', condition='New', warranty='None'),
        _sample('Pedigree', 'Pedigree Puppy Food', '$38', 22, 'Mombasa', 'Balanced nutrition for growing puppies.', 'pedigree puppy food product photo', type='Dry food', pet='Dog', material='Beef flavour', condition='New', warranty='None'),
        _sample("Hill's", "Hill's Science Diet Cat Food", '$48', 18, 'Kisumu', 'Vet-recommended formula for adult cats.', 'hills science diet cat food product photo', type='Dry food', pet='Cat', material='Chicken', condition='New', warranty='None'),
        _sample('Royal Canin', 'Royal Canin Kitten Food', '$42', 16, 'Nakuru', 'Tailored nutrition for growing kittens.', 'royal canin kitten food product photo', type='Dry food', pet='Cat', material='Chicken', condition='Like New', warranty='None'),
        _sample('KONG', 'KONG Classic Dog Toy', '$18', 24, 'Thika', 'Durable rubber toy that holds treats.', 'kong classic dog toy product photo', type='Chew toy', pet='Dog', material='Natural rubber', condition='New', warranty='6 months'),
        _sample('PetSafe', 'PetSafe Automatic Pet Feeder', '$85', 13, 'Nairobi', 'Scheduled feeder for consistent mealtimes.', 'automatic pet feeder product photo', type='Pet feeder', pet='Dog / Cat', material='Plastic', condition='New', warranty='1 year', status='sold'),
    ], 'Pet Supplies')
    return _render_category('home.petsupply.html', brands, sample_listings)


@marketplace_bp.route('/home-garden/cleaning')
def cleaning():
    brands = ['Hoover', 'Bissell', 'Shark', 'Dyson', 'Swiffer', 'Clorox']
    sample_listings = _prepare([
        _sample('Hoover', 'Hoover Upright Vacuum', '$180', 19, 'Nairobi', 'Powerful upright vacuum with HEPA filtration.', 'hoover upright vacuum cleaner product photo', type='Upright vacuum', volume='2.5 L', surface='Carpet & hard floor', condition='Like New', warranty='6 months'),
        _sample('Bissell', 'Bissell Carpet Cleaner', '$230', 15, 'Mombasa', 'Deep cleaner that lifts stains from carpets.', 'bissell carpet cleaner machine product photo', type='Carpet cleaner', volume='3.5 L', surface='Carpet & upholstery', condition='Like New', warranty='1 year'),
        _sample('Shark', 'Shark Cordless Stick Vacuum', '$260', 17, 'Kisumu', 'Lightweight cordless stick vacuum.', 'shark cordless stick vacuum product photo', type='Cordless vacuum', volume='0.8 L', surface='Hard floor & rug', condition='New', warranty='1 year'),
        _sample('Dyson', 'Dyson V12 Detect Slim', '$420', 26, 'Nakuru', 'Cordless vacuum with laser dust detection.', 'dyson cordless vacuum cleaner product photo', type='Cordless vacuum', volume='0.35 L', surface='All floors', condition='Like New', warranty='1 year'),
        _sample('Swiffer', 'Swiffer WetJet Starter Kit', '$32', 21, 'Thika', 'Spray mop kit with cleaning solution.', 'swiffer wetjet mop kit product photo', type='Spray mop', volume='500 ml', surface='Sealed hard floors', condition='New', warranty='None'),
        _sample('Clorox', 'Clorox Disinfecting Spray', '$14', 28, 'Nairobi', 'Multi-surface disinfecting spray.', 'clorox disinfecting spray bottle product photo', type='Disinfectant spray', volume='750 ml', surface='Multi-surface', condition='New', warranty='None', status='sold'),
    ], 'Cleaning & Home Care')
    return _render_category('home.cleaning.html', brands, sample_listings)


# ============ BOOKS & MEDIA ROUTES ============
@marketplace_bp.route('/books-media')
def books_media():
    brands = [
        'Textbooks', 'Novels & Fiction', 'Movies & Films', 'TV Series',
        'Music & Vinyl', 'Audiobooks', 'Comic Books', 'Academic Journals',
        'Documentaries', 'Sheet Music', 'Rare & Collectible'
    ]
    sample_listings = _prepare([
        _sample('Textbooks', 'Introduction to Economics', '$30', 12, 'Nairobi', 'One sentence description.', 'short english prompt', type='Textbook', format='Paperback', language='English', condition='Like New', warranty='None'),
        _sample('Novels & Fiction', 'Things Fall Apart', '$8', 24, 'Mombasa', 'Classic African novel in great reading condition.', 'classic african novel book product photo', type='Novel', format='Hardcover', language='English', condition='Used', warranty='None'),
        _sample('Movies & Films', 'The Godfather (DVD)', '$12', 18, 'Nairobi', 'Remastered crime classic on a single disc.', 'the godfather dvd movie product photo', type='Movie', format='DVD', language='English', condition='Like New', warranty='None'),
        _sample('TV Series', 'Breaking Bad: The Complete Series', '$45', 20, 'Kisumu', 'All five seasons in one collector box set.', 'breaking bad complete series box set product photo', type='TV Series', format='Blu-ray', language='English', condition='Like New', warranty='None'),
        _sample('Music & Vinyl', 'Fleetwood Mac - Rumours (Vinyl)', '$28', 15, 'Nakuru', 'Original pressing with warm analog sound.', 'fleetwood mac rumours vinyl record product photo', type='Vinyl LP', format='12-inch Vinyl', language='English', condition='Like New', warranty='None'),
        _sample('Audiobooks', 'Atomic Habits (Audiobook)', '$15', 22, 'Thika', 'Unabridged narration on CD, barely used.', 'atomic habits audiobook cd product photo', type='Audiobook', format='CD', language='English', condition='New', warranty='None'),
        _sample('Comic Books', 'The Amazing Spider-Man #300', '$60', 30, 'Nairobi', 'Key issue featuring the first full Venom.', 'amazing spider-man comic book product photo', type='Comic Book', format='Single Issue', language='English', condition='Used', warranty='None', status='sold'),
        _sample('Academic Journals', 'Journal of Applied Physics 2024', '$40', 9, 'Eldoret', 'Bound volume of the latest research articles.', 'academic journal physics bound volume product photo', type='Academic Journal', format='Paperback', language='English', condition='New', warranty='None'),
        _sample('Documentaries', 'Planet Earth II (Documentary)', '$22', 17, 'Machakos', 'Award-winning nature series narrated by Attenborough.', 'planet earth documentary blu-ray product photo', type='Documentary', format='Blu-ray', language='English', condition='Like New', warranty='None'),
        _sample('Sheet Music', 'Beethoven Complete Piano Sonatas', '$35', 11, 'Meru', 'Urtext edition for serious pianists.', 'beethoven sheet music piano book product photo', type='Sheet Music', format='Paperback', language='English', condition='Used', warranty='None'),
        _sample('Rare & Collectible', 'Harry Potter First Edition', '$1,200', 42, 'Nairobi', 'Rare first printing in excellent condition.', 'rare first edition harry potter book product photo', type='Collectible Book', format='Hardcover', language='English', condition='Like New', warranty='None', status='sold'),
    ], 'Books & Media')
    return _render_category('books_media.html', brands, sample_listings)

@marketplace_bp.route('/sports')
def sports():
    try:
        sports_listings = Listing.query.filter_by(
            category='Sports',
            is_active=True
        ).all()
    except:
        sports_listings = []
    return render_template('sports.html', listings=sports_listings)


@marketplace_bp.route('/beauty')
def beauty():
    try:
        beauty_listings = Listing.query.filter_by(
            category='Beauty',
            is_active=True
        ).all()
    except:
        beauty_listings = []
    return render_template('beauty.html', listings=beauty_listings)


# ============ SERVICES HUB ROUTES ============
@services_bp.route('/')
def services_home():
    try:
        services = Service.query.filter_by(is_active=True).limit(20).all()
    except:
        services = []
    return render_template('services.html', services=services)


@services_bp.route('/create', methods=['GET', 'POST'])
def create_service():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        subcategory = request.form.get('subcategory', '')
        service_type = request.form.get('service_type')
        hourly_rate = request.form.get('hourly_rate')
        fixed_price = request.form.get('fixed_price')
        location = request.form.get('location')
        years_experience = request.form.get('years_experience', 0)
        certification = request.form.get('certification', '')
        availability = request.form.get('availability', '')

        hourly_rate_val = float(hourly_rate) if hourly_rate else None
        fixed_price_val = float(fixed_price) if fixed_price else None
        years_exp_val = int(years_experience) if years_experience else 0

        new_service = Service(
            title=title,
            description=description,
            category=category,
            subcategory=subcategory,
            service_type=service_type,
            hourly_rate=hourly_rate_val,
            fixed_price=fixed_price_val,
            location=location,
            years_experience=years_exp_val,
            certification=certification,
            availability=availability,
            provider_id=1
        )

        db.session.add(new_service)
        db.session.commit()

        flash('Service created successfully!')
        return redirect(url_for('services.services_home'))

    return render_template('create_service.html')


# ============ FITNESS & TRAINING ROUTES ============
@services_bp.route('/fitness')
def fitness():
    try:
        fitness_services = Service.query.filter_by(
            category='Fitness',
            is_active=True
        ).order_by(Service.rating.desc()).all()
    except:
        fitness_services = []
    return render_template('fitness.html', services=fitness_services)


@marketplace_bp.route('/fitness')
def fitness():
    return render_template('fitness.html')
# ============ FITNESS SUBCATEGORIES ROUTES ============

@marketplace_bp.route('/fitness/personal')
def fitness_personal():
    selected_brand = request.args.get('brand', '')
    brands = ['Strength Training', 'Weight Loss', 'Bodybuilding', 'Rehab', 'General Fitness']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fitness',
            subcategory='Personal Training',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fitness.personal.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/fitness/martial-arts')
def fitness_martialarts():
    selected_brand = request.args.get('brand', '')
    brands = ['Boxing', 'Karate', 'Taekwondo', 'Judo', 'Muay Thai', 'Kung Fu', 'Aikido']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fitness',
            subcategory='Martial Arts',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fitness.martialarts.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/fitness/group')
def fitness_group():
    selected_brand = request.args.get('brand', '')
    brands = ['Dance Fitness', 'Bootcamp', 'Spin', 'Zumba', 'CrossFit', 'Aerobics']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fitness',
            subcategory='Group Classes',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fitness.group.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/fitness/nutrition')
def fitness_nutrition():
    selected_brand = request.args.get('brand', '')
    brands = ['Meal Prep', 'Diet Planning', 'Supplements', 'Weight Management', 'Sports Nutrition']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fitness',
            subcategory='Nutrition',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fitness.nutrition.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/fitness/running')
def fitness_running():
    selected_brand = request.args.get('brand', '')
    brands = ['Mountain Climbing', 'Jogging', 'Marathon', 'Half Marathon', 'Trail Running', 'Sprinting']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fitness',
            subcategory='Running',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fitness.running.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/fitness/massage')
def fitness_massage():
    selected_brand = request.args.get('brand', '')
    brands = ['Swedish', 'Deep Tissue', 'Sports', 'Thai', 'Hot Stone', 'Reflexology']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fitness',
            subcategory='Massage Therapy',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fitness.massage.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/fitness/online')
def fitness_online():
    selected_brand = request.args.get('brand', '')
    brands = ['Live Classes', 'On-Demand', 'App-Based', 'Zoom Training', 'Recorded Workouts']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fitness',
            subcategory='Online Fitness',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fitness.online.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


# ============ AUTO REPAIR ROUTES ============
@services_bp.route('/auto-repair')
def auto_repair():
    selected_brand = request.args.get('brand', '')

    brands = [
        'Engine & Performance',
        'Transmission',
        'Brake System',
        'Suspension & Steering',
        'Auto Electrical',
        'AC & Heating',
        'Exhaust & Emissions',
        'Cooling System',
        'Fuel System',
        'Tyres & Wheels',
        'Body & Panel',
        'Diagnostics',
        'Servicing',
        'Mobile Mechanic',
        'Performance Tuning'
    ]

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Auto Repair',   # adjust if your category scheme is different
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('auto_repair.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)
# ============ TUTORING & EDUCATION ROUTES ============
@services_bp.route('/tutoring')
def tutoring():
    selected_brand = request.args.get('brand', '')

    # All the tutoring categories from the original scrolling cards
    brands = [
        'Mathematics',
        'English & Literature',
        'Science',
        'Coding & Programming',
        'Languages',
        'Test Preparation',
        'History & Social Studies',
        'Business & Economics',
        'Music & Arts',
        'Special Education',
        'University & College',
        'Homework Help',
        'Adult Education',
        'STEM',
        'ESL',
        'Study Skills'
    ]

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Tutoring',   # or 'Education', adjust as needed
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('tutoring.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


# ============ BEAUTY & WELLNESS ROUTES ============
@services_bp.route('/beauty-wellness')
def beauty_wellness():
    try:
        beauty_services = Service.query.filter_by(
            category='Beauty & Wellness',
            is_active=True
        ).order_by(Service.rating.desc()).all()
    except:
        beauty_services = []
    return render_template('beauty_wellness.html', services=beauty_services)

# ============ BEAUTY & WELLNESS SUBCATEGORIES ROUTES ============

@services_bp.route('/beauty-wellness/hair')
def beauty_hair():
    selected_brand = request.args.get('brand', '')
    brands = ['Haircut', 'Coloring', 'Styling', 'Extensions', 'Braids', 'Weave', 'Perm', 'Relaxer']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Beauty & Wellness',
            subcategory='Hair Services',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('beauty.hair.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@services_bp.route('/beauty-wellness/skin')
def beauty_skin():
    selected_brand = request.args.get('brand', '')
    brands = ['Facial', 'Acne Treatment', 'Microdermabrasion', 'Chemical Peel', 'LED Therapy', 'Waxing', 'Laser Hair Removal', 'Threading']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Beauty & Wellness',
            subcategory='Skin Care & Facials',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('beauty.skin.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@services_bp.route('/beauty-wellness/massage')
def beauty_massage():
    selected_brand = request.args.get('brand', '')
    brands = ['Swedish', 'Deep Tissue', 'Sports', 'Hot Stone', 'Aromatherapy', 'Prenatal']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Beauty & Wellness',
            subcategory='Massage Therapy',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('beauty.massage.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@services_bp.route('/beauty-wellness/makeup')
def beauty_makeup():
    selected_brand = request.args.get('brand', '')
    brands = ['Bridal Makeup', 'Everyday Makeup', 'Eyelash Extensions', 'Lash Lift', 'Brow Lamination', 'Microblading']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Beauty & Wellness',
            subcategory='Makeup & Lashes',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('beauty.makeup.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@services_bp.route('/beauty-wellness/body-treatment')
def beauty_bodytreatment():
    selected_brand = request.args.get('brand', '')
    brands = ['Body Scrub', 'Body Wrap', 'Detox', 'Cellulite Treatment', 'Firming', 'Hydration']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Beauty & Wellness',
            subcategory='Body Treatments',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('beauty.bodytreatment.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@services_bp.route('/beauty-wellness/men')
def beauty_men():
    selected_brand = request.args.get('brand', '')
    brands = ['Beard Trim', 'Haircut', 'Facial', 'Waxing', 'Buff & Shine']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Beauty & Wellness',
            subcategory='Mens Grooming',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('beauty.men.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)

# ============ HOME SERVICES SUBCATEGORIES ROUTES ============

@services_bp.route('/home-services/cleaning')
def home_cleaning():
    selected_brand = request.args.get('brand', '')
    brands = []
    listings = []
    try:
        query = Service.query.filter_by(
            category='Home Services',
            subcategory='Cleaning',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('homeservice.cleaning.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@services_bp.route('/home-services/plumbing')
def home_plumbing():
    selected_brand = request.args.get('brand', '')
    brands = []
    listings = []
    try:
        query = Service.query.filter_by(
            category='Home Services',
            subcategory='Plumbing',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('homeservice.plumbing.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@services_bp.route('/home-services/electrical')
def home_electrical():
    selected_brand = request.args.get('brand', '')
    brands = []
    listings = []
    try:
        query = Service.query.filter_by(
            category='Home Services',
            subcategory='Electrical',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('homeservice.electrical.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@services_bp.route('/home-services/painting')
def home_painting():
    selected_brand = request.args.get('brand', '')
    brands = []
    listings = []
    try:
        query = Service.query.filter_by(
            category='Home Services',
            subcategory='Painting',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('homeservice.painting.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@services_bp.route('/home-services/carpentry')
def home_carpentry():
    selected_brand = request.args.get('brand', '')
    brands = []
    listings = []
    try:
        query = Service.query.filter_by(
            category='Home Services',
            subcategory='Carpentry',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('homeservice.carpentry.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@services_bp.route('/home-services/landscaping')
def home_landscaping():
    selected_brand = request.args.get('brand', '')
    brands = []
    listings = []
    try:
        query = Service.query.filter_by(
            category='Home Services',
            subcategory='Landscaping',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('homeservice.landscaping.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@services_bp.route('/home-services/hvac')
def home_hvac():
    selected_brand = request.args.get('brand', '')
    brands = []
    listings = []
    try:
        query = Service.query.filter_by(
            category='Home Services',
            subcategory='HVAC',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('homeservice.hvac.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@services_bp.route('/home-services/appliance-repair')
def home_appliancerepair():
    selected_brand = request.args.get('brand', '')
    brands = []
    listings = []
    try:
        query = Service.query.filter_by(
            category='Home Services',
            subcategory='Appliance Repair',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('homeservice.appliancerepair.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@services_bp.route('/home-services/moving')
def home_movingservices():
    selected_brand = request.args.get('brand', '')
    brands = []
    listings = []
    try:
        query = Service.query.filter_by(
            category='Home Services',
            subcategory='Moving Services',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('homeservice.movingservices.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@services_bp.route('/home-services/handyman')
def home_handyman():
    selected_brand = request.args.get('brand', '')
    brands = []
    listings = []
    try:
        query = Service.query.filter_by(
            category='Home Services',
            subcategory='Handyman',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('homeservice.handyman.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


# ============ SERVICE BOOKING ROUTES ============
@services_bp.route('/book/<int:service_id>', methods=['GET', 'POST'])
def book_service(service_id):
    """Book a service appointment"""
    try:
        service = Service.query.get_or_404(service_id)

        if request.method == 'POST':
            booking_date = request.form.get('booking_date')
            booking_time = request.form.get('booking_time')
            duration = request.form.get('duration', 1)
            notes = request.form.get('notes', '')

            new_booking = Booking(
                service_id=service_id,
                client_id=1,
                booking_date=booking_date,
                booking_time=booking_time,
                duration=int(duration),
                notes=notes,
                status='pending'
            )

            db.session.add(new_booking)
            db.session.commit()

            flash('Booking confirmed!')
            return redirect(url_for('services.services_home'))

        return render_template('book_service.html', service=service)
    except Exception as e:
        flash('Error booking service')
        return redirect(url_for('services.services_home'))


# ============ CONSTRUCTION BLUEPRINT ROUTES (ENHANCED) ============

@construction_bp.route('/building-constructors')
def building_constructors():
    selected_brand = request.args.get('brand', '')
    brands = ['Residential', 'Commercial', 'Industrial', 'Multi-Storey', 'Renovation']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Building Constructors',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.building_constructors.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/engineering-disciplines')
def engineering_disciplines():
    selected_brand = request.args.get('brand', '')
    brands = ['Civil', 'Structural', 'Mechanical', 'Electrical', 'Geotechnical']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Engineering Disciplines',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.engineering_disciplines.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/construction-specialists')
def construction_specialists():
    selected_brand = request.args.get('brand', '')
    brands = ['Concrete', 'Steel', 'Timber', 'Masonry', 'Glass', 'Roofing']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Construction Specialists',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.construction_specialists.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/professional-services')
def professional_services():
    selected_brand = request.args.get('brand', '')
    brands = ['Architect', 'Quantity Surveyor', 'Project Manager', 'Safety Officer', 'Building Inspector']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Professional Services',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.professional_services.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/site-workers')
def site_workers():
    selected_brand = request.args.get('brand', '')
    brands = ['Carpenter', 'Electrician', 'Plumber', 'Welder', 'Steel Fixer', 'Concrete Worker']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Site Workers',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.site_workers.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/builders-contractors')
def builders_contractors():
    selected_brand = request.args.get('brand', '')
    brands = ['General Contractor', 'Building Contractor', 'Civil Contractor', 'Industrial Contractor']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Builders & Contractors',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.builders_contractors.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/renovation-specialists')
def renovation_specialists():
    selected_brand = request.args.get('brand', '')
    brands = ['Kitchen Renovation', 'Bathroom Renovation', 'House Extension', 'Basement Conversion']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Renovation Specialists',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.renovation_specialists.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/roofing-specialists')
def roofing_specialists():
    selected_brand = request.args.get('brand', '')
    brands = ['Tile Roofing', 'Metal Roofing', 'Flat Roofing', 'Thatched', 'Roof Repairs']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Roofing Specialists',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.roofing_specialists.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/structural-engineers')
def structural_engineers():
    selected_brand = request.args.get('brand', '')
    brands = ['Structural Analysis', 'Foundation Design', 'Steel Structure', 'Concrete Structure']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Structural Engineers',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.structural_engineers.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/civil-engineers')
def civil_engineers():
    selected_brand = request.args.get('brand', '')
    brands = ['Road Construction', 'Drainage', 'Earthworks', 'Bridges', 'Surveying']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Civil Engineers',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.civil_engineers.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/geotechnical-engineers')
def geotechnical_engineers():
    selected_brand = request.args.get('brand', '')
    brands = ['Soil Testing', 'Foundation', 'Slope Stability', 'Ground Improvement']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Geotechnical Engineers',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.geotechnical_engineers.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/mechanical-engineers')
def mechanical_engineers():
    selected_brand = request.args.get('brand', '')
    brands = ['HVAC', 'Fire Protection', 'Plumbing', 'Elevators', 'Mechanical Design']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Mechanical Engineers',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.mechanical_engineers.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/electrical-engineers')
def construction_electrical_engineers():
    selected_brand = request.args.get('brand', '')
    brands = ['Electrical Design', 'Power Distribution', 'Lighting', 'Fire Alarm', 'Security Systems']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Electrical Engineers',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.electrical_engineers.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/concrete-specialists')
def concrete_specialists():
    selected_brand = request.args.get('brand', '')
    brands = ['Concrete Pouring', 'Formwork', 'Reinforcement', 'Floor Screed', 'Decorative Concrete']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Concrete Specialists',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.concrete_specialists.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/steel-fixers')
def steel_fixers():
    selected_brand = request.args.get('brand', '')
    brands = ['Reinforcement Steel', 'Structural Steel', 'Steel Fixing', 'Welding']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Steel Fixers',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.steel_fixers.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/welders-fabricators')
def welders_fabricators():
    selected_brand = request.args.get('brand', '')
    brands = ['MIG Welding', 'TIG Welding', 'Arc Welding', 'Metal Fabrication', 'Custom Steel Work']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Welders & Fabricators',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.welders_fabricators.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/scaffolding-experts')
def scaffolding_experts():
    selected_brand = request.args.get('brand', '')
    brands = ['Scaffold Erectors', 'Access Solutions', 'Temporary Structure', 'Scaffold Hire']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Scaffolding Experts',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.scaffolding_experts.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/piling-specialists')
def piling_specialists():
    selected_brand = request.args.get('brand', '')
    brands = ['Bored Piling', 'Driven Piling', 'Micro Piling', 'Sheet Piling', 'Foundation Piling']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Piling Specialists',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.piling_specialists.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/formwork-specialists')
def formwork_specialists():
    selected_brand = request.args.get('brand', '')
    brands = ['Timber Formwork', 'Steel Formwork', 'Climbing Formwork', 'Precast Moulds']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Formwork Specialists',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.formwork_specialists.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/architects')
def architects():
    selected_brand = request.args.get('brand', '')
    brands = ['Residential Architect', 'Commercial Architect', 'Sustainable Design', 'Urban Planning']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Architects',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.architects.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/quantity-surveyors')
def quantity_surveyors():
    selected_brand = request.args.get('brand', '')
    brands = ['Cost Estimation', 'Quantity Takeoff', 'Tendering', 'Contract Admin']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Quantity Surveyors',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.quantity_surveyors.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/project-managers')
def project_managers():
    selected_brand = request.args.get('brand', '')
    brands = ['Construction Management', 'Project Scheduling', 'Quality Control', 'Site Supervision']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Project Managers',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.project_managers.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/construction-safety-officers')
def construction_safety_officers():
    selected_brand = request.args.get('brand', '')
    brands = ['Site Safety', 'Risk Assessment', 'Safety Training', 'Incident Investigation']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Safety Officers',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.safety_officers.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/building-inspectors')
def building_inspectors():
    selected_brand = request.args.get('brand', '')
    brands = ['Building Inspection', 'Structural Inspection', 'Pre-purchase Inspection', 'Compliance Check']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Building Inspectors',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.building_inspectors.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/site-supervisors')
def site_supervisors():
    selected_brand = request.args.get('brand', '')
    brands = ['Site Supervision', 'Labour Management', 'Quality Assurance', 'Progress Monitoring']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Site Supervisors',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.site_supervisors.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/heavy-equipment-operators')
def heavy_equipment_operators():
    selected_brand = request.args.get('brand', '')
    brands = ['Excavator Operator', 'Bulldozer Operator', 'Loader Operator', 'Crane Operator']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Equipment Operators',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.heavy_equipment_operators.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/tile-marble-specialists')
def tile_marble_specialists():
    selected_brand = request.args.get('brand', '')
    brands = ['Tile Installation', 'Marble Flooring', 'Stone Cladding', 'Terrazzo']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Tile & Marble',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.tile_marble_specialists.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/painting-contractors')
def painting_contractors():
    selected_brand = request.args.get('brand', '')
    brands = ['Interior Painting', 'Exterior Painting', 'Industrial Painting', 'Decorative Painting']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Painting Contractors',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.painting_contractors.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/flooring-specialists')
def flooring_specialists():
    selected_brand = request.args.get('brand', '')
    brands = ['Wood Flooring', 'Tile Flooring', 'Carpet Installation', 'Laminate Flooring', 'Epoxy Flooring']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Flooring Specialists',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.flooring_specialists.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@construction_bp.route('/glaziers')
def glaziers():
    selected_brand = request.args.get('brand', '')
    brands = ['Glass Installation', 'Window Replacement', 'Glass Repair', 'Storefront Glazing']
    listings = []
    try:
        query = Service.query.filter_by(
            category='Construction',
            subcategory='Glaziers',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Service.rating.desc()).all()
    except:
        listings = []
    return render_template('construction.glaziers.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)
# ============ ADVERTS HUB ROUTES ==========
@adverts_bp.route('/')
def adverts_hub():
    return render_template('adverts.html')


@adverts_bp.route('/business-ads')
def business_ads():
    return render_template('adverts.business_ads.html', category='Business Ads')


@adverts_bp.route('/event-promotion')
def event_promotion():
    return render_template('adverts.event_promotion.html', category='Event Promotion')


@adverts_bp.route('/product-launch')
def product_launch():
    return render_template('adverts.product_launch.html', category='Product Launch')


@adverts_bp.route('/sales-discounts')
def sales_discounts():
    return render_template('adverts.sales_discounts.html', category='Sales & Discounts')


@adverts_bp.route('/food-beverage')
def food_beverage():
    return render_template('adverts.food_beverage.html', category='Food & Beverage')


@adverts_bp.route('/create-ad')
def create_ad():
    return render_template('adverts/create_ad.html')


# ============ BUSINESS ADS ROUTES ==========
@business_ads_bp.route('/')
def business_ads_hub():
    return render_template('adverts/business_ads.html')


@business_ads_bp.route('/corporate-services')
def corporate_services():
    return render_template('adverts/business_ads.corporate_services.html', subcategory='Corporate Services')


@business_ads_bp.route('/b2b-solutions')
def b2b_solutions():
    return render_template('adverts/business_ads.b2b_solutions.html', subcategory='B2B Solutions')


@business_ads_bp.route('/real-estate-commercial')
def real_estate_commercial():
    return render_template('adverts/business_ads.real_estate_commercial.html', subcategory='Real Estate Commercial')


@business_ads_bp.route('/financial-services')
def financial_services():
    return render_template('adverts/business_ads.financial_services.html', subcategory='Financial Services')


@business_ads_bp.route('/marketing-pr')
def marketing_pr():
    return render_template('adverts/business_ads.marketing_pr.html', subcategory='Marketing & PR')


@business_ads_bp.route('/education-training')
def education_training():
    return render_template('adverts/business_ads.education_training.html', subcategory='Education & Training')


@business_ads_bp.route('/healthcare-services')
def healthcare_services():
    return render_template('adverts/business_ads.healthcare_services.html', subcategory='Healthcare Services')


@business_ads_bp.route('/tech-it-services')
def tech_it_services():
    return render_template('adverts/business_ads.tech_it_services.html', subcategory='Tech & IT Services')

#Product launch

# ============ PRODUCT LAUNCH SUBCATEGORY ROUTES ============
@product_launch_bp.route('/electronics-gadgets')
def electronics_gadgets():
    return render_template('product_launch.electronics_gadgets.html', subcategory='Electronics & Gadgets')

@product_launch_bp.route('/fashion-apparel')
def fashion_apparel():
    return render_template('product_launch.fashion_apparel.html', subcategory='Fashion & Apparel')

@product_launch_bp.route('/beauty-cosmetics')
def beauty_cosmetics():
    return render_template('product_launch.beauty_cosmetics.html', subcategory='Beauty & Cosmetics')

@product_launch_bp.route('/food-beverage-launch')
def food_beverage():
    return render_template('product_launch.food_beverage.html', subcategory='Food & Beverage')

@product_launch_bp.route('/home-living')
def home_living():
    return render_template('product_launch.home_living.html', subcategory='Home & Living')

@product_launch_bp.route('/automotive-launch')
def automotive():
    return render_template('product_launch.automotive.html', subcategory='Automotive')

@product_launch_bp.route('/software-apps')
def software_apps():
    return render_template('product_launch.software_apps.html', subcategory='Software & Apps')

@product_launch_bp.route('/create-listing')
def create_launch_listing():
    return render_template('product_launch.create_listing.html')

# ============ EVENT PROMOTION ROUTES ==========
# ============ EVENT PROMOTION ROUTES ==========
@event_promotion_bp.route('/')
def event_promotion_hub():
    return render_template('adverts/event_promotion.html')


@event_promotion_bp.route('/concerts-music')
def concerts_music():
    return render_template('adverts/event_promotion.concerts_music.html', subcategory='Concerts & Music Festivals')


@event_promotion_bp.route('/corporate-events')
def corporate_events():
    return render_template('adverts/event_promotion.corporate_events.html', subcategory='Corporate Events')


@event_promotion_bp.route('/weddings-parties')
def weddings_parties():
    return render_template('adverts/event_promotion.weddings_parties.html', subcategory='Weddings & Parties')


@event_promotion_bp.route('/sports-events')
def sports_events():
    return render_template('adverts/event_promotion.sports_events.html', subcategory='Sports Events')


@event_promotion_bp.route('/art-exhibitions')
def art_exhibitions():
    return render_template('adverts/event_promotion.art_exhibitions.html', subcategory='Art Exhibitions')


@event_promotion_bp.route('/charity-fundraisers')
def charity_fundraisers():
    return render_template('adverts/event_promotion.charity_fundraisers.html', subcategory='Charity & Fundraisers')


@event_promotion_bp.route('/workshops-classes')
def workshops_classes():
    return render_template('adverts/event_promotion.workshops_classes.html', subcategory='Workshops & Classes')


@event_promotion_bp.route('/holiday-seasonal')
def holiday_seasonal():
    return render_template('adverts/event_promotion.holiday_seasonal.html', subcategory='Holiday & Seasonal Events')


# ADD THIS ROUTE for create_event_listing (used in your template CTA)
@event_promotion_bp.route('/create-event-listing')
def create_event_listing():
    return render_template('adverts/event_promotion.create_event_listing.html')

# ============ SALES & DISCOUNTS ROUTES ==========
@sales_discounts_bp.route('/')
def sales_discounts_hub():
    return render_template('adverts/sales_discounts.html')


@sales_discounts_bp.route('/seasonal-sales')
def seasonal_sales():
    return render_template('adverts/sales_discounts.seasonal_sales.html', subcategory='Seasonal Sales')


@sales_discounts_bp.route('/clearance-liquidation')
def clearance_liquidation():
    return render_template('adverts/sales_discounts.clearance_liquidation.html', subcategory='Clearance & Liquidation')


@sales_discounts_bp.route('/flash-sales')
def flash_sales():
    return render_template('adverts/sales_discounts.flash_sales.html', subcategory='Flash Sales')


@sales_discounts_bp.route('/bundle-deals')
def bundle_deals():
    return render_template('adverts/sales_discounts.bundle_deals.html', subcategory='Bundle Deals')


@sales_discounts_bp.route('/member-vip')
def member_vip():
    return render_template('adverts/sales_discounts.member_vip.html', subcategory='Member/VIP Discounts')


@sales_discounts_bp.route('/first-time-buyer')
def first_time_buyer():
    return render_template('adverts/sales_discounts.first_time_buyer.html', subcategory='First-Time Buyer Offers')


@sales_discounts_bp.route('/holiday-specials')
def holiday_specials():
    return render_template('adverts/sales_discounts.holiday_specials.html', subcategory='Holiday Specials')


@sales_discounts_bp.route('/bulk-purchase')
def bulk_purchase():
    return render_template('adverts/sales_discounts.bulk_purchase.html', subcategory='Bulk Purchase Discounts')


# ============ FOOD & BEVERAGE ROUTES ==========
@food_beverage_bp.route('/')
def food_beverage_hub():
    return render_template('adverts/food_beverage.html')


@food_beverage_bp.route('/restaurants-dining')
def restaurants_dining():
    return render_template('adverts/food_beverage.restaurants_dining.html', subcategory='Restaurants & Dining')


@food_beverage_bp.route('/cafes-coffee')
def cafes_coffee():
    return render_template('adverts/food_beverage.cafes_coffee.html', subcategory='Cafes & Coffee Shops')


@food_beverage_bp.route('/fast-food-takeaway')
def fast_food_takeaway():
    return render_template('adverts/food_beverage.fast_food_takeaway.html', subcategory='Fast Food & Takeaway')


@food_beverage_bp.route('/bakeries-desserts')
def bakeries_desserts():
    return render_template('adverts/food_beverage.bakeries_desserts.html', subcategory='Bakeries & Desserts')


@food_beverage_bp.route('/grocery-supermarkets')
def grocery_supermarkets():
    return render_template('adverts/food_beverage.grocery_supermarkets.html', subcategory='Grocery & Supermarkets')


@food_beverage_bp.route('/alcohol-beverages')
def alcohol_beverages():
    return render_template('adverts/food_beverage.alcohol_beverages.html', subcategory='Alcohol & Beverages')


@food_beverage_bp.route('/meal-prep-catering')
def meal_prep_catering():
    return render_template('adverts/food_beverage.meal_prep_catering.html', subcategory='Meal Prep & Catering')


@food_beverage_bp.route('/organic-health-foods')
def organic_health_foods():
    return render_template('adverts/food_beverage.organic_health_foods.html', subcategory='Organic & Health Foods')

@food_beverage_bp.route('/create-food-listing')
def create_food_listing():
    return render_template('food_beverage.create_food_listing.html', category='Food & Beverage')

# ============ JOBS & GIGS ROUTES ==========
@jobs_bp.route('/')
def jobs_hub():
    return render_template('jobs.html')

@jobs_bp.route('/jobsgigs')
def jobsgigs():
    return render_template('listings.jobsgigs.html')


@jobs_bp.route('/fulltime')
def fulltime():
    job_categories = [
        'Accounting & Finance', 'Admin & Office', 'Customer Service',
        'Education & Training', 'Engineering', 'Healthcare & Medical',
        'Hospitality & Tourism', 'Human Resources', 'Information Technology',
        'Legal & Compliance', 'Marketing & Advertising', 'Retail & Sales',
        'Skilled Trades', 'Transport & Logistics', 'Writing & Editing'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Full Time Jobs',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Full Time Jobs',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        # Log the error and return empty list – prevents page crash
        print(f"Database error: {e}")
        listings = []

    return render_template('jobs.fulltime.html',
                           types=job_categories,
                           selected_type=selected_type,
                           listings=listings)


@jobs_bp.route('/parttime')
def parttime():
    parttime_categories = [
        'Retail Sales',
        'Food Service',
        'Customer Support',
        'Delivery & Driving',
        'Administrative',
        'Tutoring & Teaching',
        'Cleaning & Janitorial',
        'Warehouse',
        'Event Staff',
        'Childcare & Elder Care',
        'Fitness & Wellness',
        'Seasonal & Temp',
        'Freelance & Gig',
        'Pet Care',
        'Social Media & Marketing'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Part Time Jobs',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Part Time Jobs',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('jobs.parttime.html',
                           types=parttime_categories,
                           selected_type=selected_type,
                           listings=listings)


@jobs_bp.route('/attachment')
def attachment():
    # ✅ Define the list before using it
    attachment_categories = [
        # Business & Commerce
        'Accounting',
        'Business Management',
        'Marketing',
        'Economics',
        'Human Resources',
        'Public Administration',

        # Engineering & Technology
        'Civil Engineering',
        'Electrical Engineering',
        'Mechanical Engineering',
        'Chemical Engineering',
        'Software Engineering',
        'Computer Science',
        'Information Technology',
        'Construction Engineering',
        'Surveying & Geomatics',
        'Architectural Technology',
        'Quantity Surveying',
        'Urban & Regional Planning',

        # Agriculture & Life Sciences
        'Crop Science',
        'Horticulture',
        'Agribusiness',
        'Animal Science',
        'Food Science & Technology',
        'Biotechnology',
        'Biomedical Engineering',

        # Health Sciences
        'Medical Analytics & Informatics',
        'Psychology',
        'Health Sciences',

        # Education & Social Sciences
        'Education',
        'Curriculum Design',
        'Religion & Ethics Education',

        # Creative & Applied Arts
        'Design & Technology',
        'Jewellery Design',
        'Gemology',

        # Other Professional Fields
        'Data Science',
        'Actuarial Science',
        'Cyber Security',
        'Statistics',
        'Logistics & Transport',
        'Valuation & Estate Management',
        'Tourism & Hospitality',
        'Legal Studies',
        'Translation'
    ]

    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Attachment Jobs',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Attachment Jobs',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('jobs.attachment.html',
                           types=attachment_categories,  # ✅ using the correct variable
                           selected_type=selected_type,
                           listings=listings)


@jobs_bp.route('/freelance')
def freelance():
    freelance_categories = [
        'Writing & Content',
        'Design & Creative',
        'Web Development',
        'Mobile Development',
        'Data Science',
        'Marketing & SEO',
        'Video & Animation',
        'Accounting & Finance',
        'Legal',
        'Administrative',
        'Translation',
        'Photography',
        'Consulting',
        'Customer Support',
        'Virtual Assistant'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Freelance Jobs',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Freelance Jobs',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('jobs.freelance.html',
                           types=freelance_categories,
                           selected_type=selected_type,
                           listings=listings)


@jobs_bp.route('/quickgigs')
def quickgigs():
    quickgigs_categories = [
        'Delivery & Courier',
        'Event Staff',
        'Moving Help',
        'Cleaning',
        'Pet Sitting',
        'Tutoring',
        'Handyman',
        'Warehouse',
        'Seasonal',
        'Micro‑tasks',
        'Lawn & Garden',
        'Snow Removal',
        'Childcare',
        'Photography',
        'Surveys & Studies'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Quick Gigs',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Quick Gigs',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('jobs.quickgigs.html',
                           types=quickgigs_categories,
                           selected_type=selected_type,
                           listings=listings)


# ============ EVENTS ROUTES ==========

@events_bp.route('/')
def events_hub():
    return render_template('events.html')

@listings_bp.route('/events')
def list_events():
    return render_template('listings.events.html')

@events_bp.route('/concerts')
def concerts():
    concert_categories = [
        'Concerts',
        'Music Festivals',
        'Club Show',
        'Road Shows',
        'Recital',
        'Concert Residency',
        'House Concert',
        'Charity Concert'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Concerts',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Concerts',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('events.concerts.html',
                           types=concert_categories,
                           selected_type=selected_type,
                           listings=listings)



# ========== THEATER & ARTS BLUEPRINT ==========

@events_bp.route('/theater-arts')
def theater_arts():
    theater_categories = [
        'Plays',
        'Musicals',
        'Dance',
        'Theatre Festivals',
        'Improv & Comedy',
        'Art Exhibitions',
        'Spoken Word',
        'Family Shows'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Theatre & Arts',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Theatre & Arts',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('events.theater_arts.html',
                           types=theater_categories,
                           selected_type=selected_type,
                           listings=listings)


# ========== SPORT EVENTS ==========

@events_bp.route('/sportevents')
def sportevents():
    sports_categories = [
        'Football', 'Basketball', 'Tennis', 'Marathons', 'Extreme Sports',
        'Combat Sports', 'Golf', 'E-Sports', 'Baseball', 'Cricket',
        'Rugby', 'Hockey', 'Volleyball', 'Cycling', 'Swimming'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Sports Events',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Sports Events',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('events.sportevents.html',
                           types=sports_categories,
                           selected_type=selected_type,
                           listings=listings)



# ======================= WORKSHOPS===============
@events_bp.route('/workshops')
def workshops():
    workshop_categories = [
        'Leadership',
        'Digital Marketing',
        'Data Science',
        'Graphic Design',
        'Public Speaking',
        'Project Management',
        'Coding',
        'Financial Literacy',
        'Mental Health',
        'Sales & Negotiation',
        'Creative Writing',
        'Remote Work'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Workshops',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Workshops',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('events.workshops.html',
                           types=workshop_categories,
                           selected_type=selected_type,
                           listings=listings)



# FOOD FESTIVALS===============
@events_bp.route('/food-festivals')
def food_festivals():
    food_categories = [
        'Street Food',
        'Wine & Cheese',
        'BBQ & Grill',
        'Seafood',
        'Chocolate & Dessert',
        'International Cuisine',
        'Cooking Competitions',
        'Food & Music',
        'Holiday Food'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Food Festivals',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Food Festivals',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('events.food_festivals.html',
                           types=food_categories,
                           selected_type=selected_type,
                           listings=listings)


# ============ COMMUNITY ROUTES ==========
@community_bp.route('/')
def community_hub():
    return render_template('community.html')

@community_bp.route('/local-groups')
def local_groups():
    local_group_categories = [
        'Neighborhood',
        'Parent & Family',
        'Hobby & Interest',
        'Sports & Fitness',
        'Religious & Spiritual',
        'Support & Wellness',
        'Business & Professional',
        'Cultural & Ethnic',
        'Volunteer & Activism',
        'Seniors & Retirees'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Local Groups',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Local Groups',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('community.local_groups.html',
                           types=local_group_categories,
                           selected_type=selected_type,
                           listings=listings)

# ========LOCAL GROUPS=============
@community_bp.route('/create-group')
def create_group():
    # For now, just show a placeholder page or redirect
    return redirect(url_for('community.list_local_groups'))

@community_bp.route('/local-groups')
def list_local_groups():
    local_group_categories = [
        'Neighborhood',
        'Parent & Family',
        'Hobby & Interest',
        'Sports & Fitness',
        'Religious & Spiritual',
        'Support & Wellness',
        'Business & Professional',
        'Cultural & Ethnic',
        'Volunteer & Activism',
        'Seniors & Retirees'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Local Groups',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Local Groups',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('community.local_groups.html',
                           types=local_group_categories,
                           selected_type=selected_type,
                           listings=listings)



@community_bp.route('/discussions', endpoint='list_discussions')
def list_discussions():
    discussion_categories = [
        'Family & Parenting',
        'Personal Development',
        'Community & Civic',
        'Practical & Daily Life',
        'Social & Cultural'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Discussions',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Discussions',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('community.discussions.html',
                           types=discussion_categories,
                           selected_type=selected_type,
                           listings=listings)


#======== EVENT MEET-UPS =================

@community_bp.route('/events-meetups', endpoint='list_events_meetups')
def list_events_meetups():
    event_categories = [
        'Social Gatherings',
        'Classes',
        'Outdoor Activities',
        'Wellness & Self-care',
        'Kids Gatherings',
        'Cultural & Heritage',
        'Charity Drives'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Events & Meetups',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Events & Meetups',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('community.events_meetups.html',
                           types=event_categories,
                           selected_type=selected_type,
                           listings=listings)


#=========== VOLUNTEER ==================
@community_bp.route('/volunteer', endpoint='list_volunteer')
def list_volunteer():
    volunteer_categories = [
        'Environmental',
        'Elderly Care',
        'Children & Youth',
        'Health Support',
        'Community Dev',
        'Disaster & Emergency',
        'Education & Literacy',
        'Food Security'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Volunteer',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Volunteer',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('community.volunteer.html',
                           types=volunteer_categories,
                           selected_type=selected_type,
                           listings=listings)


# ==============LOST & FOUND =============
@community_bp.route('/lost-found', endpoint='list_lost_found')
def list_lost_found():
    lost_found_categories = [
        'Lost Items',
        'Found Items'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Lost & Found',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Lost & Found',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('community.lost_found.html',
                           types=lost_found_categories,
                           selected_type=selected_type,
                           listings=listings)


@community_bp.route('/neighborhood-watch')
def neighborhood_watch():
    return render_template('community.neighborhood_watch.html', subcategory='Neighborhood Watch')


@community_bp.route('/skill-sharing')
def skill_sharing():
    return render_template('community.skill_sharing.html', subcategory='Skill Sharing')


@community_bp.route('/community-projects')
def community_projects():
    return render_template('community.community_projects.html', subcategory='Community Projects')


@community_bp.route('/start-group')
def start_group():
    return render_template('community/start_group.html')


# ============ API ROUTES ============
@main_bp.route('/api/listings')
def api_listings():
    try:
        listings = Listing.query.filter_by(is_active=True).all()
        result = []
        for listing in listings:
            result.append({
                'id': listing.id,
                'title': listing.title,
                'price': listing.price,
                'category': listing.category,
                'subcategory': listing.subcategory,
                'location': listing.location,
                'images': listing.images or []
            })
        return jsonify(result)
    except:
        return jsonify([])


@main_bp.route('/api/services')
def api_services():
    try:
        services = Service.query.filter_by(is_active=True).all()
        result = []
        for service in services:
            result.append({
                'id': service.id,
                'title': service.title,
                'category': service.category,
                'subcategory': service.subcategory,
                'service_type': service.service_type,
                'hourly_rate': service.hourly_rate,
                'fixed_price': service.fixed_price,
                'location': service.location,
                'rating': service.rating,
                'years_experience': service.years_experience
            })
        return jsonify(result)
    except:
        return jsonify([])


@main_bp.route('/api/services/category/<category>')
def api_services_by_category(category):
    try:
        services = Service.query.filter_by(
            category=category,
            is_active=True
        ).order_by(Service.rating.desc()).all()

        result = []
        for service in services:
            result.append({
                'id': service.id,
                'title': service.title,
                'category': service.category,
                'subcategory': service.subcategory,
                'hourly_rate': service.hourly_rate,
                'fixed_price': service.fixed_price,
                'location': service.location,
                'rating': service.rating,
                'years_experience': service.years_experience
            })
        return jsonify(result)
    except:
        return jsonify([])


# ============ DATABASE INITIALIZATION ROUTE ============
@main_bp.route('/init-db')
def init_database():
    try:
        db.create_all()
        return "✅ Database tables created successfully!"
    except Exception as e:
        return f"❌ Error creating tables: {str(e)}"