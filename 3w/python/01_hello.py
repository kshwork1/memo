a = 'spartacodingclub@gmail.com'

#채워야하는 함수
def check_mail(s):


    mydomain = s
    search = "@"
    if search in mydomain:
        return True
    else:
        return False

#결과값
print(check_mail(a))

#아래와 같이 출력됩니다
True