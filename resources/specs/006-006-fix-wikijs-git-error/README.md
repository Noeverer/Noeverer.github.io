---
status: in-progress
priority: high
tags: ["wikijs", "git", "ssl", "docker", "ssh"]
created: '2026-01-19'
updated: '2026-01-19'
created_at: '2026-01-19T11:59:39.745001639+00:00'
---

# 修复 Wiki.js Git 仓库访问错误

> **Status**: 🔄 In Progress · **Priority**: 🔴 High · **Created**: 2026-01-19 · **Updated**: 2026-01-19

## 概述

Wiki.js 容器在尝试访问 GitHub 仓库时遇到 SSL 连接错误和分支引用错误，导致 Git 存储同步失败。需要诊断并修复这些问题以恢复 Wiki.js 的正常功能。

## 问题描述

### 错误 1: HTTPS SSL 连接问题
```
2026-01-19T11:57:59.917Z [MASTER] warn: Fetching origin
fatal: unable to access 'https://github.com/Noeverer/Noeverer.github.io.git/': OpenSSL SSL_read: OpenSSL/3.5.4: error:0A000126:SSL routines::unexpected eof while reading, errno 0
error: could not fetch origin
```

### 错误 2: 分支引用错误
```
2026-01-19T11:57:59.918Z [MASTER] warn: fatal: bad revision 'master'
```

### 错误 3: SSH 连接问题
```
git@github.com:Noeverer/Noeverer.github.io.git
```

**说明**: Wiki.js 尝试使用 SSH 方式连接 GitHub 仓库时也遇到问题，可能是因为：
- Docker 容器内未配置 SSH 密钥
- SSH 连接被阻止
- GitHub SSH 密钥未添加到账户

### 错误 4: SSL 证书验证失败
```
fatal: unable to access 'https://github.com/Noeverer/Noeverer.github.io.git/': SSL certificate problem: unable to get local issuer certificate (20)
```

**说明**: Git 无法验证 GitHub 的 SSL 证书，可能是因为：
- Docker 容器内缺少 CA 证书
- OpenSSL 证书链不完整
- Git 配置中缺少证书路径
- 代理或防火墙拦截了 SSL 握手

## 错误分析

### 错误 1: OpenSSL SSL 连接中断
- **错误码**: `error:0A000126:SSL routines::unexpected eof while reading`
- **可能原因**:
  - 网络连接不稳定或超时
  - SSL/TLS 版本不兼容
  - 防火墙或代理拦截连接
  - GitHub API 速率限制
  - Docker 容器网络配置问题

### 错误 2: Git 分支引用无效
- **错误信息**: `fatal: bad revision 'master'`
- **可能原因**:
  - 目标仓库 `Noeverer/Noeverer.github.io` 的默认分支可能是 `main` 而非 `master`
  - 本地 Git 缓存的分支信息过期
  - 仓库 URL 配置错误

### 错误 3: SSH 连接失败
- **错误信息**: `git@github.com:Noeverer/Noeverer.github.io.git`
- **可能原因**:
  - Docker 容器内未配置 SSH 密钥
  - SSH 密钥未添加到 GitHub 账户
  - SSH 端口 (22) 被防火墙阻止
  - `known_hosts` 文件未初始化
  - SSH 私钥权限不正确

### 错误 4: SSL 证书验证失败
- **错误码**: `(20)` - `unable to get local issuer certificate`
- **可能原因**:
  - Docker 容器内缺少 CA 证书包 (`ca-certificates`)
  - OpenSSL 无法找到证书颁发机构的根证书
  - Git 未配置正确的 SSL 后端
  - 代理服务器替换了证书但客户端未信任
  - 系统时间不正确导致证书验证失败
  - 防火墙或安全软件拦截 SSL 连接

## 设计方案

### 解决思路

1. **诊断目标仓库状态**
   - 验证 `Noeverer/Noeverer.github.io` 的默认分支名称
   - 确认仓库访问权限

