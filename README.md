# AI-python
平时网络巡检时，总要出一份报告。需要挨个登录设备查看，当设备一多时就变得很繁琐，要不停的重复导出，分析并写报告。当巡检遇上 python+AI，解放你的双手只需简单几步，让 python 为你收集信息， AI 为你分析给出报告。  
# Project Name

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![DeepSeekv3](https://img.shields.io/badge/DeepSeek-v3-006AFF?logo=deepseek&logoColor=white)](https://www.deepseek.com)


自动化工具：集成 OpenAI、网络设备操作与文档生成的智能工作流

## ✨ 功能特性
- **AI 集成**：通过 OpenAI API 实现自然语言交互
- **网络设备管理**：支持 SSH 连接 Cisco/Huawei 等主流网络设备
- **智能报告生成**：自动生成Markdown格式的报告
- **环境安全**：`.env` 文件管理敏感配置信息
- **本地大模型支持**：兼容 Ollama 本地模型服务

## 🚀 快速开始

### 安装依赖
```bash
# 安装核心依赖
pip install openai netmiko python-docx python-dotenv ollama
```
### 运行方式
```bash
python network_file.py
```
![image](https://github.com/user-attachments/assets/86392cff-b0c3-43ad-822c-9bc3f7971d57)
