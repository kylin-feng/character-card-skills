#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MiniMax 图像生成 —— 文生图 / 人物主体参考图生图

对应技能：minimax-media
接口：POST https://api.minimaxi.com/v1/image_generation

设计约束：
  - 零第三方依赖（仅标准库），避免污染用户环境
  - API Key 只从「命令行参数 > 环境变量 > secrets 文件」读取，绝不硬编码
  - 默认 base64 返回并直接落盘，规避 24 小时 URL 过期问题

用法示例：
  # 文生图
  python minimax_image.py --prompt "雪夜街道上的银发少女" --aspect 9:16 --out ./out

  # 图生图（人物一致性）—— 同样是麟鸣，换场景换动作
  python minimax_image.py --prompt "她坐在教室窗边翻书" --ref ./refs/ref-02-classroom.jpg --out ./out

  # 批量 4 张，固定种子便于复现
  python minimax_image.py --prompt "..." --n 4 --seed 42 --out ./out
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# Windows 控制台中文输出兜底
for _stream in (sys.stdout, sys.stderr):
    try:
        if getattr(_stream, "encoding", "") and _stream.encoding.lower() not in ("utf-8", "utf8"):
            _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

API_HOST_DEFAULT = "https://api.minimaxi.com"
ENDPOINT = "/v1/image_generation"
SECRETS_FILE = Path.home() / ".workbuddy" / "secrets" / "minimax.env"
MAX_REF_BYTES = 10 * 1024 * 1024
MAX_PROMPT_CHARS = 1500
ASPECT_CHOICES = ["1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16", "21:9"]

ERROR_CODES = {
    "0": "成功",
    "1002": "触发限流，请降低并发后重试",
    "1004": "鉴权失败，请检查 API Key 是否正确",
    "1008": "余额不足，请前往 MiniMax 账户充值",
    "1026": "输出内容描述敏感，请调整 prompt",
    "2013": "输入参数异常，请检查参数取值",
    "2049": "无效的 API Key",
}


