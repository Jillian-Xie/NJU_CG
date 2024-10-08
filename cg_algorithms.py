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
    if p_list == '':
        return []

    p_list = [[int(p[0]), int(p[1])] for p in p_list]

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


def Bezier(p_list, n, t):
    result = [p for p in p_list]
    for i in range(1, n):
        for j in range(n - i):
            result[j] = [(1 - t) * result[j][0] + t * result[j + 1][0], (1 - t) * result[j][1] + t * result[j + 1][1]]
    return result[0]


def deBoorCox(i, p, t):
    if p == 0:
        if i <= t and t < i + 1:
            return 1
        return 0
    return (t - i) / p * deBoorCox(i, p - 1, t) + (i + p + 1 - t) / p * deBoorCox(i + 1, p - 1, t)


def B_spline(p_list, t):
    result = [0, 0]
    for i, p in enumerate(p_list):
        B = deBoorCox(i, 3, t)
        result[0] += p[0] * B
        result[1] += p[1] * B
    return result


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    p_list = [[int(p[0]), int(p[1])] for p in p_list]
    num = len(p_list)
    if num == 0:
        return []
    elif num == 1:
        return [p_list[0]]
    result = [p_list[0]]
    n = 0
    delta = 1
    for i in range(num - 1):
        n += max(abs(p_list[i][0] - p_list[i + 1][0]), abs(p_list[i][1] - p_list[i + 1][1]))
    if not n == 0:
        delta = 1 / n
    if algorithm == 'Bezier':
        for i in range(1, n):
            result.append(Bezier(p_list, num, i * delta))
    # 参考课程：https://www.icourse163.org/learn/CAU-45006?tid=1450413503#/learn/announce
    elif algorithm == 'B-spline':
        if len(p_list) < 4:
            return [[int(p[0]), int(p[1])] for p in p_list]
        t = 3
        while t < num:
            result.append(B_spline(p_list, t))
            t += delta
    # 参考资料：https://www.icourse163.org/learn/CAU-45006?tid=1450413503#/learn/announce
    #           https://en.wikipedia.org/wiki/De_Boor%27s_algorithm
    return [[int(p[0]), int(p[1])] for p in result]


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    return [[p[0] + dx, p[1] + dy] for p in p_list]


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    rad = r * math.pi / 180
    p_list = [[int(p[0]), int(p[1])] for p in p_list]
    p_temp = [[x + (p[0] - x) * math.cos(rad) - (p[1] - y) * math.sin(rad), y + (p[0] - x) * math.sin(rad) + (p[1] - y) * math.cos(rad)] for p in p_list]
    return [[int(p[0]), int(p[1])] for p in p_temp]


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    p_list = [[int(p[0]), int(p[1])] for p in p_list]
    p_temp = [[p[0] * s + x * (1 - s), p[1] * s + y * (1 - s)] for p in p_list]
    return [[int(p[0]), int(p[1])] for p in p_temp]


def encode(x, y, x_min, y_min, x_max, y_max):
    code = [False, False, False, False]
    if x < x_min:
        code[0] = True
    if x > x_max:
        code[1] = True
    if y < y_min:
        code[2] = True
    if y > y_max:
        code[3] = True
    return code


def code_and(code1, code2):
    return [code1[0] and code2[0], code1[1] and code2[1], code1[2] and code2[2], code1[3] and code2[3]]


def code_or(code1, code2):
    return [code1[0] or code2[0], code1[1] or code2[1], code1[2] or code2[2], code1[3] or code2[3]]


def judge_inside(code):
    return not (code[0] or code[1] or code[2] or code[3])


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
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if algorithm == 'Cohen-Sutherland':
        code1 = encode(x0, y0, x_min, y_min, x_max, y_max)
        code2 = encode(x1, y1, x_min, y_min, x_max, y_max)
        while not (judge_inside(code1) and judge_inside(code2)):
            if not code_and(code1, code2) == [False, False, False, False]:
                return ''
            if code_or(code1, code2) == [False, False, False, False]:
                return [[int(x0), int(y0)], [int(x1), int(y1)]]
            if code1 == [False, False, False, False]:
                x0, y0, x1, y1 = x1, y1, x0, y0
                code1, code2 = code2, code1
            if code1[0]:
                y0 = y0 + (y1 - y0) * (x_min - x0) / (x1 - x0)
                x0 = x_min
            elif code1[1]:
                y0 = y0 + (y1 - y0) * (x_max - x0) / (x1 - x0)
                x0 = x_max
            elif code1[2]:
                x0 = x0 + (x1 - x0) * (y_min - y0) / (y1 - y0)
                y0 = y_min
            elif code1[3]:
                x0 = x0 + (x1 - x0) * (y_max - y0) / (y1 - y0)
                y0 = y_max
            code1 = encode(x0, y0, x_min, y_min, x_max, y_max)
            code2 = encode(x1, y1, x_min, y_min, x_max, y_max)
        return [[int(x0), int(y0)], [int(x1), int(y1)]]
    elif algorithm == 'Liang-Barsky':
        p = [x0 - x1, x1 - x0, y0 - y1, y1 - y0]
        q = [x0 - x_min, x_max - x0, y0 - y_min, y_max - y0]
        Uone = 0
        Utwo = 1
        for i in range(4):
            if p[i] < 0:
                Uone = max(Uone, q[i] / p[i])
            elif p[i] > 0:
                Utwo = min(Utwo, q[i] / p[i])
            elif p[i] == 0 and q[i] < 0:
                return ''
    if Uone > Utwo:
        return ''
    else:
        return [[int(x0 + Uone * p[1]), int(y0 + Uone * p[3])],
                [int(x0 + Utwo * p[1]), int(y0 + Utwo * p[3])]]
