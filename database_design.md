# 个人博客系统数据库设计

## 数据库概述

本系统使用MySQL数据库，支持用户创建和管理文章、路线图、思维导图，并通过标签系统进行内容组织。

## 表结构设计

### 1. 用户表 (users)

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    avatar_url VARCHAR(255),
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

### 2. 文章表 (articles)

```sql
CREATE TABLE articles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content LONGTEXT NOT NULL,  -- TipTap编辑器的JSON格式内容
    content_html LONGTEXT,      -- 渲染后的HTML内容（用于展示）
    excerpt TEXT,               -- 文章摘要
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    is_tag_article BOOLEAN DEFAULT FALSE,  -- 是否为标签文章
    roadmap_id INT NULL,        -- 关联的路线图ID
    mindmap_id INT NULL,        -- 关联的思维导图ID
    view_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    published_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (roadmap_id) REFERENCES roadmaps(id) ON DELETE SET NULL,
    FOREIGN KEY (mindmap_id) REFERENCES mindmaps(id) ON DELETE SET NULL,
    INDEX idx_user_status (user_id, status),
    INDEX idx_published_at (published_at),
    INDEX idx_is_tag_article (is_tag_article)
);
```

### 3. 路线图表 (roadmaps)

```sql
CREATE TABLE roadmaps (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    content LONGTEXT NOT NULL,  -- Vue Flow的JSON格式数据
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    view_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    published_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_status (user_id, status),
    INDEX idx_published_at (published_at)
);
```

### 4. 思维导图表 (mindmaps)

```sql
CREATE TABLE mindmaps (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    content LONGTEXT NOT NULL,  -- Simple Mind Map的JSON格式数据
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    view_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    published_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_status (user_id, status),
    INDEX idx_published_at (published_at)
);
```

### 5. 标签表 (tags)

```sql
CREATE TABLE tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#1677ff',  -- 标签颜色（十六进制）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_tag (user_id, name),
    INDEX idx_user_id (user_id)
);
```

### 6. 标签关系表 (tag_relations)

用于实现标签的有向无环图结构：

```sql
CREATE TABLE tag_relations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    parent_tag_id INT NOT NULL,
    child_tag_id INT NOT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    FOREIGN KEY (child_tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_relation (parent_tag_id, child_tag_id),
    INDEX idx_parent_tag (parent_tag_id),
    INDEX idx_child_tag (child_tag_id),
    INDEX idx_user_id (user_id)
);
```

### 7. 文章标签关联表 (article_tags)

```sql
CREATE TABLE article_tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    article_id INT NOT NULL,
    tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    UNIQUE KEY unique_article_tag (article_id, tag_id),
    INDEX idx_article_id (article_id),
    INDEX idx_tag_id (tag_id)
);
```

### 8. 路线图标签关联表 (roadmap_tags)

```sql
CREATE TABLE roadmap_tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    roadmap_id INT NOT NULL,
    tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    UNIQUE KEY unique_roadmap_tag (roadmap_id, tag_id),
    INDEX idx_roadmap_id (roadmap_id),
    INDEX idx_tag_id (tag_id)
);
```

### 9. 思维导图标签关联表 (mindmap_tags)

```sql
CREATE TABLE mindmap_tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mindmap_id INT NOT NULL,
    tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mindmap_id) REFERENCES mindmaps(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    UNIQUE KEY unique_mindmap_tag (mindmap_id, tag_id),
    INDEX idx_mindmap_id (mindmap_id),
    INDEX idx_tag_id (tag_id)
);
```

### 10. 上传文件表 (uploads)

```sql
CREATE TABLE uploads (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);
```

## 数据库约束和规则

### 标签有向无环图验证

为了确保标签关系形成有向无环图，需要在应用层实现以下验证逻辑：

1. **循环检测**：在添加新的标签关系前，检查是否会形成循环
2. **深度限制**：限制标签层级深度，避免过深的嵌套
3. **关系验证**：确保父子标签都属于同一用户

### 数据完整性约束

1. **用户数据隔离**：所有用户数据通过user_id进行隔离
2. **软删除支持**：重要数据支持软删除（通过status字段）
3. **级联删除**：用户删除时，相关数据自动删除
4. **唯一性约束**：防止重复数据（如用户名、邮箱、标签名等）

## 索引优化

1. **查询优化**：为常用查询字段添加索引
2. **复合索引**：为多字段查询添加复合索引
3. **外键索引**：为所有外键字段添加索引

## 数据类型说明

1. **JSON内容存储**：编辑器内容以JSON格式存储，便于前端直接使用
2. **HTML内容缓存**：为文章生成HTML版本，提高展示性能
3. **时间戳管理**：统一使用TIMESTAMP类型，支持自动更新
4. **状态管理**：使用ENUM类型管理内容状态

