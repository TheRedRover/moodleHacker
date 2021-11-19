import argparse

parser = argparse.ArgumentParser(description='Moodle parser')
parser.add_argument("--password", type=str, help="Password flag")
parser.add_argument("--login", type=str, help="Login flag")
parser.add_argument("--no-logs", type=bool, default=True, help="Show logs in commands line")
args = parser.parse_args()

print(args.password)