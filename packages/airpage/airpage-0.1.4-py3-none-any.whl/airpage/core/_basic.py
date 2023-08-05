import os
import sys
import time
import uuid
import files3
import random
import typing
import winreg
import platform

import pyautogui
from airtest.core.api import *
from airtest.core.cv import Predictor
from concurrent.futures import ThreadPoolExecutor

''' -------------------------------------------------- '''

cpu_count = os.cpu_count()
pyautogui.FAILSAFE=False


if platform.system() == 'Windows':
    # redirect user-environ to system-environ
    reg_path = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
    reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
    system_environment_variables = winreg.QueryValueEx(reg_key, 'Path')[0]
    os.environ["PATH"] = system_environment_variables

def GetTempName():
    """
    获取一个临时名称，所有临时名称之间不会重复
    :return: str
    """
    return str(uuid.uuid1())

class __Null__():
    def __bool__(self):
        return False
Null = __Null__()

class DeviceExceoption(Exception):
    ...

def GetDevice():
    if G.DEVICE is None:
        raise DeviceExceoption("\n\tDEVICE is NoneType. Please check your device connection and program entrance.")
    return G.DEVICE

def time2str(_time, _fmt_level=0) -> str:
    """
    将标准时间戳转化为项目中标准的字符串格式
    :Param _fmt_level:
        0  %Y-%m-%d
        1  %H:%M:%S
        2  %Y-%m-%d %H:%M:%S
    """
    '''Select'''
    if _fmt_level == 0:
        _fmt = "%Y-%m-%d"
    elif _fmt_level == 1:
        _fmt = "%H:%M:%S"
    elif _fmt_level == 2:
        _fmt = "%Y-%m-%d %H:%M:%S"
    else:
        raise Exception("[Basic - ERROR]: Unknown time-fmt type.")

    '''Translation'''
    time_struct = time.localtime(_time)
    date_string = time.strftime(_fmt, time_struct)
    return date_string

''' ------------------------------- Basic Functions End ---------------------------------------- '''

def label(desc):
    print(f'[Label]: {desc}')
    return True

def debug(*why):
    txt = '[Debug]:\n'
    for each in why:
        txt += '\t' + each + '\n'
    print(txt)
    # G.LOGGING.debug(txt)
    return True

def info(*why):
    txt = '[Info]:\n'
    for each in why:
        txt += '\t' + each + '\n'
    print(txt)
    # G.LOGGING.info(txt)
    return True

def warn(*why):
    txt = '[Warning]:\n'
    for each in why:
        txt += '\t' + each + '\n'
    print(txt)
    # G.LOGGING.warning(txt)
    return True

def error(err_type: str, *why):
    txt = "\n\n[{}]:".format(err_type)
    for each in why:
        txt += "\n\t" + str(each)
    txt += "\n"
    print(txt)
    # G.LOGGING.error(txt)
    raise type(err_type, (Exception, ), {})(txt)

''' ---------------------------------- Basic Information functions End ----------------------------------- '''
def ap_pos(record_pos_x, record_pos_y):
    """
    将airtest的相对百分比坐标转换为device的相对坐标
    airtest百分比坐标原点位于device的屏幕中心
    :param record_pos_x: 百分比坐标的x部分 -0.5 - 0.5
    :param record_pos_y: 百分比坐标的y部分 -0.5 - 0.5
    :return: tuple(x, y)
    """
    return Predictor.get_predict_point((record_pos_x, record_pos_y), GetDevice().get_current_resolution())

def ap_area(tpl:Template, toint=False):
    """
    根据template在当前的screen中确定对应的区域
    :param tpl: 根据template在当前的screen中确定对应的区域
    :return: tuple(x0, y0, x1, y1)
    """
    image_hw = tpl._imread().shape[:2]
    area = Predictor.get_predict_area(tpl.record_pos, (image_hw[1], image_hw[0]), tpl.resolution, GetDevice().get_current_resolution())
    if toint:
        area = int(area[0] + 0.5), int(area[1] + 0.5), int(area[2] + 0.5), int(area[3] + 0.5)
    return area

