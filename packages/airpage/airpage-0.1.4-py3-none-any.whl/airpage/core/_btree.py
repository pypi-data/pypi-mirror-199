from math import inf
from airpage.core._basic import *

# directly import will cause Exception:
class __:
    encoding = 'utf-8'
_stdout = sys.stdout
sys.stdout = __()

from py_trees.common import Status
from py_trees.behaviour import *
from py_trees.composites import *
from py_trees.decorators import *

sys.stdout = _stdout

''' ----------------------------------------- '''

_id_dict = {}

def GetNewId(cls_name:str):
    get = _id_dict.get(cls_name)
    if get is None:
        get = -1

    _id_dict[cls_name] = get + 1
    return get + 1

def GetNewName(cls_name:str):
    _id = GetNewId(cls_name)
    return f'{cls_name}{_id}'

''' -------------------------------- GetNewXXX End ------------------------------------- '''


class NoneException(Exception):
    ...

class ConditionNotComplete(Exception):
    ...

''' -------------------------------- Exception End ------------------------------------- '''

'''
行为树的三种返回值
返回Status非常严谨，诚然优秀。
但我更喜欢随意有效的返回值，因此，ap中用于行为树的函数的返回值必须为以下值。
* 返回None将抛出NoneException
* 返回非bool and 非... 将会将其解释为bool
** 由以上注意事项可知，在ap中返回Status中任何值都会被视作True。请注意这一点
'''
SUCCESS = True
RUNNING = ...
FAILURE = False

def ToStatus(ap_status, *, fn=None):

    if ap_status is None:
        txt_fn = f'(fn={fn.__name__})' if fn is not None else 'ToStatus'
        txt = f"\n\t{txt_fn} has returned None. which is not valid, please return bool or ..."
        raise NoneException(txt)

    if ap_status == ...:
        return Status.RUNNING

    else:
        ap_status = bool(ap_status)
        if ap_status:
            return Status.SUCCESS
        else:
            return Status.FAILURE

def FromStatus(status):
    if status == Status.INVALID:
        return None
    elif status == Status.SUCCESS:
        return True
    elif status == Status.FAILURE:
        return False
    elif status == Status.RUNNING:
        return ...
    else:
        raise TypeError(f"Unknown statustype: {status}")

''' -------------------------------- Status End ------------------------------------- '''
# redirect

class Action(Behaviour):
    """
    叶子节点Action。
    * 这个class的任务是包装任意函数, 使其可以塞到行为树中
    * 被包装的函数的返回值需要为 bool或是...
    """
    def setup(self, target:typing.Callable, *args: typing.Any, _sys_before_=None, _sys_after_=None, **kwargs: typing.Any) -> None:
        """
        指定需要action包装的fn
        :param target: 该action所包装的fn
        :param args: fn的参数
        :param kwargs: fn的kv参数
        :return:
        """
        self.target = target
        self.target_args = args
        self.target_kwargs = kwargs

        # AP Part
        self._before = _sys_before_
        self._after = _sys_after_

    def update(self) -> common.Status:
        if self._before:
            self._before()
        result = self.target(*self.target_args, **self.target_kwargs)
        if self._after:
            self._after()
        result = ToStatus(result, fn=self.target)
        # print(result)
        self.feedback_message = f'{self} return {result}'
        return result

    def __str__(self):
        args = f", args={self.target_args}" if len(self.target_args) else ''
        kwargs = f", kwargs={self.target_kwargs}" if len(self.target_kwargs) else ''
        return f"{self.__class__.__name__}:{self.name}(fn={self.target.__name__}{args}{kwargs})"

# class ActionSleep(Behaviour):
#     def setup(self, duration=1.0, **kwargs: typing.Any) -> None:
#         self.duration = duration
#
#     def initialise(self) -> None:
#         self.start_time = time.time()
#
#     def update(self) -> common.Status:
#         if time.time() >= (self.start_time + self.duration):
#             return Status.SUCCESS
#         return Status.RUNNING

