import subprocess
import os

os.chdir('/Users/howdy/github_project/MultiAgent-WebUI')

# 尝试恢复代码
print("尝试从git恢复代码...")

# 重置所有修改
result = subprocess.run(['git', 'reset', '--hard', 'HEAD'], capture_output=True, text=True)
print("git reset --hard HEAD:", result.stdout, result.stderr)

# 检查状态
result = subprocess.run(['git', 'status'], capture_output=True, text=True)
print("git status:", result.stdout, result.stderr)

print("恢复完成！")