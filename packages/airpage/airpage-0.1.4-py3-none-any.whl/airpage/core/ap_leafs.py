import airpage.core._btree as bt

from math import inf
from airpage.core.page import *

import pydotplus as pydot

def ResetMousePosition():
    pyautogui.moveTo(1, 1)

def ResetMousePositionAndFlush():
    pyautogui.moveTo(1, 1)
    GlobalScreen_Flush()

def screen_flush():
    return action(
        GlobalScreen_Flush,
        _reback=3,  # pack时需要额外往后移动一级
    )

def screen_update():
    return action(
        GlobalScreen_Update,
        _reback=3,  # pack时需要额外往后移动一级
    )

def condition_wait(querys, *, timeout=ST.FIND_TIMEOUT, threshold=None, interval=0.5, snapshot=True):
    return condition(
        wait,
        querys,
        timeout=timeout,
        threshold=threshold,
        interval=interval,
        snapshot=snapshot,
        _reback=3, # pack时需要额外往后移动一级
    )

def condition_exists(querys, *, threshold=None, snapshot=True):
    return condition(
        exists,
        querys,
        threshold=threshold,
        snapshot=snapshot,
        _reback=3, # pack时需要额外往后移动一级
    )
# 默认标准的检查时间
def action_touch(v, *, times=1, match=True, delay=None, timeout=ST.FIND_TIMEOUT, threshold=None, interval=0.5, snapshot=True, **kwargs):
    return action(
        touch,
        v,
        times=times,
        match=match,
        delay=delay,
        timeout=timeout,
        threshold=threshold,
        interval=interval,
        snapshot=snapshot,
        _sys_after_ = ResetMousePositionAndFlush,  # 这类action可能会改变屏幕，所以清除掉屏幕，强迫更新屏幕
        _reback=3, # pack时需要额外往后移动一级
        ** kwargs
    )

# 默认较短的检查时间
def action_tickle(v, *, times=1, match=True, delay=None, timeout=ST.FIND_TIMEOUT_TMP, threshold=None, interval=0.5, snapshot=True, **kwargs):
    return action(
        touch,
        v,
        times=times,
        match=match,
        delay=delay,
        timeout=timeout,
        threshold=threshold,
        interval=interval,
        snapshot=snapshot,
        _sys_after_ = ResetMousePositionAndFlush,  # 这类action可能会改变屏幕，所以清除掉屏幕，强迫更新屏幕
        _reback=3, # pack时需要额外往后移动一级
        ** kwargs
    )

def action_sleep(duration=1.0):
    return action(
        ap_sleep,
        duration,
        _reback=3, # pack时需要额外往后移动一级
    )

def action_swipe(v1, v2=None, *, vector=None, match=True, duration=1.0, delay=None, timeout=ST.FIND_TIMEOUT_TMP, threshold=None, interval=0.5, snapshot=True, **kwargs):
    return action(
        swipe,
        v1,
        v2,
        vector=vector,
        match=match,
        duration=duration,
        delay=delay,
        timeout=timeout,
        threshold=threshold,
        interval=interval,
        snapshot=snapshot,
        _sys_after_ = ResetMousePositionAndFlush,  # 这类action可能会改变屏幕，所以清除掉屏幕，强迫更新屏幕
        _reback=3, # pack时需要额外往后移动一级
        **kwargs
    )


def action_pinch(in_or_out='in', center=None, percent=0.5, delay=None):
    return action(
        pinch,
        in_or_out=in_or_out,
        center=center,
        percent=percent,
        delay=delay,
        _sys_after_ = ResetMousePositionAndFlush,  # 这类action可能会改变屏幕，所以清除掉屏幕，强迫更新屏幕
        _reback=3, # pack时需要额外往后移动一级
    )


def action_text(_text, *, enter=True, delay=None, **kwargs):
    return action(
        text,
        _text,
        enter=enter,
        delay=delay,
        _sys_after_ = ResetMousePositionAndFlush,  # 这类action可能会改变屏幕，所以清除掉屏幕，强迫更新屏幕
        _reback=3, # pack时需要额外往后移动一级
        **kwargs
    )


def action_keyevent(keyname, *, delay=None, **kwargs):
    return action(
        keyevent,
        keyname,
        delay=delay,
        _sys_after_ = ResetMousePositionAndFlush,  # 这类action可能会改变屏幕，所以清除掉屏幕，强迫更新屏幕
        _reback=3, # pack时需要额外往后移动一级
        **kwargs
    )

def action_keyboard(*key_code, internal=0.1, delay=None):
    return action(
        keyboard,
        *key_code,
        internal=internal,
        delay=delay,
        _sys_after_ = ResetMousePositionAndFlush,  # 这类action可能会改变屏幕，所以清除掉屏幕，强迫更新屏幕
        _reback=3, # pack时需要额外往后移动一级
    )

action_click = action_touch


''' --------------------------AP Action End------------------------------ '''

def action_label(desc):
    return action(label, desc, _reback=3)

def action_info(*args):
    return action(info, *args, _reback=3)

def action_warn(*args):
    return action(warn, *args, _reback=3)

