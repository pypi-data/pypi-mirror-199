# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
"""
<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.7,<=3.10-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/paddleocr_convert/"><img alt="PyPI" src="https://img.shields.io/pypi/v/paddleocr_convert"></a>
    <a href="https://pepy.tech/project/paddleocr_convert"><img src="https://static.pepy.tech/personalized-badge/paddleocr_convert?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
</p>

该模块是paddleocr_convert转换模型的核心代码。主要包括下载模型、解压模型、转换模型和更改模型为动态输入四部分。
由于目前`paddle2onnx`转换工具较为成熟，可以就没有添加转换前后模型精度验证是否满足要求的操作。

支持模型的url和本地路径两种输入方式。其中针对`rec`的模型，需要提供对应的字典文件，该库会自动将字典文件写入到onnx中。
这里需要搭配[RapidOCR](https://github.com/RapidAI/RapidOCR)推理代码使用

"""

from .main import PaddleOCRModelConvert
from .utils import download_file