class Condition(Action):
    """
    叶子节点Condition。
    * 这个class的任务是包装任意函数, 使其可以塞到行为树中
    * 被包装的函数的返回值需要为 bool
    ** Condition节点不能返回..., 否则抛出ConditionNotComplete
    """
    def update(self) -> common.Status:
        result = self.target(*self.target_args, **self.target_kwargs)
        if result == ...:
            txt = f"\n\t{self.target.__name__} has returned RUNNING in a Condition Node."
            raise ConditionNotComplete(txt)
        result = ToStatus(result, fn=self.target)
        self.feedback_message = f'{self} return {result}'
        return result


class ThreadParallel(Parallel):
    """
    这个组合节点是在composite.Parallel的基础上修改的
    Parallels enable a kind of spooky at-a-distance concurrency.

    .. graphviz:: dot/parallel.dot

    A parallel ticks every child every time the parallel is itself ticked.
    The parallelism however, is merely conceptual. The children have actually been
    sequentially ticked, but from both the tree and the parallel's purview, all
    children have been ticked at once.

    The parallelism too, is not true in the sense that it kicks off multiple threads
    or processes to do work. Some behaviours *may* kick off threads or processes
    in the background, or connect to existing threads/processes. The behaviour itself
    however, merely monitors these and is itself encosced in a py_tree which only ever
    ticks in a single-threaded operation.

    * Parallels will return :data:`~py_trees.common.Status.FAILURE` if any
      child returns :py:data:`~py_trees.common.Status.FAILURE`
    * Parallels with policy :class:`~py_trees.common.ParallelPolicy.SuccessOnAll`
      only returns :py:data:`~py_trees.common.Status.SUCCESS` if **all** children
      return :py:data:`~py_trees.common.Status.SUCCESS`
    * Parallels with policy :class:`~py_trees.common.ParallelPolicy.SuccessOnOne`
      return :py:data:`~py_trees.common.Status.SUCCESS` if **at least one** child
      returns :py:data:`~py_trees.common.Status.SUCCESS` and others are
      :py:data:`~py_trees.common.Status.RUNNING`
    * Parallels with policy :class:`~py_trees.common.ParallelPolicy.SuccessOnSelected`
      only returns :py:data:`~py_trees.common.Status.SUCCESS` if a **specified subset**
      of children return :py:data:`~py_trees.common.Status.SUCCESS`

    Policies :class:`~py_trees.common.ParallelPolicy.SuccessOnAll` and
    :class:`~py_trees.common.ParallelPolicy.SuccessOnSelected` may be configured to be
    *synchronised* in which case children that tick with
    :data:`~py_trees.common.Status.SUCCESS` will be skipped on subsequent ticks until
    the policy criteria is met, or one of the children returns
    status :data:`~py_trees.common.Status.FAILURE`.

    Parallels with policy :class:`~py_trees.common.ParallelPolicy.SuccessOnSelected` will
    check in both the :meth:`~py_trees.behaviour.Behaviour.setup` and
    :meth:`~py_trees.behaviour.Behaviour.tick` methods to to verify the
    selected set of children is actually a subset of the children of this parallel.

    .. seealso::
       * :ref:`Context Switching Demo <py-trees-demo-context-switching-program>`
    """

    def __init__(
        self,
        name: str,
        policy: common.ParallelPolicy.Base,
        thread_num: int = 2 * cpu_count,
        children: typing.Optional[typing.List[behaviour.Behaviour]] = None,
    ):
        """
        Initialise the behaviour with name, policy and a list of children.

        Args:
            name: the composite behaviour name
            policy: policy for deciding success or otherwise (default: SuccessOnAll)
            thread_num: max thread num, it's better to be decided by your cpu_count
            children: list of children to add
        """
        super(ThreadParallel, self).__init__(name, policy, children)
        self.thread_num = thread_num

    def initialise(self) -> None:
        super().initialise()
        self.pool = ThreadPoolExecutor(max_workers=self.thread_num)

    def tick(self) -> typing.Iterator[behaviour.Behaviour]:
        """
        Tick over the children.

        Yields:
            :class:`~py_trees.behaviour.Behaviour`: a reference to itself or one of its children

        Raises:
            RuntimeError: if the policy configuration was invalid
        """
        self.logger.debug("%s.tick()" % self.__class__.__name__)
        self.validate_policy_configuration()

        # reset
        if self.status != common.Status.RUNNING:
            self.logger.debug("%s.tick(): re-initialising" % self.__class__.__name__)
            for child in self.children:
                # reset the children, this ensures old SUCCESS/FAILURE status flags
                # don't break the synchronisation logic below
                if child.status != common.Status.INVALID:
                    child.stop(common.Status.INVALID)
            self.current_child = None
            # subclass (user) handling
            self.initialise()

        # nothing to do
        if not self.children:
            self.current_child = None
            self.stop(common.Status.SUCCESS)
            yield self
            return


        tasks = [self.pool.submit(lambda : list(child.tick())) for child in self.children]
        _, results = wait_results(tasks, timeout=inf)

        for item in results:
            for node in item:
                yield node

        # determine new status
        new_status = common.Status.RUNNING
        self.current_child = self.children[-1]
        try:
            failed_child = next(
                child
                for child in self.children
                if child.status == common.Status.FAILURE
            )
            self.current_child = failed_child
            new_status = common.Status.FAILURE
        except StopIteration:
            if type(self.policy) is common.ParallelPolicy.SuccessOnAll:
                if all([c.status == common.Status.SUCCESS for c in self.children]):
                    new_status = common.Status.SUCCESS
                    self.current_child = self.children[-1]
            elif type(self.policy) is common.ParallelPolicy.SuccessOnOne:
                successful = [
                    child
                    for child in self.children
                    if child.status == common.Status.SUCCESS
                ]
                if successful:
                    new_status = common.Status.SUCCESS
                    self.current_child = successful[-1]
            elif type(self.policy) is common.ParallelPolicy.SuccessOnSelected:
                if all(
                    [c.status == common.Status.SUCCESS for c in self.policy.children]
                ):
                    new_status = common.Status.SUCCESS
                    self.current_child = self.policy.children[-1]
            else:
                raise RuntimeError(
                    "this parallel has been configured with an unrecognised policy [{}]".format(
                        type(self.policy)
                    )
                )
        # this parallel may have children that are still running
        # so if the parallel itself has reached a final status, then
        # these running children need to be terminated so they don't dangle
        if new_status != common.Status.RUNNING:
            self.stop(new_status)
        self.status = new_status
        yield self

    def stop(self, new_status: common.Status = common.Status.INVALID) -> None:
        """
        Ensure that any running children are stopped.

        Args:
            new_status : the composite is transitioning to this new status
        """
        # close pool
        if self.pool:
            self.pool.shutdown()

        super(ThreadParallel, self).stop(new_status)



