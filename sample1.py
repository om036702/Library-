'''
import sys
import os

# 親ディレクトリのパスを取得
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 親ディレクトリをsys.pathに追加
sys.path.append(parent_dir)
'''

from library import Library
user=Library()
user.allBookList()
user.bookReturn('B01')
exit()
user.getBookName('B01')
user.userCheckin('taro')
i=user.getBookName('B01')
print(i)
exit()
if i:
    user.bookRent('B01')
else:
    print('not found')
exit()

user.bookReturn('B09')