def action_error(err_type:str, *args):
    return action(error, err_type, *args, _reback=3)

''' --------------------------AP Information End------------------------------ '''

def condition_identity(identity, *, timeout=ST.FIND_TIMEOUT, threshold=None, interval=0.5, snapshot=True):
    return condition(
        Identity.Check,
        identity,
        timeout=timeout,
        threshold=threshold,
        interval=interval,
        snapshot=snapshot,
        _reback=3, # pack时需要额外往后移动一级
    )


def condition_page(page, *, timeout=ST.FIND_TIMEOUT, threshold=None, interval=0.5, snapshot=True):
    return condition(
        Page.Check,
        page,
        timeout=timeout,
        threshold=threshold,
        interval=interval,
        snapshot=snapshot,
        _reback=3,  # pack时需要额外往后移动一级
    )

def action_transit(*args):
    return action(
        Page.Transit, *args,
        _sys_after_ = ResetMousePositionAndFlush,  # 这类action可能会改变屏幕，所以清除掉屏幕，强迫更新屏幕
        _reback=3, # pack时需要额外往后移动一级
    )

def action_dotask(page_name, task_name, *args, **kwargs):
    return action(Page.DoTask, page_name, task_name,
        *args,
        **kwargs,
        _sys_after_ = ResetMousePositionAndFlush,  # 这类action可能会改变屏幕，所以清除掉屏幕，强迫更新屏幕
        _reback=3, # pack时需要额外往后移动一级
    )

''' --------------------------AP Composite Action&Condition End------------------------------ '''

def action_fwrite(file, string):
    """
    文件写入操作
    * 可以是一般文件
    * 可以是标准输出
    * 可以是自定义输出
    :param file: 具有方法: .write(__s)的任意对象
    :param string: 待写入的字符串
    :return: Behaviour
    """
    return action(
        file.write,
        string,
        delay=delay,
        _sys_after_ = ResetMousePositionAndFlush,  # 这类action可能会改变屏幕，所以清除掉屏幕，强迫更新屏幕
        _reback=3, # pack时需要额外往后移动一级
    )

def AP_Polling(btree:bt.Behaviour, oneshot=False):
    """
    轮询行为树, 并返回轮询结果
    * 具有AP特色
    :param btree: BehaviourTree
    :return: bool or ...
    """
    while True:
        btree.tick_once()
        result = btree.status

        if result != bt.Status.RUNNING or not oneshot:
            break

    return FromStatus(result)

bt.SetTreeEntryence(AP_Polling)

''' --------------------------AP Polling End------------------------------ '''

_default_values=dict(
    v2=None,
    vector=None,
    times=1,
    match=True,
    delay=None,
    timeout=ST.FIND_TIMEOUT,
    threshold=None,
    interval=0.5,
    snapshot=True,
    duration=1.0,
)

