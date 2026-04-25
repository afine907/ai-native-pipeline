# 后端编码规范 (Golang)

本文档定义Golang后端项目的编码规范，确保生成的代码符合团队标准。

---

## 1. 技术栈

| 技术 | 版本/规范 |
|------|-----------|
| Go | 1.21+ |
| Web框架 | Gin |
| ORM | GORM |
| 配置 | Viper |
| 日志 | Zap |
| 认证 | JWT |
| API文档 | Swagger |

---

## 2. 目录结构

```
├── cmd/                    # 程序入口
│   └── server/
│       └── main.go
├── internal/               # 内部包（不可导出）
│   ├── config/            # 配置管理
│   │   └── config.go
│   ├── handler/           # 处理器层（Controller）
│   │   ├── user.go
│   │   └── auth.go
│   ├── middleware/        # 中间件
│   │   ├── cors.go
│   │   ├── jwt.go
│   │   └── logger.go
│   ├── service/           # 业务逻辑层
│   │   ├── user.go
│   │   └── auth.go
│   ├── repository/        # 数据访问层
│   │   ├── user.go
│   │   └── init.go
│   ├── model/             # 数据模型
│   │   ├── user.go
│   │   └── init.go
│   ├── request/           # 请求参数
│   │   └── user.go
│   ├── response/          # 响应结构
│   │   └── response.go
│   └── utils/             # 工具函数
│       ├── jwt.go
│       └── password.go
├── api/                   # API定义（Swagger）
│   └── swagger.yaml
├── configs/               # 配置文件
│   └── config.yaml
├── migrations/            # 数据库迁移
├── scripts/               # 脚本
├── go.mod
├── go.sum
└── Makefile
```

---

## 3. 命名规范

### 3.1 包命名

```go
// 使用小写字母，多个单词用下划线分隔
package config     // 正确
package configMgr  // 错误
package configs    // 错误
```

### 3.2 文件命名

```go
// 使用小写字母，多个单词用下划线分隔
user.go        // 正确
userModel.go   // 错误
User.go        // 错误
```

### 3.3 结构体命名

```go
// 使用帕斯卡命名
type User struct {}        // 正确
type user struct {}        // 错误（仅包内使用可用）

// 表名用单数
type User struct {         // 对应 users 表
    gorm.Model
}

// 字段用驼峰命名
type User struct {
    ID        uint      `gorm:"primaryKey"`
    Username  string    `gorm:"column:username;size:50;uniqueIndex"`
    Email     string    `gorm:"column:email;size:100;uniqueIndex"`
    Status    int       `gorm:"column:status;default:1"`
    CreatedAt time.Time `gorm:"column:created_at"`
    UpdatedAt time.Time `gorm:"column:updated_at"`
}

func (User) TableName() string {
    return "users"
}
```

### 3.4 变量/函数命名

```go
// 变量：驼峰命名
userList := []User{}       // 正确
user_list := []User{}      // 错误

// 常量：大写下划线
const MaxPageSize = 100    // 正确
const max_page_size = 100  // 错误

// 函数：驼峰命名（导出）
func GetUserByID(id uint) (*User, error) {}

// 函数：驼峰命名（不导出）
func validateEmail(email string) bool {}
```

---

## 4. 代码结构

### 4.1 Handler层

```go
// internal/handler/user.go
package handler

import (
    "net/http"
    "strconv"

    "github.com/gin-gonic/gin"
    "github.com/your/project/internal/model"
    "github.com/your/project/internal/request"
    "github.com/your/project/internal/response"
    "github.com/your/project/internal/service"
)

type UserHandler struct {
    userService *service.UserService
}

func NewUserHandler(userService *service.UserService) *UserHandler {
    return &UserHandler{
        userService: userService,
    }
}

// GetUserList 获取用户列表
// @Summary 获取用户列表
// @Tags 用户管理
// @Accept json
// @Produce json
// @Param page query int false "页码"
// @Param pageSize query int false "每页数量"
// @Success 200 {object} response.PageResponse
// @Router /api/v1/users [get]
func (h *UserHandler) GetUserList(c *gin.Context) {
    // 1. 参数绑定
    page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
    pageSize, _ := strconv.Atoi(c.DefaultQuery("pageSize", "20"))

    // 2. 参数校验
    if page < 1 {
        page = 1
    }
    if pageSize < 1 || pageSize > 100 {
        pageSize = 20
    }

    // 3. 调用服务层
    users, total, err := h.userService.GetUserList(c.Request.Context(), page, pageSize)
    if err != nil {
        response.Error(c, http.StatusInternalServerError, err.Error())
        return
    }

    // 4. 返回响应
    response.Success(c, gin.H{
        "list": users,
        "pagination": gin.H{
            "page":       page,
            "pageSize":   pageSize,
            "total":      total,
            "totalPages": (total + pageSize - 1) / pageSize,
        },
    })
}

// CreateUser 创建用户
// @Summary 创建用户
// @Tags 用户管理
// @Accept json
// @Produce json
// @Param request body request.CreateUserRequest true "请求体"
// @Success 200 {object} model.User
// @Router /api/v1/users [post]
func (h *UserHandler) CreateUser(c *gin.Context) {
    // 1. 绑定参数
    var req request.CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        response.Error(c, http.StatusBadRequest, "参数错误: "+err.Error())
        return
    }

    // 2. 调用服务层
    user, err := h.userService.CreateUser(c.Request.Context(), &req)
    if err != nil {
        response.Error(c, http.StatusInternalServerError, err.Error())
        return
    }

    // 3. 返回响应
    response.Success(c, user)
}
```

