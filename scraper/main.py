from bs4 import BeautifulSoup
import requests

FAQ_URL = "https://drexel.edu/undergrad/apply/freshmen-instructions/faq/"

if __name__ == "__main__":
    response = requests.get(FAQ_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    file_name = (soup.title.string.rstrip().lstrip())

    with open(file_name + ".yaml", "w+") as f:
        # * Begin getting categories
        f.write('categories:\n')
        __categories = soup.findAll('h2')
        for cat in __categories:
            # ! Exclude <h2 id="site-title">
            if cat.find(id='bodytag_2_hlSiteName'):
                continue
            f.write("- " + cat.string + "\n")

        # * Begin getting conversations
        f.write('conversations:\n')
        __conversations = soup.findAll('h3')

        __article = soup.find('article')
        __article_children = __article.children
        # __article_children = list(filter(lambda child: (child.string != None ), __article_children))
        '''
        # ! Begin going down the tree:
        # * Ignore all h2 (already as categories)
        # * If see h3 -> create new question
        # * If see others (p and so on) -> add as answer
        '''
        answer = ""
        for art in __article_children:
            if art.name == "h2":
                # print(art)
                continue
            elif art.name == "h3":
                # print(art)
                if answer != "":
                    f.write("  - " + answer.replace(':', "-") + "\n")
                answer = ""
                f.write("- - " + art.string.replace(':', "-") + "\n")
            elif art.name == "p":
                try:
                    for content in art.contents:
                        answer += str(content).rstrip(']').lstrip('[').rstrip('"').rstrip("'").lstrip('"').lstrip("'").rstrip().lstrip()
                    # print((''.join(str(art.contents))))
                    # f.write("  - " + ''.join(str(art.contents)).rstrip(']').lstrip('[').rstrip('"').rstrip("'").lstrip('"').lstrip("'") + "\n")
                except:
                    pass
        
        # ! Just to make sure everything is printed out
        if answer != "":
            f.write("  - " + answer.replace(':', "-"))
        # print(__article)
        # for con in __conversations:
        #     print(con)

    # print(soup)