class Succeedor(Decorator):
    def update(self) -> common.Status:
        return Status.SUCCESS

class Repeater(Decorator):
    """
    这个类基于Repeat
    Repeat.

    :data:`~py_trees.common.Status.SUCCESS` is
    :data:`~py_trees.common.Status.RUNNING` up to a specified number at
    which point this decorator returns :data:`~py_trees.common.Status.SUCCESS`.

    :data:`~py_trees.common.Status.FAILURE` is always
    :data:`~py_trees.common.Status.FAILURE`.

    Args:
        child: the child behaviour or subtree
        times: repeat max times (-1 to repeat indefinitely)
        until: repeat until inner_node return True/False.
    """

    def __init__(self, name: str, child: behaviour.Behaviour, times: int=-1, until:bool=None):
        super().__init__(name=name, child=child)
        self.left_times = 0
        self.max_times = inf if times <= 0 else times
        self.until = None if until is None else ToStatus(until)

    def initialise(self) -> None:
        """Reset the currently registered number of successes."""
        self.left_times = self.max_times

    def tick(self) -> typing.Iterator[behaviour.Behaviour]:
        """
        Manage the decorated child through the tick.

        Yields:
            a reference to itself or one of its children
        """
        self.logger.debug("%s.tick()" % self.__class__.__name__)
        # initialise just like other behaviours/composites
        if self.status != common.Status.RUNNING:
            self.initialise()
        # interrupt proceedings and process the child node
        # (including any children it may have as well)
        for node in self.decorated.tick():
            yield node
        # resume normal proceedings for a Behaviour's tick
        new_status = self.update()
        if new_status not in list(common.Status):
            self.logger.error(
                "A behaviour returned an invalid status, setting to INVALID [%s][%s]"
                % (new_status, self.name)
            )
            new_status = common.Status.INVALID
        if new_status != common.Status.RUNNING:
            self.stop(new_status)
        self.status = new_status
        yield self

    def update(self) -> common.Status:
        """
        Repeat until the nth consecutive success.

        Returns:
            :data:`~py_trees.common.Status.SUCCESS` on nth success,
            :data:`~py_trees.common.Status.RUNNING` on running, or pre-nth success
            :data:`~py_trees.common.Status.FAILURE` failure.
        """

        if self.decorated.status == Status.RUNNING:
            return Status.RUNNING
        else:
            self.left_times -= 1

            if self.until is not None and self.decorated.status == self.until:
                self.feedback_message = f"success end until:{self.until}"
                return Status.SUCCESS
            elif self.until is not None and self.left_times <= 0:
                self.feedback_message = f"failure end for ran out of times and not meet until:{self.until}"
                return Status.FAILURE
            elif self.left_times <= 0:
                self.feedback_message = f"success end for ran out of times"
                return Status.SUCCESS
            else:
                return Status.RUNNING


