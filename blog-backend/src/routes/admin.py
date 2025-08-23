from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from src.models import db, User, Tag, Article
from functools import wraps
import json

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """管理员权限装饰器"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            return jsonify({
                'success': False,
                'error': '需要管理员权限',
                'code': 403
            }), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/register', methods=['POST'])
def admin_register():
    """管理员注册"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'{field}不能为空',
                    'code': 400
                }), 400
        
        username = data['username'].strip()
        email = data['email'].strip()
        password = data['password']
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'error': '用户名已存在',
                'code': 409
            }), 409
        
        # 检查邮箱是否已存在
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'error': '邮箱已存在',
                'code': 409
            }), 409
        
        # 创建管理员用户
        admin_user = User(
            username=username,
            email=email,
            display_name=data.get('display_name', username),
            is_admin=True
        )
        admin_user.set_password(password)
        
        db.session.add(admin_user)
        db.session.commit()
        
        # 生成访问令牌
        access_token = create_access_token(identity=str(admin_user.id))
        
        return jsonify({
            'success': True,
            'data': {
                'user': admin_user.to_dict(),
                'access_token': access_token
            },
            'message': '管理员注册成功',
            'code': 201
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'注册失败：{str(e)}',
            'code': 500
        }), 500

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """管理员登录"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': '用户名和密码不能为空',
                'code': 400
            }), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # 查找用户
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({
                'success': False,
                'error': '用户名或密码错误',
                'code': 401
            }), 401
        
        if not user.is_admin:
            return jsonify({
                'success': False,
                'error': '该账户不是管理员',
                'code': 403
            }), 403
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': '账户已被禁用',
                'code': 403
            }), 403
        
        # 生成访问令牌
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'access_token': access_token
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

@admin_bp.route('/tags', methods=['GET'])
@admin_required
def get_admin_tags():
    """获取所有标签（管理员）"""
    try:
        user_id = get_jwt_identity()
        
        # 查询参数
        search = request.args.get('search', '').strip()
        
        # 构建查询 - 管理员可以看到自己创建的标签
        query = Tag.query.filter_by(user_id=user_id)
        
        # 搜索筛选
        if search:
            query = query.filter(Tag.name.contains(search))
        
        # 排序
        query = query.order_by(Tag.name)
        tags = query.all()
        
        return jsonify({
            'success': True,
            'data': [tag.to_dict() for tag in tags],
            'message': '获取标签列表成功',
            'code': 200
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取标签列表失败：{str(e)}',
            'code': 500
        }), 500

@admin_bp.route('/tags', methods=['POST'])
@admin_required
def create_admin_tag():
    """创建标签文章（管理员）"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('name'):
            return jsonify({
                'success': False,
                'error': '标签名不能为空',
                'code': 400
            }), 400
        
        name = data['name'].strip()
        
        # 检查标签名是否已存在
        if Tag.query.filter_by(user_id=user_id, name=name).first():
            return jsonify({
                'success': False,
                'error': '标签名已存在',
                'code': 409
            }), 409
        
        # 创建标签
        tag = Tag(
            user_id=user_id,
            name=name,
            description=data.get('description', ''),
            color=data.get('color', '#1677ff')
        )
        
        db.session.add(tag)
        db.session.flush()  # 获取标签ID
        
        # 创建对应的标签文章
        article_content = data.get('content', {
            'type': 'doc',
            'content': [
                {
                    'type': 'heading',
                    'attrs': {'level': 1},
                    'content': [{'type': 'text', 'text': name}]
                },
                {
                    'type': 'paragraph',
                    'content': [{'type': 'text', 'text': data.get('description', '')}]
                }
            ]
        })
        
        article = Article(
            user_id=user_id,
            title=name,
            excerpt=data.get('description', ''),
            status='published',
            is_tag_article=True
        )
        
        # 处理内容
        if isinstance(article_content, str):
            try:
                content_dict = json.loads(article_content)
                article.set_content(content_dict)
            except json.JSONDecodeError:
                article.set_content({'type': 'doc', 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': article_content}]}]})
        elif isinstance(article_content, dict):
            article.set_content(article_content)
        else:
            article.set_content({'type': 'doc', 'content': []})
        
        article.publish()
        
        db.session.add(article)
        db.session.flush()
        
        # 关联标签和文章
        article.tags = [tag]
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'tag': tag.to_dict(),
                'article': article.to_dict()
            },
            'message': '创建标签文章成功',
            'code': 201
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'创建标签文章失败：{str(e)}',
            'code': 500
        }), 500

@admin_bp.route('/tags/<int:tag_id>', methods=['PUT'])
@admin_required
def update_admin_tag():
    """更新标签文章（管理员）"""
    try:
        user_id = get_jwt_identity()
        tag_id = request.view_args['tag_id']
        tag = Tag.query.get(tag_id)
        
        if not tag:
            return jsonify({
                'success': False,
                'error': '标签不存在',
                'code': 404
            }), 404
        
        if tag.user_id != user_id:
            return jsonify({
                'success': False,
                'error': '无权修改此标签',
                'code': 403
            }), 403
        
        data = request.get_json()
        
        # 更新标签基本信息
        if 'name' in data:
            new_name = data['name'].strip()
            # 检查新名称是否与其他标签冲突
            existing_tag = Tag.query.filter_by(user_id=user_id, name=new_name).first()
            if existing_tag and existing_tag.id != tag_id:
                return jsonify({
                    'success': False,
                    'error': '标签名已存在',
                    'code': 409
                }), 409
            tag.name = new_name
        
        if 'description' in data:
            tag.description = data['description']
        if 'color' in data:
            tag.color = data['color']
        
        # 查找对应的标签文章
        tag_article = Article.query.filter_by(
            user_id=user_id,
            is_tag_article=True
        ).filter(Article.tags.any(Tag.id == tag_id)).first()
        
        if tag_article:
            # 更新文章标题和内容
            if 'name' in data:
                tag_article.title = data['name']
            if 'description' in data:
                tag_article.excerpt = data['description']
            if 'content' in data:
                content = data['content']
                if isinstance(content, str):
                    try:
                        content_dict = json.loads(content)
                        tag_article.set_content(content_dict)
                    except json.JSONDecodeError:
                        tag_article.set_content({'type': 'doc', 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': content}]}]})
                elif isinstance(content, dict):
                    tag_article.set_content(content)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'tag': tag.to_dict(),
                'article': tag_article.to_dict() if tag_article else None
            },
            'message': '更新标签文章成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'更新标签文章失败：{str(e)}',
            'code': 500
        }), 500

@admin_bp.route('/tags/<int:tag_id>', methods=['DELETE'])
@admin_required
def delete_admin_tag(tag_id):
    """删除标签文章（管理员）"""
    try:
        user_id = get_jwt_identity()
        tag = Tag.query.get(tag_id)
        
        if not tag:
            return jsonify({
                'success': False,
                'error': '标签不存在',
                'code': 404
            }), 404
        
        if tag.user_id != user_id:
            return jsonify({
                'success': False,
                'error': '无权删除此标签',
                'code': 403
            }), 403
        
        # 查找并删除对应的标签文章
        tag_article = Article.query.filter_by(
            user_id=user_id,
            is_tag_article=True
        ).filter(Article.tags.any(Tag.id == tag_id)).first()
        
        if tag_article:
            db.session.delete(tag_article)
        
        # 删除标签
        db.session.delete(tag)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '删除标签文章成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'删除标签文章失败：{str(e)}',
            'code': 500
        }), 500

