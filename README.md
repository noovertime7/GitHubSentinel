# GitHub Sentinel

GitHub Sentinel 是一款开源的 AI Agent 工具，专为开发者和项目管理人员设计，用于自动跟踪和汇总 GitHub 仓库动态。通过定期获取订阅仓库的最新更新，帮助团队保持对项目进展的实时掌握。

## 🌟 主要特性

- **订阅管理**: 灵活订阅和管理感兴趣的 GitHub 仓库
- **自动更新**: 定期自动获取仓库最新动态
- **智能通知**: 及时推送重要更新和变更信息
- **报告生成**: 自动生成详细的更新报告
- **高度可配置**: 支持自定义更新频率和通知设置

## 🚀 快速开始

### 前置要求

- Python 3.8+
- GitHub Personal Access Token
- OpenAI API Key

### 安装

1. 克隆仓库
```bash
git clone https://github.com/noovertime7/github-sentinel.git
cd github-sentinel
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境
```bash
# 复制配置文件模板
cp config.example.yaml config.yaml
cp subscriptions.example.json subscriptions.json
```

4. 编辑配置文件
- 修改 `config.yaml`：
```yaml
github_token: "your_github_token"    # GitHub Personal Access Token
api_key: "your_openai_api_key"       # OpenAI API Key
update_interval: 3600                 # 更新间隔（秒）
```

- 修改 `subscriptions.json`：
```json
{
  "settings": {
    "hours": 24,     # 默认检查最近24小时的更新
    "auto_sync": true
  },
  "repositories": [
    {
      "name": "owner/repo",
      "hours": 12    # 可选，覆盖默认设置
    }
  ]
}
```

### 使用方法

[在这里添加具体的使用说明]

## ⚙️ 配置说明

主要配置项：

- `GITHUB_TOKEN`: GitHub Personal Access Token
- `UPDATE_INTERVAL`: 更新检查间隔（以秒为单位，默认 86400 秒/24小时）
- `notification_settings`: 通知相关配置
  - `enabled`: 是否启用通知
  - `frequency`: 通知频率

## 🛠️ 技术栈

- Python
- Pydantic
- python-dotenv
- [其他使用的主要技术]

## 📝 待办事项

- [ ] 添加更多的通知渠道支持
- [ ] 优化报告生成格式
- [ ] 添加 Web 界面
- [ ] 支持更多的订阅源类型

## 🤝 贡献指南

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目开发。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👥 作者

[noovertime7]

## 📬 联系方式

- 项目问题请提交 [Issue](https://github.com/noovertime7/GithubSentinel/issues)
- 其他问题请联系 [1849539179@qq.com]

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！
