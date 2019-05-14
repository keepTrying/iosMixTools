#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys
import random
import string
import re
import hashlib
import time
import json
import shutil
import hashlib 
import time
import argparse
import codecs

methodPrefix = ""
classPrefix = ""
codePath = ""
methodList = set()
classList = set()

script_path = os.path.split(os.path.realpath(sys.argv[0]))[0]

#确保添加的函数不重名
randomName_set = set()

#单词列表，用以随机名称
with open(os.path.join(script_path, "./word_list.json"), "r") as fileObj:
    word_name_list = json.load(fileObj)

#获取一个随机名称
def getOneName():
    global word_name_list
    index = random.randint(0,len(word_name_list))
    name = word_name_list[index]
    return name
def parse_args():
    parser = argparse.ArgumentParser(description='生成混淆头文件.\n')
    parser.add_argument('--method_prefix', dest='method_prefix', type=str, required=True, default="", help='方法前缀')
    parser.add_argument('--class_prefix', dest='class_prefix', type=str, required=True, default="", help='类名前缀')
    parser.add_argument('--code_path', dest='code_path', type=str, required=True, default="", help='代码文件夹路径')
    args = parser.parse_args()
    return args

def createHeader():
    with open(os.path.join(codePath,'oc_mix.h'),'w') as file:
        str = '#ifndef OC_MIX_H\n#define OC_MIX_H\n\n'
        for name in methodList:
            str += '#ifndef ' + name + '\n#define '+ name + ' ' + getOneName()+'\n'+'#endif\n'
        str = str + '\n#endif'
        file.write(str)
        
def main():
    arr = '//'.__class__
    global methodPrefix,classPrefix,codePath,classList,methodList
    app_args = parse_args()
    methodPrefix = app_args.method_prefix
    classPrefix = app_args.class_prefix
    codePath = app_args.code_path

    if not os.path.exists(codePath):
        print ("code path not exists: " + codePath)
        exit(0)
    
    for parent, folders, files in os.walk(codePath):
        for file in files:
            if (file.endswith(".h") or file.endswith(".m") or file.endswith(".mm")) and file.startswith(classPrefix):
                full_path = os.path.join(parent, file)

                with open(full_path, "r") as fileObj:
                    lines = fileObj.readlines()
                for line in lines:
                    line=line.strip()
                    c = line.__class__                      
                    if len(line)==0:                 
                        continue
                    
                    if line.startswith('@interface ') and not '()' in line:
                        strs = line.split(" ")
                        if len(strs)==1:
                            continue
                        className = line.split(" ")[1]
                        classList.add(className)

                        # print("\n classLine:"+line)
                        print("\n className:"+className)
                    
                    if line.startswith('-') and (')'+ methodPrefix+'_') in line:
                        # print("\n methodLine:"+line)
                        if '//'in line:
                            index = line.find('//')
                            line = line[0:index]
                        firstStr = line.split(':')[0]
                        index = firstStr.find(methodPrefix+'_')
                        firstStr = firstStr[index:]
                        firstStr = firstStr.replace('{','')
                        firstStr = firstStr.replace(';','')
                        firstStr = firstStr.strip()
                        methodList.add(firstStr)
                        print("\n method:"+firstStr)
    
    createHeader()
    print ("finish!")

if __name__ == "__main__":
    main()