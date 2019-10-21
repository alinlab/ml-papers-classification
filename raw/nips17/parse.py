from urllib import request
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

URL = "https://nips.cc/Conferences/2017/Schedule?bySubject=&selectedSubject="
PAPER_URL = "http://papers.nips.cc/book/advances-in-neural-information-processing-systems-30-2017"

content = request.urlopen(URL).read().decode()
items = content.split("<input type=\"checkbox\" name=\"selectedSubject\"")[1:]

items = [item.split("</label>")[0] for item in items]
items = [[item.split("=")[1].split()[0][1:-1],
          item.split(">")[-1].strip()] for item in items]

print("{} Categories".format(len(items)))
with open("papers_categories.txt", "w") as f:
    for _, c in items:
        f.write(c + "\n")

papers_per_category = {}
for item in items:
    content = request.urlopen(URL + item[0]).read().decode()
    bs = BeautifulSoup(content, "html.parser")
    papers = bs.findAll("div", attrs={"class": "maincardBody"})
    papers = [p.text.strip().lower() for p in papers]
    papers_per_category[item[1]] = papers

content = request.urlopen(PAPER_URL).read().decode()
content.split("<ul>")[-1].split("</ul>")[0]
items = content.split("<li>")[2:]

print("{} Papers".format(len(items)))
bug_papers = []
with open("papers_info.txt", "w") as f:
    for item in items:
        pid = item.split("paper/")[1].split("-")[0]
        url = "http://papers.nips.cc" + item.split("\"")[1]
        content = request.urlopen(url).read().decode()
        bs = BeautifulSoup(content, 'html.parser')
        title = bs.find("h2", attrs={"class": "subtitle"}).text.strip()
        abstract = bs.find("p", attrs={"class": "abstract"}).text.strip()

        print(title)

        f.write(title + "\n")
        f.write(url + ".pdf\n")
        cs = []
        for c, papers in papers_per_category.items():
            for t in papers:
                if similar(t, title.lower()) > 0.9:
                    cs.append(c)
        if len(cs) == 0:
            bug_papers.append(title)
        f.write(" | ".join(cs) + "\n")
        f.write(abstract + "\n\n")
print(bug_papers)
