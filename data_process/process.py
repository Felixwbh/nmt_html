import jieba

def preprocess(input: str) -> str:
    val = []
    strr = list(jieba.cut(input))
    sentence = ""
    word = 0
    count = 0
    while word < len(strr):
        if strr[word] == '<':
            tmp = []
            word += 1
            if strr[word] == '/':
                word += 1
                check = ""
                while strr[word] != '>':
                    check += strr[word] + " "
                    word += 1
                cc = len(val)
                while cc > 0:
                    if (val[cc - 1][0] == check.strip() and val[cc - 1][1] == 1):
                        val[cc - 1][1] = 0
                        break
                    cc -= 1
            else:
                tmp.append("")
                while strr[word] != '>':
                    tmp[0] += strr[word] + " "
                    word += 1
                tmp.append(1)
                tmp[0] = tmp[0].strip()
                val.append(tmp)

        else:
            for i in range(0, len(val)):
                if val[i][1] == 1:
                    val[i].append(count)
            count += 1
            sentence += strr[word] + " "
        word += 1
    return sentence.strip(),val

def backprocess(input:str, val) -> str:
    traval = input.strip().split()
    ali = open('./fast_align/final.align', 'r', encoding = 'UTF-8')
    strr = ali.readlines()[9999]
    test = []
    trans = ""
    for i in range(0, len(traval)):
        test.append([])
    for vall in val:
        tmpval = []
        tmpval.append(vall[0])
        for i in vall[2:]:
            for align in strr.split():
                tmp = align.split('-')
                tmp1 =tmp[0]
                tmp2 =tmp[1]
                if int(i) == int(tmp1) :
                    if tmpval[0] not in test[int(tmp2)]:
                        test[int(tmp2)].append(tmpval[0])
    for i in range(0, len(test)):
        if test[i] == []:
            trans += traval[i]+" "
            print(traval[i]+" ",end='')
        else:
            for j in range(0, len(test[i])):
                print("< " + test[i][j] + " > ",end='')
                trans += "< " + test[i][j] + "> "
            print(traval[i],end='')
            trans += traval[i]
            for j in range(len(test[i])-1, -1, -1):
                print("< / " + test[i][j] + " > ",end='')
                trans += "< / " + test[i][j] + "> "
    test = []
    return trans
