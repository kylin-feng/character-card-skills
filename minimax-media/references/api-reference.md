# MiniMax 接口参考

来源：MiniMax 开放平台官方文档（2026-09 核对）
- 文生图：https://platform.minimaxi.com/docs/api-reference/image-generation-t2i
- 图生图：https://platform.minimaxi.com/docs/api-reference/image-generation-i2i
- 图像生成指南：https://platform.minimaxi.com/docs/guides/image-generation
- 模型总览：https://platform.minimaxi.com/docs/guides/models-intro
- 官方 MCP：https://github.com/MiniMax-AI/MiniMax-MCP

## 端点

```
POST https://api.minimaxi.com/v1/image_generation
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `model` | string | 是 | `image-01` 或 `image-01-live` |
| `prompt` | string | 是 | 画面描述，**最长 1500 字符** |
| `subject_reference` | object[] | 否 | 人物主体参考，**数组长度仅支持 1** |
| `style` | object | 否 | 画风设置，**仅 `image-01-live` 生效** |
| `aspect_ratio` | string | 否 | 默认 `1:1` |
| `width` / `height` | int | 否 | 仅 `image-01`；需同时设置，[512, 2048]，8 的倍数。与 aspect_ratio 同时给时**后者优先** |
| `response_format` | string | 否 | `url`（默认，**24 小时过期**）/ `base64` |
| `seed` | int64 | 否 | 固定可复现；不给则每张图各自随机 |
| `n` | int | 否 | 1–9，默认 1 |
| `prompt_optimizer` | bool | 否 | 默认 `false` |
| `aigc_watermark` | bool | 否 | 默认 `false` |

### aspect_ratio 对照

| 值 | 像素 |
|---|---|
| `1:1` | 1024×1024 |
| `16:9` | 1280×720 |
| `4:3` | 1152×864 |
| `3:2` | 1248×832 |
| `2:3` | 832×1248 |
| `3:4` | 864×1152 |
| `9:16` | 720×1280 |
| `21:9` | 1344×576（仅 image-01） |

### subject_reference 子字段

| 字段 | 说明 |
|---|---|
| `type` | 固定 `"character"`（人像主体参考） |
| `image_file` | 参考图。支持 `data:image/jpeg;base64,{data}` 或公网可访问 URL |

约束：单人**人脸正面照**效果最佳；jpg/jpeg/png；**< 10 MB**；数组长度 1。

## 响应结构

```json
{
  "id": "03ff3cd0820949eb8a410056b5f21d38",
  "data": {
    "image_urls": ["..."]        // response_format=url 时
    // "image_base64": ["..."]   // response_format=base64 时
  },
  "metadata": {
    "success_count": "1",
    "failed_count": "0"          // 被内容安全拦截的数量
  },
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

## 错误码

| code | 含义 |
|---|---|
| 0 | 成功 |
| 1002 | 限流 |
| 1004 | 鉴权失败 |
| 1008 | 余额不足 |
| 1026 | 输出内容描述敏感 |
| 2013 | 参数异常 |
| 2049 | 无效 API Key |

## 实测记录（2026-09-12）

在本机验证通过：

| 场景 | 参数 | 结果 |
|---|---|---|
| 文生图 | `aspect=9:16` `seed=20260912` | 19.1s，720×1280，268 KB |
| 图生图 | `--ref ref-01` `aspect=4:3` | 22.1s，1152×864，198.7 KB |

两张均 SOI/EOI 完整，宽高比与请求一致。**base64 模式落盘正常，无二次下载**。

## 平台其它可用能力（本技能未封装）

按需扩展时可用：

| 方向 | 代表模型 |
|---|---|
| 视频 | MiniMax H3（文生/图生/首尾帧/多模态参考，768P/2K，4–15s） |
| 语音 | Speech-2.8-HD / Speech-2.8-Turbo（TTS、音色克隆、音色设计） |
| 音乐 | music-3.0（注：2026-08-20 起不再对新用户开放付费接口） |
| 语言 | MiniMax-M3 / M2.7 |

视频与语音的官方 MCP（Python / JS）见 https://github.com/MiniMax-AI/MiniMax-MCP，
支持 stdio / SSE / REST 传输。