def wait_results(tasks, timeout=ST.FIND_TIMEOUT, interval=0.5):
    """
    等待由ThreadPoolExecutor创建的所有task完全执行结束
    :param tasks: list of (由ThreadPoolExecutor创建的所有task)
    :param timeout: 超时时间
    :param interval: 间隔时间
    :return: whether all success(all ok will return True, False else), list of result(No result will replace with Null)
    """
    flag, length = False, len(tasks)
    results = [Null for i in range(length)]

    timeout_time = time.time() + timeout

    while time.time() <= timeout_time:
        flag = True
        time.sleep(interval)
        for i, task in enumerate(tasks):
            if results[i] is Null:
                if task.done():
                    results[i] = task.result()
                else:
                    flag = False

        if flag:
            break


    return flag, results

_global_screens = {
    False: None  # 默认截图
}

def GlobalScreen_Update(sid=True):
    """
    更新屏幕截图
    :param sid: 更新截图到指定的screen index下(默认保存到False下)
    :return:
    """
    _global_screens[sid] = GetDevice().snapshot(filename=None, quality=ST.SNAPSHOT_QUALITY)
    return True

def GlobalScreen_Flush(sid=False):
    _global_screens[sid] = None
    return True

def GlobalScreen_Write(sid=False, _screen=None):
    _global_screens[sid] = _screen
    return True

def GlobalScreen_Read(sid=False):
    return _global_screens[sid]

def GetScreen(snapshot=True):
    tmp = _global_screens.get(snapshot)
    if snapshot is True or tmp is None:
        return GetDevice().snapshot(filename=None, quality=ST.SNAPSHOT_QUALITY)
    return tmp


def ap_wait(querys, *, timeout=ST.FIND_TIMEOUT, threshold=None, interval=0.5, snapshot=True):
    """
    升级版loop_find
    这段代码修改自airtest.core.cv.loop_find,
        * 去除其中的报错部分，改为返回None
        * 线程池调度，支持并发检测


    Args:
        fn_return: 返回函数，用于输出返回值
        querys: image template to be found in screenshot. Can be single tpl or multiple tpls
        timeout: time interval how long to look for the image template
        threshold: default is None
        interval: sleep interval before next attempt to find the image template
        snapshot: bool 是否进行snapshot。如果为False，那么优先使用globalscreen；但是如果globalscreen为None，那么还是会进行snapshot

    Returns:
        None or Position( or list of [None or Position])

    """

    isi_tpl = isinstance(querys, Template)
    isi_lt = isinstance(querys, (list, tuple))
    length = 1 if isi_tpl else len(querys)

    assert isi_tpl or (isi_lt and length > 0), f"Unexpected querys: {querys}"

    # ------

    G.LOGGING.info("Try finding: %s", querys)
    if length == 1:
        tpl = querys if isi_tpl else querys[0]

        start_time = time.time()
        while True:
            screen = GetScreen(snapshot)

            if screen is None:
                G.LOGGING.warning("Screen is None, may be locked")
            else:
                if threshold:
                    tpl.threshold = threshold
                match_pos = tpl.match_in(screen)
                if match_pos:
                    try_log_screen(screen)
                    return match_pos if isi_tpl else [match_pos]

            # 超时返回None，否则等待下次操作，
            if (time.time() - start_time) > timeout:
                try_log_screen(screen)
                G.LOGGING.info("Failed finding: %s", tpl)
                return False if isi_tpl else [False]
            else:
                time.sleep(interval)
    else:
        '''
        内存池的大小选取原则:
        一般来说，我们线程池究竟设置多大是基于要线程池任务来分析的，不同的任务类型，我们设置的方式当然也需要改变。
        通常的任务类型一般是：CPU密集型、IO密集型，对不同类型的任务我们就需要分配不同大小的线程池
        1)、CPU密集型
        这种任务我们要尽量使用较小的线程池，一般是Cpu核心数+1
        因为CPU密集型任务CPU的使用率很高，若开过多的线程，只能增加线程上下文的切换次数，带来额外的开销
        2)、IO密集型
        方法一：可以使用较大的线程池，一般CPU核心数 * 2
        IO密集型CPU使用率不高，可以让CPU等待IO的时候处理别的任务，充分利用cpu时间
        方法二：线程等待时间所占比例越高，需要越多线程。线程CPU时间所占比例越高，需要越少线程。
        '''
        pool = ThreadPoolExecutor(max_workers=min(cpu_count + 1, length))

        left = length
        results = [Null for i in range(length)]

        start_time = time.time()
        while left > 0:
            screen = GetScreen(snapshot)

            if screen is None:
                G.LOGGING.warning("Screen is None, may be locked")
            else:
                # 创建仍需match的任务表和对应映射表
                tasks, fntable = [ ], [ ]
                for i, tpl in enumerate(querys):
                    if results[i] is Null:
                        tmp = pool.submit(tpl.match_in, screen)
                        tasks.append(tmp)
                        fntable.append(i)

                _, task_results = wait_results(tasks, timeout, interval)

                for t, item in enumerate(task_results):
                    if item is not Null:
                        results[fntable[t]] = item
                        left -= 1

                # 超时对应元素返回None，否则等待下次操作，
                if (time.time() - start_time) > timeout:
                    try_log_screen(screen)

                    querys_timeout = []
                    for i, result in enumerate(results):
                        if result is Null:
                            results[i] = None  # 修改Null为None
                            querys_timeout.append(querys[i])

                    G.LOGGING.info("Failed finding: %s", querys_timeout)
                    break
                else:
                    time.sleep(interval)

        pool.shutdown()

        return results


