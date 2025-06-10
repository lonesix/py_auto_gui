```

```

## 项目功能概括

这是一个专为网站：[Guess the PIN](https://www.guessthepin.com/)设计的**PIN码暴力破解自动化工具**，主要功能包括：

### 核心功能

- **自动化PIN码尝试**：从8999倒序尝试到7999，自动在指定的输入框中输入PIN码**（可更改相关代码）**
- **智能区域监控**：通过截图和OCR文字识别技术监控两个区域的变化
- **结果判断机制**：
  - 监控错误提示区域，检测是否出现"Sorry"文字来判断PIN码错误
  - 监控数字显示区域，确认PIN码输入是否生效
- **交互式坐标设置**：通过鼠标点击设置PIN输入框位置和监控区域坐标
- **实时进度显示**：显示尝试进度、耗时统计和执行速度当前

### 优化

当前逻辑较慢，待优化。

### 技术特点

- 使用PyAutoGUI进行GUI自动化操作
- 集成Tesseract OCR引擎进行文字识别
- 采用Windows API获取鼠标位置和状态
- 具备异常处理和用户中断保护机制

## 环境配置方法

### 1. Python依赖包安装

文件位置：[requirements.txt](requirements.txt)

使用以下命令安装所需的Python包：

```bash
pip install -r requirements.txt
```

### 2. Tesseract OCR引擎配置

**Windows系统安装步骤：**

1. 下载Tesseract OCR安装包：https://github.com/UB-Mannheim/tesseract/wiki
2. 安装到默认路径：`C:\Program Files\Tesseract-OCR\`
3. 代码中已配置OCR路径，如安装到其他位置需修改路径

文件位置：[guess_pin.py](guess_pin.py)

**其他系统安装方法：**

- macOS：`brew install tesseract`
- Ubuntu/Debian：`sudo apt-get install tesseract-ocr`

### 3. 系统要求

- Windows系统（因使用了win32api）
- Python 3.7+
- 支持图形界面的桌面环境

### 4. 使用前准备

运行程序后需要通过鼠标点击设置5个关键位置：

1. PIN输入框位置
2. 错误提示区域的左上角和右下角坐标
3. 数字显示区域的左上角和右下角坐标

程序会自动计算监控区域范围并开始执行PIN码破解任务。