# --------------------------------------------------------------------------
# 凭据解析
# --------------------------------------------------------------------------
def _read_secrets(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.is_file():
        return data
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        data[key.strip()] = value.strip()
    return data


def resolve_credentials(cli_key: str | None) -> tuple[str, str]:
    secrets = _read_secrets(SECRETS_FILE)
    key = (cli_key or os.environ.get("MINIMAX_API_KEY") or secrets.get("MINIMAX_API_KEY") or "").strip()
    host = (os.environ.get("MINIMAX_API_HOST") or secrets.get("MINIMAX_API_HOST") or API_HOST_DEFAULT).strip()
    if not key:
        sys.exit(
            "错误：未找到 MiniMax API Key。\n"
            f"  方案一：将 `MINIMAX_API_KEY=sk-api-...` 写入 {SECRETS_FILE}\n"
            "  方案二：设置环境变量 MINIMAX_API_KEY"
        )
    return key, host.rstrip("/")


# --------------------------------------------------------------------------
# 人物主体参考图 → subject_reference
# --------------------------------------------------------------------------
def build_subject_reference(ref: str) -> list[dict]:
    """本地文件转 data URL；公网 URL 原样透传。"""
    if re.match(r"^https?://", ref, re.I):
        return [{"type": "character", "image_file": ref}]

    path = Path(ref).expanduser()
    if not path.is_file():
        sys.exit(f"错误：参考图不存在 -> {path}")

    size = path.stat().st_size
    if size > MAX_REF_BYTES:
        sys.exit(f"错误：参考图 {size / 1048576:.1f} MB，超过 10 MB 上限 -> {path}")

    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    if mime not in ("image/jpeg", "image/png"):
        sys.exit(f"错误：参考图格式 {mime} 不受支持，仅支持 jpg / jpeg / png -> {path}")

    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return [{"type": "character", "image_file": f"data:{mime};base64,{encoded}"}]


# --------------------------------------------------------------------------
# 请求
# --------------------------------------------------------------------------
def call_api(payload: dict, key: str, host: str, timeout: int = 180) -> dict:
    request = urllib.request.Request(
        host + ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        sys.exit(f"错误：HTTP {exc.code}\n{body[:800]}")
    except urllib.error.URLError as exc:
        sys.exit(f"错误：网络请求失败 -> {exc.reason}")
    except json.JSONDecodeError:
        sys.exit("错误：接口返回的不是合法 JSON")


def slugify(text: str, limit: int = 24) -> str:
    slug = re.sub(r"[^\w]+", "-", text, flags=re.UNICODE).strip("-")
    return slug[:limit].strip("-") or "image"


# --------------------------------------------------------------------------
# 主流程
# --------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="MiniMax 生图（文生图 / 人物主体参考图生图）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--prompt", required=True, help="画面描述，最长 1500 字符")
    parser.add_argument("--out", default=".", help="输出目录（默认当前目录）")
    parser.add_argument("--name", help="输出文件名（不含扩展名）；默认「时间戳-提示词摘要」")
    parser.add_argument("--aspect", default="1:1", choices=ASPECT_CHOICES, help="宽高比，默认 1:1")
    parser.add_argument("--n", type=int, default=1, help="生成张数 1-9，默认 1")
    parser.add_argument(
        "--model", default="image-01", choices=["image-01", "image-01-live"],
        help="image-01（写实细腻）/ image-01-live（手绘卡通增强）",
    )
    parser.add_argument("--seed", type=int, help="随机种子，固定它可复现结果")
    parser.add_argument("--ref", help="人物主体参考图：本地路径或公网 URL，用于保持角色一致性")
    parser.add_argument("--optimize", action="store_true", help="开启 prompt 自动优化")
    parser.add_argument("--watermark", action="store_true", help="添加 AIGC 水印（默认不加）")
    parser.add_argument("--dry-run", action="store_true", help="只打印将发送的请求，不真正调用")
    parser.add_argument("--json", action="store_true", dest="as_json", help="以 JSON 输出结果")
    parser.add_argument("--api-key", help="临时指定 API Key（一般不用，交给 secrets 文件即可）")
    args = parser.parse_args()

    prompt = args.prompt.strip()
    if not prompt:
        sys.exit("错误：prompt 不能为空")
    if len(prompt) > MAX_PROMPT_CHARS:
        sys.exit(f"错误：prompt 长 {len(prompt)} 字符，超过 {MAX_PROMPT_CHARS} 上限")

    key, host = resolve_credentials(args.api_key)

    payload: dict = {
        "model": args.model,
        "prompt": prompt,
        "aspect_ratio": args.aspect,
        "n": max(1, min(9, args.n)),
        "response_format": "base64",
        "aigc_watermark": bool(args.watermark),
    }
    if args.optimize:
        payload["prompt_optimizer"] = True
    if args.seed is not None:
        payload["seed"] = args.seed
    if args.ref:
        payload["subject_reference"] = build_subject_reference(args.ref)

    if args.dry_run:
        preview = dict(payload)
        if "subject_reference" in preview:
            preview["subject_reference"] = [
                {"type": "character", "image_file": "<base64 已省略，长度 %d>" % len(preview["subject_reference"][0]["image_file"])}
            ]
        print(json.dumps({"host": host, "endpoint": ENDPOINT, "payload": preview}, ensure_ascii=False, indent=2))
        return

    if not args.as_json:
        mode = "图生图（人物参考）" if args.ref else "文生图"
        print(f"[{mode}] model={args.model} aspect={args.aspect} n={payload['n']}", file=sys.stderr)

    started = time.time()
    result = call_api(payload, key, host)
    elapsed = time.time() - started

    base_resp = result.get("base_resp") or {}
    status = str(base_resp.get("status_code", ""))
    if status != "0":
        hint = ERROR_CODES.get(status, "未知错误")
        sys.exit(f"错误：status_code={status} ({hint})\n  status_msg: {base_resp.get('status_msg')}")

    data = result.get("data") or {}
    images = data.get("image_base64") or []
    metadata = result.get("metadata") or {}
    failed = int(metadata.get("failed_count") or 0)

    if not images:
        sys.exit("错误：接口返回成功但未包含图片数据"
                 + (f"（failed_count={failed}，可能被内容安全策略拦截）" if failed else ""))

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    stamp = time.strftime("%Y%m%d-%H%M%S")
    stem = slugify(args.name, limit=60) if args.name else f"{stamp}-{slugify(prompt)}"
    saved: list[str] = []
    for index, encoded in enumerate(images):
        suffix = f"-{index + 1}" if len(images) > 1 else ""
        path = out_dir / f"{stem}{suffix}.jpeg"
        path.write_bytes(base64.b64decode(encoded))
        saved.append(str(path.resolve()))

    if args.as_json:
        print(json.dumps({
            "task_id": result.get("id"),
            "model": payload["model"],
            "mode": "image-to-image" if args.ref else "text-to-image",
            "count": len(saved),
            "failed_count": failed,
            "elapsed_seconds": round(elapsed, 2),
            "files": saved,
        }, ensure_ascii=False, indent=2))
    else:
        print(f"完成：{len(saved)} 张，耗时 {elapsed:.1f}s")
        if failed:
            print(f"  注意：另有 {failed} 张被内容安全策略拦截，未返回", file=sys.stderr)
        for path in saved:
            print(path)


if __name__ == "__main__":
    main()
