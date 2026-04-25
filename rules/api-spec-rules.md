# API接口定义规范

本文档定义PRD中API接口的标准格式，确保生成的接口文档结构一致、可直接用于开发。

---

## 1. API命名规范

### 1.1 URL路径规范

| 场景 | 规范 | 示例 |
|------|------|------|
| 资源复数 | 使用复数形式 | `/users`, `/orders` |
| 单个资源 | `/资源/{id}` | `/users/{userId}` |
| 嵌套资源 | `/父资源/{id}/子资源` | `/users/{userId}/orders` |
| 动作资源 | `/资源/{id}/动作` | `/users/{userId}/activate` |
| 列表查询 | `/资源` + Query参数 | `/users?status=active` |

### 1.2 HTTP方法规范

| 方法 | 用途 | 幂等 |
|------|------|------|
| GET | 查询资源 | ✅ |
| POST | 创建资源 | ❌ |
| PUT | 完整更新资源 | ✅ |
| PATCH | 部分更新资源 | ❌ |
| DELETE | 删除资源 | ✅ |

---

## 2. 请求参数定义

### 2.1 Header参数

```yaml
Headers:
  - name: Authorization
    type: string
    required: true
    description: "Bearer {token}"
  - name: Content-Type
    type: string
    required: true
    default: "application/json"
  - name: Accept
    type: string
    required: false
    default: "application/json"
```

### 2.2 Query参数

```yaml
Query Params:
  - name: page
    type: integer
    required: false
    default: 1
    description: "页码"
  - name: pageSize
    type: integer
    required: false
    default: 20
    description: "每页数量，最大100"
  - name: sortBy
    type: string
    required: false
    description: "排序字段"
  - name: order
    type: string
    required: false
    enum: [asc, desc]
    default: "asc"
```

### 2.3 Request Body (JSON)

```yaml
Request Body:
  type: object
  properties:
    username:
      type: string
      required: true
      minLength: 3
      maxLength: 50
      description: "用户名"
    email:
      type: string
      required: true
      format: email
      description: "邮箱"
    password:
      type: string
      required: true
      minLength: 8
      description: "密码"
  required: [username, email, password]
```

---

## 3. 响应格式定义

### 3.1 成功响应

```yaml
# 通用成功响应
Response (200 OK):
  code: 0
  message: "success"
  data: <T>
  timestamp: 1704067200000

# 分页响应
Response (200 OK):
  code: 0
  message: "success"
  data:
    list: [...]
    pagination:
      page: 1
      pageSize: 20
      total: 100
      totalPages: 5
```

### 3.2 错误响应

```yaml
# 通用错误响应
Response (Error):
  code: <error_code>
  message: "<error_message>"
  details: {...}  # 可选，详细错误信息
  timestamp: 1704067200000
```

---

## 4. 错误码规范

### 4.1 错误码范围

| 错误码范围 | 含义 |
|-----------|------|
| 0 | 成功 |
| 1xxx | 通用错误 |
| 2xxx | 认证/授权错误 |
| 3xxx | 参数校验错误 |
| 4xxx | 业务逻辑错误 |
| 5xxx | 第三方服务错误 |

### 4.2 常用错误码

| 错误码 | 消息 | 解决方案 |
|--------|------|----------|
| 0 | 成功 | - |
| 1001 | 系统内部错误 | 请稍后重试或联系管理员 |
| 2001 | Token无效 | 请重新登录 |
| 2002 | Token已过期 | 请重新登录 |
| 2003 | 无访问权限 | 缺少必要权限 |
| 3001 | 参数缺失 | 检查必填参数 |
| 3002 | 参数格式错误 | 检查参数格式 |
| 3003 | 参数值超出范围 | 检查参数取值范围 |
| 4001 | 资源不存在 | 检查资源ID |
| 4002 | 资源已存在 | 检查唯一性约束 |
| 4003 | 资源状态异常 | 检查资源当前状态 |
| 5001 | 服务不可用 | 请稍后重试 |

---

## 5. 完整示例

