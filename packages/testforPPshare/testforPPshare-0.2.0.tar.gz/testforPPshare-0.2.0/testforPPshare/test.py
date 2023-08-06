import testforPPshare as tp
from fuzzywuzzy import process
import pandas as pd

df = pd.read_excel('./info.xlsx')
def get_method(df, name, mode=True):
    ls = df['describe']
    result = process.extractOne(name,ls)[0]
    method = df.loc[df['describe'] ==result,['method']].values[0][0]
    print(method)
    print(f"您希望获取的数据最可能是\"{result}\"，其调用方法为{method}")
    if mode:
        print("正在帮您获取数据……")
        return eval("tp."+method)()
    else:
        return 0

x = get_method(df,"chinbor")
print(x)

