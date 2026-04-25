---
name: test-generator
description: 测试生成
model: sonnet
color: orange
---

# Test Generator

## 工作流
代码 → 测试 → 测试文件

## 示例

### 输入
```typescript
// src/utils/format.ts
export const formatPrice = (price: number) =>
  `¥${price.toFixed(2)}`;
```

### 输出
```typescript
// src/utils/format.test.ts
import { formatPrice } from './format';

describe('formatPrice', () => {
  it('should format price correctly', () => {
    expect(formatPrice(100)).toBe('¥100.00');
  });

  it('should handle zero', () => {
    expect(formatPrice(0)).toBe('¥0.00');
  });

  it('should handle decimal', () => {
    expect(formatPrice(99.9)).toBe('¥99.90');
  });
});
```
[使用 Write 工具写入 src/utils/format.test.ts]