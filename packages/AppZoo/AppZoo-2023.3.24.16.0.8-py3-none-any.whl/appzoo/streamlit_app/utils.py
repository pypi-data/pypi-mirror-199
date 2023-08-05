#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : utils
# @Time         : 2022/10/18 下午1:29
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import textwrap
import streamlit as st
from streamlit.components.v1 import html


def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")
        

def columns_placed(bins=2, default_position=0, gap='small'):  # ("small", "medium", or "large")
    _ = st.columns(spec=bins, gap=gap)
    if len(_) < default_position:
        default_position = -1
    return _[default_position]


def show_code(func):
    """Showing the code of the demo."""
    _ = st.sidebar.checkbox("Show code", False)
    if _:
        # Showing the code of the demo.
        st.markdown("---")
        st.markdown("## Main Code")
        sourcelines, _ = inspect.getsourcelines(func)
        st.code(textwrap.dedent("".join(sourcelines[1:])))
        st.markdown("---")


def st_form(before_submit, after_submit, label='Submit', key='Form', ):
    with st.form(key):
        before_submit
    submitted = st.form_submit_button(label)
    if submitted:
        after_submit


def display_pdf(base64_pdf, width='100%', height=1000):
    pdf_display = f"""<embed src="data:application/pdf;base64,{base64_pdf}" width="{width}" height="{height}" type="application/pdf">"""

    st.markdown(pdf_display, unsafe_allow_html=True)


def display_html(text='会飞的文字'):  # html("""<marquee bgcolor="#00ccff" behavior="alternate">这是一个滚动条</marquee>""")
    _ = f"""
        <marquee direction="down" width="100%" height="100%" behavior="alternate" style="border:solid"  bgcolor="#00FF00">

          <marquee behavior="alternate">

            {text}

          </marquee>

        </marquee>
        """
    st.markdown(_, unsafe_allow_html=True)