class Reflictor(Decorator):
    def setup(self, status_x, status_y, **kwargs: typing.Any) -> None:
        self.status_x = status_x
        self.status_y = status_y

    def update(self) -> common.Status:
        """
        Reflect :data:`~py_trees.common.Status.RUNNING` as :data:`~py_trees.common.Status.SUCCESS`.

        Returns:
            the behaviour's new status :class:`~py_trees.common.Status`
        """
        if self.decorated.status == self.status_x:
            self.feedback_message = f"running is {self.status_x}" + (
                " [%s]" % self.decorated.feedback_message + f" -- reflict to {self.status_y}"
                if self.decorated.feedback_message
                else ""
            )
            return self.status_y
        self.feedback_message = self.decorated.feedback_message
        return self.decorated.status

''' -------------------------------- Class:Leaf End ------------------------------------- '''
Behaviour.__call__ = Behaviour.tick_once

def get_gradparent_calling_function(_reback_level=2):
    """finds the calling function's calling function in many decent cases."""
    fr = sys._getframe(_reback_level)   # inspect.stack()[2][0]
    co = fr.f_code
    for get in (
        lambda:fr.f_globals[co.co_name],
        lambda:getattr(fr.f_locals['self'], co.co_name),
        lambda:getattr(fr.f_locals['cls'], co.co_name),
        lambda:fr.f_back.f_locals[co.co_name], # nested
        lambda:fr.f_back.f_locals['func'],  # decorators
        lambda:fr.f_back.f_locals['meth'],
        lambda:fr.f_back.f_locals['f'],
        ):
        try:
            func = get()
        except (KeyError, AttributeError):
            pass
        else:
            if func.__code__ == co:
                return func
    raise AttributeError("func not found")

