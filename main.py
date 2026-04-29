from fetcher import fetch_quote


def main():
    content, author = fetch_quote()
    print(f'"{content}"')
    print(f"— {author}")


if __name__ == "__main__":
    main()
