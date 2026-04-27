---
paths: "src/**/*.{ts,tsx}"
---

# 前端编码规范 (React + antd)

本文档定义React前端项目的编码规范，确保生成的代码符合团队标准。

---

## 1. 技术栈

| 技术 | 版本/规范 |
|------|-----------|
| React | 18.x |
| TypeScript | 5.x |
| 组件库 | antd 5.x |
| 状态管理 | React Context / Zustand |
| 请求库 | axios + react-query |
| 路由 | react-router 6.x |
| 构建工具 | Vite |

---

## 2. 目录结构

```
src/
├── api/                    # API接口定义
│   ├── index.ts           # axios实例配置
│   ├── user.ts            # 用户相关接口
│   └── types.ts           # 接口类型定义
├── components/            # 通用组件
│   ├── Common/
│   │   └── Button/
│   │       ├── index.tsx
│   │       └── index.less
│   └── index.ts
├── pages/                 # 页面组件
│   ├── Home/
│   │   ├── index.tsx
│   │   └── index.less
│   └── User/
│       └── ...
├── hooks/                 # 自定义Hooks
│   ├── useUser.ts
│   └── index.ts
├── store/                 # 状态管理
│   ├── userStore.ts
│   └── index.ts
├── utils/                 # 工具函数
│   ├── format.ts
│   └── validate.ts
├── constants/             # 常量定义
│   └── index.ts
├── types/                 # TypeScript类型
│   └── index.ts
├── App.tsx
└── main.tsx
```

---

## 3. 命名规范

### 3.1 文件命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件 | kebab-case + index.tsx | `user-list/index.tsx` |
| 工具函数 | kebab-case.ts | `format-date.ts` |
| 类型定义 | kebab-case.type.ts | `user.type.ts` |
| Hooks | useXxx.ts | `useUser.ts` |

### 3.2 组件命名

```tsx
// 组件文件：UserList.tsx
// 组件名：UserList (帕斯卡命名)
export const UserList: React.FC<Props> = ({ users }) => {
  // ...
};

// 组件目录结构
UserList/
├── index.tsx      # 组件实现
├── index.less     # 样式文件
└── type.ts        # 类型定义（可选）
```

### 3.3 变量命名

```typescript
// 常量：大写下划线
const MAX_COUNT = 100;
const API_BASE_URL = '/api/v1';

// 变量/函数：驼峰命名
const userList = [];
const getUserInfo = () => {};

// 接口/类型：帕斯卡命名
interface UserInfo {
  id: string;
  name: string;
}

// 枚举：帕斯卡命名
enum UserStatus {
  Active = 'active',
  Inactive = 'inactive',
}
```

---

## 4. React组件规范

### 4.1 组件结构

```tsx
import React, { useState, useEffect } from 'react';
import { Button, Table, Modal } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { userListApi, deleteUserApi } from '@/api/user';
import styles from './index.less';

// 类型定义
interface Props {
  visible: boolean;
  onClose: () => void;
}

interface UserRecord {
  id: string;
  name: string;
  email: string;
}

// 组件实现
export const UserList: React.FC<Props> = ({ visible, onClose }) => {
  // State
  const [loading, setLoading] = useState(false);
  const [dataSource, setDataSource] = useState<UserRecord[]>([]);

  // Effects
  useEffect(() => {
    if (visible) {
      fetchData();
    }
  }, [visible]);

  // 方法
  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await userListApi();
      setDataSource(res.data);
    } catch (error) {
      // 错误处理
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    // 确认逻辑
    await deleteUserApi(id);
    fetchData();
  };

  // 表格列定义
  const columns: ColumnsType<UserRecord> = [
    {
      title: '姓名',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Button type="link" danger onClick={() => handleDelete(record.id)}>
          删除
        </Button>
      ),
    },
  ];

  return (
    <Modal
      title="用户列表"
      open={visible}
      onCancel={onClose}
      width={800}
      footer={null}
    >
      <Table
        columns={columns}
        dataSource={dataSource}
        loading={loading}
        rowKey="id"
      />
    </Modal>
  );
};

export default UserList;
```

