from src.models.user import db
from datetime import datetime
import json

class Mindmap(db.Model):
    __tablename__ = 'mindmaps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)  # Simple Mind Map JSON格式
    status = db.Column(db.Enum('draft', 'published', 'archived', name='mindmap_status'), default='draft')
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime, nullable=True)
    
    # 关系
    tags = db.relationship('Tag', secondary='mindmap_tags', backref='mindmaps', lazy=True)
    linked_articles = db.relationship('Article', backref='linked_mindmap', lazy=True)
    
    def __repr__(self):
        return f'<Mindmap {self.title}>'
    
    def set_content(self, content_dict):
        """设置内容（将字典转换为JSON字符串）"""
        self.content = json.dumps(content_dict, ensure_ascii=False)
    
    def get_content(self):
        """获取内容（将JSON字符串转换为字典）"""
        try:
            return json.loads(self.content) if self.content else {}
        except json.JSONDecodeError:
            return {}
    
    def publish(self):
        """发布思维导图"""
        self.status = 'published'
        self.published_at = datetime.utcnow()
    
    def to_dict(self, include_content=True):
        """转换为字典格式"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'view_count': self.view_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'author': self.author.to_dict() if self.author else None,
            'tags': [tag.to_dict() for tag in self.tags] if self.tags else []
        }
        
        if include_content:
            data['content'] = self.get_content()
            
        return data

