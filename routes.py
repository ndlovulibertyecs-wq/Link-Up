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
    types = []
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
    types = []
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
    types = []
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
    types = []
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
    types = []
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
    types = ['Angus', 'Hereford', 'Holstein', 'Jersey', 'Brahman', 'Charolais', 'Simmental', 'Limousin', 'Shorthorn', 'Gelbvieh']
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
    brands = ['Office Space', 'Hall', 'Meeting Space', 'Retail', 'Warehouse', 'Industrial', 'Co-working', 'Mixed Use']
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
    listings = []
    if selected_brand:
        try:
            listings = Listing.query.filter_by(
                category='Electronics',
                subcategory='Smartphones',
                brand=selected_brand,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('smartphones.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/laptops')
def laptops():
    selected_brand = request.args.get('brand', '')
    brands = ['Dell', 'HP', 'Lenovo', 'Apple', 'Asus',
              'Acer', 'MSI', 'Huawei', 'Microsoft', 'Samsung', 'Avantis', 'LG', 'Toshiba']
    listings = []
    if selected_brand:
        try:
            listings = Listing.query.filter_by(
                category='Electronics',
                subcategory='Laptops',
                brand=selected_brand,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('laptops.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/audio')
def audio():
    selected_brand = request.args.get('brand', '')
    brands = ['Headphones', 'EarBuds', 'AirPods', 'Earphones', 'Speaker', 'SoundBars']
    listings = []
    if selected_brand:
        try:
            listings = Listing.query.filter_by(
                category='Electronics', subcategory='Audio',
                brand=selected_brand, is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('audio.html', listings=listings, selected_brand=selected_brand, brands=brands)


@marketplace_bp.route('/cameras')
def cameras():
    selected_brand = request.args.get('brand', '')
    brands = ['Canon', 'Nikon', 'Sony', 'Fujifilm', 'GoPro', 'Panasonic', 'Olympus', 'Leica', 'Sigma', 'DJI']
    listings = []
    if selected_brand:
        try:
            listings = Listing.query.filter_by(
                category='Electronics', subcategory='Cameras',
                brand=selected_brand, is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('cameras.html', listings=listings, selected_brand=selected_brand, brands=brands)


@marketplace_bp.route('/gaming')
def gaming():
    selected_brand = request.args.get('brand', '')
    brands = ['Sony', 'Microsoft', 'Nintendo', 'Razer', 'Logitech', 'SteelSeries', 'Corsair', 'ASUS', 'MSI', 'HyperX']
    listings = []
    if selected_brand:
        try:
            listings = Listing.query.filter_by(
                category='Electronics', subcategory='Gaming',
                brand=selected_brand, is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('gaming.html', listings=listings, selected_brand=selected_brand, brands=brands)


@marketplace_bp.route('/accessories')
def accessories():
    selected_brand = request.args.get('brand', '')
    brands = ['Phone Accessories', 'Laptop Accessories', 'Watches', 'Other']
    listings = []
    if selected_brand:
        try:
            listings = Listing.query.filter_by(
                category='Electronics', subcategory='Accessories',
                brand=selected_brand, is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('accessories.html', listings=listings, selected_brand=selected_brand, brands=brands)


@marketplace_bp.route('/tablets')
def tablets():
    selected_brand = request.args.get('brand', '')
    brands = ['iPad', 'Samsung', 'Microsoft', 'Lenovo', 'Huawei', 'Amazon', 'Xiaomi', 'ASUS', 'Google', 'TCL']
    listings = []
    if selected_brand:
        try:
            listings = Listing.query.filter_by(
                category='Electronics', subcategory='Tablets',
                brand=selected_brand, is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('tablets.html', listings=listings, selected_brand=selected_brand, brands=brands)


@marketplace_bp.route('/home-tech')
def home_tech():
    selected_brand = request.args.get('brand', '')
    brands = ['Climate', 'Security', 'Lighting', 'Entertainment', 'Kitchen', 'Cleaning', 'Power', 'Other']
    listings = []
    if selected_brand:
        try:
            listings = Listing.query.filter_by(
                category='Electronics', subcategory='Home Tech',
                brand=selected_brand, is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('home_tech.html', listings=listings, selected_brand=selected_brand, brands=brands)


@marketplace_bp.route('/drones')
def drones():
    selected_brand = request.args.get('brand', '')
    brands = ['DJI', 'Parrot', 'Autel', 'Holy Stone', 'Skydio', 'Yuneec', 'Hubsan', 'Ryze', 'PowerVision', 'Walkera']
    listings = []
    if selected_brand:
        try:
            listings = Listing.query.filter_by(
                category='Electronics', subcategory='Drones',
                brand=selected_brand, is_active=True
            ).order_by(Listing.created_at.desc()).all()
        except:
            listings = []
    return render_template('drones.html', listings=listings, selected_brand=selected_brand, brands=brands)

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
    selected_brand = request.args.get('brand', '')
    brands = ['Travelling Bags', 'Wallets', 'Sling Bags', 'Back Packs', 'Hand Bags']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fashion',
            subcategory='Bags',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fashion.bags.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/fashion/clothing')
def clothing():
    selected_brand = request.args.get('brand', '')
    brands = ['T-Shirts', 'Shirts', 'Jackets', 'Sweater', 'Hoody',
              'Scuffs', 'Blouses & tops', 'Dresses', 'Trousers', ' Jeans',
              'Pants', 'Shorts','Track-Suits', 'Pyjamas']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fashion',
            subcategory='Clothing',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fashion.clothing.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/fashion/footwear')
def footwear():
    selected_brand = request.args.get('brand', '')
    brands = ['Sneakers', 'Loafers',
              'Sandals', 'Boots',
              'Crocs', 'School Shoes', 'Slippers & flip-flops', 'Ballet flats', 'Heels & Wedges']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fashion',
            subcategory='Footwear',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fashion.footwear.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/fashion/formal')
def formal_wear():
    selected_brand = request.args.get('brand', '')
    brands = ['Hugo Boss', 'Armani', 'Calvin Klein', 'Ralph Lauren', 'Tom Ford', 'Brooks Brothers']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fashion',
            subcategory='Formal Wear',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fashion.formal.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/fashion/jewellery')
def jewellery():
    selected_brand = request.args.get('brand', '')
    brands = ['Necklace', 'Ear-rings', 'Bandles', 'Rings']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fashion',
            subcategory='Watches & Jewelry',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fashion.jewellery.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/fashion/kids')
def kids_fashion():
    selected_type = request.args.get('type', '')   # ?type=Socks
    types = ['Socks', 'Jackets', 'Shirts', 'T‑Shirts', 'Tracksuits', 'Dresses', 'Shorts', 'Jeans', 'Pajamas', 'Hoodies']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fashion',
            subcategory='Kids Fashion',
            is_active=True
        )
        if selected_type:
            query = query.filter_by(clothing_type=selected_type)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fashion.kids.html',
                           types=types,
                           selected_type=selected_type,
                           listings=listings)

@marketplace_bp.route('/fashion/preloved')
def preloved():
    selected_type = request.args.get('type', '')   # ?type=Socks
    types = ['Socks', 'Jackets', 'Hoody', 'T‑Shirts', 'Shirts', 'Shoes', 'Sneakers', 'Jeans', 'Dresses', 'Shorts']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fashion',
            subcategory='Preloved',
            is_active=True
        )
        if selected_type:
            # Filter by a clothing_type field (adjust if your column is named differently)
            query = query.filter_by(clothing_type=selected_type)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fashion.preloved.html',
                           types=types,
                           selected_type=selected_type,
                           listings=listings)


@marketplace_bp.route('/fashion/sports')
def activewear():
    selected_brand = request.args.get('brand', '')
    brands = [
  "Soccer",  "Basketball",  "Tennis",  "Cricket",
  "Rugby",  "Running & Athletics",  "Swimming",  "Cycling",
  "Golf",  "Boxing & Martial Arts", "Baseball",  "Hockey",  "Volleyball",  "Gymnastics",
  "Skiing & Snowboarding",  "Field Hockey",  "Badminton",
  "Weightlifting & Crossfit",  "Netball"
]

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Fashion',
            subcategory='Activewear',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('fashion.sports.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)

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
    selected_brand = request.args.get('brand', '')
    brands = ['Jurgens', 'Sprite', 'Bush Lapa', 'Conqueror', 'Afrispoor', 'Echo']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Vehicles',
            subcategory='Caravans & Campers',   # or 'Campers' — adjust to your actual subcategory name
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('vehicles.caravans.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/vehicles/cars')
def cars():
    selected_brand = request.args.get('brand', '')
    brands = ['Vintage', 'Toyota', 'Volkswagen', 'BMW', 'Mercedes-Benz', 'Ford', 'Honda', 'Hyundai', 'Audi', 'Nissan', 'Mitsubishi']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Vehicles',
            subcategory='Cars',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('vehicles.cars.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/vehicles/commercial')
def vehicles_commercial():
    selected_brand = request.args.get('brand', '')
    brands = ['Toyota', 'Mercedes-Benz', 'Volvo', 'Scania', 'MAN', 'Iveco', 'Tata', 'Hino']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Vehicles',
            subcategory='Commercial',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('vehicles.commercial.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/vehicles/motorcycles')
def motorcycles():
    selected_brand = request.args.get('brand', '')
    brands = ['Harley-Davidson', 'Honda', 'Yamaha', 'Suzuki', 'Kawasaki', 'BMW', 'Ducati', 'Triumph']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Vehicles',
            subcategory='Motorcycles',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('vehicles.motorcycles.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/vehicles/parts')
def parts():
    selected_brand = request.args.get('brand', '')
    brands = ['Rims', 'Engine', 'Batteries', 'ATF', 'Engine Oil', 'Brake Fluid', 'Tyres', 'Shocks']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Vehicles',
            subcategory='Parts & Accessories',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('vehicles.parts.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/vehicles/trucks')
def trucks():
    selected_brand = request.args.get('brand', '')
    brands = ['Below 1 Tonne', '1 tonne', '2 tonnes', '3 tonnes', '5 tonne', '7 tonne', '10 tonne', '15 tonne', '30 tonne']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Vehicles',
            subcategory='Trucks',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('vehicles.trucks.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)

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
    selected_brand = request.args.get('brand', '')
    brands = ['Chairs', 'Table sets', 'Wardrobes', 'Cupboards', 'Stool', 'Desk', 'Furniture Sets', 'Couch', 'Coffy Tables']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Home & Garden',
            subcategory='Furniture',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('home.furniture.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/home-garden/home-decor')
def home_decor():
    selected_brand = request.args.get('brand', '')
    brands = ['Wall Art', 'Kirkland', 'HomeGoods', 'Target', 'Walmart', 'Etsy']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Home & Garden',
            subcategory='Home Decor',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('home.homedeco.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/home-garden/kitchen-dining')
def kitchen_dining():
    selected_brand = request.args.get('brand', '')
    brands = ['KitchenAid', 'Cuisinart', 'Instant Pot', 'Pyrex', 'Corningware', 'Hamilton Beach']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Home & Garden',
            subcategory='Kitchen & Dining',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('home.kitchen.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/home-garden/bedding-bath')
def bedding_bath():
    selected_brand = request.args.get('brand', '')
    brands = ['Cannon', 'Fieldcrest', 'Martha Stewart', 'Laura Ashley', 'Tommy Hilfiger', 'Ralph Lauren']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Home & Garden',
            subcategory='Bedding & Bath',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('home.bedding&bath.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/home-garden/lighting')
def lighting():
    selected_brand = request.args.get('brand', '')
    brands = ['Philips', 'GE', 'IKEA', 'Westinghouse', 'Lithonia', 'Kichler']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Home & Garden',
            subcategory='Lighting',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('home.lighting.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/home-garden/storage')
def storage():
    selected_brand = request.args.get('brand', '')
    brands = ['Sterilite', 'ClosetMaid', 'Rubbermaid', 'IKEA', 'Simplehuman', 'Honey-Can-Do']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Home & Garden',
            subcategory='Storage & Organization',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('home.storage.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/home-garden/garden')
def garden():
    selected_brand = request.args.get('brand', '')
    brands = ['Weber', 'Toro', 'Scotts', 'Miracle-Gro', 'Husqvarna', 'Suncast']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Home & Garden',
            subcategory='Garden & Outdoor',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('home.garden.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/home-garden/smart-home')
def smart_home():
    selected_brand = request.args.get('brand', '')
    brands = ['Amazon', 'Google', 'Philips Hue', 'Ring', 'Nest', 'Samsung SmartThings']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Home & Garden',
            subcategory='Smart Home',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('home.smarthome.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/home-garden/baby-kids')
def baby_kids():
    selected_brand = request.args.get('brand', '')
    brands = ['Graco', 'Fisher-Price', 'Chicco', 'Evenflo', 'Summer Infant', 'Safety 1st']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Home & Garden',
            subcategory='Baby & Kids',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('home.baby&kids.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/home-garden/pet-supplies')
def pet_supplies():
    selected_brand = request.args.get('brand', '')
    brands = ['Purina', 'Pedigree', "Hill's", 'Royal Canin', 'KONG', 'PetSafe']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Home & Garden',
            subcategory='Pet Supplies',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('home.petsupply.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


@marketplace_bp.route('/home-garden/cleaning')
def cleaning():
    selected_brand = request.args.get('brand', '')
    brands = ['Hoover', 'Bissell', 'Shark', 'Dyson', 'Swiffer', 'Clorox']

    listings = []
    try:
        query = Listing.query.filter_by(
            category='Home & Garden',
            subcategory='Cleaning & Home Care',
            is_active=True
        )
        if selected_brand:
            query = query.filter_by(brand=selected_brand)
        listings = query.order_by(Listing.created_at.desc()).all()
    except:
        listings = []

    return render_template('home.cleaning.html',
                           brands=brands,
                           selected_brand=selected_brand,
                           listings=listings)


# ============ BOOKS & MEDIA ROUTES ============
@marketplace_bp.route('/books-media')
def books_media():
    categories = [
        'Textbooks', 'Novels & Fiction', 'Movies & Films', 'TV Series',
        'Music & Vinyl', 'Audiobooks', 'Comic Books', 'Academic Journals',
        'Documentaries', 'Sheet Music', 'Rare & Collectible'
    ]
    selected_type = request.args.get('type', '')
    try:
        if selected_type:
            listings = Listing.query.filter_by(
                category='Books & Media',
                brand=selected_type,
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
        else:
            listings = Listing.query.filter_by(
                category='Books & Media',
                is_active=True
            ).order_by(Listing.created_at.desc()).all()
    except Exception as e:
        print(f"Database error: {e}")
        listings = []

    return render_template('books_media.html',
                           types=categories,
                           selected_type=selected_type,
                           listings=listings)

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
        'Project Mgmt',
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