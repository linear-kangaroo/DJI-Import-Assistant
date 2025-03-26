# 🛬 DJI Import Assistant

一个帮助你自动识别大疆运动相机并导入素材的小工具，具备图形化界面、文件增量识别、路径迁移等实用功能。

---

## ✨ 功能亮点

- ✅ 自动识别设备（通过设备卷标名，如 DJI_Action2）
- 📂 按日期导入新文件，避免重复导入
- 🗂️ 可分类导入不同文件类型（如 .mp4, .jpg, .wav）
- 🔁 支持导入目录修改，并自动迁移历史文件
- 🗑️ 导入完成后询问是否清除相机原文件
- 🖥️ 简洁图形界面（使用 Tkinter）

---

## 🖥️ 使用方式

1. 插入你的 DJI 相机设备
2. 运行程序（`.exe` 文件或 `python dji_import_assistant.py`）
3. 点击“📥 导入新文件”
4. 可点击“🛠️ 更改导入目录”进行迁移和设置

---

## 📁 项目结构说明

```
DJI_Import_Assistant/
├── dji_import_assistant.py     # 主程序
├── config.json                 # 程序自动生成的导入记录文件（无需手动修改）
├── docs/                       # 开发文档目录
│   ├── 01_需求分析模板.md
│   ├── 02_功能设计模板.md
│   └── 03_任务拆解模板.md
├── CHANGELOG.md                # 更新日志
└── README.md                   # 项目说明（本文件）
```

---

## 🧠 开发文档入口

- [📌 需求分析](docs/01_需求分析模板.md)
- [⚙️ 功能设计](docs/02_功能设计模板.md)
- [✅ 任务拆解](docs/03_任务拆解模板.md)
- [📝 更新日志](CHANGELOG.md)

---

## 📦 打包说明

1. 安装依赖：
   ```bash
   pip install psutil pywin32
   ```

2. 打包：
   ```bash
   pyinstaller --onefile --windowed dji_import_assistant.py
   ```

---

## 📃 License

本项目基于 MIT License 开源。
