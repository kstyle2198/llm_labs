#pip install "gensim==3.8.2"
#pip install scipy==1.12

from gensim.summarization.summarizer import summarize
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping


if __name__ == "__main__":
    text = '''This document contains confidential proprietary information.
            Hence, the reproduction, transfer and/or utilization in whole
            or in part are prohibited without the written permission of
            Hyundai Samho Heavy Industries Co., Ltd.'''
    print(summarize(text))