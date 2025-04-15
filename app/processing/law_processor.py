import requests
import xml.etree.ElementTree as ET

OC = "chetera"
BASE = "http://www.law.go.kr"

def get_law_list_from_api(query):
    url = f"{BASE}/DRF/lawSearch.do?OC={OC}&target=law&type=XML&display=100&search=2&knd=A0002&query={query}"
    res = requests.get(url)
    res.encoding = 'utf-8'
    laws = []
    if res.status_code == 200:
        root = ET.fromstring(res.content)
        for law in root.findall("law"):
            name = law.findtext("법령명한글").strip()
            mst = law.findtext("법령일련번호")
            detail = law.findtext("법령상세링크")
            full_link = BASE + detail
            laws.append({"법령명": name, "MST": mst, "URL": full_link})
    return laws

def get_law_text_by_mst(mst):
    url = f"{BASE}/DRF/lawService.do?OC={OC}&target=law&MST={mst}&type=XML"
    res = requests.get(url)
    res.encoding = 'utf-8'
    if res.status_code == 200:
        return res.content
    return None

def find_term_in_articles(xml_data, query):
    tree = ET.fromstring(xml_data)
    articles = tree.findall(".//조문")
    matches = []
    for article in articles:
        jo = article.findtext("조번호")
        hang_texts = article.findall("항")
        if not hang_texts:
            content = article.findtext("조문내용", "")
            if query in content:
                matches.append((jo, None))
        else:
            for hang in hang_texts:
                ha = hang.findtext("항번호")
                text = hang.findtext("항내용", "")
                if query in text:
                    matches.append((jo, ha))
    return matches

def process_laws(query):
    result_lines = []
    law_list = get_law_list_from_api(query)
    for law in law_list:
        xml_data = get_law_text_by_mst(law["MST"])
        if not xml_data:
            continue
        matches = find_term_in_articles(xml_data, query)
        if matches:
            line = f"① {law['법령명']} " + ", ".join(
                [f"제{jo}조" + (f"제{ha}항" if ha else "") for jo, ha in matches]
            ) + f" 중 “{query}”"
            result_lines.append(line)
    return "\n".join(result_lines)
