class James:
    """
    คลาส james คือ
    ข้อมูลที่เกี่ยวข้องกับ เจมส์
    ประกอบด้วยชื่อเพจ
    ชื่อช่องยูทูป

    Example
    #---------------------#
    jm = james()
    jm.show_name()
    jm.show_youtube()
    jm.show_page()
    jm.about()
    jm.show_art()
    #---------------------#
    """
    def __init__(self):
        self.name = 'james'
        self.page = 'https://www.facebook.com'

    def show_name(self):
        print('hello my name is {}'.format(self.name))

    def show_youtube(self):
        print('Youtube: https://www.youtube.com')

    def show_page(self):
        print('FB page {}'.format(self.page))

        

    def about(self):
        text = """ 
        #--------------------------------#
             hello hello hello hello 
        #--------------------------------#
        """
        print(text)
    
    def show_art(self):
        text = """ 
              .--.   |V|
             /    \ _| /
             q .. p \ /
              \--/  //
             __||__//
            /.    _/
           // \  /
          //   || jgs

          """
        print(text)

if __name__ == '__main__':
    jm = James()
    jm.show_name()
    jm.show_youtube()
    jm.show_page()
    jm.about()
    jm.show_art()

