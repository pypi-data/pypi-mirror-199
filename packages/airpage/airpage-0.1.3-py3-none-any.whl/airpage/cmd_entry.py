import os.path

from airpage.core import *

new_main_content = f"""__author__ = '{os.getlogin()}'
from airpage import GetEnviron
env = GetEnviron(__file__)
''' ------------------ Environment Ready -------------------- '''
# Create your script here:
from page import *


"""
new_page_content = f"""from backend import *
Page('shut', Not(IDENTITY))     # page when game not start.
Page('main', IDNETITY)          # main page (like menu).

''' ------------------ Page Definition End -------------------- '''
# @transfer(page_a, page_b)
# Page.LinkWith(page_a, page_b, fn_a2b, fn_b2a)

Page.LinkWith(
    'shut',
    'main',
    sequence(XXX),  # How to start game
    sequence(XXX),  # How to close game
)

''' ------------------ Page Transition End -------------------- '''
# @page(page_name)
# Page.LoginTask(page_name, fn_task)

"""
new_backend_content = f"""from airpage import *
# define custom functions


"""
def NewProject(project_path:str):
    """
    新建airpage工程。
    :param project_path: 工程路径，可以是空的，也可以是已经刚刚由airtest创建的工程
    :return: bool 成功返回True，失败返回False
    """
    if project_path[-4:].lower() != '.air':
        error("TypeError", "Project path must be endwith '.air'")

    if os.path.exists(project_path):
        warn(f"Exists {project_path}, Failed to create.")
        return False
    else:
        ''' 不存在项目，可以开始快乐创建空项目了 '''
        os.makedirs(project_path)
        assert os.path.exists(project_path), f"Failed to create directory:{project_path}"

        # 创建主脚本
        fname = os.path.basename(project_path)
        if fname[-4:].lower() == '.air':
            fname = fname[:-4]
        with open(os.path.join(project_path, fname + '.py'), 'w') as f:
            f.write(new_main_content)

        # 创建page脚本
        with open(os.path.join(project_path, 'page.py'), 'w') as f:
            f.write(new_page_content)
        return True

def CMD_NewProject(*argv):
    if len(argv):
        return NewProject(*argv)
    else:
        print("Missing Parameter.\n", help(NewProject))

def CMD_Version(*argv):
    import pkg_resources
    print(f"airpage version:{pkg_resources.get_distribution('airpage').version}")

if __name__ == '__main__':
    CMD_Version()