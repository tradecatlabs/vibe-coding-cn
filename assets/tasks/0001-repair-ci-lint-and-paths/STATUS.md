# STATUS — 任务真相源

## 状态机

- Status: **Done**
- Owner: 执行 Agent（待分配）
- Last Updated: 2026-02-27

## 仓库状态快照（Live Evidence）

### 分支与工作区

```text
branch: develop
dirty: ?? assets/repo/backups/gz/
```

### 关键失败信号（CI 等价命令）

```text
$ markdownlint --config .github/lint_config.json '**/*.md'
Cannot read or parse config file '.github/lint_config.json': ENOENT: no such file or directory, open '.github/lint_config.json'
```

### 候选配置验证（在 tasks 内部验证通过）

```text
$ markdownlint --config assets/tasks/0001-repair-ci-lint-and-paths/artifacts/lint_config.candidate.json '**/*.md'
EXIT:0
sha256: cac90c3741a847e181cc184cc593778467fad70da85acb683545608612a77cda
```

### 可应用补丁准备完成（仅生成补丁，不自动落地）

```text
$ git apply --check assets/tasks/0001-repair-ci-lint-and-paths/patches/0001-fix-ci-lint-and-paths.patch
OK
```

### 补丁已落地（仓库根验证）

```text
$ markdownlint --config .github/lint_config.json '**/*.md'
EXIT:0

$ make lint
EXIT:0

$ git status --porcelain=v1
(无 assets/repo/backups/gz 噪音)
```

### `make lint` 当前行为（存在假通过风险）

```text
Makefile: markdownlint **/*.md
/bin/sh -> dash（不支持 globstar）
```

## 阻塞详情

- Blocked by: 无

## 已执行命令（审计阶段）

- `git status --porcelain=v1`
- `sed -n '1,200p' Makefile`
- `sed -n '1,220p' .github/workflows/ci.yml`
- `markdownlint --config .github/lint_config.json '**/*.md'`
- `make lint`
- `git apply assets/tasks/0001-repair-ci-lint-and-paths/patches/0001-fix-ci-lint-and-paths.patch`
- `markdownlint --config .github/lint_config.json '**/*.md'`
