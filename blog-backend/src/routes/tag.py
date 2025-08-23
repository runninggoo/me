from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, Tag, TagRelation, User
from sqlalchemy import or_

tag_bp = Blueprint('tag', __name__)

@tag_bp.route('', methods=['GET'])
def get_tags():
    """获取标签列表"""
    try:
        # 查询参数
        user_id = request.args.get('user_id', type=int)
        parent_id = request.args.get('parent_id', type=int)
        search = request.args.get('search', '').strip()
        
        # 构建查询
        query = Tag.query
        
        # 用户筛选
        if user_id:
            query = query.filter(Tag.user_id == user_id)
        
        # 父标签筛选
        if parent_id:
            # 查找指定父标签的子标签
            child_tag_ids = db.session.query(TagRelation.child_tag_id).filter(
                TagRelation.parent_tag_id == parent_id
            ).subquery()
            query = query.filter(Tag.id.in_(child_tag_ids))
        
        # 搜索筛选
        if search:
            query = query.filter(
                or_(
                    Tag.name.contains(search),
                    Tag.description.contains(search)
                )
            )
        
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

@tag_bp.route('/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    """获取标签详情"""
    try:
        tag = Tag.query.get(tag_id)
        
        if not tag:
            return jsonify({
                'success': False,
                'error': '标签不存在',
                'code': 404
            }), 404
        
        # 获取父标签和子标签
        parent_relations = TagRelation.query.filter_by(child_tag_id=tag_id).all()
        child_relations = TagRelation.query.filter_by(parent_tag_id=tag_id).all()
        
        tag_data = tag.to_dict()
        tag_data['parent_tags'] = [rel.parent_tag.to_dict() for rel in parent_relations]
        tag_data['child_tags'] = [rel.child_tag.to_dict() for rel in child_relations]
        
        return jsonify({
            'success': True,
            'data': tag_data,
            'message': '获取标签成功',
            'code': 200
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取标签失败：{str(e)}',
            'code': 500
        }), 500

@tag_bp.route('', methods=['POST'])
@jwt_required()
def create_tag():
    """创建标签"""
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
        
        # 处理父标签关系
        parent_tag_ids = data.get('parent_tags', [])
        for parent_tag_id in parent_tag_ids:
            # 验证父标签存在且属于当前用户
            parent_tag = Tag.query.filter_by(id=parent_tag_id, user_id=user_id).first()
            if not parent_tag:
                continue
            
            # 验证DAG
            is_valid, msg = TagRelation.validate_dag(user_id, parent_tag_id, tag.id)
            if not is_valid:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'error': f'标签关系错误：{msg}',
                    'code': 400
                }), 400
            
            # 创建关系
            relation = TagRelation(
                parent_tag_id=parent_tag_id,
                child_tag_id=tag.id,
                user_id=user_id
            )
            db.session.add(relation)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': tag.to_dict(),
            'message': '创建标签成功',
            'code': 201
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'创建标签失败：{str(e)}',
            'code': 500
        }), 500

@tag_bp.route('/<int:tag_id>', methods=['PUT'])
@jwt_required()
def update_tag(tag_id):
    """更新标签"""
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
                'error': '无权修改此标签',
                'code': 403
            }), 403
        
        data = request.get_json()
        
        # 更新基本字段
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
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': tag.to_dict(),
            'message': '更新标签成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'更新标签失败：{str(e)}',
            'code': 500
        }), 500

@tag_bp.route('/<int:tag_id>', methods=['DELETE'])
@jwt_required()
def delete_tag(tag_id):
    """删除标签"""
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
        
        # 删除相关的标签关系
        TagRelation.query.filter(
            or_(
                TagRelation.parent_tag_id == tag_id,
                TagRelation.child_tag_id == tag_id
            )
        ).delete()
        
        db.session.delete(tag)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '删除标签成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'删除标签失败：{str(e)}',
            'code': 500
        }), 500

