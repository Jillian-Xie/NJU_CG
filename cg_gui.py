#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import cg_algorithms as alg
import math
import copy
from typing import Optional
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtGui



class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''
        self.color = QColor(0, 0, 0)
        self.pen_width = 2

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None

        self.basepoint = [-1, -1]
        self.clippoint = [-1, -1]
        self.core = [-1, -1]
        self.temp_plist = []

    # 考虑鲁棒性
    def judge_finish(self) -> bool:
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        if self.status == 'polygon':
            if self.temp_item is not None:
                self.temp_item.p_list.append(self.temp_item.p_list[0])
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.temp_id = self.main_window.get_id()
                self.temp_item = None
                self.updateScene([self.sceneRect()])
                return False
        elif self.status == 'curve':
            if self.temp_item is not None:
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.temp_id = self.main_window.get_id()
                self.temp_item = None
                self.updateScene([self.sceneRect()])
                return False
        return True

    def set_color(self, item_id):
        color_chosen = QColorDialog()
        self.color = color_chosen.getColor()
        if not self.judge_finish():
            self.temp_id = str(int(item_id) + 1)
        if self.selected_id != '':
            self.temp_item.pen.setColor(self.color)

    def set_thin_width(self, item_id):
        self.pen_width = 1
        if not self.judge_finish():
            self.temp_id = str(int(item_id) + 1)
        if self.selected_id != '':
            self.temp_item.pen.setWidth(self.pen_width)
        self.updateScene([self.sceneRect()])

    def set_mid_width(self, item_id):
        self.pen_width = 2
        if not self.judge_finish():
            self.temp_id = str(int(item_id) + 1)
        if self.selected_id != '':
            self.temp_item.pen.setWidth(self.pen_width)
        self.updateScene([self.sceneRect()])

    def set_thick_width(self, item_id):
        self.pen_width = 3
        if not self.judge_finish():
            self.temp_id = str(int(item_id) + 1)
        if self.selected_id != '':
            self.temp_item.pen.setWidth(self.pen_width)
        self.updateScene([self.sceneRect()])

    def start_draw_line(self, algorithm, item_id):
        if not self.judge_finish():
            item_id = str(int(item_id) + 1)
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_polygon(self, algorithm, item_id):
        if not self.judge_finish():
            item_id = str(int(item_id) + 1)
        if self.status == 'selection' or self.status == '' or self.status == 'translate' or self.status == 'rotate' or self.status == 'scale' or self.status == 'clip':
            self.temp_item = None
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_ellipse(self, item_id):
        if not self.judge_finish():
            item_id = str(int(item_id) + 1)
        self.status = 'ellipse'
        self.temp_id = item_id

    def start_draw_curve(self, algorithm, item_id):
        if not self.judge_finish():
            item_id = str(int(item_id) + 1)
        if self.status == 'selection' or self.status == '' or self.status == 'translate' or self.status == 'rotate' or self.status == 'scale' or self.status == 'clip':
            self.temp_item = None
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_clip(self, item_id, algorithm) -> bool:
        if not self.judge_finish():
            self.temp_id = str(int(item_id) + 1)
        if self.selected_id == '' or (not self.item_dict[self.selected_id].item_type == 'line'):
            self.status = ''
            self.basepoint = [-1, -1]
            return False
        self.status = 'clip'
        self.temp_algorithm = algorithm
        self.temp_id = self.selected_id
        self.temp_item = self.item_dict[self.temp_id]
        self.basepoint = [-1, -1]
        return True

    def start_translate(self, item_id) -> bool:
        if not self.judge_finish():
            self.temp_id = str(int(item_id) + 1)
        if self.selected_id == '':
            self.status = ''
            self.basepoint = [-1, -1]
            return False
        self.status = 'translate'
        self.temp_id = self.selected_id
        self.temp_item = self.item_dict[self.temp_id]
        self.basepoint = [-1, -1]
        return True

    def start_rotate(self, item_id) -> bool:
        if not self.judge_finish():
            self.temp_id = str(int(item_id) + 1)
        if self.selected_id == ''or self.item_dict[self.selected_id].item_type == 'ellipse':
            self.status = ''
            self.basepoint = [-1, -1]
            return False
        self.status = 'rotate'
        self.temp_id = self.selected_id
        self.temp_item = self.item_dict[self.temp_id]
        self.basepoint = [-1, -1]
        return True

    def start_scale(self, item_id):
        if not self.judge_finish():
            self.temp_id = str(int(item_id) + 1)
        if self.selected_id == '':
            self.status = ''
            self.basepoint = [-1, -1]
            return False
        self.status = 'scale'
        self.temp_id = self.selected_id
        self.temp_item = self.item_dict[self.temp_id]
        self.basepoint = [-1, -1]
        return True

    def clear_canvas(self):
        self.scene().clear()
        self.updateScene([self.sceneRect()])
        self.item_dict.clear()
        self.item_dict = {}
        self.selected_id = ''
        self.status = ''
        self.temp_item = None

    def finish_draw(self):
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        self.temp_item = None
        self.temp_id = self.main_window.get_id()

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def start_select(self, item_id):
        if not self.judge_finish():
            self.temp_id = str(int(item_id) + 1)
        self.status = 'selection'
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def selection_changed(self, selected):
        if self.main_window.item_cnt == 0:
            return
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.basepoint = [-1, -1]
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.temp_item = self.item_dict[selected]
        self.updateScene([self.sceneRect()])
        if not self.status == 'selection':
            self.status = ''

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.pen_width, self.color, self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'polygon':
            if self.temp_item is None:
                self.temp_item = MyItem(self.pen_width, self.color, self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
                self.scene().addItem(self.temp_item)
            else:
                self.temp_item.p_list.append([x, y])
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.pen_width, self.color, self.temp_id, self.status,
                                    [[x - 1, y + 1], [x + 1, y - 1]],self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'curve':
            if self.temp_item is None:
                self.temp_item = MyItem(self.pen_width, self.color, self.temp_id, self.status, [[x, y]], self.temp_algorithm)
                self.scene().addItem(self.temp_item)
            else:
                self.temp_item.p_list.append([x, y])
        elif self.status == 'translate':
            self.basepoint = [x, y]
            self.temp_plist = self.temp_item.p_list[:]
        elif self.status == 'rotate':
            if self.basepoint == [-1, -1]:
                self.basepoint = [x, y]
                self.temp_plist = self.temp_item.p_list[:]
                x_list = [x[0] for x in self.temp_plist]
                y_list = [y[1] for y in self.temp_plist]
                self.core = [(min(x_list) + max(x_list)) / 2, (min(y_list) + max(y_list)) / 2]
        elif self.status == 'scale':
            if self.basepoint == [-1, -1]:
                self.basepoint = [x, y]
                self.temp_plist = self.temp_item.p_list[:]
                x_list = [x[0] for x in self.temp_plist]
                y_list = [y[1] for y in self.temp_plist]
                self.core = [(min(x_list) + max(x_list)) / 2, (min(y_list) + max(y_list)) / 2]
        elif self.status == 'clip':
            self.basepoint = [x, y]
        elif self.status == 'selection':
            item = self.scene().itemAt(pos, QtGui.QTransform())
            if item is not None:
                self.selection_changed(item.id)
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.pen_width, self.color, self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.pen_width, self.color, self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'polygon':
            if self.temp_item is not None:
                self.temp_item.p_list.append(self.temp_item.p_list[0])
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.finish_draw()
        elif self.status == 'curve':
            if self.temp_item is not None:
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.finish_draw()

        self.updateScene([self.sceneRect()])
        super().mouseDoubleClickEvent(event)

    def get_angle(self, p0, corepoint, p1) -> int:
        if p0 == corepoint or p0 == p1 or p1 == corepoint:
            return 0
        angle0 = math.atan2(p0[1] - corepoint[1], p0[0] - corepoint[0])
        angle1 = math.atan2(p1[1] - corepoint[1], p1[0] - corepoint[0])
        angle = math.degrees(angle1 - angle0)
        return angle

    def get_multiple(self, p0, corepoint, p1) -> int:
        if p0[0] == corepoint[0]:
            return 1
        d0 = abs(p0[0] - corepoint[0])
        d1 = abs(p1[0] - corepoint[0])
        return d1 / d0

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
            print([x, y])
        elif self.status == 'polygon':
            self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'curve':
            self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'translate':
            QApplication.setOverrideCursor(Qt.SizeAllCursor)
            self.temp_item.p_list = copy.deepcopy(alg.translate(self.temp_plist, x - self.basepoint[0], y - self.basepoint[1]))
            self.temp_item.p_list = [[int(p[0]), int(p[1])] for p in self.temp_item.p_list]
        elif self.status == 'rotate':
            QApplication.setOverrideCursor(Qt.ClosedHandCursor)
            r = self.get_angle(self.basepoint, self.core, [x, y])
            self.temp_item.p_list = copy.deepcopy(alg.rotate(self.temp_plist, self.core[0], self.core[1], r))
            self.temp_item.p_list = [[int(p[0]), int(p[1])] for p in self.temp_item.p_list]
        elif self.status == 'scale':
            dx = x - self.core[0]
            dy = y - self.core[1]
            if (dx > 0 and dy > 0) or (dx < 0 and dy < 0):
                QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
            else:
                QApplication.setOverrideCursor(Qt.SizeBDiagCursor)
            s = self.get_multiple(self.basepoint, self.core, [x, y])
            self.temp_item.p_list = copy.deepcopy(alg.scale(self.temp_plist, self.core[0], self.core[1], s))
            self.temp_item.p_list = [[int(p[0]), int(p[1])] for p in self.temp_item.p_list]
        elif self.status == 'clip':
            QApplication.setOverrideCursor(Qt.CrossCursor)
            self.clippoint = [x, y]
            self.temp_item.clip_plist = [self.basepoint, self.clippoint]

        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'translate' or self.status == 'rotate' or self.status == 'scale':
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.basepoint = [-1, -1]
            self.temp_plist = self.temp_item.p_list[:]
        elif self.status == 'clip':
            self.temp_item.clip_plist = None
            self.clippoint = [x, y]
            if self.temp_item.item_type == 'line':
                print([x, y])
                clipped_list = copy.deepcopy(alg.clip(self.temp_item.p_list,
                                    min(self.basepoint[0], self.clippoint[0]),
                                    min(self.basepoint[1], self.clippoint[1]),
                                    max(self.basepoint[0], self.clippoint[0]),
                                    max(self.basepoint[1], self.clippoint[1]),
                                    self.temp_algorithm))
            if not clipped_list == '':
                self.temp_item.p_list = clipped_list

            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.basepoint = [-1, -1]
            self.clippoint = [-1, -1]
            self.temp_plist = self.temp_item.p_list[:]
            self.updateScene([self.sceneRect()])

        super().mouseReleaseEvent(event)


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """

    def __init__(self, pen_width: int, color: QColor, item_id: str, item_type: str, p_list: list, algorithm: str = '',
                 parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id  # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list  # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.temp_list = None
        self.pen = QPen()
        self.pen_selected = QPen()
        self.pen.setColor(color)
        self.pen.setWidth(pen_width)
        self.pen.setStyle(Qt.SolidLine)
        self.pen_selected.setColor(QColor(220, 20, 60))
        self.pen_selected.setStyle(Qt.DashLine)
        self.clip_plist = None

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
        elif self.item_type == 'polygon':
            item_pixels = alg.my_draw_polygon(self.p_list, self.algorithm)
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
        for p in item_pixels:
            painter.setPen(self.pen)
            painter.drawPoint(*p)
        if self.selected:
            painter.setPen(self.pen_selected)
            painter.drawRect(self.boundingRect())
        if not self.clip_plist is None:
            x0, y0 = self.clip_plist[0]
            x1, y1 = self.clip_plist[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            border_pen = QPen(QColor(32,178,170), 2, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(border_pen)
            painter.drawRect(QRectF(x - 1, y - 1, w + 2, h + 2))

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'polygon':
            x_list = [x[0] for x in self.p_list]
            y_list = [y[1] for y in self.p_list]
            x = min(x_list)
            y = min(y_list)
            w = max(x_list) - x
            h = max(y_list) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'curve':
            x_list = [x[0] for x in self.p_list]
            y_list = [y[1] for y in self.p_list]
            x = min(x_list)
            y = min(y_list)
            w = max(x_list) - x
            h = max(y_list) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)


class MainWindow(QMainWindow):
    """
    主窗口类
    """

    def __init__(self):
        super().__init__()
        self.item_cnt = 0
        self.w = 600
        self.h = 600

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        reset_canvas_act = file_menu.addAction('调整画布大小')
        clear_canvas_act = file_menu.addAction('清空画布')
        exit_act = file_menu.addAction('退出')
        save_act = file_menu.addAction('保存')
        pen_menu = menubar.addMenu('画笔')
        set_pen_act = pen_menu.addAction('设置画笔颜色')
        set_width_act = pen_menu.addMenu('设置画笔宽度')
        set_thin_act = set_width_act.addAction("细笔画")
        set_mid_act = set_width_act.addAction("中笔画")
        set_thick_act = set_width_act.addAction("粗笔画")
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_Bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        select_act = menubar.addAction('鼠标点选')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 设置工具栏
        toolBar = QToolBar()
        self.addToolBar(toolBar)
        # 添加图形按钮
        clear = QAction(QIcon('../picture/清空.png'), "清空画布", toolBar)
        clear.setStatusTip("清空画布")
        clear.triggered.connect(self.clear_canvas_action)
        toolBar.addAction(clear)

        save = QAction(QIcon('../picture/保存.png'), "保存画布", toolBar)
        save.setStatusTip("保存画布")
        save.triggered.connect(self.save_action)
        toolBar.addAction(save)

        choose = QAction(QIcon('../picture/鼠标选择.png'), "鼠标选择图元", toolBar)
        choose.setStatusTip("鼠标选择图元")
        choose.triggered.connect(self.select_action)
        toolBar.addAction(choose)

        color = QAction(QIcon('../picture/颜色.png'), "改变画笔颜色", toolBar)
        color.setStatusTip("改变画笔颜色")
        color.triggered.connect(self.set_pen_action)
        toolBar.addAction(color)

        thin = QAction(QIcon('../picture/画笔粗细_1.png'), "细笔画", toolBar)
        thin.setStatusTip("细笔画")
        thin.triggered.connect(self.set_thin_action)
        toolBar.addAction(thin)

        mid = QAction(QIcon('../picture/画笔粗细_3.png'), "中等笔画", toolBar)
        mid.setStatusTip("中等笔画")
        mid.triggered.connect(self.set_mid_action)
        toolBar.addAction(mid)

        thick = QAction(QIcon('../picture/画笔粗细_4.png'), "粗笔画", toolBar)
        thick.setStatusTip("粗笔画")
        thick.triggered.connect(self.set_thick_action)
        toolBar.addAction(thick)

        line = QAction(QIcon('../picture/直线.png'), "直线", toolBar)
        line.setStatusTip("直线")
        line.triggered.connect(self.line_dda_action)
        toolBar.addAction(line)

        polygon = QAction(QIcon('../picture/多边形.png'), "多边形", toolBar)
        polygon.setStatusTip("多边形")
        polygon.triggered.connect(self.polygon_bresenham_action)
        toolBar.addAction(polygon)

        ellipse = QAction(QIcon('../picture/椭圆.png'), "椭圆", toolBar)
        ellipse.setStatusTip("椭圆")
        ellipse.triggered.connect(self.ellipse_action)
        toolBar.addAction(ellipse)

        curve = QAction(QIcon('../picture/曲线.png'), "曲线", toolBar)
        curve.setStatusTip("曲线")
        curve.triggered.connect(self.curve_Bezier_action)
        toolBar.addAction(curve)

        translate = QAction(QIcon('../picture/平移.png'), "平移", toolBar)
        translate.setStatusTip("平移")
        translate.triggered.connect(self.translate_action)
        toolBar.addAction(translate)

        rotate = QAction(QIcon('../picture/旋转.png'), "旋转", toolBar)
        rotate.setStatusTip("旋转")
        rotate.triggered.connect(self.rotate_action)
        toolBar.addAction(rotate)

        scale = QAction(QIcon('../picture/缩放.png'), "缩放", toolBar)
        scale.setStatusTip("缩放")
        scale.triggered.connect(self.scale_action)
        toolBar.addAction(scale)

        clip = QAction(QIcon('../picture/裁剪.png'), "裁剪", toolBar)
        clip.setStatusTip("裁剪")
        clip.triggered.connect(self.clip_liang_barsky_action)
        toolBar.addAction(clip)

        # 连接信号和槽函数
        exit_act.triggered.connect(qApp.quit)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_Bezier_act.triggered.connect(self.curve_Bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        set_pen_act.triggered.connect(self.set_pen_action)
        set_thin_act.triggered.connect(self.set_thin_action)
        set_mid_act.triggered.connect(self.set_mid_action)
        set_thick_act.triggered.connect(self.set_thick_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        clear_canvas_act.triggered.connect(self.clear_canvas_action)
        save_act.triggered.connect(self.save_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
        select_act.triggered.connect(self.select_action)
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('181860112 谢靓静')

        # 设置窗口样式
        self.setWindowIcon(QIcon('../picture/画笔.png'))
        self.setStyleSheet("background-color: floralwhite;")
        menubar.setStyleSheet("background-color: wheat;"+"font-weight: bold;" + "border: 2px solid wheat")
        self.list_widget.setStyleSheet("font-weight: bold;" + "border: 4px inset wheat;"+"background-color: antiquewhite;")
        self.statusBar().setStyleSheet("background-color: wheat;" + "border: 2px solid wheat")
        self.canvas_widget.setStyleSheet("background-color: white;"+ "border: 2px solid wheat")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "退出确认", "确定要退出程序吗?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id

    def line_naive_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_line('Naive', self.get_id())
        else:
            self.canvas_widget.start_draw_line('Naive', str(self.item_cnt - 1))
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_line('DDA', self.get_id())
        else:
            self.canvas_widget.start_draw_line('DDA', str(self.item_cnt - 1))
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_line('Bresenham', self.get_id())
        else:
            self.canvas_widget.start_draw_line('Bresenham', str(self.item_cnt - 1))
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_polygon('DDA', self.get_id())  # 这里发现一个问题，每次调用get_id时id都会递增，导致切换菜单选项时图元编号跳跃
        else:
            self.canvas_widget.start_draw_polygon('DDA', str(self.item_cnt - 1))
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_bresenham_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_polygon('Bresenham',
                                                  self.get_id())  # 这里发现一个问题，每次调用get_id时id都会递增，导致切换菜单选项时图元编号跳跃
        else:
            self.canvas_widget.start_draw_polygon('Bresenham', str(self.item_cnt - 1))
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_Bezier_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_curve('Bezier', self.get_id())  # 这里发现一个问题，每次调用get_id时id都会递增，导致切换菜单选项时图元编号跳跃
        else:
            self.canvas_widget.start_draw_curve('Bezier', str(self.item_cnt - 1))
        self.statusBar().showMessage('Bezier算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_curve('B-spline', self.get_id())  # 这里发现一个问题，每次调用get_id时id都会递增，导致切换菜单选项时图元编号跳跃
        else:
            self.canvas_widget.start_draw_curve('B-spline', str(self.item_cnt - 1))
        self.statusBar().showMessage('B-spline算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_ellipse(self.get_id())
        else:
            self.canvas_widget.start_draw_ellipse(str(self.item_cnt - 1))
        self.statusBar().showMessage('绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def translate_action(self):
        if not self.canvas_widget.start_translate(str(self.item_cnt - 1)):
            self.statusBar().showMessage('您还没有选择要平移的图元！')
        else:
            self.statusBar().showMessage('图元平移')

    def clip_liang_barsky_action(self):
        if not self.canvas_widget.start_clip(str(self.item_cnt - 1), 'Liang-Barsky'):
            self.statusBar().showMessage('请正确选择要裁剪的图元！')
        else:
            self.statusBar().showMessage('Liang-Barsky算法图元裁剪')

    def clip_cohen_sutherland_action(self):
        if not self.canvas_widget.start_clip(str(self.item_cnt - 1), 'Cohen-Sutherland'):
            self.statusBar().showMessage('请正确选择要裁剪的图元！')
        else:
            self.statusBar().showMessage('Cohen-Sutherland算法图元裁剪')

    def rotate_action(self):
        if not self.canvas_widget.start_rotate(str(self.item_cnt - 1)):
            self.statusBar().showMessage('请正确选择要旋转的图元！')
        else:
            self.statusBar().showMessage('图元旋转')

    def scale_action(self):
        if not self.canvas_widget.start_scale(str(self.item_cnt - 1)):
            self.statusBar().showMessage('您还没有选择要缩放的图元！')
        else:
            self.statusBar().showMessage('图元缩放')

    def set_pen_action(self):
        self.canvas_widget.set_color(str(self.item_cnt - 1))

    def set_thin_action(self):
        self.canvas_widget.set_thin_width(str(self.item_cnt - 1))

    def set_mid_action(self):
        self.canvas_widget.set_mid_width(str(self.item_cnt - 1))

    def set_thick_action(self):
        self.canvas_widget.set_thick_width(str(self.item_cnt - 1))

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def reset_canvas_action(self):
        dialog = QDialog()
        layout = QFormLayout(dialog)
        heightEdit = QLineEdit(dialog)
        widthEdit = QLineEdit(dialog)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)
        layout.addRow("画布高度：", heightEdit)
        layout.addRow("画布宽度：", widthEdit)
        layout.addWidget(buttonBox)
        dialog.setWindowTitle("请输入两个整数")
        if dialog.exec():
            if self.is_number(heightEdit.text()) and self.is_number(widthEdit.text()):
                height = int(heightEdit.text())
                width = int(widthEdit.text())
                s1 = height / self.h
                s2 = width / self.w
                s = 1
                if s1 <= 1 and s2 <= 1:
                    s = max(s1, s2)
                else:
                    s = min(s1, s2)
                self.h = height
                self.w = width
                for item in self.canvas_widget.item_dict:
                    self.canvas_widget.item_dict[item].p_list = copy.deepcopy(alg.scale(self.canvas_widget.item_dict[item].p_list, 0,
                                                                          0, s))
                self.scene.setSceneRect(0, 0, width, height)
                self.canvas_widget.setFixedSize(width, height)

    def clear_canvas_action(self):
        self.item_cnt = 0
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        self.list_widget.clear()
        self.canvas_widget.clear_canvas()

    def save_action(self):
        dialog = QFileDialog()
        filename = dialog.getSaveFileName(filter="Image Files(*.jpg *.png *.bmp)")
        if not filename[0] == '':
            pixmap = QPixmap()
            pixmap = self.canvas_widget.grab(self.canvas_widget.sceneRect().toRect())
            pixmap.save(filename[0])

    def select_action(self):
        self.canvas_widget.start_select(str(self.item_cnt - 1))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
