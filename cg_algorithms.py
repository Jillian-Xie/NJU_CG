#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]

    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0

    result = []
    dx = x1 - x0
    dy = y1 - y0

    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            k = dy / dx
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))

    elif algorithm == 'DDA':
        if x0 == x1:
            for y in range(min(y0, y1), max(y0, y1) + 1):
                result.append((x0, y))
        elif y0 == y1:
            for x in range(x0, x1 + 1):
                result.append((x, y0))
        elif dx == dy:
            for x in range(min(x0, x1), max(x0, x1) + 1):
                result.append((x, x - x0 + y0))
        elif dx == -dy:
            for x in range(x0, x1 + 1):
                result.append((x, -x + x0 + y0))
        else:
            k = dy / dx
            if abs(dx) > abs(dy):
                x = x0
                y = y0
                result.append((x, y))
                for i in range(abs(dx) + 1):
                    x = x + 1
                    y = y + k
                    result.append((x, round(y)))
            else:
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                m = 1 / k
                x = x0
                y = y0
                result.append((x, y))
                for i in range(abs(dy) + 1):
                    x = x + m
                    y = y + 1
                    result.append((round(x), y))

    elif algorithm == 'Bresenham':
        if x0 == x1:
            for y in range(min(y0, y1), max(y0, y1) + 1):
                result.append((x0, y))
        elif y0 == y1:
            for x in range(x0, x1 + 1):
                result.append((x, y0))
        elif dx == dy:
            for x in range(x0, x1 + 1):
                result.append((x, x - x0 + y0))
        elif dx == -dy:
            for x in range(x0, x1 + 1):
                result.append((x, -x + x0 + y0))
        else:
            k = dy / dx
            x = x0
            y = y0
            dx = abs(dx)
            dy = abs(dy)
            dx2 = 2 * dx
            dy2 = 2 * dy
            d = dx - dy2
            if 0 < k < 1:
                for i in range(dx + 1):
                    result.append((int(x), int(y)))
                    x = x + 1
                    if d < 0:
                        y = y + 1
                        d = d + dx2 - dy2
                    else:
                        d = d - dy2
            elif -1 < k < 0:
                for i in range(dx + 1):
                    result.append((int(x), int(y)))
                    x = x + 1
                    if d < 0:
                        y = y - 1
                        d = d + dx2 - dy2
                    else:
                        d = d - dy2
            elif k > 1:
                for i in range(dy + 1):
                    result.append((int(x), int(y)))
                    y = y + 1
                    if d < 0:
                        x = x + 1
                        d = d + dy2 - dx2
                    else:
                        d = d - dx2
            elif k < -1:
                for i in range(dy + 1):
                    result.append((int(x), int(y)))
                    y = y - 1
                    if d < 0:
                        x = x + 1
                        d = d + dy2 - dx2
                    else:
                        d = d - dx2

    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def my_draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list) - 1):
        line = draw_line([p_list[i], p_list[i + 1]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if x0 > x1:
        x0, x1 = x1, x0
    if y0 < y1:
        y0, y1 = y1, y0
    a = (x1 - x0) / 2
    b = (y0 - y1) / 2
    xc = (x0 + x1) / 2
    yc = (y0 + y1) / 2
    b2 = pow(b, 2)
    a2 = pow(a, 2)
    d = b2 - a2 * b + a2 / 4
    x = 0
    y = b
    result = []
    while a2 * y > b2 * x:
        result.append([x, y])
        result.append([x, -y])
        result.append([-x, y])
        result.append([-x, -y])
        if d < 0:
            d = d + b2 * (2 * x + 3)
        else:
            d = d + b2 * (2 * x + 3) + a2 * (-2 * y + 2)
            y = y - 1
        x = x + 1
    d = b2 * pow((x + 0.5), 2) + a2 * pow((y - 1), 2) - a2 * b2
    while y >= 0:
        result.append([x, y])
        result.append([x, -y])
        result.append([-x, y])
        result.append([-x, -y])
        # 此处课本更新d值的公式有误
        # 新的公式参考自 https://blog.csdn.net/u012866328/article/details/52607439
        if d < 0:
            d = d + 2 * b2 * x + 2 * b2 - 2 * a2 * y + 3 * a2
            x = x + 1
        else:
            d = d - 2 * a2 * y + 3 * a2
        y = y - 1

    for p in result:
        p[0] += xc
        p[1] += yc
        p[0] = int(p[0])
        p[1] = int(p[1])

    return result

def deCasteljau(p_list, n, i, t):
    if n == 0:
        return p_list[i]
    else:
        p1 = deCasteljau(p_list, n - 1, i, t)
        p2 = deCasteljau(p_list, n - 1, i + 1, t)
        return [(1 - t) * p1[0] + t * p2[0], (1 - t) * p1[1] + t * p2[1]]

def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    n = 0
    len = len(p_list)-1
    result = [p_list[0]]
    for i in range(len(p_list)-1):
        temp = max(abs(p_list[i][0] - p_list[i+1][0]), abs(p_list[i][1] - p_list[i+1][1]))
        n += temp
    delta = 1/n
    if algorithm == 'Bezier':
        for i in range(1, n):
            result.append(deCasteljau(p_list, len, 0, i * delta))
        return result
    elif algorithm == 'B-spline':
        pass

def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    pass
