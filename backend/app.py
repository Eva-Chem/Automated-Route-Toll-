def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))
    
    # Init extensions
    db.init_app(app)
    JWTManager(app)
    CORS(app)
    
    # -------------------------
    # Register Blueprints
    # -------------------------
    from routes.test_routes import test_bp
    from routes.toll_zones import toll_zones_bp

    app.register_blueprint(test_bp, url_prefix='/api')
    app.register_blueprint(toll_zones_bp)   # already has /api in routes
    
    # -------------------------
    # Health & Root
    # -------------------------
    @app.route('/health', methods=['GET'])
    def health_check():
        return {
            'status': 'healthy',
            'message': 'Toll Tracker API is running'
        }, 200
    
    @app.route('/', methods=['GET'])
    def index():
        return {
            "status": "online",
            "message": "Automated Route Toll API is running",
            "environment": os.getenv('FLASK_ENV', 'development')
        }, 200

    return app
