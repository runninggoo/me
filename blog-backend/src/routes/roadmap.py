from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, Roadmap, User, Tag
from sqlalchemy import or_, and_

roadmap_bp = Blueprint('roadmap', __name__)

@roadmap_bp.route('', methods=['GET'])
def get_roadmaps():
    """获取路线图列表"""
    try:
        # 查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        status = request.args.get('status', 'published')
        tag_id = request.args.get('tag_id', type=int)
        search = request.args.get('search', '').strip()
        user_id = request.args.get('user_id', type=int)
        
        # 构建查询
        query = Roadmap.query
        
        # 状态筛选
        if status:
            query = query.filter(Roadmap.status == status)
        
        # 用户筛选
        if user_id:
            query = query.filter(Roadmap.user_id == user_id)
        
        # 标签筛选
        if tag_id:
            query = query.filter(Roadmap.tags.any(Tag.id == tag_id))
        
        # 搜索筛选
        if search:
            query = query.filter(
                or_(
                    Roadmap.title.contains(search),
                    Roadmap.description.contains(search)
                )
            )
        
        # 排序和分页
        query = query.order_by(Roadmap.published_at.desc(), Roadmap.created_at.desc())
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        roadmaps = [roadmap.to_dict(include_content=False) for roadmap in pagination.items]
        
        return jsonify({
            'success': True,
            'data': {
                'roadmaps': roadmaps,
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            },
            'message': '获取路线图列表成功',
            'code': 200
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取路线图列表失败：{str(e)}',
            'code': 500
        }), 500

@roadmap_bp.route('/<int:roadmap_id>', methods=['GET'])
@jwt_required()
def get_roadmap(roadmap_id):
    """获取路线图详情"""
    try:
        roadmap = Roadmap.query.get(roadmap_id)
        
        if not roadmap:
            return jsonify({
                'success': False,
                'error': '路线图不存在',
                'code': 404
            }), 404
        
        # 只有已发布的路线图或作者本人可以查看
        current_user_id = None
        try:
            current_user_id = int(get_jwt_identity())
            print(get_jwt_identity())
        except:
            pass
        
        if roadmap.status != 'published' and roadmap.user_id != current_user_id:
            return jsonify({
                'success': False,
                'error': '无权访问此路线图'+str(roadmap.user_id)+str(current_user_id),
                'code': 403
            }), 403
        
        # 增加浏览量（非作者访问时）
        if current_user_id != roadmap.user_id:
            roadmap.view_count += 1
            db.session.commit()
        
        return jsonify({
            'success': True,
            'data': roadmap.to_dict(),
            'message': '获取路线图成功',
            'code': 200
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取路线图失败：{str(e)}',
            'code': 500
        }), 500

@roadmap_bp.route('', methods=['POST'])
@jwt_required()
def create_roadmap():
    """创建路线图"""
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
        
        # 创建路线图
        roadmap = Roadmap(
            user_id=user_id,
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'draft')
        )
        
        roadmap.set_content(data['content'])
        
        # 如果是发布状态，设置发布时间
        if roadmap.status == 'published':
            roadmap.publish()
        
        db.session.add(roadmap)
        db.session.flush()  # 获取路线图ID
        
        # 处理标签关联
        tag_ids = data.get('tags', [])
        if tag_ids:
            tags = Tag.query.filter(
                and_(Tag.id.in_(tag_ids), Tag.user_id == user_id)
            ).all()
            roadmap.tags = tags
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': roadmap.to_dict(),
            'message': '创建路线图成功',
            'code': 201
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'创建路线图失败：{str(e)}',
            'code': 500
        }), 500

@roadmap_bp.route('/<int:roadmap_id>', methods=['PUT'])
@jwt_required()
def update_roadmap(roadmap_id):
    """更新路线图"""
    try:
        user_id = int(get_jwt_identity())
        roadmap = Roadmap.query.get(roadmap_id)
        
        if not roadmap:
            return jsonify({
                'success': False,
                'error': '路线图不存在',
                'code': 404
            }), 404
        
        if roadmap.user_id != user_id:
            return jsonify({
                'success': False,
                'error': '无权修改此路线图',
                'code': 403
            }), 403
        
        data = request.get_json()
        
        # 更新字段
        if 'title' in data:
            roadmap.title = data['title']
        if 'description' in data:
            roadmap.description = data['description']
        if 'content' in data:
            roadmap.set_content(data['content'])
        if 'status' in data:
            old_status = roadmap.status
            roadmap.status = data['status']
            # 如果从草稿变为发布，设置发布时间
            if old_status != 'published' and roadmap.status == 'published':
                roadmap.publish()
        
        # 处理标签关联
        if 'tags' in data:
            tag_ids = data['tags']
            tags = Tag.query.filter(
                and_(Tag.id.in_(tag_ids), Tag.user_id == user_id)
            ).all() if tag_ids else []
            roadmap.tags = tags
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': roadmap.to_dict(),
            'message': '更新路线图成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'更新路线图失败：{str(e)}',
            'code': 500
        }), 500

@roadmap_bp.route('/<int:roadmap_id>', methods=['DELETE'])
@jwt_required()
def delete_roadmap(roadmap_id):
    """删除路线图"""
    try:
        user_id = int(get_jwt_identity())
        roadmap = Roadmap.query.get(roadmap_id)
        
        if not roadmap:
            return jsonify({
                'success': False,
                'error': '路线图不存在',
                'code': 404
            }), 404
        
        if roadmap.user_id != user_id:
            return jsonify({
                'success': False,
                'error': '无权删除此路线图',
                'code': 403
            }), 403
        
        db.session.delete(roadmap)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '删除路线图成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'删除路线图失败：{str(e)}',
            'code': 500
        }), 500

