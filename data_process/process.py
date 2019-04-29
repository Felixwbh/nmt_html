import jieba
val = []


def preprocess(input: str) -> str:
    strr = list(jieba.cut(input))
    print(strr)
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
    return sentence.strip()