### 4.2 Service层

```go
// internal/service/user.go
package service

import (
    "context"
    "errors"

    "github.com/your/project/internal/model"
    "github.com/your/project/internal/repository"
    "golang.org/x/crypto/bcrypt"
)

var (
    ErrUserNotFound     = errors.New("用户不存在")
    ErrUserAlreadyExist = errors.New("用户已存在")
)

type UserService struct {
    userRepo *repository.UserRepository
}

func NewUserService(userRepo *repository.UserRepository) *UserService {
    return &UserService{
        userRepo: userRepo,
    }
}

func (s *UserService) GetUserList(ctx context.Context, page, pageSize int) ([]*model.User, int64, error) {
    return s.userRepo.FindByPage(ctx, page, pageSize)
}

func (s *UserService) GetUserByID(ctx context.Context, id uint) (*model.User, error) {
    user, err := s.userRepo.FindByID(ctx, id)
    if err != nil {
        return nil, ErrUserNotFound
    }
    return user, nil
}

func (s *UserService) CreateUser(ctx context.Context, req *model.User) (*model.User, error) {
    // 业务逻辑：检查用户是否已存在
    exist, err := s.userRepo.ExistByEmail(ctx, req.Email)
    if err != nil {
        return nil, err
    }
    if exist {
        return nil, ErrUserAlreadyExist
    }

    // 密码加密
    hashedPassword, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
    if err != nil {
        return nil, err
    }
    req.Password = string(hashedPassword)

    // 创建用户
    return s.userRepo.Create(ctx, req)
}

func (s *UserService) UpdateUser(ctx context.Context, id uint, updates map[string]interface{}) error {
    // 业务逻辑：检查用户是否存在
    exist, err := s.userRepo.ExistByID(ctx, id)
    if err != nil {
        return err
    }
    if !exist {
        return ErrUserNotFound
    }

    return s.userRepo.Update(ctx, id, updates)
}

func (s *UserService) DeleteUser(ctx context.Context, id uint) error {
    return s.userRepo.Delete(ctx, id)
}
```

### 4.3 Repository层

```go
// internal/repository/user.go
package repository

import (
    "context"

    "github.com/your/project/internal/model"
    "gorm.io/gorm"
)

type UserRepository struct {
    db *gorm.DB
}

func NewUserRepository(db *gorm.DB) *UserRepository {
    return &UserRepository{db: db}
}

func (r *UserRepository) FindByPage(ctx context.Context, page, pageSize int) ([]*model.User, int64, error) {
    var users []*model.User
    var total int64

    // 查询总数
    r.db.Model(&model.User{}).Count(&total)

    // 分页查询
    offset := (page - 1) * pageSize
    err := r.db.Offset(offset).Limit(pageSize).Order("created_at DESC").Find(&users).Error

    return users, total, err
}

func (r *UserRepository) FindByID(ctx context.Context, id uint) (*model.User, error) {
    var user model.User
    err := r.db.First(&user, id).Error
    if errors.Is(err, gorm.ErrRecordNotFound) {
        return nil, err
    }
    return &user, err
}

func (r *UserRepository) FindByEmail(ctx context.Context, email string) (*model.User, error) {
    var user model.User
    err := r.db.Where("email = ?", email).First(&user).Error
    if errors.Is(err, gorm.ErrRecordNotFound) {
        return nil, err
    }
    return &user, err
}

func (r *UserRepository) ExistByEmail(ctx context.Context, email string) (bool, error) {
    var count int64
    err := r.db.Model(&model.User{}).Where("email = ?", email).Count(&count).Error
    return count > 0, err
}

func (r *UserRepository) ExistByID(ctx context.Context, id uint) (bool, error) {
    var count int64
    err := r.db.Model(&model.User{}).Where("id = ?", id).Count(&count).Error
    return count > 0, err
}

func (r *UserRepository) Create(ctx context.Context, user *model.User) error {
    return r.db.Create(user).Error
}

func (r *UserRepository) Update(ctx context.Context, id uint, updates map[string]interface{}) error {
    return r.db.Model(&model.User{}).Where("id = ?", id).Updates(updates).Error
}

func (r *UserRepository) Delete(ctx context.Context, id uint) error {
    return r.db.Delete(&model.User{}, id).Error
}
```