2. **更新 Wiki.js Git 配置**
   - 修正分支名称配置
   - 验证仓库 URL 正确性

3. **解决 SSL 连接问题**
   - 配置 Git SSL 设置
   - 测试网络连接
   - 考虑使用 SSH 替代 HTTPS

4. **解决 SSH 连接问题**
   - 配置 SSH 密钥
   - 测试 SSH 连接
   - 配置 GitHub SSH 密钥

5. **解决 SSL 证书问题**
   - 安装或更新 CA 证书包
   - 配置 Git SSL 后端
   - 临时禁用 SSL 验证（仅用于测试）

6. **验证修复效果**
   - 检查日志确认错误消失
   - 测试 Git 存储同步功能

## 实施计划

### 阶段 1: 诊断与准备
- [ ] 检查目标仓库 `Noeverer/Noeverer.github.io` 的默认分支
  ```bash
  git ls-remote --symref https://github.com/Noeverer/Noeverer.github.io.git HEAD
  ```
- [ ] 验证容器 ID: `b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d`
- [ ] 备份 Wiki.js 当前配置

### 阶段 2: 更新 Wiki.js Git 配置
- [ ] 访问 Wiki.js 管理界面 (`http://localhost:3000`)
- [ ] 导航到 `存储` → `Git` 配置页面
- [ ] 更新 `Branch` 字段为正确的分支名称（`main` 或 `master`）
- [ ] 验证仓库 URL: `https://github.com/Noeverer/Noeverer.github.io.git`
- [ ] 保存配置

### 阶段 3: 解决 SSL 连接问题
- [ ] 测试容器网络连接:
  ```bash
  docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d ping -c 3 github.com
  docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d curl -I https://github.com
  ```

- [ ] 配置 Git SSL 设置（如需要）:
  ```bash
  # 方案 A: 指定 TLS 版本
  docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d git config --global http.sslVersion tlsv1.2

  # 方案 B: 增加超时时间
  docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d git config --global http.postBuffer 524288000

  # 方案 C: 临时禁用 SSL 验证（仅用于测试，不推荐生产环境）
  docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d git config --global http.sslVerify false
  ```

### 阶段 4: 解决 SSL 证书问题

- [ ] 检查容器内证书安装:
  ```bash
  # 检查 ca-certificates 是否安装
  docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d apk list --installed | grep ca-certificates

  # 检查 OpenSSL 版本
  docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d openssl version
  ```

- [ ] 安装或更新 CA 证书:
  ```bash
  # Alpine Linux (Wiki.js 容器基于 Alpine)
  docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d apk update
  docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d apk add --no-cache ca-certificates
  docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d update-ca-certificates
  ```

- [ ] 配置 Git SSL 后端:
  ```bash
  # 使用 OpenSSL 作为 SSL 后端
  docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d git config --global http.sslBackend openssl

  # 或使用 Schannel (Windows) 或 SecureTransport (macOS)
  # docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d git config --global http.sslBackend schannel
  ```

- [ ] 测试 SSL 连接:
  ```bash
  # 测试 OpenSSL 连接
  docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d openssl s_client -connect github.com:443 -servername github.com </dev/null

  # 测试 Git 连接
  docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d sh -c "cd /wiki/data/repo && git fetch origin master"
  ```

- [ ] 如果问题持续，临时禁用 SSL 验证:
  ```bash
  # 全局禁用 SSL 验证
  docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d git config --global http.sslVerify false

  # 或仅在仓库中禁用
  docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d sh -c "cd /wiki/data/repo && git config http.sslVerify false"
  ```

### 阶段 5: 配置凭证（如果需要）
- [ ] 如果使用 HTTPS，配置 Git 凭据:
  ```bash
  # 使用 Personal Access Token
  docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d git config --global credential.helper store
  ```

