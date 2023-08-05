import login_gmail_selenium.util as LGS_util
import login_gmail_selenium.common as LGS_common
import time
import os

if __name__ == '__main__':
    option = 3
    if option == 1:
        # No proxy
        profile = LGS_util.profile.ChromeProfile('krinxng@gmail.com',
                                                 '9docVqRsOqaIVB8LdMi3kHuDi',
                                                 'careyshe441470@hotmail.com')
        # profile = LGS_util.profile.ChromeProfile('gmail',
        #                                          'password',
        #                                          'backup')
    elif option == 2:
        # For private proxy
        proxy_folder = os.path.join(LGS_common.constant.PROXY_FOLDER, f'proxy_auth')
        profile = LGS_util.profile.ChromeProfile('krinxng@gmail.com',
                                                 '9docVqRsOqaIVB8LdMi3kHuDi',
                                                 'careyshe441470@hotmail.com',
                                                 'private',
                                                 None,
                                                 'user22996:SKB3RN@51.81.141.133:22996',
                                                 'http',
                                                 proxy_folder)
        # profile = LGS_util.profile.ChromeProfile('gmail',
        #                                          'password',
        #                                          'backup',
        #                                          'private',
        #                                          None,
        #                                          'username:pass@ip:port',
        #                                          'http',
        #                                          proxy_folder)
    else:
        # For public proxy
        proxy_folder = os.path.join(LGS_common.constant.PROXY_FOLDER, f'proxy_auth')
        profile = LGS_util.profile.ChromeProfile('krinxng@gmail.com',
                                                 '9docVqRsOqaIVB8LdMi3kHuDi',
                                                 'careyshe441470@hotmail.com',
                                                 'public',
                                                 None,
                                                 '173.255.208.224:30034',
                                                 'http',
                                                 proxy_folder)

    driver = profile.retrieve_driver()
    profile.start()
    driver.get('https://www.google.com/')
    time.sleep(1000)
    driver.quit()
