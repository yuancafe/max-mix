# RELEASE

## EN

## Versioning

Recommended semantic style:

- `v0.1.0` initial public release
- `v0.1.x` docs/fixes
- `v0.2.0` new skills or breaking workflow changes

## Current Release

- Version: `v0.1.0`
- Highlights:
  - 9 skills included
  - bilingual `README.md` and `QUICKSTART.md`
  - `plan -> run` workflow for generation skills
  - direct-first flow for `max-search` and `max-vision`

## Release Checklist

1. Run dependency checks

```bash
bash ./check-deps.sh
```

2. Verify install script

```bash
bash -n ./install.sh
```

3. Spot-check key flows

```bash
python3 skills/max-search/scripts/max_search.py --q "hello" --dry-run
python3 skills/max-vision/scripts/max_vision.py --image ./example.png --prompt "describe" --dry-run
python3 skills/max-image-gen/scripts/max_image_gen.py plan --prompt "test" --plan-file /tmp/p.json
python3 skills/max-image-gen/scripts/max_image_gen.py run --plan-file /tmp/p.json --dry-run
```

4. Secret scan

- Ensure no raw API keys are committed.
- Keep credentials only in env vars or local runtime config.

5. Commit and tag

```bash
git add .
git commit -m "release: v0.1.0"
git tag v0.1.0
git push && git push --tags
```

## Changelog

### v0.1.0

- Initial public package `max-mix`
- Added 9 MiniMax skills:
  - max-image-gen
  - max-video-gen
  - max-tts
  - max-voice-clone
  - max-music-gen
  - max-music-cover
  - max-search
  - max-vision
  - max-text-chat
- Added bilingual docs

---

## 中文

## 版本策略

建议语义化版本：

- `v0.1.0` 首次公开发布
- `v0.1.x` 文档与修复
- `v0.2.0` 新增技能或流程变更

## 当前发布

- 版本：`v0.1.0`
- 亮点：
  - 包含 9 个技能
  - `README.md` 与 `QUICKSTART.md` 双语
  - 生成类技能支持 `plan -> run`
  - `max-search` / `max-vision` 默认直连调用

## 发布检查清单

1. 依赖检查

```bash
bash ./check-deps.sh
```

2. 安装脚本语法检查

```bash
bash -n ./install.sh
```

3. 关键流程抽样验证

```bash
python3 skills/max-search/scripts/max_search.py --q "hello" --dry-run
python3 skills/max-vision/scripts/max_vision.py --image ./example.png --prompt "describe" --dry-run
python3 skills/max-image-gen/scripts/max_image_gen.py plan --prompt "test" --plan-file /tmp/p.json
python3 skills/max-image-gen/scripts/max_image_gen.py run --plan-file /tmp/p.json --dry-run
```

4. 敏感信息检查

- 确认仓库中没有明文 API key
- 凭据仅保留在环境变量或本地配置

5. 提交并打标签

```bash
git add .
git commit -m "release: v0.1.0"
git tag v0.1.0
git push && git push --tags
```

## 变更记录

### v0.1.0

- 首次公开发布 `max-mix`
- 新增 9 个 MiniMax 技能：
  - max-image-gen
  - max-video-gen
  - max-tts
  - max-voice-clone
  - max-music-gen
  - max-music-cover
  - max-search
  - max-vision
  - max-text-chat
- 新增双语文档