@tag_bp.route('/graph', methods=['GET'])
def get_tag_graph():
    """获取标签关系图"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': '用户ID不能为空',
                'code': 400
            }), 400
        
        # 获取用户的所有标签
        tags = Tag.query.filter_by(user_id=user_id).all()
        
        # 获取标签关系
        relations = TagRelation.query.filter_by(user_id=user_id).all()
        
        # 构建图结构
        graph_data = {
            'nodes': [tag.to_dict() for tag in tags],
            'edges': [relation.to_dict() for relation in relations]
        }
        
        return jsonify({
            'success': True,
            'data': graph_data,
            'message': '获取标签关系图成功',
            'code': 200
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取标签关系图失败：{str(e)}',
            'code': 500
        }), 500

@tag_bp.route('/validate-relation', methods=['POST'])
@jwt_required()
def validate_tag_relation():
    """验证标签关系"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        parent_tag_id = data.get('parent_tag_id')
        child_tag_id = data.get('child_tag_id')
        
        if not parent_tag_id or not child_tag_id:
            return jsonify({
                'success': False,
                'error': '父标签ID和子标签ID不能为空',
                'code': 400
            }), 400
        
        # 验证标签存在且属于当前用户
        parent_tag = Tag.query.filter_by(id=parent_tag_id, user_id=user_id).first()
        child_tag = Tag.query.filter_by(id=child_tag_id, user_id=user_id).first()
        
        if not parent_tag or not child_tag:
            return jsonify({
                'success': False,
                'error': '标签不存在或无权访问',
                'code': 404
            }), 404
        
        # 验证DAG
        is_valid, msg = TagRelation.validate_dag(user_id, parent_tag_id, child_tag_id)
        
        return jsonify({
            'success': True,
            'data': {
                'is_valid': is_valid,
                'message': msg
            },
            'message': '验证完成',
            'code': 200
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'验证失败：{str(e)}',
            'code': 500
        }), 500

@tag_bp.route('/relations', methods=['POST'])
@jwt_required()
def create_tag_relation():
    """创建标签关系"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        parent_tag_id = data.get('parent_tag_id')
        child_tag_id = data.get('child_tag_id')
        
        if not parent_tag_id or not child_tag_id:
            return jsonify({
                'success': False,
                'error': '父标签ID和子标签ID不能为空',
                'code': 400
            }), 400
        
        # 验证标签存在且属于当前用户
        parent_tag = Tag.query.filter_by(id=parent_tag_id, user_id=user_id).first()
        child_tag = Tag.query.filter_by(id=child_tag_id, user_id=user_id).first()
        
        if not parent_tag or not child_tag:
            return jsonify({
                'success': False,
                'error': '标签不存在或无权访问',
                'code': 404
            }), 404
        
        # 检查关系是否已存在
        existing_relation = TagRelation.query.filter_by(
            parent_tag_id=parent_tag_id,
            child_tag_id=child_tag_id
        ).first()
        
        if existing_relation:
            return jsonify({
                'success': False,
                'error': '标签关系已存在',
                'code': 409
            }), 409
        
        # 验证DAG
        is_valid, msg = TagRelation.validate_dag(user_id, parent_tag_id, child_tag_id)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': msg,
                'code': 400
            }), 400
        
        # 创建关系
        relation = TagRelation(
            parent_tag_id=parent_tag_id,
            child_tag_id=child_tag_id,
            user_id=user_id
        )
        
        db.session.add(relation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': relation.to_dict(),
            'message': '创建标签关系成功',
            'code': 201
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'创建标签关系失败：{str(e)}',
            'code': 500
        }), 500

@tag_bp.route('/relations/<int:relation_id>', methods=['DELETE'])
@jwt_required()
def delete_tag_relation(relation_id):
    """删除标签关系"""
    try:
        user_id = get_jwt_identity()
        relation = TagRelation.query.get(relation_id)
        
        if not relation:
            return jsonify({
                'success': False,
                'error': '标签关系不存在',
                'code': 404
            }), 404
        
        if relation.user_id != user_id:
            return jsonify({
                'success': False,
                'error': '无权删除此标签关系',
                'code': 403
            }), 403
        
        db.session.delete(relation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '删除标签关系成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'删除标签关系失败：{str(e)}',
            'code': 500
        }), 500