### 示例：用户登录接口

```yaml
# API接口文档

## 1. 用户登录

### 接口信息

| 项目 | 内容 |
|------|------|
| 接口名称 | 用户登录 |
| 接口路径 | POST /api/v1/auth/login |
| HTTP方法 | POST |
| 认证方式 | 无需认证 |

### 请求头

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Content-Type | string | 是 | application/json |

### 请求体

```json
{
  "username": "string",
  "password": "string",
  "captcha": "string",
  "captchaKey": "string"
}
```

#### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名/邮箱/手机号 |
| password | string | 是 | 密码（MD5加密传输） |
| captcha | string | 否 | 图形验证码（需验证码时必填） |
| captchaKey | string | 否 | 验证码key（需验证码时必填） |

### 成功响应

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "tokenType": "Bearer",
    "expiresIn": 7200,
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshExpiresIn": 604800,
    "user": {
      "id": "1001",
      "username": "zhangsan",
      "email": "zhangsan@example.com",
      "nickname": "张三",
      "avatar": "https://example.com/avatar/1001.jpg",
      "roles": ["user"],
      "permissions": ["user:read", "user:write"]
    }
  },
  "timestamp": 1704067200000
}
```

#### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| token | string | 访问令牌 |
| tokenType | string | 令牌类型，默认Bearer |
| expiresIn | integer | 令牌有效期（秒），默认2小时 |
| refreshToken | string | 刷新令牌 |
| refreshExpiresIn | integer | 刷新令牌有效期（秒），默认7天 |
| user | object | 用户信息 |
| user.id | string | 用户ID |
| user.username | string | 用户名 |
| user.email | string | 邮箱 |
| user.nickname | string | 昵称 |
| user.avatar | string | 头像URL |
| user.roles | string[] | 角色列表 |
| user.permissions | string[] | 权限列表 |

### 错误响应

#### 用户名或密码错误 (4003)

```json
{
  "code": 4003,
  "message": "用户名或密码错误",
  "timestamp": 1704067200000
}
```

#### 需要图形验证码 (4004)

```json
{
  "code": 4004,
  "message": "需要图形验证码",
  "details": {
    "requireCaptcha": true,
    "captchaKey": "captcha:1704067200000"
  },
  "timestamp": 1704067200000
}
```

#### 参数校验失败 (3002)

```json
{
  "code": 3002,
  "message": "参数格式错误",
  "details": {
    "errors": [
      {
        "field": "username",
        "message": "用户名不能为空"
      },
      {
        "field": "password",
        "message": "密码长度不能少于8位"
      }
    ]
  },
  "timestamp": 1704067200000
}
```

### 错误码汇总

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 3001 | 参数缺失 |
| 3002 | 参数格式错误 |
| 4003 | 用户名或密码错误 |
| 4004 | 需要图形验证码 |
| 5001 | 服务不可用 |
```

---

## 6. 接口文档模板

### 6.1 标准模板

```yaml
## [接口名称]

### 接口信息

| 项目 | 内容 |
|------|------|
| 接口名称 | [名称] |
| 接口路径 | [HTTP方法] /api/v1/[资源路径] |
| HTTP方法 | [GET/POST/PUT/DELETE/PATCH] |
| 认证方式 | [无需认证/Bearer Token/API Key] |

### 请求头

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Authorization | string | 是 | Bearer {token} |

### 请求体

```json
{
  "field1": "string",
  "field2": 0
}
```

### 成功响应

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

### 错误响应

```json
{
  "code": 4001,
  "message": "资源不存在"
}
```

### 错误码汇总

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| xxxx | xxx |
```

---

## 7. 检查清单

生成API文档时，必须检查以下项目：

- [ ] URL路径符合RESTful规范
- [ ] HTTP方法使用正确
- [ ] 必填参数已标记
- [ ] 参数类型和格式已定义
- [ ] 响应格式符合统一规范
- [ ] 错误码已定义并有解决方案
- [ ] 示例完整且可直接使用
- [ ] 字段说明清晰