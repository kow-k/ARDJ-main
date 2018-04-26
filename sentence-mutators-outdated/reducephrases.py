#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import string
import re
import Struc
import random
import CaboCha
from itertools import combinations

import io
out_enc = in_enc = "utf-8"
sys.stdin  = io.TextIOWrapper(sys.stdin.buffer, encoding=in_enc)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=out_enc)

if __name__=='__main__':
    import argparse
    # コマンドラインオプション
    ap=argparse.ArgumentParser(description="主節の述語に係る句を削除する")
    ap.add_argument('--debug',action='store_true',help='debug')
    ap.add_argument('--exclude_wa',action='store_true',help='"NPは"は削除しない')
    ap.add_argument('--lb',type=int,help='除去して残る句の数の下限(default:2)',default=2)
    args=ap.parse_args()
    cab=CaboCha.Parser('-f1')

    try:
        if args.debug: print("encoding: %s" % sys.getdefaultencoding())
        while True:
            inp=input().rstrip()
            if args.debug:
                print('Input : '+inp)

            cabocha=cab.parseToString(inp)
            sentence=Struc.structure(cabocha)
            target=sentence[len(sentence)-1]['deps']
            phrase=[]
            for c in sentence:
                temp=''
                for m in c['morphs']:
                    line=re.split('\t',m)
                    temp+=line[0]
                phrase.append(temp)
                                
            for i in range(len(phrase)):
                if i not in target and i != len(phrase)-1:
                    phrase[sentence[i]['link']]=phrase[i]+phrase[sentence[i]['link']]
                    phrase[i]=''

            phrase=[x for x in phrase if x!='']
            # 最後のchunkは固定
            pred=phrase.pop()

            # 削除対象の抽出
            phraseidx=[]
            for i in range(0,len(phrase)):
                if args.exclude_wa:
                    if not re.search('は(?:$|(?:，|、)$)',phrase[i]):
                        phraseidx.append(i)
                else:
                    phraseidx.append(i)
            
 
            # 削除する項を一つずつ増やしていく
            # 終了条件
            end=args.lb
            
            c=1
            if args.debug:
                print('Phrases:',phrase)
                print('Reduce Candidates:',phraseidx)
                
            while True:
                if len(phrase)-c<end: break

                if args.debug:
                    print('## delete',c,'phrase(s)')
                rests=combinations(phraseidx,c)
                for r in rests:
                    result=[]
                    for i in range(0,len(phrase)):
                        if not i in r:
                            result.append(phrase[i])
                    print(''.join(result)+pred)
                c+=1
            

    except EOFError:
        pass

## end of program
