import zipfile as zf
import tempfile as tf
import os,re


def extract_zip(input_zip):
    input_zip=zf.ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}

unzipped=extract_zip('data/test.txt.zip')
found=(0,'')
for fname,value in unzipped.iteritems():
    if len(value) > found[0]:
        found=(len(value),value)

pat=re.compile('^([\d\s]+)\s+([\d\s]+)\s*\-\s*([^$]+)$')
cnt=0
for st in found[1].split('\n'):
    dst=st.decode('cp1251').encode('utf8')
    cnt+=1
    if cnt>10:
        break
    m=pat.search(dst)
    if m:
        print m.group(1),m.group(3)
