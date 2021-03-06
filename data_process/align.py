import os
import subprocess

def add(pre_input, pre_trans):
    c = open("./fast_align/9999.c", "a", encoding='utf-8')
    c.write(pre_input)
    e = open("./fast_align/9999.e", "a", encoding='utf-8')
    e.write(pre_trans)
    c.close()
    e.close()

def add1(pre_input, pre_trans):
    c = open("./fast_align/9999.c", "a", encoding='utf-8')
    e = open("./fast_align/9999.e", "a", encoding='utf-8')
    print(pre_input)
    print(pre_trans)
    print(len(pre_input))
    print(len(pre_trans))
    e.write(pre_input)
    c.write(pre_trans)
    c.close()
    e.close()

def delete():
    with open('./fast_align/9999.c', 'r', encoding='utf-8') as cr:
        lines = cr.readlines()
    with open('./fast_align/9999.c', 'w', encoding='utf-8') as cw:
        for l in range(0,len(lines)-1):
            cw.write(lines[l])
    with open('./fast_align/9999.e', 'r', encoding='utf-8') as er:
        lines = er.readlines()
    with open('./fast_align/9999.e', 'w', encoding='utf-8') as ew:
        for l in range(0,len(lines)-1):
            ew.write(lines[l])
    cr.close()
    er.close()
    cw.close()
    ew.close()

def salign():
    f1 = open('./fast_align/fast.c-e', 'w',encoding = 'UTF-8')
    with open('./fast_align/9999.c', 'r',encoding = 'UTF-8') as f2:
        with open('./fast_align/9999.e', 'r', encoding='UTF-8') as f3:
            for line1,line2 in zip(f2,f3):
                f1.write(line1.strip('\n'))
                f1.write(' ||| ')
                f1.write(line2)
    fast = r'./fast_align/build/fast_align'
    atools = r'./fast_align/build/atools'
    fset = ['-i ./fast_align/fast.c-e -d -o -v > ./fast_align/forward.align']
    rset = ['-i ./fast_align/fast.c-e -d -o -v -r > ./fast_align/reverse.align']
    aset = ['-i ./fast_align/forward.align -j ./fast_align/reverse.align -c grow-diag-final-and > ./fast_align/final.align']
    fline = ' '.join([fast]+fset)
    rline = ' '.join([fast]+rset)
    aline = ' '.join([atools]+aset)
    fproc = subprocess.Popen(fline, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rproc = subprocess.Popen(rline, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def salign1():
    f1 = open('./fast_align/fast.e-c', 'w',encoding = 'UTF-8')
    with open('./fast_align/9999.e', 'r',encoding = 'UTF-8') as f2:
        with open('./fast_align/9999.c', 'r', encoding='UTF-8') as f3:
            for line1,line2 in zip(f2,f3):
                f1.write(line1.strip('\n'))
                f1.write(' ||| ')
                f1.write(line2)
    fast = r'./fast_align/build/fast_align'
    fset = ['-i ./fast_align/fast.c-e -d -o -v > ./fast_align/forward.align']
    rset = ['-i ./fast_align/fast.c-e -d -o -v -r > ./fast_align/reverse.align']
    fline = ' '.join([fast]+fset)
    rline = ' '.join([fast]+rset)
    fproc = subprocess.Popen(fline, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rproc = subprocess.Popen(rline, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def salign2():
    atools = r'./fast_align/build/atools'
    aset = ['-i ./fast_align/forward.align -j ./fast_align/reverse.align -c grow-diag-final-and > ./fast_align/final.align']
    aline = ' '.join([atools]+aset)
    aproc = subprocess.Popen(aline, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    aproc.communicate()


if __name__ == "__main__":
    salign()
    salign2()
