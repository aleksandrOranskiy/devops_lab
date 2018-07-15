import argparse
import calendar
from datetime import datetime
import getpass
import requests


def get_args():

    parser = argparse.ArgumentParser(
        usage='\n%(prog)s [options] <user> [<repo>]'
              '\n%(prog)s --version'
              '\n%(prog)s (-h | --help)')
    parser.add_argument('-n', action='store_true', default=False,
                        dest='boolean_n', help='Number of days opened')
    parser.add_argument('-w', action='store_true', default=False,
                        dest='boolean_w', help='Day of the week opened')
    parser.add_argument('-H', action='store_true', default=False,
                        dest='boolean_H', help='Hour of the day opened')
    parser.add_argument('-u', action='store_true', default=False,
                        dest='boolean_u', help='User who opened')
    parser.add_argument('-a', action='store_true', default=False,
                        dest='boolean_a', help='Attached labels')
    parser.add_argument(metavar='<user>', type=str,
                        dest='username', help='the login to GitHub')
    parser.add_argument(metavar='[<repo>]', type=str, nargs='+',
                        dest='repos', help='a list of repos from GitHub')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    return args


def github_req(username, repo):
    login = input("Login to GitHub: ")
    password = getpass.getpass(prompt='Password: ')
    result = requests.get('https://api.github.com/repos/'
                          '{0}/{1}/pulls?'
                          'page=1&per_page=100'.format(username, repo),
                          auth=(login, password))
    return result


def func_n(date_format, pr_list):
    today = datetime.now()
    for pr in pr_list:
        pr_id = pr["id"]
        string_date = pr["created_at"]
        creation_date = datetime.strptime(string_date, date_format)
        delta = today - creation_date
        print("PR with id={0} opened {1} days".format(pr_id, delta.days))


def func_w(date_format, pr_list):
    for pr in pr_list:
        pr_id = pr["id"]
        string_date = pr["created_at"]
        creation_date = datetime.strptime(string_date, date_format)
        day = calendar.day_name[creation_date.weekday()]
        print("PR with id="
              "{0} opened in {1}".format(pr_id, day))


def func_h(date_format, pr_list):
    for pr in pr_list:
        pr_id = pr["id"]
        string_date = pr["created_at"]
        creation_date = datetime.strptime(string_date, date_format)
        print("PR with id={0} opened at {1} "
              "hour of the day".format(pr_id, creation_date.hour))


def func_u(date_format, pr_list):
    for pr in pr_list:
        pr_id = pr["id"]
        user = pr["user"]["login"]
        print("PR with id={0} opened by user {1}".format(pr_id, user))


def func_a(date_format, pr_list):
    for pr in pr_list:
        pr_id = pr["id"]
        labels = pr["labels"]
        print("Attached labels for PR with id={0}:\n".format(pr_id))
        for i in labels:
            print(i["name"])


def process():

    args = get_args()
    args_dict = {
        func_n: args.boolean_n,
        func_w: args.boolean_w,
        func_h: args.boolean_H,
        func_u: args.boolean_u,
        func_a: args.boolean_a
    }

    date_format = '%Y-%m-%dT%H:%M:%SZ'
    username = args.username
    for i in args.repos:
        request = github_req(username, i)
        pr_list = request.json()
        if len(pr_list):
            for k, v in args_dict.items():
                if v:
                    k(date_format, pr_list)
        else:
            print("There isn't any pull request in the repo", i)


process()
