from argparse import ArgumentParser

from server import Server


def main(args):
    server = Server(port=args.port)
    server.run() # run forever


if __name__ == '__main__':

    # handle arg parser
    argparse = ArgumentParser()
    argparse.add_argument('-p', '--port', type=int, default=9527)
    args = argparse.parse_args()

    main(args)