### 4.2 Hooks规范

```typescript
// hooks/useUser.ts
import { useState, useEffect } from 'react';
import { userInfoApi } from '@/api/user';
import type { UserInfo } from '@/types';

export const useUser = (userId: string) => {
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      setLoading(true);
      try {
        const res = await userInfoApi(userId);
        setUserInfo(res.data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchUser();
    }
  }, [userId]);

  return { userInfo, loading, error };
};
```

---

## 5. antd 使用规范

### 5.1 Form表单

```tsx
import { Form, Input, Button, Select } from 'antd';
import { useForm, useWatch } from 'antd/es/form/Form';

interface FormValues {
  username: string;
  email: string;
  role: string;
}

export const UserForm: React.FC = () => {
  const [form] = useForm<FormValues>();
  const role = useWatch('role', form);

  const onFinish = (values: FormValues) => {
    console.log('Success:', values);
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={onFinish}
      initialValues={{ role: 'user' }}
    >
      <Form.Item
        label="用户名"
        name="username"
        rules={[{ required: true, message: '请输入用户名' }]}
      >
        <Input placeholder="请输入用户名" />
      </Form.Item>

      <Form.Item
        label="邮箱"
        name="email"
        rules={[
          { required: true, message: '请输入邮箱' },
          { type: 'email', message: '请输入正确的邮箱格式' },
        ]}
      >
        <Input placeholder="请输入邮箱" />
      </Form.Item>

      <Form.Item
        label="角色"
        name="role"
        rules={[{ required: true, message: '请选择角色' }]}
      >
        <Select placeholder="请选择角色">
          <Select.Option value="user">普通用户</Select.Option>
          <Select.Option value="admin">管理员</Select.Option>
        </Select>
      </Form.Item>

      {/* 条件渲染：当选择管理员时显示额外字段 */}
      {role === 'admin' && (
        <Form.Item label="权限码" name="permissions">
          <Select mode="multiple" placeholder="选择权限">
            <Select.Option value="read">读取</Select.Option>
            <Select.Option value="write">写入</Select.Option>
          </Select>
        </Form.Item>
      )}

      <Form.Item>
        <Button type="primary" htmlType="submit">
          提交
        </Button>
      </Form.Item>
    </Form>
  );
};
```

### 5.2 Table表格

```tsx
import { Table, Button, Space, Tag } from 'antd';
import type { ColumnsType } from 'antd/es/table';

interface RecordType {
  id: string;
  name: string;
  status: 'active' | 'inactive';
}

const columns: ColumnsType<RecordType> = [
  {
    title: 'ID',
    dataIndex: 'id',
    width: 80,
  },
  {
    title: '名称',
    dataIndex: 'name',
    ellipsis: true, // 超出省略
  },
  {
    title: '状态',
    dataIndex: 'status',
    width: 100,
    render: (status: string) => (
      <Tag color={status === 'active' ? 'green' : 'red'}>
        {status === 'active' ? '启用' : '禁用'}
      </Tag>
    ),
  },
  {
    title: '操作',
    key: 'action',
    width: 150,
    fixed: 'right',
    render: (_, record) => (
      <Space>
        <Button type="link" size="small" onClick={() => handleEdit(record)}>
          编辑
        </Button>
        <Button type="link" danger size="small" onClick={() => handleDelete(record)}>
          删除
        </Button>
      </Space>
    ),
  },
];

// 组件中使用
<Table
  columns={columns}
  dataSource={dataSource}
  rowKey="id"
  pagination={{
    current: 1,
    pageSize: 20,
    total: 100,
    showSizeChanger: true,
    showQuickJumper: true,
  }}
  scroll={{ x: 1000 }}
/>
```

### 5.3 弹窗 Modal

```tsx
import { Modal, Form, Input } from 'antd';

// 使用/useModal hook管理弹窗
const [modal, contextHolder] = Modal.useModal();

const showConfirm = () => {
  modal.confirm({
    title: '确认删除',
    content: '确定要删除该用户吗？',
    onOk: async () => {
      await deleteApi(id);
      message.success('删除成功');
    },
  });
};
```

