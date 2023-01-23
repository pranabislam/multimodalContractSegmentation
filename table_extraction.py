from bs4 import BeautifulSoup
import re, os, json, statistics
import toc_labelling

def extract_td(cell):
    text = ''
    if cell.p:
        text = cell.p.text
    if cell.text:
        text = cell.text
    text = re.sub(r'[^\x00-\x7f]',r'', text) 
    text = text.replace("\n", " ")
    return text.strip()

def clean(table_list):
    try:
        num_cols = statistics.mode([len(x) for x in table_list])
    except statistics.StatisticsError as e:
        print('Multi mode, skipping')
        return table_list
    table_list = [x for x in table_list if len(x)==num_cols]
    return table_list


def parse_html(soup):
    table_holder = []
    for table in soup.find_all('table'):
        for row in table.tbody.find_all('tr'):
            row_holder = []
            for cell in row.find_all('td'):
                text = extract_td(cell)
                if text:
                    row_holder.append(text)
            if row_holder:
                table_holder.append(row_holder)
    if table_holder:
        table_holder = clean(table_holder)
    return table_holder
    
    
def filter_contents(s):
    multi_page_join_distance = 5000
    cont = re.split('table of contents', s, flags=re.IGNORECASE)
    if len(cont) == 1:
        cont = re.split('contents', s, flags=re.IGNORECASE)
    remaining = ''.join(cont[1:])
    ind_start = remaining.find('<table')
    remaining = remaining[ind_start:]

    indices = [m.start() for m in re.finditer('</table>', remaining, flags=re.IGNORECASE)]
    valid_index = [x for x in indices if x< multi_page_join_distance]
    if valid_index:
        print('Combining table on next page')
        return remaining[:valid_index[-1]+10]
    return remaining[:multi_page_join_distance]
 
def main():
    html_file_folder = '''/Users/shaan/My Drive/Master's DS/Capstone/project/multimodalContractSegmentation/cuad_htmls'''
    html_files = [x for x in os.listdir(html_file_folder) if x.endswith('.html')]
    data = {}
    for file in html_files:
        with open(os.path.join(html_file_folder, file), "r", encoding='latin1') as f:
            contents = f.read()
        
        contents = filter_contents(contents)
        s = BeautifulSoup(contents, 'lxml')
        table = parse_html(s)
        data[file] = table
        if not table:
            print(file)
   
    data = toc_labelling.extract_labels_to_folder(data)
    print(data)
   
    
if __name__ == "__main__":
   main()

