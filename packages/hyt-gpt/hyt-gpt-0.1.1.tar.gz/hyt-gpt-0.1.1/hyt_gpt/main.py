from yt_gpt import summary


def main():
    print("Hello, World!")

    ylink = 'https://www.youtube.com/watch?v=exuzPI59yg4'
    res = summary(ylink)
    print(res)


if __name__ == "__main__":
    main()
