import requests
from bs4 import BeautifulSoup

def get_word_data(word):
    url = f"https://urdu.wordinn.com/{word}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": f"Failed to fetch data for '{word}'"}

    soup = BeautifulSoup(response.text, 'html.parser')
    data = {'word': word.capitalize()}

    # --- Extract only English meaning ---
    meaning_section = soup.select_one('#content .section.center-align')
    if meaning_section:
        eng_meaning_tag = meaning_section.find_all('p')
        eng_meaning = eng_meaning_tag[0].text.strip() if eng_meaning_tag else ''
        data['meaning'] = [eng_meaning] if eng_meaning else []

    # --- Extract example sentences (only if both EN and HI exist) ---
    examples = []
    example_h2 = soup.find('h2', string="Example Sentences")
    if example_h2:
        for subsec in example_h2.find_all_next('div', class_='subsec'):
            ps = subsec.find_all('p')
            if not ps:
                continue
            eng = ps[0].text.strip()
            hin = subsec.find('p', class_='hdfont')
            if eng and hin and hin.text.strip():
                examples.append((eng, hin.text.strip()))
            next_tag = subsec.find_next_sibling()
            if next_tag and next_tag.name == 'h2':
                break
    data['examples'] = examples

    return data
