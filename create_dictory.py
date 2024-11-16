import os

# 要创建的目录结构
directories = [
    "xizang/xizang",
    "xinjiang/xinjiang",
    "sichuan/sichuan",
    "qinghai/qinghai",
    "neimeng/neimeng",
    "gansu/gansu"
]

# 遍历并创建每个目录
for directory in directories:
    # 使用 os.makedirs 来递归创建目录
    os.makedirs(directory, exist_ok=True)

print("目录创建完成！")