def action(fn, *args, name=None, pack=False, _reback=2, **kwargs):
    """
    基于Behaviour的Action，运行时实际执行一个fn对象。该fn需要返回SUCCESS FAILURE RUNNING中的一种值作为该节点的状态
    :param fn: 实际需要执行的fn对象
    :param args: fn对象需要的args参数
    :param name: 当前节点的名称，传入None时使用默认名称(注:名称和在渲染图中的名称不是一个值)
    :param pack: 是否打包该节点及其子节点为一个模块
            * 主要在渲染行为树时生效
            * 被打包的行为树节点会被渲染器视作一个子节点
    :param kwargs: 对应的Behaviour节点初始化时可选的额外kv参数
    :return: Behaviour
    """
    act = Action(name if name else fn.__name__)
    act.setup(fn, *args, **kwargs)
    if pack:
        act.packer = get_gradparent_calling_function(_reback).__name__
    return act

def condition(fn, *args, name=None, pack=False, _reback=2, **kwargs):
    """
    基于Action，两者唯一的区别是condition不能返回RUNNING
    :param fn: 实际需要执行的fn对象
    :param args: fn对象需要的args参数
    :param name: 当前节点的名称，传入None时使用默认名称(注:名称和在渲染图中的名称不是一个值)
    :param pack: 是否打包该节点及其子节点为一个模块
            * 主要在渲染行为树时生效
            * 被打包的行为树节点会被渲染器视作一个子节点
    :param kwargs: 对应的Behaviour节点初始化时可选的额外kv参数
    :return: Behaviour
    """
    cond = Condition(name if name else fn.__name__)
    cond.setup(fn, *args, **kwargs)
    if pack:
        cond.packer = get_gradparent_calling_function(_reback).__name__
    return cond

# --- Leaf ---

def fallback(*nodes, name=None, pack=False, **kwargs):
    """
    依次执行子节点组, 直到某个子节点返回True/RUNNING时返回True/RUNNING。如果所有子节点都返回了False，那么返回False
    :param *nodes: 子节点组
    :param name: 当前节点的名称，传入None时使用默认名称(注:名称和在渲染图中的名称不是一个值)
    :param pack: 是否打包该节点及其子节点为一个模块
            * 主要在渲染行为树时生效
            * 被打包的行为树节点会被渲染器视作一个子节点
    :param kwargs: 对应的组合节点初始化时可选的额外kv参数
    :return: Composite
    """
    new_node = Selector(name if name else GetNewName('Fallback'), memory=True, children=nodes)
    new_node.setup(**kwargs)
    if pack:
        new_node.packer = get_gradparent_calling_function().__name__
    return new_node

def sequence(*nodes, name=None, pack=False, **kwargs):
    """
    依次执行子节点组, 直到某个子节点返回False/RUNNING时返回False/RUNNING。如果所有子节点都返回了True，那么返回True
    :param *nodes: 子节点组
    :param name: 当前节点的名称，传入None时使用默认名称(注:名称和在渲染图中的名称不是一个值)
    :param pack: 是否打包该节点及其子节点为一个模块
            * 主要在渲染行为树时生效
            * 被打包的行为树节点会被渲染器视作一个子节点
    :param kwargs: 对应的组合节点初始化时可选的额外kv参数
    :return: Composite
    """
    new_node = Sequence(name if name else GetNewName('Sequence'), memory=True, children=nodes)
    new_node.setup(**kwargs)
    if pack:
        new_node.packer = get_gradparent_calling_function().__name__
    return new_node

