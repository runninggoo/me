from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, Upload, User
import os
import uuid
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_filename(original_filename):
    """生成唯一的文件名"""
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    return unique_filename

@upload_bp.route('/image', methods=['POST'])
@jwt_required()
def upload_image():
    """上传图片"""
    try:
        user_id = get_jwt_identity()
        
        # 检查文件是否存在
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '没有选择文件',
                'code': 400
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '没有选择文件',
                'code': 400
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': '不支持的文件格式，只支持：png, jpg, jpeg, gif, webp',
                'code': 400
            }), 400
        
        # 生成唯一文件名
        original_filename = secure_filename(file.filename)
        filename = generate_filename(original_filename)
        
        # 保存文件
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # 获取文件信息
        file_size = os.path.getsize(file_path)
        mime_type = file.content_type or 'image/jpeg'
        
        # 保存到数据库
        upload_record = Upload(
            user_id=user_id,
            filename=filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type
        )
        
        db.session.add(upload_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': upload_record.to_dict(),
            'message': '上传成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'上传失败：{str(e)}',
            'code': 500
        }), 500

@upload_bp.route('', methods=['GET'])
@jwt_required()
def get_uploads():
    """获取上传文件列表"""
    try:
        user_id = get_jwt_identity()
        
        # 查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        # 构建查询
        query = Upload.query.filter_by(user_id=user_id)
        query = query.order_by(Upload.created_at.desc())
        
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        uploads = [upload.to_dict() for upload in pagination.items]
        
        return jsonify({
            'success': True,
            'data': {
                'uploads': uploads,
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            },
            'message': '获取上传文件列表成功',
            'code': 200
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取上传文件列表失败：{str(e)}',
            'code': 500
        }), 500

@upload_bp.route('/<int:upload_id>', methods=['DELETE'])
@jwt_required()
def delete_upload(upload_id):
    """删除上传文件"""
    try:
        user_id = get_jwt_identity()
        upload_record = Upload.query.get(upload_id)
        
        if not upload_record:
            return jsonify({
                'success': False,
                'error': '文件不存在',
                'code': 404
            }), 404
        
        if upload_record.user_id != user_id:
            return jsonify({
                'success': False,
                'error': '无权删除此文件',
                'code': 403
            }), 403
        
        # 删除物理文件
        try:
            if os.path.exists(upload_record.file_path):
                os.remove(upload_record.file_path)
        except Exception as e:
            print(f"删除物理文件失败：{e}")
        
        # 删除数据库记录
        db.session.delete(upload_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '删除文件成功',
            'code': 200
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'删除文件失败：{str(e)}',
            'code': 500
        }), 500

