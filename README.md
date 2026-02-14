# Diaries 📓

一个简约现代的本地日记 Web 应用，专为个人记录生活而设计。支持富文本（标题、副标题、正文）和最多 9 张图片的上传与展示，所有数据均保存在本地 SQLite 数据库中，图片存储在 `static/uploads` 文件夹。

---

## ✨ 功能特点

- **记录日记**：填写标题、副标题、正文，并上传 0-9 张图片。
- **图片预览**：选择图片后实时预览，可删除已选图片。
- **往期回顾**：以卡片网格形式展示所有日记，每篇日记显示标题、日期、正文预览及图片缩略图。
- **日记详情页**：点击卡片可查看完整日记内容及所有大图。
- **粉青主题**：柔和的主色调，搭配霞鹜文楷（中文字体）与 Montserrat（英文字体），阅读舒适。
- **响应式设计**：在手机、平板和电脑上均可获得良好体验。
- **纯本地存储**：无需联网，所有数据保存在你的电脑中。

---

## 🛠️ 技术栈

- 后端：Python + Flask（轻量级 Web 框架）
- 数据库：SQLite（内置，无需额外安装）
- 前端：原生 HTML / CSS / JavaScript
- 字体：Google Fonts（Montserrat, LXGW WenKai）

---

## 📁 项目结构

```
my_diary/
├── app.py                 # 主程序入口
├── database.db            # SQLite 数据库文件（首次运行自动生成）
├── requirements.txt       # 依赖列表
├── templates/             # HTML 模板文件夹
│   ├── homepage.html      # 首页
│   ├── update.html        # 上传新日记页
│   ├── success.html       # 提交成功页
│   ├── failure.html       # 提交失败页
│   ├── flashback.html     # 往期日记列表页
│   └── view.html          # 日记详情页
└── static/                # 静态文件
    └── uploads/           # 上传图片存储目录（自动创建）
```

---

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名
```

### 2. 创建虚拟环境（可选，但推荐）
```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```
> 如果尚未生成 `requirements.txt`，可手动安装 Flask：
> ```bash
> pip install flask
> ```

### 4. 运行应用
```bash
python app.py
```
启动后，终端会显示类似 `Running on http://127.0.0.1:5000` 的地址，在浏览器中打开即可访问。

---

## 🖥️ 使用说明

- **首页** (`/`)：欢迎页，有两个按钮：“上传新日记”和“查看往期所有日记”。
- **上传新日记** (`/update/`)：填写标题、副标题、正文，点击“添加图片”按钮可选择多张图片（最多 9 张），点击“提交日记”保存。
- **提交成功** (`/update/success/`)：显示成功信息，可返回首页。
- **往期日记** (`/flashback/`)：所有日记按更新时间倒序排列，点击任意卡片可查看详情。
- **日记详情** (`/diary/<id>`)：显示完整日记内容及所有图片。

---

## ⚙️ 配置说明

- **数据库**：默认使用当前目录下的 `diaries.db`，首次运行自动创建表结构。
- **图片上传**：图片保存在 `static/uploads` 文件夹，支持扩展名 `png, jpg, jpeg, heic`，单个日记最多 9 张。
- **文件大小限制**：整个请求（含图片）默认最大 **48MB**（可在 `app.py` 中修改 `MAX_CONTENT_LENGTH`）。
- **时区**：由于 SQLite 的 `CURRENT_TIMESTAMP` 返回 UTC 时间，应用在显示时手动增加了 8 小时（东八区）。如果你在其他时区，请调整代码中的 `timedelta(hours=8)`。

---

## 🧪 开发说明

- **修改密钥**：`app.secret_key` 默认是示例值，生产环境建议改为强随机字符串。
- **添加依赖**：如需使用第三方库，请更新 `requirements.txt`：
  ```bash
  pip freeze > requirements.txt
  ```

---

## 📄 许可证

本项目仅供个人学习使用，未经许可不得用于商业用途。

---

## 💬 问题反馈

如果在使用中遇到任何问题，欢迎在 GitHub 仓库提交 Issue，或直接联系作者。

---

**Happy Journaling!** 🎉