---

## 5. Model定义

```go
// internal/model/user.go
package model

import (
    "time"

    "gorm.io/gorm"
)

// 用户状态
const (
    UserStatusInactive = 0 // 未激活
    UserStatusActive   = 1 // 正常
    UserStatusBanned   = 2 // 禁用
)

// 用户角色
const (
    RoleUser  = "user"  // 普通用户
    RoleAdmin = "admin" // 管理员
)

type User struct {
    ID        uint           `gorm:"primaryKey" json:"id"`
    Username  string         `gorm:"column:username;size:50;uniqueIndex;not null" json:"username"`
    Email     string         `gorm:"column:email;size:100;uniqueIndex;not null" json:"email"`
    Password  string         `gorm:"column:password;size:255;not null" json:"-"`
    Nickname  string         `gorm:"column:nickname;size:50" json:"nickname"`
    Avatar    string         `gorm:"column:avatar;size:255" json:"avatar"`
    Status    int            `gorm:"column:status;default:1;not null" json:"status"`
    Role      string         `gorm:"column:role;size:20;default:'user';not null" json:"role"`
    CreatedAt time.Time      `gorm:"column:created_at;autoCreateTime" json:"createdAt"`
    UpdatedAt time.Time      `gorm:"column:updated_at;autoUpdateTime" json:"updatedAt"`
    DeletedAt gorm.DeletedAt `gorm:"column:deleted_at;index" json:"-"`
}

func (User) TableName() string {
    return "users"
}
```

---

## 6. Request/Response

### 6.1 请求参数

```go
// internal/request/user.go
package request

type CreateUserRequest struct {
    Username string `json:"username" binding:"required,min=3,max=50"`
    Email    string `json:"email" binding:"required,email"`
    Password string `json:"password" binding:"required,min=8,max=20"`
    Nickname string `json:"nickname" binding:"max=50"`
}

type UpdateUserRequest struct {
    Nickname string `json:"nickname" binding:"max=50"`
    Avatar   string `json:"avatar" binding:"max=255"`
    Status   *int   `json:"status" binding:"oneof=0 1 2"`
}

type LoginRequest struct {
    Email    string `json:"email" binding:"required,email"`
    Password string `json:"password" binding:"required"`
}
```

### 6.2 响应结构

```go
// internal/response/response.go
package response

import (
    "github.com/gin-gonic/gin"
)

type Response struct {
    Code    int         `json:"code"`
    Message string      `json:"message"`
    Data    interface{} `json:"data,omitempty"`
    Time    int64       `json:"timestamp"`
}

// 成功响应
func Success(c *gin.Context, data interface{}) {
    c.JSON(200, Response{
        Code:    0,
        Message: "success",
        Data:    data,
        Time:    currentTimeMillis(),
    })
}

// 错误响应
func Error(c *gin.Context, code int, message string) {
    c.JSON(code, Response{
        Code:    code,
        Message: message,
        Time:    currentTimeMillis(),
    })
}

func currentTimeMillis() int64 {
    return time.Now().UnixMilli()
}
```

---

## 7. 中间件

### 7.1 JWT认证