def parallel(*nodes, name=None, pack=False, policy='and', thread_num=cpu_count+1, **kwargs):
    """
    并行运行所有子节点，等待所有子节点结束。返回结果与policy有关.
    :param *nodes: 子节点组
    :param name: 当前节点的名称，传入None时使用默认名称(注:名称和在渲染图中的名称不是一个值)
    :param pack: 是否打包该节点及其子节点为一个模块
            * 主要在渲染行为树时生效
            * 被打包的行为树节点会被渲染器视作一个子节点
    :param policy: 'and' 'or'
        * 'and' 所有子节点的结果都为SUCCESS，才返回SUCCESS，否则返回FAILURE
        ** and模式下如果出现FAILURE会直接无视RUNNING返回FAILURE
        * 'or' 任意子节点的结果为SUCCESS，就返回SUCCESS，除非所有子节点都返回FAILURE才返回FAILURE
        ** or模式下如果出现SUCCESS会直接无视RUNNING返回SUCCESS
        *** 否则返回RUNNING
    :param thread_num: 最大线程数，默认cpu_count+1
    :param kwargs: 对应的组合节点初始化时可选的额外kv参数
    :return: Composite
    """
    if policy == 'and':
        policy = common.ParallelPolicy.SuccessOnAll()
    elif policy == 'or':
        policy = common.ParallelPolicy.SuccessOnOne()
    else:
        raise TypeError(f"Unknown typekind of policy: {policy}")

    new_node = ThreadParallel(name if name else GetNewName('Parallel'), policy, thread_num, nodes)
    new_node.setup(**kwargs)
    if pack:
        new_node.packer = get_gradparent_calling_function().__name__
    return new_node

# --- Composite ---

def succeedor(*nodes, name=None, pack=False, **kwargs):
    """
    不论子节点返回了什么，总是像上一节点返回True
    :param *nodes: 子节点。
            * 当子节点个数超过两个时自动为其创建sequence
    :param name: 当前节点的名称，传入None时使用默认名称(注:名称和在渲染图中的名称不是一个值)
    :param pack: 是否打包该节点及其子节点为一个模块
            * 主要在渲染行为树时生效
            * 被打包的行为树节点会被渲染器视作一个子节点
    :param kwargs: 对应的装饰节点初始化时可选的额外kv参数
    :return: Decorator
    """
    if len(nodes) > 1:
        node = sequence(*nodes)
    else:
        node = nodes[0]
    new_node = Succeedor(name if name else GetNewName('Succeedor'), node)
    new_node.setup(**kwargs)
    if pack:
        new_node.packer = get_gradparent_calling_function().__name__
    return new_node

def repeater(*nodes, name=None, pack=False, times=-1, until=None, **kwargs):
    """
    重复循环子节点n次后返回True。如果定义了until, 那么在耗尽循环次数n前满足until时返回True, 否则返回False。子节点返回RUNNING时也返回RUNNING
    * 只有返回非RUNNING时才视作完成了一次循环
    :param *nodes: 子节点。
            * 当子节点个数超过两个时自动为其创建sequence
    :param name: 当前节点的名称，传入None时使用默认名称(注:名称和在渲染图中的名称不是一个值)
    :param pack: 是否打包该节点及其子节点为一个模块
            * 主要在渲染行为树时生效
            * 被打包的行为树节点会被渲染器视作一个子节点
    :param times: 最大循环次数，传入-1视作无限循环
    :param until: 循环跳出条件, 当子节点的返回值与该条件相符时会提前结束循环。默认None
    :param kwargs: 对应的装饰节点初始化时可选的额外kv参数
    :return: Decorator
    """
    if len(nodes) > 1:
        node = sequence(*nodes)
    else:
        node = nodes[0]
    new_node = Repeater(name if name else GetNewName('Repeater'), node, times, until)
    new_node.setup(**kwargs)
    if pack:
        new_node.packer = get_gradparent_calling_function().__name__
    return new_node

