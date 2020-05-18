from ftplib import FTP
import ftplib
import os
import logging


class FTPClient():
    def __init__(self, host, user='kubeedge', passwd='admin', port=0):
        self.port = port
        self.host = host
        self.user = user
        self.passwd = passwd
        self.ftp: FTP = None

    def login(self):
        self.ftp = FTP(self.host, self.user, self.passwd)

    def logout(self):
        self.ftp.quit()

    def download_file(self, path, dest_dir: str):
        self.login()
        logging.info(f'start downloading file:{path}')
        arr = path.split('/')
        for d in arr[:-1]:
            if d == '': continue
            logging.info(f'enter dir {d}')
            self.chdir(d)
        filename = arr[-1]
        try:
            dest_file = os.path.join(dest_dir, filename)
            self.ftp.retrbinary(f'RETR {filename}',
                                open(dest_file, 'wb').write)
        except ftplib.error_perm:
            logging.warning('ERROR: cannot read file "%s"' % filename)
            os.unlink(dest_file)
        else:
            logging.info('*** download file:%s to path:%s' % (filename, dest_file))
        self.ftp.cwd('/')
        self.logout()

    def upload_file(self, filename, dest: str):
        self.login()
        arr = dest.split('/')
        for d in arr[:-1]:
            if d == '': continue
            logging.info(f'enter dir {d}')
            self.chdir(d)

        try:
            logging.info(f'start uploading file:{filename}')
            self.ftp.storbinary(f'STOR {arr[-1]}',
                                open(filename, 'rb'))

        except ftplib.error_perm as e:
            logging.warning(e)
            logging.warning('ERROR: cannot read file "%s"' % filename)
        else:
            logging.info('*** uploaded file %s to CWD' % filename)
        self.ftp.cwd('/')
        self.logout()

    def chdir(self, dir):
        if self.directory_exists(dir) is False:
            self.ftp.mkd(dir)
        self.ftp.cwd(dir)

    def directory_exists(self, dir):
        filelist = []
        self.ftp.retrlines('LIST', filelist.append)
        for f in filelist:
            if f.split()[-1] == dir and f.upper().startswith('D'):
                return True
        return False