```go
// internal/middleware/jwt.go
package middleware

import (
    "net/http"
    "strings"

    "github.com/gin-gonic/gin"
    "github.com/golang-jwt/jwt/v5"
    "github.com/your/project/internal/utils"
)

func JWTAuth(secret string) gin.HandlerFunc {
    return func(c *gin.Context) {
        // 从Header获取Token
        authHeader := c.GetHeader("Authorization")
        if authHeader == "" {
            c.JSON(http.StatusUnauthorized, gin.H{"message": "请先登录"})
            c.Abort()
            return
        }

        // 解析Bearer Token
        parts := strings.Split(authHeader, " ")
        if len(parts) != 2 || parts[0] != "Bearer" {
            c.JSON(http.StatusUnauthorized, gin.H{"message": "Token格式错误"})
            c.Abort()
            return
        }

        // 验证Token
        tokenString := parts[1]
        token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
            return []byte(secret), nil
        })

        if err != nil || !token.Valid {
            c.JSON(http.StatusUnauthorized, gin.H{"message": "Token已过期"})
            c.Abort()
            return
        }

        // 提取用户信息
        claims, ok := token.Claims.(jwt.MapClaims)
        if !ok {
            c.JSON(http.StatusUnauthorized, gin.H{"message": "无效的Token"})
            c.Abort()
            return
        }

        // 设置上下文
        c.Set("userID", uint(claims["user_id"].(float64)))
        c.Set("username", claims["username"].(string))
        c.Set("role", claims["role"].(string))

        c.Next()
    }
}

// 角色校验中间件
func RequireRole(roles ...string) gin.HandlerFunc {
    return func(c *gin.Context) {
        userRole, _ := c.Get("role")
        for _, role := range roles {
            if userRole == role {
                c.Next()
                return
            }
        }
        c.JSON(http.StatusForbidden, gin.H{"message": "权限不足"})
        c.Abort()
    }
}
```

### 7.2 CORS

```go
// internal/middleware/cors.go
package middleware

import (
    "github.com/gin-gonic/gin"
)

func CORS() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
        c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
        c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
        c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, DELETE, PATCH")

        if c.Request.Method == "OPTIONS" {
            c.AbortWithStatus(204)
            return
        }

        c.Next()
    }
}
```

---

## 8. Router注册

```go
// cmd/server/main.go
package main

import (
    "log"

    "github.com/gin-gonic/gin"
    "github.com/your/project/internal/config"
    "github.com/your/project/internal/handler"
    "github.com/your/project/internal/middleware"
    "github.com/your/project/internal/model"
    "github.com/your/project/internal/repository"
    "github.com/your/project/internal/service"
    "gorm.io/driver/mysql"
    "gorm.io/gorm"
)

func main() {
    // 1. 初始化配置
    cfg := config.Load()

    // 2. 初始化数据库
    db, err := gorm.Open(mysql.Open(cfg.DSN), &gorm.Config{})
    if err != nil {
        log.Fatal(err)
    }

    // 3. 自动迁移
    db.AutoMigrate(&model.User{})

    // 4. 初始化各层
    userRepo := repository.NewUserRepository(db)
    userService := service.NewUserService(userRepo)
    userHandler := handler.NewUserHandler(userService)

    // 5. 注册路由
    r := gin.Default()
    r.Use(middleware.CORS())

    // API路由组
    api := r.Group("/api/v1")
    {
        // 公开接口
        auth := api.Group("/auth")
        {
            auth.POST("/login", userHandler.Login)
            auth.POST("/register", userHandler.Register)
        }

        // 需要认证的接口
        users := api.Group("/users")
        users.Use(middleware.JWTAuth(cfg.JWTSecret))
        {
            users.GET("", userHandler.GetUserList)
            users.GET("/:id", userHandler.GetUser)
            users.POST("", middleware.RequireRole("admin"), userHandler.CreateUser)
            users.PUT("/:id", userHandler.UpdateUser)
            users.DELETE("/:id", middleware.RequireRole("admin"), userHandler.DeleteUser)
        }
    }

    // 6. 启动服务
    r.Run(":8080")
}
```

---

## 9. 检查清单

编写Go代码时，必须检查：

- [ ] 包名使用小写
- [ ] 文件名使用小写下划线
- [ ] 结构体/函数名使用帕斯卡命名
- [ ] 变量/常量名使用驼峰/大写下划线
- [ ] 接口定义清晰，参数绑定有校验
- [ ] 错误处理完善（返回具体错误）
- [ ] 数据库操作使用事务
- [ ] 密码使用bcrypt加密存储
- [ ] API使用RESTful风格
- [ ] 中间件正确使用（认证、鉴权、日志）
- [ ] 日志记录关键操作
- [ ] 配置使用Viper管理
- [ ] 遵循Go代码规范（go fmt, go vet）