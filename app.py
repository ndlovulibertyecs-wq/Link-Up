from flask import Flask, render_template, jsonify
from config import Config
from extensions import db
import routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints/routes
    app.register_blueprint(routes.main_bp)

    # Market Center
    app.register_blueprint(routes.marketplace_bp, url_prefix='/marketplace')

    # Services
    app.register_blueprint(routes.services_bp, url_prefix='/services')

    # Hire Zone
    app.register_blueprint(routes.hire_bp, url_prefix='/hire')

    # Machinery
    app.register_blueprint(routes.machinery_bp, url_prefix='/machinery')

    # Construction
    app.register_blueprint(routes.construction_bp, url_prefix='/construction')

    # Farmers Room
    app.register_blueprint(routes.farmers_bp, url_prefix='/farmers')

    # Housing
    app.register_blueprint(routes.housing_bp, url_prefix='/housing')

    # ========== ADVERTS HUB BLUEPRINTS ==========
    app.register_blueprint(routes.adverts_bp, url_prefix='/adverts')
    app.register_blueprint(routes.business_ads_bp, url_prefix='/adverts/business-ads')
    app.register_blueprint(routes.event_promotion_bp, url_prefix='/adverts/event-promotion')
    app.register_blueprint(routes.product_launch_bp, url_prefix='/adverts/product-launch')
    app.register_blueprint(routes.sales_discounts_bp, url_prefix='/adverts/sales-discounts')
    app.register_blueprint(routes.food_beverage_bp, url_prefix='/adverts/food-beverage')

    # ========== JOBS & GIGS BLUEPRINTS ==========
    app.register_blueprint(routes.jobs_bp, url_prefix='/jobs')

    # ========== EVENTS BLUEPRINT (contains concerts, theater, etc.) ==========
    app.register_blueprint(routes.events_bp, url_prefix='/events')

    # ========== COMMUNITY BLUEPRINT ==========
    app.register_blueprint(routes.community_bp, url_prefix='/community')

    # ========== CONCERTS BLUEPRINT ==========
    app.register_blueprint(routes.concerts_bp, url_prefix='/concerts')

    # ========== LISTINGS BLUEPRINT ==========
    app.register_blueprint(routes.listings_bp)

    # Electronics routes (keep if still needed)
    @app.route('/electronics')
    def electronics_page():
        return render_template('electronics.html')

    @app.route('/marketplace/electronics')
    def marketplace_electronics():
        return render_template('electronics.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)