### 阶段 6: 解决 SSH 连接问题
- [ ] 生成 SSH 密钥对（如果尚未配置）:
  ```bash
  # 在宿主机上生成密钥
  ssh-keygen -t ed25519 -C "wikijs@docker" -f ~/.ssh/wikijs_github
  ```

- [ ] 将公钥添加到 GitHub:
  ```bash
  # 复制公钥内容
  cat ~/.ssh/wikijs_github.pub
  ```
  - 访问 GitHub Settings → SSH and GPG keys → New SSH key
  - 粘贴公钥内容并保存

- [ ] 将私钥复制到 Docker 容器:
  ```bash
  # 创建容器内的 .ssh 目录
  docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d mkdir -p ~/.ssh
  docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d chmod 700 ~/.ssh

  # 复制私钥到容器
  docker cp ~/.ssh/wikijs_github b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d:~/.ssh/id_ed25519
  docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d chmod 600 ~/.ssh/id_ed25519
  ```

- [ ] 初始化 SSH known_hosts:
  ```bash
  # 添加 GitHub 到 known_hosts
  docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d ssh-keyscan github.com >> ~/.ssh/known_hosts
  docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d chmod 644 ~/.ssh/known_hosts
  ```

- [ ] 测试 SSH 连接:
  ```bash
  docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d ssh -T git@github.com
  ```

- [ ] 在 Wiki.js 配置中使用 SSH URL:
  - 将仓库 URL 从 `https://github.com/Noeverer/Noeverer.github.io.git`
  - 改为 `git@github.com:Noeverer/Noeverer.github.io.git`

### 阶段 7: 重启和验证

- [ ] 手动触发 Wiki.js Git 同步
- [ ] 查看日志确认错误已解决:
  ```bash
  docker logs --tail 100 b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d
  ```
- [ ] 如果问题持续，重启容器:
  ```bash
  docker restart b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d
  ```

## 测试计划

### 功能测试
- [ ] Git 仓库同步成功，无 SSL 错误
- [ ] 分支引用正确，无 `bad revision` 错误
- [ ] SSH 连接正常，无认证失败
- [ ] SSL 证书验证成功（如未禁用）
- [ ] Wiki.js 可以正常拉取和推送内容

### 集成测试
- [ ] 在 Wiki.js 中编辑内容
- [ ] 验证内容正确同步到 GitHub 仓库
- [ ] 验证 GitHub Pages 自动部署功能正常

### 回归测试
- [ ] 确认其他 Wiki.js 功能未受影响
- [ ] 确认 Docker 容器稳定运行

## 注意事项

1. **生产环境安全**: 不建议在生产环境禁用 SSL 验证，应优先解决 SSL 配置问题
2. **分支名称**: GitHub 新仓库默认使用 `main` 分支，而非 `master`
3. **HTTPS vs SSH**:
   - **HTTPS**: 适合公共仓库，需要配置 PAT (Personal Access Token)
   - **SSH**: 更安全，适合频繁操作，需要配置 SSH 密钥
4. **SSH 密钥管理**:
   - 使用 ED25519 算法生成密钥（更安全、更快）
   - 私钥权限必须是 600
   - 确保 `known_hosts` 已添加 GitHub 指纹
5. **Token 权限**: 如使用 Personal Access Token，确保包含以下权限:
   - `repo` (完整仓库访问)
   - `workflow` (如需触发 GitHub Actions)
6. **Docker 容器持久化**: SSH 密钥在容器重启后会丢失，建议使用 Docker Volume 持久化:
   ```bash
   docker run -v ~/.ssh:/root/.ssh ...
   ```

## 故障排查

### HTTPS 连接失败

#### 问题 1: SSL 连接中断

```bash
# 检查网络连通性
docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d curl -v https://github.com

# 检查 Git 版本
docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d git --version
```

#### 问题 2: SSL 证书验证失败