def ap_exists(querys, *, threshold=None, snapshot=False):
    """
    like ap_wait, but timeout is 0, which mean this function only check screen once
    :param querys:
    :param threshold:
    :param snapshot:
    :return:
    """
    return ap_wait(querys, timeout=0, threshold=threshold, snapshot=snapshot)


def ap_touch(v, *, times=1, match=True, delay=None, timeout=ST.FIND_TIMEOUT, threshold=None, interval=0.5, snapshot=True, **kwargs):
    """
    这段代码修改自airtest.touch

    Perform the touch action on the device screen

    :param v: target to touch, either a ``Template`` instance or absolute coordinates (x, y)
    :param times: how many touches to be performed
    :param match: bool whether match template on screen. If False mean click the position about template.
    :param kwargs: platform specific `kwargs`, please refer to corresponding docs
    :return: finial position to be clicked, e.g. (100, 100)
    :platforms: Android, Windows, iOS
    :Example:
        Click absolute coordinates::

        >>> touch((100, 100))

        Click the center of the picture(Template object)::

        >>> touch(Template(r"tpl1606730579419.png", target_pos=5))

        Click 2 times::

        >>> touch((100, 100), times=2)

        Under Android and Windows platforms, you can set the click duration::

        >>> touch((100, 100), duration=2)

        Right click(Windows)::

        >>> touch((100, 100), right_click=True)

    """
    # assert fn_return is not None, "This function must have fn_return!"
    if isinstance(v, Template):
        if not match and v.record_pos:
            pos = Predictor.get_predict_point(v.record_pos, GetDevice().get_current_resolution())
        else:
            pos = ap_wait(v, timeout=timeout, threshold=threshold, interval=interval, snapshot=snapshot)
    else:
        try_log_screen()
        pos = v

    if not pos :
        return False

    for _ in range(times):
        GetDevice().touch(pos, **kwargs)
        time.sleep(0.05)
    time.sleep(delay if delay is not None else ST.OPDELAY)
    return pos

