import core.function as fun
import core.fileHandle as fh
Glist = fh.csvResolve('dataset/bitcoinData.csv')
fun.paint(Glist,[],"测试")
# fun.paint(Glist,[1, 4, 6, 7, 13, 537, 425],"测试")