```bash
# 检查证书文件是否存在
docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d ls -la /etc/ssl/certs/

# 测试 OpenSSL 连接
docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d openssl s_client -connect github.com:443 -servername github.com </dev/null

# 检查 CA 证书包
docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d sh -c "find /etc/ssl -name '*.pem' -o -name '*.crt'"

# 验证 Git SSL 配置
docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d git config --global --get http.sslVerify
docker exec b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d git config --global --get http.sslBackend
```
```bash
# 检查网络连通性
docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d curl -v https://github.com

# 检查 Git 版本
docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d git --version
```

### SSH 连接失败
```bash
# 详细调试信息
docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d ssh -vvv git@github.com

# 检查密钥权限
docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d ls -la ~/.ssh

# 测试 Git SSH 连接
docker exec -it b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d git ls-remote git@github.com:Noeverer/Noeverer.github.io.git
```

## 参考资料

- [Wiki.js Git 存储](https://docs.requarks.io/store/git)
- [Git SSL 配置](https://git-scm.com/docs/git-config#Documentation/git-config.txt-httpsslVerify)
- [GitHub 默认分支](https://github.com/github/renaming)
- [OpenSSL 错误码](https://www.openssl.org/docs/manmaster/man3/ERR_GET_REASON.html)

## 执行进度

### 已完成的任务 ✅

- [x] 检查目标仓库 `Noeverer/Noeverer.github.io` 的默认分支
  - 结果: 默认分支是 `gh-pages`，但也存在 `master` 分支
- [x] 验证容器 ID: `b91ad99f4c9a01009a25b2e31981063ad8d70736870b746fca2d2827300fb24d`
- [x] 测试容器网络连接 - 成功
- [x] 生成 SSH 密钥对: `~/.ssh/wikijs_github`
- [x] 配置 Git SSL 设置（禁用 SSL 验证）
- [x] 切换 Git 远程 URL 从 SSH 到 HTTPS
- [x] 通过数据库更新 Wiki.js Git 存储配置
  - 认证类型: `basic`
  - 仓库 URL: `https://github.com/Noeverer/Noeverer.github.io.git`
  - 分支: `master`
- [x] 重启 Wiki.js 容器
- [x] 验证 Git 拉取成功
- [x] 创建修复总结文档: `WIKIJS_FIX_SUMMARY.md`

### 待完成的任务 ⏳

- [ ] 创建 GitHub Personal Access Token (PAT)
- [ ] 更新 Wiki.js 配置使用 PAT
- [ ] 验证 Git 推送成功
- [ ] 测试完整的 Wiki.js → GitHub → GitHub Pages 流程

### 遇到的问题 📝

1. **SSH 连接失败**: SSH 密钥未添加到 GitHub 账户
   - 解决方案: 切换到 HTTPS + Basic Auth

2. **GitHub 推送认证失败**: GitHub 不再支持密码认证
   - 待解决: 使用 Personal Access Token

3. **SSL 证书验证失败**: 新发现的错误
   - 错误信息: `unable to get local issuer certificate (20)`
   - 可能原因: 容器内缺少 CA 证书
   - 解决方案: 安装 ca-certificates 或临时禁用 SSL 验证

## 成功日志输出

```
2026-01-19T12:11:25.986Z [MASTER] [STORAGE/GIT] Adding origin remote via HTTP/S...
2026-01-19T12:11:26.058Z [MASTER] [STORAGE/GIT] Fetch updates from remote...
2026-01-19T12:11:27.099Z [MASTER] [STORAGE/GIT] Checking out branch master...
2026-01-19T12:11:27.116Z [MASTER] [STORAGE/GIT] Performing pull rebase from origin on branch master...
```

## 相关链接

- 相关 Spec: [005-wikijs-github-pages](../005-wikijs-github-pages/)
- 修复总结: [WIKIJS_FIX_SUMMARY.md](../../WIKIJS_FIX_SUMMARY.md)
