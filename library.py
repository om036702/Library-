import pathlib
import csv
import re

class Library:
    #ログインしているユーザのインデックス　−1の時はチェックインされていない状態

    _libUser=-1

    _p = (pathlib.Path(__file__)).parent / 'data'
    _book_dat= _p / 'book.dat'
    _bookcat_dat= _p / 'bookcat.dat'
    _user_dat= _p / 'user.dat'
    _rent_dat= _p / 'rent.dat'

    def __init__(self):
        
        self.book=self.__load_data(Library._book_dat)
        self.bookcat=self.__load_data(Library._bookcat_dat)
        self.user=self.__load_data(Library._user_dat)
        self.rent=self.__load_data(Library._rent_dat)

    def userCheckin(self,Luser):
        if Library._libUser >= 0:
            print(f'別の利用者がチェックイン中です。チェックインできません')
            return 
        
        for i,v in enumerate(self.user):
            if Luser == v[0]:
                Library._libUser=i
                print(f'{Luser}({Library._libUser})はLibraryにチェックインされました')
                break
        else:
            print(f'ユーザ {Luser} は登録されていません')
            Library._libUser=-1
            return 

    def userCheckout(self,Luser):
        for i,v in enumerate(self.user):
            if Luser == v[0]:
                if Library._libUser==i:
                    print(f'{Luser}({Library._libUser})はLibraryにチェックアウトされました')
                    Library._libUser = -1
                    break
                else:
                    print(f'{Luser}({Library._libUser})はLibraryにチェックインされていません')
                    break
        else:
            print(f'ユーザ {Luser} は登録されていません')
            return 

    def userReg(self,Ruser):
        # ユーザの登録　（admin(0)ユーザのみ登録可能）
        if Library._libUser != 0:
            print('admin権限がないとユーザ登録できません')
            return
        
        for i,v in enumerate(self.user):
            if v[0]==Ruser:
                print(f'{Ruser}は登録されています。')
                return
        
        (self.user).append([Ruser,0])
        self.__save_data(Library._user_dat,self.user)

        print(f'{Ruser}は登録されました。')
        Library._libUser=-1

    def userList(self):
        # ユーザ一覧　（admin(0)ユーザのみ登録可能）
        if Library._libUser != 0:
            print('admin権限がないとこの処理はできません')
            return
        
        for i,v in enumerate(self.user):
            print(v)
                    
        Library._libUser=-1

    def bookOnLoan(self,bookCode):
        #本が貸し出し中かどうか判定する
        for i,v in enumerate(self.rent):
            if v[0]==bookCode:
                return i
        else:
            #貸し出しされていない
            return False

    def bookRent(self,bookCode):
        if self.bookCheck(bookCode) is False:
            print(f'{bookCode}はありません')
            return

        # 対象の本コードを貸し出す
        if Library._libUser == -1:
            print(f'チェックインされていないので貸し出しできません。')
            return

        if self.bookOnLoan(bookCode) is not False:
            print(f'{bookCode}は貸出中です')
            return
        
        w=int(self.user[Library._libUser][1])
        if w == 3:
            print(f'{self.user[Library._libUser][0]}の貸し出しは限度になっています。貸出できません')
            return

        self.user[Library._libUser][1]=w+1
        self.user[Library._libUser].append(bookCode)
        self.__save_data(Library._user_dat,self.user)
        (self.rent).append([bookCode,Library._libUser])
        self.__save_data(Library._rent_dat,self.rent)
        print(f'{self.user[Library._libUser][0]}に{bookCode}を貸出しました。')

    def bookReturn(self,bookCode):
        if self.bookCheck(bookCode) is False:
            print(f'{bookCode}はありません')
            return
        
        # 貸し出している本を返す処理
        bflg=False
        for i,row in enumerate(self.user):
            if row[1]!='0':
                for v in row[2:]:
                    if v == bookCode:
                        self.user[i].remove(bookCode)
                        self.user[i][1]=int(row[1])-1
                        self.__save_data(Library._user_dat,self.user)
                        self.rent = [row for row in self.rent if row[0] != bookCode]
                        self.__save_data(Library._rent_dat,self.rent)
                        print(f'{row[0]}が借りている{bookCode}を返却しました')

                        bflg=True
                        break
            if bflg:
                break
        else:
            print(f'{bookCode}は見つかりませんでした')

    def getBookName(self,bookCode):
        if self.bookCheck(bookCode) is False:
            print(f'{bookCode}はありません')
            return False

        # 本コードから本のタイトル、著者、貸し出し有無を確認する
        for i,v in enumerate(self.book):
            if v[0]==bookCode:
                if self.bookOnLoan(v[0]) is False:
                    w='  ***( 貸出できます }***'
                else:
                    w=', <<貸し出し中>>'
                print(f'{bookCode} タイトル:{v[1]},著者:{v[2]}{w}')
                return i
        else:
            print(f'対象のコード{bookCode}のタイトルは見つかりません')
            return False

    def allBookList(self):
        # 本全ての一覧（貸し出しの場合は***がついている）
        for v in self.book:
            if self.bookOnLoan(v[0]) is False:
                w='    '
            else:
                w='*** '
            
            print(f'{w}{v[0]},{v[1]},{v[2]}')

    def allBookcatList(self):
        # 本のカテゴリの一覧
        for v in self.bookcat:
            print(v)

    def selBookbyCat(self,catletter=''):
        # 本の一覧をカテゴリー別で一覧表示する
        # 正規表現パターンの設定
        if catletter:
            pattern = re.compile(r'^' + re.escape(catletter))
        else:
            pattern = re.compile(r'^.*')

        filtered_rows = []
        # 各行を処理
        for row in self.book:
            # 行の先頭の項目がパターンにマッチするか確認
            if pattern.match(row[0]):
                print(row)

    def bookCheck(self, bookCode):
        for i,row in enumerate(self.book):
            if bookCode == row[0]:
                return i
        else:
            return False
        
    def __load_data(self,fname):
    # ファイルを読み込むための関数
        with open(fname , 'r', encoding='utf-8') as f:
            data = csv.reader(f)
            l = [row for row in data]
        return l

    def __save_data(self,fname,buf):
    # ファイルを書き込むための関数
        with open(fname, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(buf)
        
        
if __name__=="__main__":
    user=Library()
#    user.userCheckin('admin')
    user.userCheckin('taro')
    user.allBookList()
#    user.allBookList()
#    user.getBookName('B01')


    '''
    user.userCheckin('admin')
    user.bookReturn('B91')
    user.allBookList()
    user.allBookcatList()
    user.userList()
    user.userList()
    user.getBookName('B01')
    user.userCheckin('hana')
    user.userReg('take')
    user.userCheckin('岡井')
    user.bookRent('C01')
    user.userCheckout('岡井')
    user.allBookList()
    user.userReg('岡井')
    user.bookReturn ('B001')
    user.bookReturn ('A010')
    user.allBookList()
    user.allBookcatList()
    user.selBookbyCat('B')
    '''