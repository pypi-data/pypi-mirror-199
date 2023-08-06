import testforPPshare as tp
from fuzzywuzzy import process
import pandas as pd
import os


def get_method(name, mode=True):
    df = pd.read_excel(
        f'{os.path.dirname(os.path.realpath(__file__))}\info.xlsx')
    ls = df['describe']
    result = process.extractOne(name, ls)[0]
    method = df.loc[df['describe'] == result, ['method']].values[0][0]
    print(method)
    print(f"您希望获取的数据最可能是\"{result}\"，其调用方法为{method}")
    if mode:
        print("正在帮您获取数据……")
        return eval("tp." + method)()
    else:
        return 0


if __name__ == '__main__':
    x = get_method("中国企业商品价格指数")
    print(x)
