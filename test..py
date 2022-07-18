import core.function as fun
import core.fileHandle as fh
Glist = fh.csvResolve('dataset/wiki-vote.csv')
fun.paint(Glist,[],"测试")