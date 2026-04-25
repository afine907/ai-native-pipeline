# TDD 编码范式

## 核心原则

1. **测试先行** - 先写测试，再写实现
2. **红绿重构** - 红（失败）→ 绿（通过）→ 重构
3. **小步前进** - 每次只做最小改动

## 流程

```
1. 写一个失败的测试（Red）
2. 写最少的代码让测试通过（Green）
3. 重构代码（Refactor）
4. 重复
```

## 输出格式

### 输入
```typescript
// 需求：实现一个加法函数
function add(a: number, b: number): number {
  return a + b;
}
```

### TDD 步骤

**Step 1: 写测试**
```typescript
// src/utils/calc.test.ts
import { add } from './calc';

describe('add', () => {
  it('should add two numbers', () => {
    expect(add(1, 2)).toBe(3);
  });
});
```

**Step 2: 写实现**
```typescript
// src/utils/calc.ts
export const add = (a: number, b: number): number => a + b;
```

**Step 3: 重构**（如需要）

## 测试文件命名

```
源文件: src/utils/calc.ts
测试文件: src/utils/calc.test.ts
```

## 常用测试框架

| 语言 | 框架 |
|------|------|
| JavaScript/TypeScript | Jest, Vitest |
| Go | testing, ginkgo |
| Python | pytest, unittest |