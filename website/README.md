# Neurospan 企业官网

国际化、高端科技公司形象的单页官网，基于「让智能具备反身性，让组织拥有世界模型」的使命与「数字神经系统」愿景构建。

## 内容结构

- **Mission**：让智能具备反身性，让组织拥有世界模型；认知计算基础设施，加速 User AGI 与 Business AGI 的范式跃迁
- **Vision**：人类与机器共生进化的数字神经系统；蜂群智慧与个体觉醒并存的新纪元
- **Capabilities**：认知计算平台、世界模型与知识层、智能体与蜂群编排、企业级安全与治理
- **CTA**：联系与合作入口

## 使用方式

在项目根目录下：

```bash
# 用本地服务器打开（推荐）
cd website && python3 -m http.server 8080
# 浏览器访问 http://localhost:8080
```

或直接用浏览器打开 `website/index.html`。

## 国际化

- 页面默认使用英文主文案，`lang="zh-Hans"` 与 `data-i18n` 已预留，便于接入 i18n 脚本或替换为中文主站。
- 中文版可直接替换各 `data-i18n` 对应节点内的文案，或新增 `index-zh.html` 复用同一套样式。

## 部署到 Cases 静态服务器

网站可部署到 Cases 静态资源服务器（`/data/cases`，对外 `http://cases.wumaitech.com:8081`）：

```bash
# 在项目根目录执行，按提示确认
REMOTE_USER=你的SSH用户 ./scripts/deploy_website_to_cases.sh
```

可选环境变量：`REMOTE_HOST`（默认 cases.wumaitech.com）、`REMOTE_PATH`（默认 /data/cases）。部署后访问：http://cases.wumaitech.com:8081/

## 技术说明

- 纯静态：`index.html` + `styles.css`，无构建步骤
- 字体：Syne（标题）、DM Sans（正文），通过 Google Fonts 加载
- 响应式：支持移动端导航折叠与触控
