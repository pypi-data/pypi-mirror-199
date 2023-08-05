from airpage.core.core import *

class Page:
    """
    定义了一个关于页面的节点模型

    * 有一个页面判别方法(Function)
    * 维护一个跳转字典，目标id:跳转方法(Action)
    * BFS页面跳转寻路

    --------------------------------------
    :param name: str 页面唯一标识符
    :param identity: Identity|list|tuple|Not|tpl 页面的逻辑判别，airpage定义的逻辑组合
            详细定义参见Core文件内的Identity对象
    """

    def __new__(cls, name, identity):
        # 检查name的重复性 & 将该Name注入公共空间
        env = GetEnviron()
        if env.GetPage(name) is None:
            tmp = super().__new__(cls)
            env.SetPage(name, tmp)
            return tmp
        else:
            error("DupublicNameError", f"You want to new a Page with dupublic name '{name}'.")

    def __init__(self, name, identity):
        self.name = name  # 一个Page的标识符
        self.identity: Identity = identity if isinstance(identity, Identity) else Identity(identity)  # 页面标识
        self.links = {}  # 页面跳转链接集 page:function
        self.tasks = {}  # 任务集 name: function

    def __str__(self):
        return f"Page:{self.name}"

    def __repr__(self):
        return f"Page:{self.name}"

    def check(self, timeout=ST.FIND_TIMEOUT, threshold=None, interval=0.5, snapshot=True):
        """
        检查当前画面是否是目标界面
        :return: bool
        """
        return self.identity.check(timeout=timeout, threshold=threshold, interval=interval, snapshot=snapshot)  # 只检查一次

    def _burstCheck(self, timeout=ST.FIND_TIMEOUT, interval=0.5, snapshot=True):
        """
        爆发式检测
        * 在短时间内没有任何!'操作'!
        * 在短时间内需要大量检测
        * 需要外部库内调用check方法(传参困难)
        :return:
        """
        return self.identity.check(timeout=timeout, interval=interval, snapshot=snapshot)

    def next(self, _next):
        """
        移动到相邻的页面
        :param _next: str|PageNode
        :return: bool
        """
        _next = _next if isinstance(_next, Page) else GetEnviron().GetPage(_next)

        _function = self.links.get(_next)

        if _function is None:
            error("MissingTransFunctionError", f"Miss transfunction for {self.name} -> {_next.name}")
            return False
        info(f"move Page:{self.name} next to Page:{_next.name}")
        return _function()

    def do(self, task_name, *args, **kwargs):
        """
        执行已经注册到当前PageNode中的任务
        :param task_name: 任务名称，与login时传入的名称相一致
        :param *args: 任务所需的参数
        :param **kwargs: 任务所需的kv参数
        :return: task的返回值 or None(找不到任务)
        """
        fn = self.tasks.get(task_name)
        if fn is not None:
            tmp = self.check(timeout=ST.FIND_TIMEOUT_TMP)
            # debug(f"Check:{tmp} when execute Task:{task_name} on Page:{self.name}")
            if not tmp:  # check and not self.check(timeout=ST.FIND_TIMEOUT_TMP):
                if not self.Transit(self.name):
                    return False
            info(f"Execute Task:{task_name} on Page:{self.name}")

            ''' --------- Specific --------- '''
            if isinstance(fn, Behaviour):
                kwargs['oneshot'] = True

            result = fn(*args, **kwargs)

            print(f"Execute Task:{task_name}  on Page:{self.name} Result:{result}")
            return result
        else:
            error("UnknownTask", f"Can not find Task:{task_name} in {self}")

    # 下面的段落描述了: 如何创建链接 & BFS链接搜索
    def link(self, page, action):
        """
        链接两个页面
        :param page: PageNode 目标页面
        :param action: 转移操作
        :return: None
        """
        print(f"Link Page:{self.name} to Page:{page.name}")
        assert isinstance(page, Page), "When you use 'link', the param1 must be a Page."
        if action is None:
            return
        if self.links.get(page):
            warn(f"You are replacing exist link:{page.name}")
        if page is self:
            error("LinkSelfError", "You can not link self to self.")
        self.links[page] = action

    def unlink(self, page):
        """
        断开与特定页面的链接
        :param page: PageNode 目标页面
        :return: None
        """
        self.links.pop(page)

    def login(self, arg1, arg2=None):
        """
        注册任务到指定页面
        :param arg1: function:str or name:str
        :param arg2: function or None
        :return:
        """
        if arg2 is None:
            name = arg1.__name__
            function = arg2
        else:
            name = arg1
            function = arg2

        if self.tasks.get(name):
            warn(f"You are replacing exist task:{name}")
        self.tasks[name] = function

    def logoff(self, name):
        self.tasks.pop(name)
        self.task_checks.pop(name)

    @classmethod
    def Check(cls, page, *, timeout=ST.FIND_TIMEOUT, threshold=None, interval=0.5, snapshot=True):
        if isinstance(page, str):
            page = GetEnviron().GetPage(page)
        return page.check(
            timeout=timeout,
            threshold=threshold,
            interval=interval,
            snapshot=snapshot,
        )


    @staticmethod
    def ParallelCheck(sources=None, timeout=ST.FIND_TIMEOUT, interval=0.5):
        """
        根据当前界面推测对应的Page
        :param sources: list 所有参与推测的page
        :param timeout:
        :param interval:
        :return: page or None
        """

        info("Auto analyse page, It will take few time...")

        if sources is None:
            sources = list(GetEnviron()._pages.values())

        # 使用统一截图, 并创建pool
        sid = GetTempName()
        GlobalScreen_Update(sid)
        pool = ThreadPoolExecutor(max_workers=min(cpu_count * 2, len(sources)))

        # --- 创建check任务并提交到事件内核 ---
        tasks = [
            pool.submit(page._burstCheck, ST.FIND_TIMEOUT_TMP, interval, sid) for page in sources
        ]

        # --- 等待任务结束 ---
        _, results = wait_results(tasks, timeout, interval)

        # 清空全局截图，同时释放pool
        GlobalScreen_Flush(sid)
        pool.shutdown()

        # --- 读取各个Page.check返回的结果 ---
        for i, item in enumerate(results):
            if item:
                info(f"It's probably on Page:{sources[i]}")
                return sources[i]

        warn("Can not find a page match with screen now.")
        return

    ''' ------------------------------------------------- '''


    @staticmethod
    def _bfs_path_found(page_a, page_b):
        """
        寻找由page_a到page_b的路径
        :param page_a:
        :param page_b:
        :return: list of page, head is page_a, end is page_b.
                * return [] if failed.
        """

        def _inner_(from_node, target, excepts):
            """
            实现一轮迭代，如果找到结果，返回target; 重复输入返回[]; 其余情况返回下一轮的queue:[]
            :param from_node:
            :param target:
            :param excepts:
            :return:
            """
            if target in excepts:
                return []

            excepts.append(from_node)

            queue = []
            for each in from_node.links:
                if each is target:
                    return target
                queue.append(each)

            return queue

        g_queue, excepts = [([page_a], page_a), ], []
        while True:
            _ = []
            for path, each in g_queue:
                # print(path, each, page_b, excepts)
                queue = _inner_(each, page_b, excepts)

                if isinstance(queue, Page):  # 函数出口
                    return path + [page_b]

                for each in queue:  # 加入下一次循环队列
                    _.append((path + [each], each))  # 基本单元是(path, next_node)

            if not _:  # 未能寻找到结果
                return []

            g_queue = _

    ''' ---------------------------------------------------------- '''

    @staticmethod
    def LinkWith(page_name_a, page_name_b, action_a2b=None, action_b2a=None):
        """
        创建一个界面与另一个界面的链接
        :param page_a:
        :param page_b:
        :param action_a2b: None表示无法跳转
        :param action_b2a: None表示无法回退
        :return:
        """
        page_a = GetEnviron().GetPage(page_name_a)
        page_b = GetEnviron().GetPage(page_name_b)

        page_a.link(page_b, action_a2b)
        page_b.link(page_a, action_b2a)

    @staticmethod
    def DoTask(page_name, task_name, *args, check=None, **kwargs):
        """
        执行已经注册到当前Page中的任务
        :param page_name:
        :param task_name: 任务名称，与login时传入的名称相一致
        :param *args: 任务所需的参数
        :param check: 执行任务前是否需要检测当前screen是否为当前页面
        :param **kwargs: 任务所需的kv参数
        :return: task的返回值 or None(找不到任务)
        """
        return GetEnviron().GetPage(page_name).do(task_name, *args, check=check, **kwargs)

    @staticmethod
    def LoginTask(page_name, arg1, arg2=None):
        """
        注册任务到指定页面.
        :param arg1: function:str or name:str
        :param arg2: function or None
        :return:
        """
        return GetEnviron().GetPage(page_name).login(arg1, arg2)

    @classmethod
    def Transit(cls, arg1, arg2=None, timeout=ST.FIND_TIMEOUT, interval=0.5):
        """
        移动当前页面到指定页面
        * arg2 is None时，arg1表示目标页面，会自动检查当前页面
        * arg1和arg2均存在时，表示开发人员已确定当前页面为arg1，arg2为目标页面
        :param arg1: str|PageNode
        :param arg2: str|PageNode
        :return: bool
        """
        env = GetEnviron()

        # 检查参数的个数，判断用户的意图(1个参数: 参数表示终点，起点需要程序寻找; 2个参数，起点和终点均已给出)
        arg1 = arg1 if isinstance(arg1, Page) else env.GetPage(arg1)
        arg2 = None if arg2 is None else (arg2 if isinstance(arg2, Page) else env.GetPage(arg1))

        # 检查参数的类型, 确定当前页面(如果需要搜索当前页面的话)，并将其统一转为Page对象
        page_a = cls.ParallelCheck(timeout=timeout, interval=interval) if arg2 is None else arg1
        page_b = arg1 if arg2 is None else arg2

        # 检查第一个参数(如果参数二存在时)
        if arg2 is not None:
            if not page_a.check():
                warn(f"检查页面起点:{page_a}失败. 由页面:{page_a}到{page_b}的操作未能完成.")
                return False

        if page_a is None:
            return False

        if page_a.name == page_b.name:
            return True

        _path = Page._bfs_path_found(page_a, page_b)
        end_page = _path[-1]

        if not _path:
            warn(f"搜寻路径{page_a}->{page_b}失败. 由页面:{page_a}到{page_b}的操作未能完成.")
            return False

        if len(_path) < 2:
            error("UnexpectedShortLength", "len of path can not shorter than 2")

        _flag = True
        for i in range(len(_path[:-1])):
            _flag = _flag and _path[i].next(_path[i + 1])

            if not _flag:
                break

            sleep(ST.FIND_TIMEOUT_TMP)

        if not _flag or not end_page.check(timeout, interval):
            warn(f"执行页面:{_path[i]}->{_path[i + 1]}的过渡函数失败. 由页面:{page_a}到{page_b}的操作未能完成.")
            return False

        return True

    @staticmethod
    def RenderTask(page_name, task_name, *render_args, **render_kwargs):
        return GetEnviron().GetPage(page_name).tasks[task_name].render(*render_args, name=f"{page_name}_{task_name}",
                                                                        **render_kwargs)

    def __call__(self, fn: typing.Callable):
        """
        装饰任务函数。被装饰的函数会被当作一个Task
        :param fn: 任务函数
        :param args: fn参数
        :param kwargs: fn的kv参数
        :return:
        """
        self.login(fn.__name__, fn)

        def _inner_(*args, **kwargs):
            return self.do(fn.__name__, *args, **kwargs)

        return _inner_

''' --------------------------------------------------------------------------------------------------------------- '''


# Task装饰器
def page(page_name: str) -> Page:
    """
    获得特定名称的page
    * Page的实例其实是对Task的装饰器
    :param page_name: page的名称
    :return: Page - wrapper
    """
    return GetEnviron().GetPage(page_name)


# Link装饰器
def transfer(page_a: typing.Union[str, Page], page_b: typing.Union[str, Page]) -> typing.Callable:
    """
    装饰从page_a转移到page_b的函数
    :param page_a: page a或其名称
    :param page_a: page b或其名称
    :return : wrapper fn
    """

    _page_a = page_a
    _page_b = page_b

    def _wrapper_(fn):
        page_a = _page_a if isinstance(_page_a, Page) else GetEnviron().GetPage(_page_a)
        page_b = _page_b if isinstance(_page_b, Page) else GetEnviron().GetPage(_page_b)
        page_a.link(page_b, fn)
        return fn

    return _wrapper_
