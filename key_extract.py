import getpass
import platform
import os
import logging

username = getpass.getuser()
operating_system = platform.platform()
logging.basicConfig(filename='passwords.log', format='%(message)s', level=logging.INFO)


def parse(log_file):
    password_set = set()
    with open(log_file, 'r') as f:
        for line in f:
            words = line.split(',')
            for word in words:
                if 'password' in word.lower() and 'signing' in word.lower():
                    password_set.add('{0} {1}'.format(line[:10], word))
    return password_set


def get_fullpath_nonwin(directory):
    log_files = ['{0}/{1}'.format(directory, filename) for filename
                 in os.listdir(directory) if 'idea.log' in filename]
    return log_files


def get_fullpath_win(directory):
    log_files = ['{0}\\{1}'.format(directory, filename) for filename
                 in os.listdir(directory) if 'idea.log' in filename]
    return log_files


if __name__ == '__main__':
    if 'windows' in operating_system.lower():
        logs_list = []
        password_uses = set()
        dir_path = 'C:\\Users\\{}'.format(username)
        android_dirs = ['{0}\\{1}\\system\\log'.format(dir_path, directory) for directory
                        in os.listdir(dir_path) if 'android' in directory.lower()]
        for directory in android_dirs:
            logs_list.extend(get_fullpath_win(directory))
        for log_file in logs_list:
            password_uses = password_uses | parse(log_file)
        for entry in sorted(password_uses):
            logging.info(entry)

    elif 'darwin' in operating_system.lower() or 'linux' in operating_system.lower():
        logs_list = []
        password_uses = set()
        dir_path = '/Users/{}/Library/Logs'.format(username)
        android_dirs = ['{0}/{1}'.format(dir_path, directory) for directory
                        in os.listdir(dir_path) if 'android' in directory.lower()]
        for directory in android_dirs:
            logs_list.extend(get_fullpath_nonwin(directory))
        for log_file in logs_list:
            password_uses = password_uses | parse(log_file)
        for entry in sorted(password_uses):
            logging.info(entry)

    else:
        print('I\'m sorry I\'m not familiar with your operating system')