def ap_swipe(v1, v2=None, *, vector=None, match=True, duration=1.0, delay=None, timeout=ST.FIND_TIMEOUT, threshold=None, interval=0.5, snapshot=True, **kwargs):
    """
    这段代码修改自airtest.swipe，目的是使其支持根据图像坐标的模式，而不是必须要进行模板匹配

    Perform the swipe action on the device screen.

    There are two ways of assigning the parameters
        * ``swipe(v1, v2=Template(...))``   # swipe from v1 to v2
        * ``swipe(v1, vector=(x, y))``      # swipe starts at v1 and moves along the vector.


    :param v1: the start point of swipe,
               either a Template instance or absolute coordinates (x, y)
    :param v2: the end point of swipe,
               either a Template instance or absolute coordinates (x, y)
    :param vector: a vector coordinates of swipe action, either absolute coordinates (x, y) or percentage of
                   screen e.g.(0.5, 0.5)
    :param match: bool whether match template on screen.
    :param **kwargs: platform specific `kwargs`, please refer to corresponding docs
    :raise Exception: general exception when not enough parameters to perform swap action have been provided
    :return: Origin position and target position
    :platforms: Android, Windows, iOS
    :Example:

        >>> swipe(Template(r"tpl1606814865574.png"), vector=[-0.0316, -0.3311])
        >>> swipe((100, 100), (200, 200))

        Custom swiping duration and number of steps(Android and iOS)::

        >>> # swiping lasts for 1 second, divided into 6 steps
        >>> swipe((100, 100), (200, 200), duration=1, steps=6)

    """
    # assert fn_return is not None, "This function must have fn_return!"
    if isinstance(v1, Template):
        try:
            if not match and v1.record_pos:
                pos1 = Predictor.get_predict_point(v1.record_pos, GetDevice().get_current_resolution())
            else:
                pos1 = ap_wait(v1, timeout=timeout, threshold=threshold, interval=interval, snapshot=snapshot)
        except TargetNotFoundError:
            # 如果由图1滑向图2，图1找不到，会导致图2的文件路径未被初始化，可能在报告中不能正确显示
            if v2 and isinstance(v2, Template):
                v2.filepath
            raise
    else:
        try_log_screen()
        pos1 = v1

    if v2:
        if isinstance(v2, Template):
            if not match and v2.record_pos:
                pos2 = Predictor.get_predict_point(v2.record_pos, GetDevice().get_current_resolution())
            else:
                pos2 = ap_wait(v2, timeout=timeout, threshold=threshold, interval=interval, snapshot=snapshot)
        else:
            pos2 = v2
    elif vector:
        if vector[0] <= 1 and vector[1] <= 1:
            w, h = GetDevice().get_current_resolution()
            vector = (int(vector[0] * w), int(vector[1] * h))
        pos2 = (pos1[0] + vector[0], pos1[1] + vector[1])
    else:
        raise Exception("no enough params for swipe")

    GetDevice().swipe(pos1, pos2, duration=duration, **kwargs)
    time.sleep(delay if delay is not None else ST.OPDELAY)
    return pos1, pos2

ap_click = ap_touch

def ap_sleep(duration=1.0):
    """
    sleep 函数
    :param duration:
    :return:
    """
    time.sleep(duration)
    return True

def ap_text(_text, *, enter=True, delay=None, **kwargs):
    """
    这段代码修改自airtest.text

    Input text on the target device. Text input widget must be active first.

    :param text: text to input, unicode is supported
    :param enter: input `Enter` keyevent after text input, default is True
    :return: None
    :platforms: Android, Windows, iOS
    :Example:

        >>> text("test")
        >>> text("test", enter=False)

        On Android, sometimes you need to click the search button after typing::

        >>> text("test", search=True)

        .. seealso::

            Module :py:mod:`airtest.core.android.ime.YosemiteIme.code`

            If you want to enter other keys on the keyboard, you can use the interface::

                >>> text("test")
                >>> device().yosemite_ime.code("3")  # 3 = IME_ACTION_SEARCH

            Ref: `Editor Action Code <http://developer.android.com/reference/android/view/inputmethod/EditorInfo.html>`_

    """
    GetDevice().text(_text, enter=enter, **kwargs)
    time.sleep(delay if delay is not None else ST.OPDELAY)
    return True

def ap_keyevent(keyname, delay=None, **kwargs):
    """
    这段代码修改自airtest.keyevent
    Perform key event on the device

    :param keyname: platform specific key name
    :param **kwargs: platform specific `kwargs`, please refer to corresponding docs
    :return: None
    :platforms: Android, Windows, iOS
    :Example:

        * ``Android``: it is equivalent to executing ``adb shell input keyevent KEYNAME`` ::

        >>> keyevent("HOME")
        >>> # The constant corresponding to the home key is 3
        >>> keyevent("3")  # same as keyevent("HOME")
        >>> keyevent("BACK")
        >>> keyevent("KEYCODE_DEL")

        .. seealso::

           Module :py:mod:`airtest.core.android.adb.ADB.keyevent`
              Equivalent to calling the ``android.adb.keyevent()``

           `Android Keyevent <https://developer.android.com/reference/android/view/KeyEvent#constants_1>`_
              Documentation for more ``Android.KeyEvent``

        * ``Windows``: Use ``pywinauto.keyboard`` module for key input::

        >>> keyevent("{DEL}")
        >>> keyevent("%{F4}")  # close an active window with Alt+F4

        .. seealso::

            Module :py:mod:`airtest.core.win.win.Windows.keyevent`

            `pywinauto.keyboard <https://pywinauto.readthedocs.io/en/latest/code/pywinauto.keyboard.html>`_
                Documentation for ``pywinauto.keyboard``

        * ``iOS``: Only supports home/volumeUp/volumeDown::

        >>> keyevent("HOME")
        >>> keyevent("volumeUp")

    """
    GetDevice().keyevent(keyname, **kwargs)
    time.sleep(delay if delay is not None else ST.OPDELAY)
    return True

