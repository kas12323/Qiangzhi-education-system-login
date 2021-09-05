# -*- coding:utf-8 -*-
# Author: Jin Zichen
import requests
import os
import base64
from bs4 import BeautifulSoup

session = requests.session()
login_url = 'http://jiaowu.qlmu.edu.cn/jsxsd'
main_page_url = login_url + '/framework/xsMain.jsp'
user_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                          'application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Proxy-Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38'}


def base64_encode(user, pwd):  # 将用户名和密码进行编码提交给服务器
    a = base64.b64encode(user.encode('utf-8'))
    b = base64.b64encode(pwd.encode('utf-8'))
    return a.decode('utf-8') + '%%%' + b.decode('utf-8')


def login():  # 登录教务系统
    global session, login_url, user_headers
    verify_code_url = login_url + '/verifycode.servlet'
    post_user_info_url = login_url + '/xk/LoginToXk'
    session.get(login_url, headers=user_headers)
    get_verify_code = session.get(verify_code_url, headers=user_headers)
    with open('verifycode.jfif', 'wb') as verify_code_file:
        verify_code_file.write(get_verify_code.content)
        verify_code_file.close()
    user_name = input('请输入用户名, 按回车确认\n')
    user_pwd = input('请输入密码，按回车确认\n')
    os.system('start verifycode.jfif')
    verify_code = input('即将打开验证码图片，请输入图片中的验证码，按回车确认\n')
    os.system('del verifycode.jfif')
    data = {'userAccount': user_name,
            'userPassword': '',
            'RANDOMCODE': verify_code,
            'encoded': base64_encode(user_name, user_pwd)}
    post_user_info = session.post(post_user_info_url, data=data, headers=user_headers, allow_redirects=False)
    return post_user_info


def check_if_logged_in(login_page):  # 检查是否成功登录
    global main_page
    main_page = session.get(main_page_url, headers=user_headers)
    try:
        main_page.raise_for_status()
        return False
    except:
        soup = BeautifulSoup(login_page.text, 'html.parser')
        wrong_info = soup.find_all(id="showMsg")[0].string
        if '验证码' in wrong_info:
            print('验证码输入有误，请重新输入')
        elif '用户名' in wrong_info:
            print('用户名或密码输入有误，请重新输入')
        else:
            print('信息输入有误，请重新输入')
        return True


# 以下是主程序的开始
if __name__ == '__main__':
    while check_if_logged_in(login()):
        pass