def CreateNode(graph: pydot.Dot, behaviour: bt.Behaviour, root=False):
    def create_template_subnodes(_graph, _node_name, *templates):
        """
        创建有关Template的节点，传入Template以及可能包含Template的列表
        * 返回是否实际处理了Template
        :return: bool
        """
        _result = False
        for tpl in templates:
            if isinstance(tpl, Template):
                _i = bt.GetNewId('Template')
                graph.add_node(pydot.Node(
                    name=f"{_node_name}_tpl{_i}",
                    shape="plaintext",
                    label='',
                    image=os.path.join(ProjectPath(), tpl.filename),
                ))

                graph.add_edge(pydot.Edge(
                    name, f"{name}_tpl{_i}",
                    style='dashed',
                    arrowhead='none',
                ))
                _result |= True
            elif isinstance(tpl, (list, tuple)):
                _result |= create_template_subnodes(_graph, _node_name, *tpl)
        return _result

    def is_pos(item):
        if not isinstance(item, (list, tuple)):
            return False

        _flag = True
        for each in item:
            if not isinstance(each, (int, float)):
                _flag = False
                break

        return _flag

    name = f"node{bt.GetNewId('_node')}"
    if not root and hasattr(behaviour, 'packer'):
        node = pydot.Node(
            name=name,
            label=behaviour.packer,
            shape="folder",
            style="filled",
            fillcolor="khaki",
            fontsize=16,
            fontcolor="black",
        )

        graph.add_node(node)
    elif isinstance(behaviour, (bt.Action, bt.Condition)):
        # 确定Action和Condition节点的名称，并对ap_xxx的名称的显示进行优化
        _label = behaviour.target.__name__ if behaviour.target else behaviour.name
        if len(_label) >= 3 and _label[0:3] == 'ap_':
            _label = _label[3:]

        node = pydot.Node(
            name=name,
            label=_label,
            shape="ellipse" if isinstance(behaviour, bt.Condition) else "box",
            style="filled",
            fillcolor="lightgray",
            fontsize=12,
            fontcolor="black",
        )
        graph.add_node(node)

        ''' --- 为action和condition创建参数节点 --- '''
        args, kwargs = behaviour.target_args, behaviour.target_kwargs
        any_flag = False  # 用于判断是否需要渲染参数节点

        # 生成label
        # 检查有无tpl
        _label, _i = "", 0
        for a in args:
            if isinstance(a, Template) or isinstance(a, (list, tuple)):
                if is_pos(a):
                    any_flag |= True
                    _label += f"{a}, \n"
                else:
                    create_template_subnodes(graph, name, a)
            else:
                any_flag |= True
                if isinstance(a, str):
                    a = f"'{a}'"
                _label += f"{a}, \n"

        for k, v in kwargs.items():
            if k not in _default_values or _default_values[k] != v:
                if isinstance(v, Template) or isinstance(v, (list, tuple)):
                    if is_pos(v):
                        any_flag |= True
                        _label += f"{k}={v}, \n"
                    else:
                        create_template_subnodes(graph, name, v)
                else:
                    any_flag |= True
                    if isinstance(v, str):
                        v = f"'{v}'"
                    _label += f"{k}={v}, \n"

        # 只有实际处理了参数的节点才进行显示
        if any_flag:
            if len(_label) >= 3 and _label[-3:] == ', \n':
                _label = _label[:-3]

            graph.add_node(pydot.Node(
                name=f"{name}_param",
                label=_label,
                shape="ellipse",
                style="filled",
                fillcolor="ghostwhite",
                fontsize=10,
            ))

            graph.add_edge(pydot.Edge(
                name, f"{name}_param",
                style='dashed',
                arrowhead='none',
                fontsize=8,
            ))

    elif isinstance(behaviour, bt.Composite):
        isi_seq = isinstance(behaviour, bt.Sequence)
        isi_par = isinstance(behaviour, bt.Parallel)
        # isi_fab = isinstance(behaviour, bt.Selector)  # No need to if it

        node = pydot.Node(
            name=name,
            label=' -> ' if isi_seq else (" => " if isi_par else " ? "),
            shape="square",
            style="filled",
            fillcolor='orange' if isi_seq else ("gold" if isi_par else "tomato"),
            fontsize=16,
            fontcolor="black",
        )

        graph.add_node(node)

        for child in behaviour.children:
            subnode = CreateNode(graph, child)
            graph.add_edge(pydot.Edge(
                name, subnode.obj_dict['name']
            ))

    elif isinstance(behaviour, bt.Decorator):

        _label = behaviour.name

        if isinstance(behaviour, bt.Repeater):
            _label = "While\n"
            _tmp = ""
            if behaviour.max_times is not inf:
                _tmp += f"{behaviour.max_times}, "
            if behaviour.until is not None:
                _tmp += f"{bt.FromStatus(behaviour.until)}"
            if _tmp:
                _label += f"({_tmp})"
        elif isinstance(behaviour, bt.Reflictor):
            _label = "Fn\n"
            _label += f"({bt.FromStatus(behaviour.status_x)}->{bt.FromStatus(behaviour.status_y)})"
        elif isinstance(behaviour, bt.Timeout):
            _label = "Time\n"
            _label += f"({behaviour.duration}s)"
        elif isinstance(behaviour, bt.EternalGuard):
            _label = "If\n"
            if behaviour.condition:
                _label += f"({behaviour.condition.__name__}s)"
        elif isinstance(behaviour, bt.Succeedor):
            _label = "True"
        elif isinstance(behaviour, bt.Inverter):
            _label = "Not"
        elif isinstance(behaviour, bt.OneShot):
            _label = "Oneshot"

        node = pydot.Node(
            name=name,
            label=_label,
            shape="diamond",
            style="filled",
            fillcolor='skyblue',
            fontsize=10,
            fontcolor="black",
        )

        graph.add_node(node)

        for child in behaviour.children:
            subnode = CreateNode(graph, child)
            graph.add_edge(pydot.Edge(
                name, subnode.obj_dict['name']
            ))
    else:
        node = pydot.Node(
            name=name,
            label=str(behaviour),
            shape="ellipse",
            style="filled",
            fillcolor="gray",
            fontsize=10,
            fontcolor="black",
        )
        graph.add_node(node)

    return node

def AP_Render(btree:bt.Behaviour, name=None, open=False):
    """
    渲染行为树
    * 具有AP特色
    :param btree: BehaviourTree
    :param name: 指定文件名，默认None，即使用节点名称
    :param open: bool 是否立刻打开svg文件(因为svg文件比png清楚)
    :return: None
    """
    graph = pydot.Dot(graph_type="digraph", ordering="out")
    CreateNode(graph, btree, root=True)
    output_path_noext = os.path.join(ProjectPath(), btree.name if name is None else name)
    graph.write_png(output_path_noext + '.png')
    graph.write_svg(output_path_noext + '.svg')

    if open:
        os.startfile(output_path_noext + '.svg')


bt.SetTreeRender(AP_Render)

''' --------------------------AP Render End------------------------------ '''


if __name__ == '__main__':
    def if_something(sth):
        return bool(sth)

    def do_something(sth):
        return True

    t = fallback(
    sequence(
    condition(if_something, "条件1"),
    repeater(action(do_something, "事请1"), times=3),
    ),
    action(do_something, "事请2"),
    )

    t.render(name="tree", open=True)
    print("ok")