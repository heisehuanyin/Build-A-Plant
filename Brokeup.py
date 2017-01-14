#!/usr/bin/python
# -*- Encoding:UTF-8 -*-
# 验证植物生长过程数学公式

cons_chushi = 30000         # 植物体营养蕴藏量
deg_root = 4                        # 初始植物体根须繁荣度，胚体折算值
deg_leaf = 140                        # 初试植物体茎叶繁荣度，胚芽折算值
xishu_zhizao = 0.05            # 植物体养分生成系数
xishu_xiaohao = 0.002           # 植物体养分消耗系数
persent_nxtstep = 0.4          # 植物体转阶段定比百分点
xishu_gxshengzhang = 0.00002      # 根须生长速率
xishu_jyshengzhang = 0.00002      # 茎叶生长速率
xishu_shengzhangxing = 0.0003    # 植物体生长过程消耗养分系数
zhanbi_rizhao = 0.3           # 植物体接受日照时间占整天时间的比例
deg_fanrong = 4050000000         # 植物体生长阶段最终极限


'''
    公式逻辑如下：
    y*(1+0.5*xishu_gxshengzhang)*xishu_xiaohao*time + y*xishu_gxshengzhang*time*xishu_shengzhangxing = cons_chushi*persent_nxtstep

    time = cons_chushi*persent_nxtstep / (y*( (1 + 0.5*xishu_gxshengzhang)*xishu_xiaohao + xishu_gxshengzhang*xishu_shengzhangxing) )

    营养物质消耗量 s = y*( (1 + 0.5*xishu_gxshengzhang)*xishu_xiaohao + xishu_gxshengzhang*xishu_shengzhangxing)*time

    根须整体生长度 ys= y*(1 + xishu_gxshengzhang)

    作为程序需要转换为渐次积累模式：

    如下：
'''

# 种子萌发

time = 0                    # 时间统计
nutrient_consume = 0                         # 营养消耗量统计

while True:
    time += 1
    nutrient_consume += deg_root * ((1 + 0.5 * xishu_gxshengzhang) * xishu_xiaohao + xishu_gxshengzhang * xishu_shengzhangxing)
    deg_root += deg_root * xishu_gxshengzhang

    if (cons_chushi*persent_nxtstep <= nutrient_consume):
        print '==当前阶段：种子萌发=========================='
        print '当前植物体繁荣度', deg_root
        print '当前时间：', time
        break


# 植物生长

ptime = 0                     # 第二阶段时间积累变量
J_light = 0.0                 # 日照时刻下的养分积累
X_day = 0.0                   # 植物体养分消耗量

while True:
    ptime += 1
    if ptime/3600 % 24 < 24*zhanbi_rizhao:                                    # 日照时刻养分积累控制
        J_light += deg_leaf * (1 + 0.5 * xishu_jyshengzhang) * xishu_zhizao     # 积累量

    # 日常消耗量统计（包括生长性消耗和呼吸消耗）
    X_day += xishu_xiaohao * (deg_leaf*(1 + 0.5 * xishu_jyshengzhang) + deg_root*(1+0.5*xishu_gxshengzhang))
    X_day += xishu_shengzhangxing * (deg_leaf * xishu_jyshengzhang + deg_root * xishu_gxshengzhang)

    # 如果本阶段积累量+初始积累量 < 本阶段营养消耗量 （植物体死亡）
    SZ_JL = J_light - X_day + cons_chushi - nutrient_consume

    deg_leaf += deg_leaf * xishu_jyshengzhang                                   # 茎叶繁荣度
    deg_root += deg_root * xishu_gxshengzhang                                   # 根须繁荣度

    if SZ_JL < 0:
        print '==当前阶段：植物生长============================'
        print '植物体死亡'
        print '当前阶段时间',ptime
        print '最终积累量', SZ_JL
        print '茎叶繁荣度', deg_leaf
        print '根茎繁荣度', deg_root
        break

    # 植物体整体繁荣度 》 预设转折点阈值
    if deg_leaf + deg_root > deg_fanrong:
        print '==植物开始坐果================================'
        print '本阶段时间', ptime
        print '最终积累量', SZ_JL
        print '茎叶繁荣度', deg_leaf
        print '根茎繁荣度', deg_root
        break

# 植物坐果
atime = 0                                               # 本阶段时间

while atime < 2600000:
    atime += 1
    if atime / 3600 % 24 < 24 * zhanbi_rizhao:
        J_light += deg_leaf * xishu_zhizao     # 积累量

    X_day += xishu_xiaohao * (deg_leaf + deg_root)
    SZ_JL = J_light - X_day

print '==当前阶段：坐果============================='
print '本阶段时间', atime
print '最终积累量', SZ_JL
print '茎叶繁荣度', deg_leaf
print '根茎繁荣度', deg_root