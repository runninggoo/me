# 个人博客系统 - v0.1

基于Vue3和Flask的现代化个人博客系统，集成了富文本编辑、路线图和思维导图功能。

## 🚀 功能特性

### 用户功能
- ✅ 用户注册和登录系统
- ✅ 富文本文章编辑器（基于TipTap）
- ✅ 路线图编辑器（交互式学习路径）
- ✅ 思维导图编辑器（知识结构整理）
- ✅ 文章草稿保存和发布
- ✅ 个人仪表板管理
- ✅ 响应式设计，支持移动端

### 管理员功能
- ✅ 管理员独立登录系统
- ✅ 标签文章管理
- ✅ 用户内容审核
- ✅ 系统数据统计

### 技术特性
- ✅ JWT身份认证
- ✅ 密码加密存储
- ✅ RESTful API设计
- ✅ SQLite数据库
- ✅ CORS跨域支持
- ✅ 图片上传功能

## 🛠️ 技术栈

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 现代化构建工具
- **TailwindCSS** - 实用优先的CSS框架
- **TipTap** - 现代化富文本编辑器
- **Vue Router** - 官方路由管理器
- **Pinia** - 状态管理

### 后端
- **Flask** - 轻量级Python Web框架
- **SQLAlchemy** - Python SQL工具包
- **Flask-JWT-Extended** - JWT认证扩展
- **Flask-CORS** - 跨域资源共享
- **bcrypt** - 密码加密

## 📦 安装和运行

### 环境要求
- Node.js 16+
- Python 3.8+
- npm 或 yarn

### 后端启动
```bash
cd blog-backend
pip install -r requirements.txt
python src/main.py
```
后端将运行在 http://localhost:5001

### 前端启动
```bash
cd front
npm install
npm run dev
```
前端将运行在 http://localhost:5173

## 👤 默认账号

### 管理员账号
- 用户名: `admin`
- 密码: `admin123`
- 邮箱: `admin@example.com`

### 测试用户账号
可以通过注册页面创建新的用户账号

## 📝 使用说明

### 用户端使用
1. 访问 http://localhost:5173
2. 注册新账号或使用已有账号登录
3. 在仪表板中创建文章、路线图或思维导图
4. 使用富文本编辑器编写内容
5. 保存草稿或直接发布

### 管理员端使用
1. 访问 http://localhost:5173/admin/login
2. 使用管理员账号登录
3. 管理标签文章和用户内容
4. 查看系统统计数据

## 🗄️ 数据库设计

### 主要数据表
- `users` - 用户信息表
- `articles` - 文章内容表
- `roadmaps` - 路线图数据表
- `mindmaps` - 思维导图数据表
- `tags` - 标签管理表
- `uploads` - 文件上传记录表

### 关系设计
- 用户与内容：一对多关系
- 文章与标签：多对多关系
- 标签系统：有向无环图结构

## 🔧 API接口

### 认证接口
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

### 内容接口
- `GET /api/articles` - 获取文章列表
- `POST /api/articles` - 创建新文章
- `PUT /api/articles/:id` - 更新文章
- `DELETE /api/articles/:id` - 删除文章

### 管理员接口
- `POST /api/admin/login` - 管理员登录
- `GET /api/admin/tags` - 获取标签列表
- `POST /api/admin/tags` - 创建标签文章

## 🚨 已知问题

1. **文章保存问题** - 部分情况下保存可能失败，需要检查网络连接
2. **管理员路由** - 管理员页面路由配置需要进一步优化
3. **图片上传** - 大文件上传可能需要更长时间
4. **移动端适配** - 部分复杂编辑器功能在移动端体验待优化

## 🔮 后续开发计划

- [ ] 完善文章搜索功能
- [ ] 添加评论系统
- [ ] 实现文章分类管理
- [ ] 优化移动端体验
- [ ] 添加数据导出功能
- [ ] 实现主题切换
- [ ] 集成第三方登录

## 📄 开源协议

MIT License

## 🤝 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目。

## 📞 技术支持

如有问题，请通过以下方式联系：
- 创建GitHub Issue
- 发送邮件至项目维护者

---

**注意**: 这是一个演示项目，请勿在生产环境中直接使用。在部署到生产环境前，请确保进行充分的安全测试和性能优化。