def ap_pinch(in_or_out='in', center=None, percent=0.5, delay=None):
    """
    这段代码修改自airtest.pinch
    Perform the pinch action on the device screen

    :param in_or_out: pinch in or pinch out, enum in ["in", "out"]
    :param center: center of pinch action, default as None which is the center of the screen
    :param percent: percentage of the screen of pinch action, default is 0.5
    :return: None
    :platforms: Android
    :Example:

        Pinch in the center of the screen with two fingers::

        >>> pinch()

        Take (100,100) as the center and slide out with two fingers::

        >>> pinch('out', center=(100, 100))
    """
    try_log_screen()
    GetDevice().pinch(in_or_out=in_or_out, center=center, percent=percent)
    time.sleep(delay if delay is not None else ST.OPDELAY)
    return True

def ap_keyboard(*key_code, internal=0.1, delay=None):
    """
    模拟键盘操作
    :param key_code: str
        "\t",
        "\n",
        "\r",
        " ",
        "!",
        '"',
        "#",
        "$",
        "%",
        "&",
        "'",
        "(",
        ")",
        "*",
        "+",
        ",",
        "-",
        ".",
        "/",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        ":",
        ";",
        "<",
        "=",
        ">",
        "?",
        "@",
        "[",
        "\\",
        "]",
        "^",
        "_",
        "`",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "{",
        "|",
        "}",
        "~",
        "accept",
        "add",
        "alt",
        "altleft",
        "altright",
        "apps",
        "backspace",
        "browserback",
        "browserfavorites",
        "browserforward",
        "browserhome",
        "browserrefresh",
        "browsersearch",
        "browserstop",
        "capslock",
        "clear",
        "convert",
        "ctrl",
        "ctrlleft",
        "ctrlright",
        "decimal",
        "del",
        "delete",
        "divide",
        "down",
        "end",
        "enter",
        "esc",
        "escape",
        "execute",
        "f1",
        "f10",
        "f11",
        "f12",
        "f13",
        "f14",
        "f15",
        "f16",
        "f17",
        "f18",
        "f19",
        "f2",
        "f20",
        "f21",
        "f22",
        "f23",
        "f24",
        "f3",
        "f4",
        "f5",
        "f6",
        "f7",
        "f8",
        "f9",
        "final",
        "fn",
        "hanguel",
        "hangul",
        "hanja",
        "help",
        "home",
        "insert",
        "junja",
        "kana",
        "kanji",
        "launchapp1",
        "launchapp2",
        "launchmail",
        "launchmediaselect",
        "left",
        "modechange",
        "multiply",
        "nexttrack",
        "nonconvert",
        "num0",
        "num1",
        "num2",
        "num3",
        "num4",
        "num5",
        "num6",
        "num7",
        "num8",
        "num9",
        "numlock",
        "pagedown",
        "pageup",
        "pause",
        "pgdn",
        "pgup",
        "playpause",
        "prevtrack",
        "print",
        "printscreen",
        "prntscrn",
        "prtsc",
        "prtscr",
        "return",
        "right",
        "scrolllock",
        "select",
        "separator",
        "shift",
        "shiftleft",
        "shiftright",
        "sleep",
        "space",
        "stop",
        "subtract",
        "tab",
        "up",
        "volumedown",
        "volumemute",
        "volumeup",
        "win",
        "winleft",
        "winright",
        "yen",
        "command",
        "option",
        "optionleft",
        "optionright",
    :return:
    """
    for each in key_code:
        pyautogui.keyDown(each)
        time.sleep(0.05)
        pyautogui.keyUp(each)
        time.sleep(internal)
    time.sleep(delay if delay is not None else ST.OPDELAY)
    return True


# --- Overwrite ---
touch = ap_touch
click = ap_click
wait = ap_wait
exists = ap_exists
pinch = ap_pinch
swipe = ap_swipe
sleep = ap_sleep
keyevent = ap_keyevent
keyboard = ap_keyboard


if __name__ == '__main__':
    a = ...
    print(a is ...)
