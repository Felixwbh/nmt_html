import subprocess
import os

def align_batchce(input_data: list) -> list:
    # prepare input data for fast_align
    align_input_buffer = b''
    for l in input_data:
        align_input_buffer += (l.strip() + '\n').encode('utf-8')

    # define commands
    build_root = os.path.dirname(os.path.abspath(__file__))
    fast_align_path = os.path.join(build_root, 'fast_align')
    atools_path = os.path.join(build_root, 'atools')
    fwd_cmd = fast_align_path + " -i - -d -T 3.07189 -m 1.21854 -f fwd_params"
    rev_cmd = fast_align_path + " -i - -d -T 6.64282 -m 0.907299 -f rev_params -r"
    atools_cmd = atools_path + " -i - -j - -c grow-diag-final-and"

    # run fast_align in forward
    fwd_proc = subprocess.Popen(fwd_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    fwd_outs, _ = fwd_proc.communicate(input=align_input_buffer)
    fwd_outs = fwd_outs.decode("utf-8").strip().split("\n")
    #print(fwd_outs)

    # run fast_align in reverse
    rev_proc = subprocess.Popen(rev_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    rev_outs, _ = rev_proc.communicate(input=align_input_buffer)
    rev_outs = rev_outs.decode("utf-8").strip().split("\n")
    #print(rev_outs)

    # sanity check
    assert(len(fwd_outs) == len(rev_outs))

    # prepare input data for atools
    atools_input_buffer = b''
    for fwd_l, rev_l in zip(fwd_outs, rev_outs):
        #print(fwd_l)
        #print(rev_l)
        atools_input_buffer += (fwd_l.split('|||')[2].strip() + '\n').encode('utf-8')
        atools_input_buffer += (rev_l.split('|||')[2].strip() + '\n').encode('utf-8')

    # run atools
    atools_proc = subprocess.Popen(atools_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    # run fast_align in forward
    fwd_proc = subprocess.Popen(fwd_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    fwd_outs, _ = fwd_proc.communicate(input=align_input_buffer)
    fwd_outs = fwd_outs.decode("utf-8").strip().split("\n")
    #print(fwd_outs)

    # run fast_align in reverse
    rev_proc = subprocess.Popen(rev_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    rev_outs, _ = rev_proc.communicate(input=align_input_buffer)
    rev_outs = rev_outs.decode("utf-8").strip().split("\n")
    #print(rev_outs)

    # sanity check
    assert(len(fwd_outs) == len(rev_outs))

    # prepare input data for atools
    atools_input_buffer = b''
    for fwd_l, rev_l in zip(fwd_outs, rev_outs):
        #print(fwd_l)
        #print(rev_l)
        atools_input_buffer += (fwd_l.split('|||')[2].strip() + '\n').encode('utf-8')
        atools_input_buffer += (rev_l.split('|||')[2].strip() + '\n').encode('utf-8')

    # run atools
    atools_proc = subprocess.Popen(atools_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    atools_outs, _ = atools_proc.communicate(input=atools_input_buffer)
    atools_outs = atools_outs.decode("utf-8").strip().split("\n")
    #print(atools_outs)
    #print(len(atools_outs))
    return atools_outs


if __name__ == '__main__':
    input_data = [
        "地处 西北 边陲 的 伊犁 是 我国 对外开放 的 重要 窗口 , 改革开放 以来 , 伊犁 经济 获得 长足 发展 , 人民 生活水平 迅速 提高 . ||| located in the country 's northwestern border , yili has served as an important window during the country 's opening up to the outside world . since reform and opening up , yili has developed the economy by a large margin and rapidly improved the people 's livelihood .",
        "地处 西北 边陲 的 伊犁 是 我国 对外开放 的 重要 窗口 , 改革开放 以来 , 伊犁 经济 获得 长足 发展 , 人民 生活水平 迅速 提高 . ||| located in the country 's northwestern border , yili has served as an important window during the country 's opening up to the outside world . since reform and opening up , yili has developed the economy by a large margin and rapidly improved the people 's livelihood .",
        "地处 西北 边陲 的 伊犁 是 我国 对外开放 的 重要 窗口 , 改革开放 以来 , 伊犁 经济 获得 长足 发展 , 人民 生活水平 迅速 提高 . ||| located in the country 's northwestern border , yili has served as an important window during the country 's opening up to the outside world . since reform and opening up , yili has developed the economy by a large margin and rapidly improved the people 's livelihood .",
        "地处 西北 边陲 的 伊犁 是 我国 对外开放 的 重要 窗口 , 改革开放 以来 , 伊犁 经济 获得 长足 发展 , 人民 生活水平 迅速 提高 . ||| located in the country 's northwestern border , yili has served as an important window during the country 's opening up to the outside world . since reform and opening up , yili has developed the economy by a large margin and rapidly improved the people 's livelihood .",
        "地处 西北 边陲 的 伊犁 是 我国 对外开放 的 重要 窗口 , 改革开放 以来 , 伊犁 经济 获得 长足 发展 , 人民 生活水平 迅速 提高 . ||| located in the country 's northwestern border , yili has served as an important window during the country 's opening up to the outside world . since reform and opening up , yili has developed the economy by a large margin and rapidly improved the people 's livelihood .",
        "地处 西北 边陲 的 伊犁 是 我国 对外开放 的 重要 窗口 , 改革开放 以来 , 伊犁 经济 获得 长足 发展 , 人民 生活水平 迅速 提高 . ||| located in the country 's northwestern border , yili has served as an important window during the country 's opening up to the outside world . since reform and opening up , yili has developed the economy by a large margin and rapidly improved the people 's livelihood .",
        "地处 西北 边陲 的 伊犁 是 我国 对外开放 的 重要 窗口 , 改革开放 以来 , 伊犁 经济 获得 长足 发展 , 人民 生活水平 迅速 提高 . ||| located in the country 's northwestern border , yili has served as an important window during the country 's opening up to the outside world . since reform and opening up , yili has developed the economy by a large margin and rapidly improved the people 's livelihood .",
        "地处 西北 边陲 的 伊犁 是 我国 对外开放 的 重要 窗口 , 改革开放 以来 , 伊犁 经济 获得 长足 发展 , 人民 生活水平 迅速 提高 . ||| located in the country 's northwestern border , yili has served as an important window during the country 's opening up to the outside world . since reform and opening up , yili has developed the economy by a large margin and rapidly improved the people 's livelihood .",
        "地处 西北 边陲 的 伊犁 是 我国 对外开放 的 重要 窗口 , 改革开放 以来 , 伊犁 经济 获得 长足 发展 , 人民 生活水平 迅速 提高 . ||| located in the country 's northwestern border , yili has served as an important window during the country 's opening up to the outside world . since reform and opening up , yili has developed the economy by a large margin and rapidly improved the people 's livelihood .",
        "地处 西北 边陲 的 伊犁 是 我国 对外开放 的 重要 窗口 , 改革开放 以来 , 伊犁 经济 获得 长足 发展 , 人民 生活水平 迅速 提高 . ||| located in the country 's northwestern border , yili has served as an important window during the country 's opening up to the outside world . since reform and opening up , yili has developed the economy by a large margin and rapidly improved the people 's livelihood ."
        ]
    input_data1 = ["京 公网 安备 11000002000001 号 ||| beijing <unk> <unk> <unk>", "返回 顶部 ||| return to the top"]
    _ = align_batch(input_data1)
    #align_batch(input_data)
