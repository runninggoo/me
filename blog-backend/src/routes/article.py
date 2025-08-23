from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.models import db, Article, User, Tag
from sqlalchemy import or_, and_
import json

article_bp = Blueprint('article', __name__)

@article_bp.route('', methods=['GET'])
def get_articles():
    """获取文章列表"""
    try:
        # 查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        status = request.args.get('status', 'published')
        tag_id = request.args.get('tag_id', type=int)
        search = request.args.get('search', '').strip()
        user_id = request.args.get('user_id', type=int)
        
        # 构建查询
        query = Article.query
        
        # 状态筛选
        if status:
            query = query.filter(Article.status == status)
        
        # 用户筛选
        if user_id:
            query = query.filter(Article.user_id == user_id)
        
        # 标签筛选
        if tag_id:
            query = query.filter(Article.tags.any(Tag.id == tag_id))
        
        # 搜索筛选
        if search:
            query = query.filter(
                or_(
                    Article.title.contains(search),
                    Article.excerpt.contains(search)
                )
            )
        
        # 排序和分页
        query = query.order_by(Article.published_at.desc(), Article.created_at.desc())
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        articles = [article.to_dict(include_content=False) for article in pagination.items]
        
        return jsonify({
            'success': True,
            'data': {
                'articles': articles,
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            },
            'message': '获取文章列表成功',
            'code': 200
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取文章列表失败：{str(e)}',
            'code': 500
        }), 500

@article_bp.route('/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """获取文章详情"""
    try:
        article = Article.query.get(article_id)
        
        if not article:
            return jsonify({
                'success': False,
                'error': '文章不存在',
                'code': 404
            }), 404
        
        # 检查是否有JWT token
        current_user_id = None
        try:
            from flask_jwt_extended import verify_jwt_in_request
            verify_jwt_in_request(optional=True)
            current_user_id = int(get_jwt_identity())
            if current_user_id:
                current_user_id = int(current_user_id)
        except:
            pass
        
        # 只有已发布的文章或作者本人可以查看
        if article.status != 'published' and article.user_id != current_user_id:
            return jsonify({
                'success': False,
                'error': '无权访问此文章',
                'code': 403
            }), 403
        
        # 增加浏览量（非作者访问时）
        if current_user_id != article.user_id:
            article.view_count += 1
            db.session.commit()
        
        return jsonify({
            'success': True,
            'data': article.to_dict(),
            'message': '获取文章成功',
            'code': 200
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取文章失败：{str(e)}',
            'code': 500
        }), 500

@article_bp.route('', methods=['POST'])
@jwt_required()
def create_article():
    """创建文章"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('title'):
            return jsonify({
                'success': False,
                'error': '标题不能为空',
                'code': 400
            }), 400
        
        if not data.get('content'):
            return jsonify({
                'success': False,
                'error': '内容不能为空',
                'code': 400
            }), 400
        
        # 创建文章
        article = Article(
            user_id=user_id,
            title=data['title'],
            excerpt=data.get('excerpt', ''),
            status=data.get('status', 'draft'),
            is_tag_article=data.get('is_tag_article', False),
            roadmap_id=data.get('roadmap_id'),
            mindmap_id=data.get('mindmap_id')
        )
        
        # 处理内容
        content = data['content']
        if isinstance(content, str):
            try:
                # 如果是JSON字符串，尝试解析
                content_dict = json.loads(content)
                article.set_content(content_dict)
            except json.JSONDecodeError:
                # 如果不是JSON，直接作为文本内容
                article.set_content({'type': 'doc', 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': content}]}]})
        elif isinstance(content, dict):
            # 如果已经是字典，直接设置
            article.set_content(content)
        else:
            # 其他情况，创建默认结构
            article.set_content({'type': 'doc', 'content': []})
        
        # 如果是发布状态，设置发布时间
        if article.status == 'published':
            article.publish()
        
        db.session.add(article)
        db.session.flush()  # 获取文章ID
        
        # 处理标签关联
        tag_ids = data.get('tags', [])
        if tag_ids:
            tags = Tag.query.filter(
                and_(Tag.id.in_(tag_ids), Tag.user_id == user_id)
            ).all()
            article.tags = tags
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': article.to_dict(),
            'message': '创建文章成功',
            'code': 201
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'创建文章失败：{str(e)}',
            'code': 500
        }), 500

@article_bp.route('/<int:article_id>', methods=['PUT'])
@jwt_required()
def update_article(article_id):
    """更新文章"""
    try:
        user_id = int(get_jwt_identity())
        article = Article.query.get(article_id)
        
        if not article:
            return jsonify({
                'success': False,
                'error': '文章不存在',
                'code': 404
            }), 404
        
        if article.user_id != user_id:
            return jsonify({
                'success': False,
                'error': '无权修改此文章',
                'code': 403
            }), 403
        
        data = request.get_json()
        
        # 更新字段
        if 'title' in data:
            article.title = data['title']
        if 'content' in data:
            content = data['content']
            if isinstance(content, str):
                try:
                    # 如果是JSON字符串，尝试解析
                    content_dict = json.loads(content)
                    article.set_content(content_dict)
                except json.JSONDecodeError:
                    # 如果不是JSON，直接作为文本内容
                    article.set_content({'type': 'doc', 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': content}]}]})
            elif isinstance(content, dict):
                # 如果已经是字典，直接设置
                article.set_content(content)
            else:
                # 其他情况，创建默认结构
                article.set_content({'type': 'doc', 'content': []})
        if 'excerpt' in data:
            article.excerpt = data['excerpt']
        if 'status' in data:
            old_status = article.status
            article.status = data['status']
            # 如果从草稿变为发布，设置发布时间
            if old_status != 'published' and article.status == 'published':
                article.publish()
        if 'is_tag_article' in data:
            article.is_tag_article = data['is_tag_article']
        if 'roadmap_id' in data:
            article.roadmap_id = data['roadmap_id']
        if 'mindmap_id' in data:
            article.mindmap_id = data['mindmap_id']
        
        # 处理标签关联
        if 'tags' in data:
            tag_ids = data['tags']
            tags = Tag.query.filter(
                and_(Tag.id.in_(tag_ids), Tag.user_id == user_id)
            ).all() if tag_ids else []
            article.tags = tags
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': article.to_dict(),
            'message': '更新文章成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'更新文章失败：{str(e)}',
            'code': 500
        }), 500

@article_bp.route('/<int:article_id>', methods=['DELETE'])
@jwt_required()
def delete_article(article_id):
    """删除文章"""
    try:
        user_id = int(get_jwt_identity())
        article = Article.query.get(article_id)
        
        if not article:
            return jsonify({
                'success': False,
                'error': '文章不存在',
                'code': 404
            }), 404
        
        if article.user_id != user_id:
            return jsonify({
                'success': False,
                'error': '无权删除此文章',
                'code': 403
            }), 403
        
        db.session.delete(article)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '删除文章成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'删除文章失败：{str(e)}',
            'code': 500
        }), 500

@article_bp.route('/<int:article_id>/publish', methods=['POST'])
@jwt_required()
def publish_article(article_id):
    """发布文章"""
    try:
        user_id = int(get_jwt_identity())
        article = Article.query.get(article_id)
        
        if not article:
            return jsonify({
                'success': False,
                'error': '文章不存在',
                'code': 404
            }), 404
        
        if article.user_id != user_id:
            return jsonify({
                'success': False,
                'error': '无权发布此文章',
                'code': 403
            }), 403
        
        article.publish()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': article.to_dict(),
            'message': '发布文章成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'发布文章失败：{str(e)}',
            'code': 500
        }), 500