def inverter(*nodes, name=None, pack=False, **kwargs):
    """
    对子节点的结果进行取反。子节点返回RUNNING时也返回RUNNING
    :param *nodes: 子节点。
            * 当子节点个数超过两个时自动为其创建sequence
    :param name: 当前节点的名称，传入None时使用默认名称(注:名称和在渲染图中的名称不是一个值)
    :param pack: 是否打包该节点及其子节点为一个模块
            * 主要在渲染行为树时生效
            * 被打包的行为树节点会被渲染器视作一个子节点
    :param kwargs: 对应的装饰节点初始化时可选的额外kv参数
    :return: Decorator
    """
    if len(nodes) > 1:
        node = sequence(*nodes)
    else:
        node = nodes[0]
    new_node = Inverter(name if name else GetNewName('Inverter'), node)
    new_node.setup(**kwargs)
    if pack:
        new_node.packer = get_gradparent_calling_function().__name__
    return new_node

def validator(condition_fn:typing.Callable, *nodes,name=None, pack=False, blackboard_keys:typing.List[str]=None, **kwargs):
    """
    在执行子节点前先验证条件函数的返回值. 如果条件函数返回True，则返回子节点的结果，否则返回False
    :param condition_fn: 验证函数，在正式执行子节点前，先运行验证函数。若bool(验证函数值返回值)为True, 才会执行子节点
    :param *nodes: 子节点。
            * 当子节点个数超过两个时自动为其创建sequence
    :param name: 当前节点的名称，传入None时使用默认名称(注:名称和在渲染图中的名称不是一个值)
    :param pack: 是否打包该节点及其子节点为一个模块
            * 主要在渲染行为树时生效
            * 被打包的行为树节点会被渲染器视作一个子节点
    :param blackboard_keys: provide read access for the conditional function to these keys
    :param kwargs: 对应的装饰节点初始化时可选的额外kv参数
    :return: Decorator
    """
    if len(nodes) > 1:
        node = sequence(*nodes)
    else:
        node = nodes[0]
    new_node = EternalGuard(name if name else GetNewName('Validator'), node, condition, blackboard_keys)
    new_node.setup(**kwargs)
    if pack:
        new_node.packer = get_gradparent_calling_function().__name__
    return new_node

def timeouter(*nodes, name=None, pack=False, duration=5.0, **kwargs):
    """
    带时限执行子节点。如果超时将尝试提前结束子节点并返回False，否则返回子节点的返回值
    :param *nodes: 子节点。
            * 当子节点个数超过两个时自动为其创建sequence
    :param name: 当前节点的名称，传入None时使用默认名称(注:名称和在渲染图中的名称不是一个值)
    :param pack: 是否打包该节点及其子节点为一个模块
            * 主要在渲染行为树时生效
            * 被打包的行为树节点会被渲染器视作一个子节点
    :param duration: 时限值(单位s)，超过此值后悔提前结束子节点运行
    :param kwargs: 对应的装饰节点初始化时可选的额外kv参数
    :return: Decorator
    """
    if len(nodes) > 1:
        node = sequence(*nodes)
    else:
        node = nodes[0]
    new_node = Timeout(name if name else GetNewName('Timeouter'), node, duration)
    new_node.setup(**kwargs)
    if pack:
        new_node.packer = get_gradparent_calling_function().__name__
    return new_node

def counter(*nodes, name=None, pack=False, **kwargs):
    """
    记录子节点各种状态出现的次数, 无法作为root节点。直接调用此对象将返回一段报告文本以显示子节点运行的情况
    :param *nodes: 子节点。
            * 当子节点个数超过两个时自动为其创建sequence
    :param name: 当前节点的名称，传入None时使用默认名称(注:名称和在渲染图中的名称不是一个值)
    :param pack: 是否打包该节点及其子节点为一个模块
            * 主要在渲染行为树时生效
            * 被打包的行为树节点会被渲染器视作一个子节点
    :param kwargs: 对应的装饰节点初始化时可选的额外kv参数
    :return: Decorator
    """
    if len(nodes) > 1:
        node = sequence(*nodes)
    else:
        node = nodes[0]
    new_node = Count(name if name else GetNewName('Counter'), node, duration)
    new_node.setup(**kwargs)
    if pack:
        new_node.packer = get_gradparent_calling_function().__name__
    return new_node

