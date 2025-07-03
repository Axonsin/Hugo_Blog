---
title: 模糊算法
date: 2025-02-11
tags: ['算法', '色彩']
description: "模糊算法的原理解析和实现方法"
summary: 算法原理解析
categories: [杂谈]
---

## 二维卷积模糊
```cpp
// GaussianBlur.hlsl
float4 GaussianBlur(sampler2D tex, float2 uv, float2 resolution, float radius)
{
    float4 color = float4(0, 0, 0, 0);
    float totalWeight = 0.0;
    int samples = 5; // Number of samples for blur

    for (int x = -samples; x <= samples; x++)
    {
        for (int y = -samples; y <= samples; y++)
        {
            float2 offset = float2(x, y) * radius / resolution;
            float weight = exp(-dot(offset, offset) / (2.0 * radius * radius));
            color += tex2D(tex, uv + offset) * weight;
            totalWeight += weight;
        }
    }

    return color / totalWeight;
}
```

## **Frosted Glass Blur（毛玻璃模糊，随机采样模糊）**


