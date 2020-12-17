#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


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

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None

        self.basepoint = [-1, -1]
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

    def start_draw_line(self, algorithm, item_id):
        if not self.judge_finish():
            item_id = str(int(item_id)+1)
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_polygon(self, algorithm, item_id):
        if not self.judge_finish():
            item_id = str(int(item_id)+1)
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_ellipse(self, item_id):
        if not self.judge_finish():
            item_id = str(int(item_id)+1)
        self.status = 'ellipse'
        self.temp_id = item_id

    def start_draw_curve(self, algorithm, item_id):
        if not self.judge_finish():
            item_id = str(int(item_id)+1)
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_translate(self) -> bool:
        if not self.judge_finish():
            self.item_id = str(int(self.item_id)+1)
        self.status = 'translate'
        if self.selected_id == '':
            return False
        else:
            self.temp_id = self.selected_id
            self.temp_item = self.item_dict[self.temp_id]
            self.temp_plist = self.temp_item.p_list[:]
            self.basepoint = [-1, -1]
            return True

    def start_rotate(self) -> bool:
        if not self.judge_finish():
            self.item_id = str(int(self.item_id)+1)
        self.status = 'rotate'
        if self.selected_id == '':
            return False
        else:
            self.temp_id = self.selected_id
            self.temp_item = self.item_dict[self.temp_id]
            self.basepoint = [-1, -1]
            return True

    def start_scale(self):
        if not self.judge_finish():
            self.item_id = str(int(self.item_id)+1)
        self.status = 'scale'
        if self.selected_id == '':
            return False
        else:
            self.temp_id = self.selected_id
            self.temp_item = self.item_dict[self.temp_id]
            self.basepoint = [-1, -1]
            return True

    def finish_draw(self):
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        self.temp_item = None
        self.temp_id = self.main_window.get_id()

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.temp_item = self.item_dict[selected]
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'polygon':
            if self.temp_item is None:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
                self.scene().addItem(self.temp_item)
            else:
                self.temp_item.p_list.append([x, y])
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'curve':
            if self.temp_item is None:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm)
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
                x_list = [x[0] for x in self.p_list]
                y_list = [y[1] for y in self.p_list]
                self.core = [(min(x_list) + max(x_list)) / 2, (min(y_list) + max(y_list)) / 2]

        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
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


    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'polygon':
            self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'curve':
            self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'translate':
            QApplication.setOverrideCursor(Qt.SizeAllCursor)
            self.temp_item.p_list = alg.translate(self.temp_plist, x - self.basepoint[0], y - self.basepoint[1])
        elif self.status == 'rotate':
            QApplication.setOverrideCursor(Qt.ClosedHandCursor)

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
        elif self.status == 'translate':
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.temp_id = ''
            self.basepoint = [-1, -1]
            self.temp_plist = self.temp_item.p_list[:]
        super().mouseReleaseEvent(event)


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """

    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', parent: QGraphicsItem = None):
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
            painter.drawPoint(*p)
        if self.selected:
            painter.setPen(QColor(255, 0, 0))
            painter.drawRect(self.boundingRect())

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
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        exit_act = file_menu.addAction('退出')
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
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 连接信号和槽函数
        exit_act.triggered.connect(qApp.quit)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
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
        self.setWindowTitle('CG Project')

        # 设置窗口图标
        self.setWindowIcon(QIcon('../picture/画笔.png'))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "确认", "确定要退出程序吗?",
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
            self.canvas_widget.start_draw_line('Naive', self.get_id()) # 这里发现一个问题，每次调用get_id时id都会递增，导致切换菜单选项时图元编号跳跃
        else:
            self.canvas_widget.start_draw_line('Naive', str(self.item_cnt-1))
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_line('DDA', self.get_id())  # 这里发现一个问题，每次调用get_id时id都会递增，导致切换菜单选项时图元编号跳跃
        else:
            self.canvas_widget.start_draw_line('DDA', str(self.item_cnt-1))
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_line('Bresenham', self.get_id())  # 这里发现一个问题，每次调用get_id时id都会递增，导致切换菜单选项时图元编号跳跃
        else:
            self.canvas_widget.start_draw_line('Bresenham', str(self.item_cnt-1))
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_polygon('DDA', self.get_id())  # 这里发现一个问题，每次调用get_id时id都会递增，导致切换菜单选项时图元编号跳跃
        else:
            self.canvas_widget.start_draw_polygon('DDA', str(self.item_cnt-1))
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_bresenham_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_polygon('Bresenham', self.get_id())  # 这里发现一个问题，每次调用get_id时id都会递增，导致切换菜单选项时图元编号跳跃
        else:
            self.canvas_widget.start_draw_polygon('Bresenham', str(self.item_cnt-1))
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_curve('bezier', self.get_id())  # 这里发现一个问题，每次调用get_id时id都会递增，导致切换菜单选项时图元编号跳跃
        else:
            self.canvas_widget.start_draw_curve('bezier', str(self.item_cnt-1))
        self.statusBar().showMessage('bezier算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_curve('b_spline', self.get_id())  # 这里发现一个问题，每次调用get_id时id都会递增，导致切换菜单选项时图元编号跳跃
        else:
            self.canvas_widget.start_draw_curve('b_spline', str(self.item_cnt-1))
        self.statusBar().showMessage('b_spline算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        if self.item_cnt == 0:
            self.canvas_widget.start_draw_ellipse(self.get_id())  # 这里发现一个问题，每次调用get_id时id都会递增，导致切换菜单选项时图元编号跳跃
        else:
            self.canvas_widget.start_draw_ellipse(str(self.item_cnt-1))
        self.statusBar().showMessage('绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def translate_action(self):
        if not self.canvas_widget.start_translate():
            self.statusBar().showMessage('选择图元')
        else:
            self.statusBar().showMessage('图元平移')

    def rotate_action(self):
        if not self.canvas_widget.start_rotate():
            self.statusBar().showMessage('选择图元')
        else:
            self.statusBar().showMessage('图元旋转')

    def scale_action(self):
        if not self.canvas_widget.start_scale():
            self.statusBar().showMessage('选择图元')
        else:
            self.statusBar().showMessage('图元缩放')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
