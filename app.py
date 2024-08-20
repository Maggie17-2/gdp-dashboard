import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Bar3D
import streamlit as st
import datetime

# 上传Excel文件
st.title("3D 打卡图")
uploaded_file = st.file_uploader("上传Excel文件", type=["xlsx"])

if uploaded_file is not None:
    sheets2 = pd.ExcelFile(uploaded_file).sheet_names
    sheet2_name = sheets2[-1]

    df = pd.read_excel(uploaded_file, sheet_name=sheet2_name)

    # 处理数据
    df['时间'] = pd.to_datetime(df['时间'])  # 转换为 datetime 对象
    df['小时'] = df['时间'].dt.hour  # 提取小时
    df['星期'] = df['时间'].dt.dayofweek  # 提取星期，0=Monday, 6=Sunday

    # 创建数据列表
    data3d = []
    for _, row in df.iterrows():
        day_index = row['星期']
        hour_index = row['小时']
        data3d.append([day_index, hour_index, 1])  # 每条记录计为 1 次活动

    # 将数据格式化为 [hour_index, day_index, count]
    data3d = [[hour, day, sum(1 for d in data3d if d[0] == day and d[1] == hour)] for day in range(7) for hour in
              range(24)]

    # 创建 3D 柱状图
    c3 = (
        Bar3D()
        .add(
            series_name="活动次数",
            data=data3d,
            xaxis3d_opts=opts.Axis3DOpts(type_="category", data=[f"{hour}时" for hour in range(24)]),
            yaxis3d_opts=opts.Axis3DOpts(type_="category",
                                         data=["周一", "周二", "周三", "周四", "周五", "周六", "周日"]),
            zaxis3d_opts=opts.Axis3DOpts(type_="value"),
        )
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(
                # max_=20,  # 根据实际数据调整最大值
                range_color=[
                    "#313695", "#4575b4", "#74add1", "#abd9e9",
                    "#e0f3f8", "#ffffbf", "#fee090", "#fdae61",
                    "#f46d43", "#d73027", "#a50026",
                ],
            )
        )
    )

    # 使用 Streamlit 显示图表
    # st.title("活动的 3D 打卡图")
    st.components.v1.html(c3.render_embed(), width=1200, height=500)



