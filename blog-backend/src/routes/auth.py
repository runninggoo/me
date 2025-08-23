from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models import db, User
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """验证用户名格式"""
    pattern = r'^[a-zA-Z0-9_]{3,50}$'
    return re.match(pattern, username) is not None

def validate_password(password):
    """验证密码强度"""
    if len(password) < 8:
        return False, "密码至少需要8位字符"
    if not re.search(r'[a-zA-Z]', password):
        return False, "密码必须包含字母"
    if not re.search(r'[0-9]', password):
        return False, "密码必须包含数字"
    return True, "密码有效"

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'{field}是必填字段',
                    'code': 400
                }), 400
        
        username = data['username'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        display_name = data.get('display_name', username)
        
        # 验证格式
        if not validate_username(username):
            return jsonify({
                'success': False,
                'error': '用户名只能包含字母、数字、下划线，长度3-50字符',
                'code': 400
            }), 400
        
        if not validate_email(email):
            return jsonify({
                'success': False,
                'error': '邮箱格式不正确',
                'code': 400
            }), 400
        
        is_valid, msg = validate_password(password)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': msg,
                'code': 400
            }), 400
        
        # 检查用户名和邮箱是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'error': '用户名已存在',
                'code': 409
            }), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'error': '邮箱已被注册',
                'code': 409
            }), 409
        
        # 创建新用户
        user = User(
            username=username,
            email=email,
            display_name=display_name
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # 生成JWT token
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'token': access_token
            },
            'message': '注册成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'注册失败：{str(e)}',
            'code': 500
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'error': '用户名和密码不能为空',
                'code': 400
            }), 400
        
        # 查找用户（支持用户名或邮箱登录）
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user or not user.check_password(password):
            return jsonify({
                'success': False,
                'error': '用户名或密码错误',
                'code': 401
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': '账户已被禁用',
                'code': 403
            }), 403
        
        # 生成JWT token
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'token': access_token
            },
            'message': '登录成功',
            'code': 200
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'登录失败：{str(e)}',
            'code': 500
        }), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前用户信息"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': '用户不存在',
                'code': 404
            }), 404
        
        return jsonify({
            'success': True,
            'data': user.to_dict(include_sensitive=True),
            'message': '获取用户信息成功',
            'code': 200
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取用户信息失败：{str(e)}',
            'code': 500
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新用户信息"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': '用户不存在',
                'code': 404
            }), 404
        
        data = request.get_json()
        
        # 更新允许修改的字段
        if 'display_name' in data:
            user.display_name = data['display_name']
        if 'bio' in data:
            user.bio = data['bio']
        if 'avatar_url' in data:
            user.avatar_url = data['avatar_url']
        
        # 如果要修改邮箱，需要验证格式和唯一性
        if 'email' in data:
            new_email = data['email'].strip().lower()
            if not validate_email(new_email):
                return jsonify({
                    'success': False,
                    'error': '邮箱格式不正确',
                    'code': 400
                }), 400
            
            if new_email != user.email and User.query.filter_by(email=new_email).first():
                return jsonify({
                    'success': False,
                    'error': '邮箱已被使用',
                    'code': 409
                }), 409
            
            user.email = new_email
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict(include_sensitive=True),
            'message': '更新成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'更新失败：{str(e)}',
            'code': 500
        }), 500