def oneshoter(*nodes, name=None, pack=False, policy='pass', **kwargs):
    """
    一直执行子节点，直到子节点返回非RUNNING的情况才算结束。返回值取决于policy参数的值
    :param *nodes: 子节点。
            * 当子节点个数超过两个时自动为其创建sequence
    :param name: 当前节点的名称，传入None时使用默认名称(注:名称和在渲染图中的名称不是一个值)
    :param pack: 是否打包该节点及其子节点为一个模块
            * 主要在渲染行为树时生效
            * 被打包的行为树节点会被渲染器视作一个子节点
    :param policy: 'pass' 'any'
        * 'pass' 返回子节点的返回值(比如子节点返回SUCCESS，那么oneshot也返回SUCCESS)
        * 'any' 不关心子节点执行的结果，只要执行完毕，就返回SUCCESS
    :param kwargs: 对应的装饰节点初始化时可选的额外kv参数
    :return: Decorator
    """
    if policy == 'any':
        policy = common.OneShotPolicy.ON_COMPLETION
    elif policy == 'pass':
        policy = common.OneShotPolicy.ON_SUCCESSFUL_COMPLETION
    else:
        raise TypeError(f"Unknown typekind of policy: {policy}")

    if len(nodes) > 1:
        node = sequence(*nodes)
    else:
        node = nodes[0]
    new_node = OneShot(name if name else GetNewName('OneShoter'), node, policy)
    new_node.setup(**kwargs)
    if pack:
        new_node.packer = get_gradparent_calling_function().__name__
    return new_node

def reflictor(*nodes, name=None, pack=False, x=RUNNING, y=FAILURE, **kwargs):
    """
    将子节点的某种返回值映射为另一返回值(x->y)
    :param *nodes: 子节点。
            * 当子节点个数超过两个时自动为其创建sequence
    :param name: 当前节点的名称，传入None时使用默认名称(注:名称和在渲染图中的名称不是一个值)
    :param pack: 是否打包该节点及其子节点为一个模块
            * 主要在渲染行为树时生效
            * 被打包的行为树节点会被渲染器视作一个子节点
    :param x: 输入的目标返回值。如果子节点返回值属于x的类型，那么将返回y
    :param y: 转换后的返回值
    :param kwargs: 对应的装饰节点初始化时可选的额外kv参数
    :return: Decorator
    """
    if len(nodes) > 1:
        node = sequence(*nodes)
    else:
        node = nodes[0]
    rf = Reflictor(name if name else GetNewName('Reflictor'), node)
    rf.setup(ToStatus(x), ToStatus(y), **kwargs)
    if pack:
        new_node.packer = get_gradparent_calling_function().__name__
    return rf

# --- Decorator End ---
def SetTreeEntryence(entryence_fn):
    Behaviour.__call__ = entryence_fn

# --- Run ---

def SetTreeRender(render_fn):
    Behaviour.render = render_fn

''' -------------------------------- function API END ------------------------------------- '''

if __name__ == '__main__':
    def Test_Polling(btree: Behaviour, oneshot=False):
        """
        轮询行为树, 并返回轮询结果
        * 具有AP特色
        :param btree: BehaviourTree
        :return: bool or ...
        """
        while True:
            btree.tick_once()
            result = btree.status

            if result != Status.RUNNING or not oneshot:
                break

        return FromStatus(result)

    SetTreeEntryence(Test_Polling)

    _ = [False]
    def Test(_id, slp_time=0.5):
        print(f"Enter fn-Test{_id}")
        time.sleep(slp_time)
        print(f'after sleep {slp_time}s, fn-Test{_id} finished.')
        _[0] = not _[0]
        return _[0]

    node = repeater(
        action(Test, 0),
        times=3,
        until=False
    )

    print("--- start ---")

    for i in range(1):
        node(oneshot=True)
        print(node.status)
        time.sleep(0.5)
    print('\n--- finish ---')