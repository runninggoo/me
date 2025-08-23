from src.models.user import db
from datetime import datetime

# 关联表定义
article_tags = db.Table('article_tags',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id'), nullable=False),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), nullable=False),
    db.Column('created_at', db.DateTime, default=datetime.utcnow),
    db.UniqueConstraint('article_id', 'tag_id', name='unique_article_tag')
)

roadmap_tags = db.Table('roadmap_tags',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('roadmap_id', db.Integer, db.ForeignKey('roadmaps.id'), nullable=False),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), nullable=False),
    db.Column('created_at', db.DateTime, default=datetime.utcnow),
    db.UniqueConstraint('roadmap_id', 'tag_id', name='unique_roadmap_tag')
)

mindmap_tags = db.Table('mindmap_tags',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('mindmap_id', db.Integer, db.ForeignKey('mindmaps.id'), nullable=False),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), nullable=False),
    db.Column('created_at', db.DateTime, default=datetime.utcnow),
    db.UniqueConstraint('mindmap_id', 'tag_id', name='unique_mindmap_tag')
)

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#1677ff')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 唯一约束：同一用户下标签名不能重复
    __table_args__ = (
        db.UniqueConstraint('user_id', 'name', name='unique_user_tag'),
        db.Index('idx_tags_user_id', 'user_id'),
    )
    
    # 关系
    author = db.relationship('User', backref='tags', lazy=True)
    
    def __repr__(self):
        return f'<Tag {self.name}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'author': self.author.to_dict() if self.author else None
        }

class TagRelation(db.Model):
    __tablename__ = 'tag_relations'
    
    id = db.Column(db.Integer, primary_key=True)
    parent_tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    child_tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    parent_tag = db.relationship('Tag', foreign_keys=[parent_tag_id], backref='child_relations')
    child_tag = db.relationship('Tag', foreign_keys=[child_tag_id], backref='parent_relations')
    
    # 唯一约束和索引
    __table_args__ = (
        db.UniqueConstraint('parent_tag_id', 'child_tag_id', name='unique_relation'),
        db.Index('idx_tag_relations_parent_tag', 'parent_tag_id'),
        db.Index('idx_tag_relations_child_tag', 'child_tag_id'),
        db.Index('idx_tag_relations_user_id', 'user_id'),
    )
    
    def __repr__(self):
        return f'<TagRelation {self.parent_tag_id} -> {self.child_tag_id}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'parent_tag_id': self.parent_tag_id,
            'child_tag_id': self.child_tag_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'parent_tag': self.parent_tag.to_dict() if self.parent_tag else None,
            'child_tag': self.child_tag.to_dict() if self.child_tag else None
        }
    
    @staticmethod
    def validate_dag(user_id, parent_tag_id, child_tag_id):
        """验证添加关系后是否仍为有向无环图"""
        if parent_tag_id == child_tag_id:
            return False, "标签不能关联自己"
        
        # 检查是否会形成循环：从child_tag开始，看能否到达parent_tag
        visited = set()
        
        def has_path(start_id, target_id):
            if start_id == target_id:
                return True
            if start_id in visited:
                return False
            visited.add(start_id)
            
            # 查找从start_id出发的所有子标签
            relations = TagRelation.query.filter_by(
                user_id=user_id, 
                parent_tag_id=start_id
            ).all()
            
            for relation in relations:
                if has_path(relation.child_tag_id, target_id):
                    return True
            return False
        
        if has_path(child_tag_id, parent_tag_id):
            return False, "添加此关系会形成循环"
        
        return True, "关系有效"

