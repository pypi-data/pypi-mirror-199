import numpy as np
from cnocr import CnOcr
from airpage.core._basic import *
from airtest.aircv import aircv
import warnings
import tempfile

warnings.filterwarnings("ignore")

class APOcr:
    def __init__(self):
        self.ocr = CnOcr()

    @staticmethod
    def CountIOU(RecA, RecB):
        """
        计算IOU(重叠面积大小问题)
        :param RecA: (x0, y0, x1, y1)
        :param RecB: (x0, y0, x1, y1)
        :return: float 0 - 1
        """
        xA = max(RecA[0], RecB[0])
        yA = max(RecA[1], RecB[1])
        xB = min(RecA[2], RecB[2])
        yB = min(RecA[3], RecB[3])
        # 计算交集部分面积
        interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
        # 计算预测值和真实值的面积
        RecA_Area = (RecA[2] - RecA[0] + 1) * (RecA[3] - RecA[1] + 1)
        RecB_Area = (RecB[2] - RecB[0] + 1) * (RecB[3] - RecB[1] + 1)
        # 计算IOU
        iou = interArea / float(RecA_Area + RecB_Area - interArea)
        return iou

    def NMS(self, dets, thresh=0.5):
        """
        非极大抑制
        :param dets: nd.array [[x0, y0, x1, y1, score], ...]
        :param tr: float
        :return:
        """
        x1 = dets[:, 0]
        y1 = dets[:, 1]
        x2 = dets[:, 2]
        y2 = dets[:, 3]
        scores = dets[:, 4]

        # 每一个检测框的面积
        areas = (x2 - x1 + 1) * (y2 - y1 + 1)

        # 按照score置信度降序排序
        order = scores.argsort()[::-1]

        keep = []  # 保留的结果框集合

        while order.size > 0:
            i = order[0]
            keep.append(i)  # 保留该类剩余box中得分最高的一个
            # 得到相交区域,左上及右下
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            # 计算相交的面积,不重叠时面积为0
            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)
            inter = w * h
            # 计算IoU：重叠面积 /（面积1+面积2-重叠面积）
            ovr = inter / (areas[i] + areas[order[1:]] - inter)
            # 保留IoU小于阈值的box
            inds = np.where(ovr <= thresh)[0]
            order = order[inds + 1]  # 因为ovr数组的长度比order数组少一个,所以这里要将所有下标后移一位
        return keep

    def ap_ocr(self, tpl:Template):
        """
        寻找一个tpl对应的屏幕区域存在的文字
        按照逐行逐行的顺序返回列表
        :param tpl: Template
        :return: list of text
        """
        fp = tpl.filepath
        area = ap_area(tpl, toint=True)
        screen = GetScreen()
        tmp_fname = GetTempName() + '.png'
        try:
            roi = screen[area[1]:area[3], area[0]:area[2]]
        except:
            error("RoiError", f"Area:{area} does not match with Screen_HW:{screen.shape[:2]}")

        with tempfile.TemporaryDirectory() as tmpdirname:
            tmp_fpath = os.path.join(tmpdirname, tmp_fname)

            aircv.imwrite(r'C:\Users\Administrator\Desktop\test\tmp.png', roi)

            aircv.imwrite(tmp_fpath, roi)
            result = self.ocr.ocr(fp)

        values, score_areas = [], []

        for each in result:
            if not isinstance(each, dict):
                continue
            value = each.get('text')
            score = each.get('score')
            position = each.get('position')

            if value is not None and score is not None and position is not None:
                area = *position[0], *position[2]

                values.append(value)
                score_areas.append((*area, score))

        if not len(values):
            return []

        # 非极大抑制
        _lsa = self.NMS(np.array(score_areas))

        # 还原顺序
        order = []
        for each in _lsa:
            for i, item in enumerate(score_areas):
                _flag = False
                for t in range(item):
                    if item[t] != each[t]:
                        _flag = True
                        break
                if not _flag:
                    order.append(i)
                    break

        order.sort(reverse=False)  # 升序排序

        return [values[i] for i in order]











_ocr = [None]
def GetOcr():
    if _ocr[0] is None:
        _ocr[0] = APOcr()
    return _ocr[0]







