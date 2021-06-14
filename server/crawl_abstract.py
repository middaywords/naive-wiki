import bs4
import requests


def recursive_add_text(contents):
    abstract = ""
    for element in contents:
        if isinstance(element, str) or isinstance(element, bs4.NavigableString):
            abstract += element
        if isinstance(element, bs4.Tag):
            abstract += recursive_add_text(element.contents)

    return abstract


def get_abstract(url: str) -> str:
    """
    :param url: wiki url
    :return:
    """
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")
    res_set = soup.find_all("div", {"class": "mw-parser-output"})[0].find_all("p")
    abstract = ""
    for res in res_set:
        abstract += recursive_add_text(res.contents)

    return abstract[:150] + '...'


if __name__ == '__main__':
    print(get_abstract(url="https://en.wikipedia.org/wiki/Computer_accessibility"))
    print(get_abstract(url="https://en.wikipedia.org/wiki/Keyboard shortcut"))
    print(get_abstract(url="https://en.wikipedia.org/wiki/Scripting_language"))
