from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, Mindmap, User, Tag
from sqlalchemy import or_, and_

mindmap_bp = Blueprint('mindmap', __name__)

@mindmap_bp.route('', methods=['GET'])
def get_mindmaps():
    """获取思维导图列表"""
    try:
        # 查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        status = request.args.get('status', 'published')
        tag_id = request.args.get('tag_id', type=int)
        search = request.args.get('search', '').strip()
        user_id = request.args.get('user_id', type=int)
        
        # 构建查询
        query = Mindmap.query
        
        # 状态筛选
        if status:
            query = query.filter(Mindmap.status == status)
        
        # 用户筛选
        if user_id:
            query = query.filter(Mindmap.user_id == user_id)
        
        # 标签筛选
        if tag_id:
            query = query.filter(Mindmap.tags.any(Tag.id == tag_id))
        
        # 搜索筛选
        if search:
            query = query.filter(
                or_(
                    Mindmap.title.contains(search),
                    Mindmap.description.contains(search)
                )
            )
        
        # 排序和分页
        query = query.order_by(Mindmap.published_at.desc(), Mindmap.created_at.desc())
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        mindmaps = [mindmap.to_dict(include_content=False) for mindmap in pagination.items]
        
        return jsonify({
            'success': True,
            'data': {
                'mindmaps': mindmaps,
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            },
            'message': '获取思维导图列表成功',
            'code': 200
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取思维导图列表失败：{str(e)}',
            'code': 500
        }), 500

@mindmap_bp.route('/<int:mindmap_id>', methods=['GET'])
@jwt_required()
def get_mindmap(mindmap_id):
    """获取思维导图详情"""
    try:
        mindmap = Mindmap.query.get(mindmap_id)
        
        if not mindmap:
            return jsonify({
                'success': False,
                'error': '思维导图不存在',
                'code': 404
            }), 404
        
        # 只有已发布的思维导图或作者本人可以查看
        current_user_id = None
        try:
            current_user_id = int(get_jwt_identity())
        except:
            pass
        
        if mindmap.status != 'published' and mindmap.user_id != current_user_id:
            return jsonify({
                'success': False,
                'error': '无权访问此思维导图',
                'code': 403
            }), 403
        
        # 增加浏览量（非作者访问时）
        if current_user_id != mindmap.user_id:
            mindmap.view_count += 1
            db.session.commit()
        
        return jsonify({
            'success': True,
            'data': mindmap.to_dict(),
            'message': '获取思维导图成功',
            'code': 200
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取思维导图失败：{str(e)}',
            'code': 500
        }), 500

@mindmap_bp.route('', methods=['POST'])
@jwt_required()
def create_mindmap():
    """创建思维导图"""
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
        
        # 创建思维导图
        mindmap = Mindmap(
            user_id=user_id,
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'draft')
        )
        
        mindmap.set_content(data['content'])
        
        # 如果是发布状态，设置发布时间
        if mindmap.status == 'published':
            mindmap.publish()
        
        db.session.add(mindmap)
        db.session.flush()  # 获取思维导图ID
        
        # 处理标签关联
        tag_ids = data.get('tags', [])
        if tag_ids:
            tags = Tag.query.filter(
                and_(Tag.id.in_(tag_ids), Tag.user_id == user_id)
            ).all()
            mindmap.tags = tags
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': mindmap.to_dict(),
            'message': '创建思维导图成功',
            'code': 201
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'创建思维导图失败：{str(e)}',
            'code': 500
        }), 500

@mindmap_bp.route('/<int:mindmap_id>', methods=['PUT'])
@jwt_required()
def update_mindmap(mindmap_id):
    """更新思维导图"""
    try:
        user_id = int(get_jwt_identity())
        mindmap = Mindmap.query.get(mindmap_id)
        
        if not mindmap:
            return jsonify({
                'success': False,
                'error': '思维导图不存在',
                'code': 404
            }), 404
        
        if mindmap.user_id != user_id:
            return jsonify({
                'success': False,
                'error': '无权修改此思维导图',
                'code': 403
            }), 403
        
        data = request.get_json()
        
        # 更新字段
        if 'title' in data:
            mindmap.title = data['title']
        if 'description' in data:
            mindmap.description = data['description']
        if 'content' in data:
            mindmap.set_content(data['content'])
        if 'status' in data:
            old_status = mindmap.status
            mindmap.status = data['status']
            # 如果从草稿变为发布，设置发布时间
            if old_status != 'published' and mindmap.status == 'published':
                mindmap.publish()
        
        # 处理标签关联
        if 'tags' in data:
            tag_ids = data['tags']
            tags = Tag.query.filter(
                and_(Tag.id.in_(tag_ids), Tag.user_id == user_id)
            ).all() if tag_ids else []
            mindmap.tags = tags
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': mindmap.to_dict(),
            'message': '更新思维导图成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'更新思维导图失败：{str(e)}',
            'code': 500
        }), 500

@mindmap_bp.route('/<int:mindmap_id>', methods=['DELETE'])
@jwt_required()
def delete_mindmap(mindmap_id):
    """删除思维导图"""
    try:
        user_id = int(get_jwt_identity())
        mindmap = Mindmap.query.get(mindmap_id)
        
        if not mindmap:
            return jsonify({
                'success': False,
                'error': '思维导图不存在',
                'code': 404
            }), 404
        
        if mindmap.user_id != user_id:
            return jsonify({
                'success': False,
                'error': '无权删除此思维导图'+str(type(mindmap.user_id))+"!="+str(type(user_id)),
                'code': 403
            }), 403
        
        db.session.delete(mindmap)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '删除思维导图成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'删除思维导图失败：{str(e)}',
            'code': 500
        }), 500

