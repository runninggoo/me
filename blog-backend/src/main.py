import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta

# 导入数据库和模型
from src.models import db

# 导入路由蓝图
from src.routes.auth import auth_bp
from src.routes.article import article_bp
from src.routes.roadmap import roadmap_bp
from src.routes.mindmap import mindmap_bp
from src.routes.tag import tag_bp
from src.routes.upload import upload_bp
from src.routes.admin import admin_bp

def create_app():
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # 基本配置
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-change-in-production'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
    app.config['JWT_IDENTITY_CLAIM'] = 'sub'
    
    # 数据库配置 - 开发环境使用SQLite，生产环境可配置MySQL
    # 如需使用MySQL，请修改以下配置：
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b:123456@122.51.56.206:3306/blog_db'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 文件上传配置
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    
    # 初始化扩展
    CORS(app, origins="*")  # 允许所有来源的跨域请求
    JWTManager(app)
    db.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(article_bp, url_prefix='/api/articles')
    app.register_blueprint(roadmap_bp, url_prefix='/api/roadmaps')
    app.register_blueprint(mindmap_bp, url_prefix='/api/mindmaps')
    app.register_blueprint(tag_bp, url_prefix='/api/tags')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # 创建数据库表
    with app.app_context():
        # 确保上传目录存在
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        # 确保静态目录存在
        os.makedirs(app.static_folder, exist_ok=True)
        db.create_all()
        create_default_admin()
    
    # 静态文件服务（用于前端）
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        # 排除API路由
        if path.startswith('api/'):
            return "API route not found", 404
            
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404

        # 检查请求的路径是否对应静态文件
        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            # 对于所有其他路由，返回index.html（由Vue Router处理）
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404
    
    # 上传文件服务
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    return app

def create_default_admin():
    """创建默认管理员账号"""
    try:
        from src.models.user import User
        import bcrypt
        
        # 检查是否已存在管理员账号
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # 创建默认管理员
            password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=password_hash.decode('utf-8'),
                display_name='系统管理员',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("默认管理员账号已创建:")
            print("用户名: admin")
            print("密码: admin123")
            print("邮箱: admin@example.com")
        else:
            print("管理员账号已存在")
    except Exception as e:
        print(f"创建默认管理员失败: {e}")
        db.session.rollback()

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
