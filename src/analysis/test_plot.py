import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def test_plot():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # 创建图形
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, label="sin(x)")
    plt.title("Simple Sinusoidal Curve")
    plt.xlabel("x values")
    plt.ylabel("y values")
    plt.legend()
    # 在Streamlit应用程序中显示图形
    st.pyplot()
