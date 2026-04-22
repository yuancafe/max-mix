# max-mix

MiniMax 多模态技能包，统一封装为可复用的 Agent Skills。

## Skills

- `max-image-gen` - 图片生成（image-01）
- `max-video-gen` - 视频生成（Hailuo）
- `max-tts` - 文本转语音（speech-hd）
- `max-voice-clone` - 音色复刻（upload/clone）
- `max-music-gen` - 音乐生成（music-2.5/2.6）
- `max-music-cover` - 音乐翻唱（music-cover）
- `max-search` - 搜索（coding-plan-search，direct-first）
- `max-vision` - 图像理解/OCR（coding-plan-vlm，direct-first）
- `max-text-chat` - 文本/编程对话（MiniMax-M*）

## Workflow

- 生成类技能默认支持 `plan -> run`
- `max-search` / `max-vision` 默认 direct-run，同时保留可选 `plan/run`

## Install

```bash
bash ./install.sh
bash ./check-deps.sh
```

## Security

- 本仓库 **不包含** 明文 API key。
- 运行时从以下位置读取：
  - 环境变量 `MINIMAX_API_KEY`
  - `~/.mmx/config.json`（由 `mmx auth login` 生成）
- 请勿将本地配置文件提交到 Git。

## Quick Examples

```bash
python3 skills/max-image-gen/scripts/max_image_gen.py plan --interactive
python3 skills/max-image-gen/scripts/max_image_gen.py run --plan-file <plan.json>

python3 skills/max-search/scripts/max_search.py --q "MiniMax latest updates"
python3 skills/max-vision/scripts/max_vision.py --image ./shot.png --prompt "Extract text"
```
