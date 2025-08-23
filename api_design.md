# 个人博客系统API接口设计

## API概述

本系统采用RESTful API设计，使用JSON格式进行数据交换。所有API都需要适当的身份验证和权限控制。

## 认证机制

- 使用JWT Token进行身份验证
- Token在请求头中传递：`Authorization: Bearer <token>`
- Token有效期为7天，支持刷新

## 通用响应格式

```json
{
    "success": true,
    "data": {},
    "message": "操作成功",
    "code": 200
}
```

错误响应格式：
```json
{
    "success": false,
    "error": "错误信息",
    "code": 400
}
```

## 1. 用户认证接口

### 1.1 用户注册
- **POST** `/api/auth/register`
- **请求体**：
```json
{
    "username": "string",
    "email": "string", 
    "password": "string",
    "display_name": "string"
}
```
- **响应**：
```json
{
    "success": true,
    "data": {
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "display_name": "Test User"
        },
        "token": "jwt_token_here"
    }
}
```

### 1.2 用户登录
- **POST** `/api/auth/login`
- **请求体**：
```json
{
    "username": "string",
    "password": "string"
}
```

### 1.3 获取当前用户信息
- **GET** `/api/auth/me`
- **需要认证**：是

### 1.4 更新用户信息
- **PUT** `/api/auth/profile`
- **需要认证**：是

## 2. 文章管理接口

### 2.1 获取文章列表
- **GET** `/api/articles`
- **查询参数**：
  - `page`: 页码（默认1）
  - `limit`: 每页数量（默认10）
  - `status`: 文章状态（draft/published/archived）
  - `tag_id`: 标签ID筛选
  - `search`: 搜索关键词

### 2.2 获取文章详情
- **GET** `/api/articles/{id}`

### 2.3 创建文章
- **POST** `/api/articles`
- **需要认证**：是
- **请求体**：
```json
{
    "title": "string",
    "content": {},  // TipTap JSON格式
    "excerpt": "string",
    "status": "draft|published",
    "is_tag_article": false,
    "roadmap_id": null,
    "mindmap_id": null,
    "tags": [1, 2, 3]  // 标签ID数组
}
```

### 2.4 更新文章
- **PUT** `/api/articles/{id}`
- **需要认证**：是

### 2.5 删除文章
- **DELETE** `/api/articles/{id}`
- **需要认证**：是

### 2.6 发布文章
- **POST** `/api/articles/{id}/publish`
- **需要认证**：是

## 3. 路线图管理接口

### 3.1 获取路线图列表
- **GET** `/api/roadmaps`
- **查询参数**：类似文章接口

### 3.2 获取路线图详情
- **GET** `/api/roadmaps/{id}`

### 3.3 创建路线图
- **POST** `/api/roadmaps`
- **需要认证**：是
- **请求体**：
```json
{
    "title": "string",
    "description": "string",
    "content": {},  // Vue Flow JSON格式
    "status": "draft|published",
    "tags": [1, 2, 3]
}
```

### 3.4 更新路线图
- **PUT** `/api/roadmaps/{id}`
- **需要认证**：是

### 3.5 删除路线图
- **DELETE** `/api/roadmaps/{id}`
- **需要认证**：是

## 4. 思维导图管理接口

### 4.1 获取思维导图列表
- **GET** `/api/mindmaps`

### 4.2 获取思维导图详情
- **GET** `/api/mindmaps/{id}`

### 4.3 创建思维导图
- **POST** `/api/mindmaps`
- **需要认证**：是
- **请求体**：
```json
{
    "title": "string",
    "description": "string", 
    "content": {},  // Simple Mind Map JSON格式
    "status": "draft|published",
    "tags": [1, 2, 3]
}
```

### 4.4 更新思维导图
- **PUT** `/api/mindmaps/{id}`
- **需要认证**：是

### 4.5 删除思维导图
- **DELETE** `/api/mindmaps/{id}`
- **需要认证**：是

## 5. 标签系统接口

### 5.1 获取标签列表
- **GET** `/api/tags`
- **查询参数**：
  - `parent_id`: 父标签ID（获取子标签）
  - `search`: 搜索关键词

### 5.2 获取标签详情
- **GET** `/api/tags/{id}`

### 5.3 创建标签
- **POST** `/api/tags`
- **需要认证**：是
- **请求体**：
```json
{
    "name": "string",
    "description": "string",
    "color": "#1677ff",
    "parent_tags": [1, 2]  // 父标签ID数组
}
```

### 5.4 更新标签
- **PUT** `/api/tags/{id}`
- **需要认证**：是

### 5.5 删除标签
- **DELETE** `/api/tags/{id}`
- **需要认证**：是

### 5.6 获取标签关系图
- **GET** `/api/tags/graph`
- **响应**：返回标签的有向无环图结构

### 5.7 验证标签关系
- **POST** `/api/tags/validate-relation`
- **请求体**：
```json
{
    "parent_tag_id": 1,
    "child_tag_id": 2
}
```

## 6. 文件上传接口

### 6.1 上传图片
- **POST** `/api/upload/image`
- **需要认证**：是
- **请求格式**：multipart/form-data
- **响应**：
```json
{
    "success": true,
    "data": {
        "id": 1,
        "filename": "generated_filename.jpg",
        "original_filename": "original.jpg",
        "url": "/uploads/images/generated_filename.jpg",
        "size": 1024000
    }
}
```

### 6.2 获取上传文件列表
- **GET** `/api/uploads`
- **需要认证**：是

### 6.3 删除上传文件
- **DELETE** `/api/uploads/{id}`
- **需要认证**：是

## 7. 内容关联接口

### 7.1 关联文章到路线图
- **POST** `/api/articles/{article_id}/link-roadmap`
- **请求体**：
```json
{
    "roadmap_id": 1
}
```

### 7.2 关联文章到思维导图
- **POST** `/api/articles/{article_id}/link-mindmap`
- **请求体**：
```json
{
    "mindmap_id": 1
}
```

## 8. 搜索接口

### 8.1 全局搜索
- **GET** `/api/search`
- **查询参数**：
  - `q`: 搜索关键词
  - `type`: 内容类型（article/roadmap/mindmap/all）
  - `tag_id`: 标签筛选

## 错误码定义

- `200`: 成功
- `400`: 请求参数错误
- `401`: 未认证
- `403`: 权限不足
- `404`: 资源不存在
- `409`: 资源冲突（如用户名已存在）
- `422`: 数据验证失败
- `500`: 服务器内部错误

## 权限控制

1. **公开访问**：已发布的文章、路线图、思维导图
2. **用户访问**：自己创建的所有内容（包括草稿）
3. **管理员访问**：所有内容的管理权限

## 数据验证规则

1. **用户名**：3-50字符，只能包含字母、数字、下划线
2. **邮箱**：标准邮箱格式验证
3. **密码**：最少8位，包含字母和数字
4. **标签名**：1-100字符，同一用户下不能重复
5. **标题**：1-255字符
6. **内容**：JSON格式验证