---

## 6. API调用规范

### 6.1 API定义

```typescript
// api/user.ts
import request from './index';
import type { UserInfo, UserListParams } from './types';

// 获取用户列表
export const getUserList = (params: UserListParams) => {
  return request.get<{ list: UserInfo[]; total: number }>('/users', { params });
};

// 获取用户详情
export const getUserDetail = (id: string) => {
  return request.get<UserInfo>(`/users/${id}`);
};

// 创建用户
export const createUser = (data: Partial<UserInfo>) => {
  return request.post<UserInfo>('/users', data);
};

// 更新用户
export const updateUser = (id: string, data: Partial<UserInfo>) => {
  return request.put<UserInfo>(`/users/${id}`, data);
};

// 删除用户
export const deleteUser = (id: string) => {
  return request.delete(`/users/${id}`);
};
```

### 6.2 axios实例配置

```typescript
// api/index.ts
import axios, { AxiosInstance, AxiosError } from 'axios';
import { message } from 'antd';

const createRequest = (): AxiosInstance => {
  const instance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // 请求拦截器
  instance.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // 响应拦截器
  instance.interceptors.response.use(
    (response) => {
      const { code, message: msg, data } = response.data;
      
      if (code === 0) {
        return data;
      }
      
      // 业务错误
      message.error(msg);
      return Promise.reject(new Error(msg));
    },
    (error: AxiosError) => {
      // 网络错误
      if (!error.response) {
        message.error('网络错误，请检查网络连接');
        return Promise.reject(error);
      }

      const { status } = error.response;
      if (status === 401) {
        message.error('登录已过期，请重新登录');
        localStorage.removeItem('token');
        window.location.href = '/login';
      } else if (status === 403) {
        message.error('没有权限访问');
      } else if (status >= 500) {
        message.error('服务器错误，请稍后重试');
      }

      return Promise.reject(error);
    }
  );

  return instance;
};

export default createRequest();
```

---

## 7. 类型定义规范

```typescript
// types/user.ts

// 用户信息
export interface UserInfo {
  id: string;
  username: string;
  email: string;
  nickname?: string;
  avatar?: string;
  status: 'active' | 'inactive';
  roles: string[];
  createdAt: string;
  updatedAt: string;
}

// 用户列表查询参数
export interface UserListParams {
  page: number;
  pageSize: number;
  keyword?: string;
  status?: string;
  role?: string;
}

// 分页响应
export interface PaginatedResponse<T> {
  list: T[];
  pagination: {
    page: number;
    pageSize: number;
    total: number;
    totalPages: number;
  };
}

// API统一响应
export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
  timestamp: number;
}
```

---

## 8. 样式规范

### 8.1 CSS Modules

```tsx
// index.less
.container {
  padding: 16px;
  background: #fff;
  
  .header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16px;
  }
  
  .table {
    margin-top: 16px;
  }
}

// 使用
import styles from './index.less';

<div className={styles.container}>
  <div className={styles.header}>标题</div>
</div>
```

### 8.2 antd样式覆盖

```less
// 避免直接覆盖antd全局样式
// 使用ConfigProvider局部定制

import { ConfigProvider } from 'antd';

<ConfigProvider
  theme={{
    token: {
      colorPrimary: '#1890ff',
      borderRadius: 4,
    },
  }}
>
  <App />
</ConfigProvider>
```

---

## 9. 检查清单

编写React代码时，必须检查：

- [ ] 组件名使用帕斯卡命名
- [ ] 文件名使用kebab-case
- [ ] 类型定义完整（Props、State、API Response）
- [ ] 使用useState定义状态，useEffect处理副作用
- [ ] antd组件按需引入
- [ ] API调用使用try-catch包装
- [ ] 表格使用rowKey指定唯一键
- [ ] 表单使用Form组件和useForm hook
- [ ] 样式使用CSS Modules或less
- [ ] 无硬编码字符串，使用常量或配置