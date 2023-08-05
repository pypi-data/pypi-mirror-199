from airpage.core._basic import *
from airpage.core._btree import SUCCESS, FAILURE, RUNNING, FromStatus, ToStatus
from airpage.core._btree import action, condition, Behaviour
from airpage.core._btree import sequence, fallback, parallel
from airpage.core._btree import succeedor, repeater, inverter, validator, oneshoter, timeouter, counter, reflictor

# from airpage._ocr import APOcr, GetOcr

class Not:
    """
    定义了一种not容器
    * 只能存储一个元素
    * 用在Identity中，用于表示Not逻辑
    """
    def __init__(self, item):
        self.item = item

    def __bool__(self):
        return not bool(item)

    def __len__(self):
        return 1

    def __iter__(self):
        return iter([self.item])


class Identity:
    """
    定义了一个基于tpl的逻辑表达
    * 垄断了所有的检测

    简单来说，一个Identity实例是一个and or not的逻辑表达式，只不过表达元素是tpl对象
    ---------------------------------------------
    :param identity: list|tuple|Not|tpl airpage定义的逻辑组合，可以映射成or and not
            list -> or
            tuple -> and
            Not -> not
            tpl -> single
            @ example:
                not( (a and b) or (c and d) )
                可以通过list|tuple|set这一映射转变为
                Not( [(a, b), (c, d)] )
    """
    def __init__(self, identity):
        self.express, self.identity = self._build_express(identity)
        self.identity_keys = list(self.identity.keys())
        self.identity_values = list(self.identity.values())

    @staticmethod
    def _build_express(identity):
        """
        这个函数根据identity生成对应的express和对应的数据对象
        :param identity: list|tuple|set airpage定义的逻辑组合，可以映射成or and not
        :return: (express, identity:dict)
        """
        # 计数器, 可以通过这个函数获取不重复的索引
        _cnt = [0]
        def _cnt_():
            _cnt[0] += 1
            return _cnt[0]

        _fdict = {}
        def _inner_(item_node):
            """
            :param item_node:
            :return: [_id, ...]
            """
            _id, _exp = 0, ''
            if isinstance(item_node, bool):  # 函数出口
                return str(item_node)
            elif isinstance(item_node, list):
                _exp = 'or'
            elif isinstance(item_node, tuple):
                _exp = 'and'
            elif isinstance(item_node, Not):
                _exp = 'not'
            elif isinstance(item_node, Template):  # 函数出口
                _id = f"__{_cnt_()}"
                _fdict[_id] = item_node
                return _id
            else:
                error("UnknownType", f"Expected bool|List|Tuple|Not|Template, but get {type(item_node)}")

            tmp, fmt = '', f" {_exp} "
            len_fmt = len(fmt)
            for each in item_node:
                tmp += fmt + _inner_(each)
            if tmp and _exp != 'not':
                tmp = tmp[len_fmt:]

            return f"({tmp})"

        return _inner_(identity), _fdict

    def check(self, timeout=ST.FIND_TIMEOUT, threshold=None, interval=0.5, snapshot=True):
        """
        检测当前画面是否满足Identity的要求
        :return: bool
        """
        _exp = self.express

        values = ap_wait(self.identity_values, timeout=timeout, interval=interval, threshold=threshold, snapshot=snapshot)

        # --- fill expression ---

        for k ,v in zip(self.identity_keys, values):
            _exp = _exp.replace(k, str(bool(v)))

        # --- eval expression ---
        try:
            return eval(_exp)
        except:
            warn(f"Failed check: {k} (Happen in: eval({_exp}))")
            return False

    def burstCheck(self, timeout=ST.FIND_TIMEOUT, interval=0.5, snapshot=False):
        """
        爆发式检测
        * 在短时间内没有任何!'操作'!
        * 在短时间内需要大量检测
        * 需要外部库内调用check方法(传参困难)
        :return:
        """
        return self.check(timeout=timeout, interval=interval, snapshot=snapshot)

    @classmethod
    def Check(cls):
        if isinstance(identity, Identity):
            return identity.check(timeout=timeout, interval=interval, threshold=threshold, snapshot=snapshot)
        else:
            return Identity(identity).check(timeout=timeout, interval=interval, threshold=threshold, snapshot=snapshot)

    def __bool__(self):
        return self.check()


_current_environment = [None]
_flag_environment = [False]

class APEnviron:
    """
    airpage使用的全局坏境, 启动程序时会自动创建一个默认的全局环境。一个全局环境默认只负责一款程序的自动化。
    """
    def __init__(self, project_path):
        self._pages = {}  # Page
        self._ppath = project_path

        # ...
        self.LoadProject(project_path)

    def LoadProject(self, main_file_path):
        auto_setup(main_file_path)
        sys.path.append(os.path.dirname(main_file_path))
        self._ppath = os.path.dirname(main_file_path)

    @property
    def project_path(self):
        return self._ppath

    def __del__(self):
        self.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type:typing.Type, exc_val, exc_tb):
        self.close()
        if exc_type is not None:
            raise exc_type(exc_val, exc_tb)
        return True

    def open(self, timeout:int=0xf) -> None:
        """
        将self设为当前环境, 并阻塞其他环境调用open方法
        :param timeout: 阻塞的最大等待时间，超时后抛出异常
        :return: None
        """
        if _current_environment[0] is self:
            return

        # wait
        timeout_point = time.time() + timeout
        while _flag_environment[0]:
            time.sleep(ST.OPDELAY)
            if time.time() > timeout_point:
                raise error("TimeoutError", "ran out of time for waiting APEnviron.open")

        # lock
        _flag_environment[0] = True
        _current_environment[0] = self

    def close(self):
        """
        关闭自身环境
        :return: None
        """
        if _current_environment is not self:
            return

        # unlock
        _flag_environment[0] = False

        # reset
        _current_environment[0] = None

    ''' -------------------------------------------------------------------- '''

    def GetPage(self, page_name:str):
        """
        获取指定名称的Page对象, 如果不存在，返回None
        :param page_name: str特定page的名称
        :return: Page | None
        """
        return self._pages.get(page_name)

    def SetPage(self, page_name:str, page:typing.Any):
        """
        设置Page，可以覆盖，没有检查，使用时谨慎
        :param page_name: str特定page的名称
        :param page: Page对象
        :return: None
        """
        self._pages[page_name] = page


def GetEnviron(project_path=None) -> APEnviron:
    if _current_environment[0] is None:
        if project_path is None:
            error("EnvrionMissingError", "Use airpage without envrionment.\n\n\tPlease check your code entrence.\n\tIf entrence ok, please use GetEnvrion(__file__) and try again")
        APEnviron(project_path).open()
    return _current_environment[0]

if __name__ == '__main__':
    def debug_test(a, b):
        print(a, b)
        return (a, b)


    act = action_debug_test(1, 2)

    AsyncRun(act)

    # print(test.target)















