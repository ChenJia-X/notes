import os
import shutil

# 替换文件的文件夹路径 C:\Users\man\Documents\WeChat Files\ZJUT-JC\Files\邀请好友\安卓
rootPath="D:\\man\\Documents\\work\\杭州司维科技有限公司\\UI\\支付超时\\android"
relativePath="\\"
copy_file_dir1 = rootPath+relativePath+"drawable-hdpi\\"
copy_file_dir2 = rootPath+relativePath+"drawable-xhdpi\\"
copy_file_dir3 = rootPath+relativePath+"drawable-xxhdpi\\"
copy_file_dirs = [copy_file_dir1, copy_file_dir2, copy_file_dir3]

# 被替换文件的文件夹路径
dir1 = "C:\\Users\\man\\AndroidStudioProjects\\fengxianwuyou\\app\\src\\main\\res\\drawable-hdpi\\"
dir2 = "C:\\Users\\man\\AndroidStudioProjects\\fengxianwuyou\\app\\src\\main\\res\\drawable-xhdpi\\"
dir3 = "C:\\Users\\man\\AndroidStudioProjects\\fengxianwuyou\\app\\src\\main\\res\\drawable-xxhdpi\\"
dirs = [dir1, dir2, dir3]

a = "支付超时"
b = "order_status_pay_timeout"
before_name = a + ".png"
target_name = b + ".png"
temp_name = ""

# 对替换文件改名
for copy_file_dir in copy_file_dirs:
    if os.path.exists(copy_file_dir + before_name):
        os.rename(copy_file_dir + before_name, copy_file_dir + target_name)
    else:
        print(copy_file_dir + before_name + "替换文件不存在")

# 删除被替换文件
for temp_dir in dirs:
    if os.path.exists(temp_dir + target_name):
        os.remove(temp_dir + target_name)
    else:
        print(temp_dir + target_name + "被替换文件不存在")

# 移动文件
count = 0  # 计数器
for copy_file_dir in copy_file_dirs:
    if os.path.exists(copy_file_dir + target_name):
        shutil.move(copy_file_dir + target_name, dirs[count] + target_name)
        print(copy_file_dir + target_name + "复制文件成功")
    else:
        print("复制文件失败")
    count += 1
