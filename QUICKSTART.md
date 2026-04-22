# QUICKSTART

## EN (5 minutes)

### Step 1: Install dependencies

```bash
# if mmx is not installed
npm install -g mmx-cli
```

### Step 2: Login MiniMax

```bash
mmx auth login --api-key <YOUR_MINIMAX_API_KEY>
mmx quota show
```

### Step 3: Install skills

```bash
cd /Users/yuan/Code/lab/max-mix
bash ./install.sh
bash ./check-deps.sh
```

### Step 4: Try direct-first skills

```bash
python3 skills/max-search/scripts/max_search.py --q "MiniMax latest updates"
python3 skills/max-vision/scripts/max_vision.py --image ./example.png --prompt "Describe this image"
```

### Step 5: Try plan->run skill

```bash
python3 skills/max-image-gen/scripts/max_image_gen.py plan --interactive
python3 skills/max-image-gen/scripts/max_image_gen.py run --plan-file <plan.json>
```

---

## 中文（5 分钟）

### 第 1 步：安装依赖

```bash
# 如果还没安装 mmx
npm install -g mmx-cli
```

### 第 2 步：登录 MiniMax

```bash
mmx auth login --api-key <YOUR_MINIMAX_API_KEY>
mmx quota show
```

### 第 3 步：安装技能包

```bash
cd /Users/yuan/Code/lab/max-mix
bash ./install.sh
bash ./check-deps.sh
```

### 第 4 步：体验直连技能

```bash
python3 skills/max-search/scripts/max_search.py --q "MiniMax 最新动态"
python3 skills/max-vision/scripts/max_vision.py --image ./example.png --prompt "描述这张图片"
```

### 第 5 步：体验 plan->run 技能

```bash
python3 skills/max-image-gen/scripts/max_image_gen.py plan --interactive
python3 skills/max-image-gen/scripts/max_image_gen.py run --plan-file <plan.json>
```
