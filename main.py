from pathlib import Path

import yaml
import unicodedata


# https://note.nkmk.me/python-unicodedata-east-asian-width-count/
def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count


def loss(x, pages):
    n = len(pages)
    return sum((page - sum(pages) / n)**2 + (page - x)**2 for page in pages)


def objective(x, sections, n):
    pages = [0]*n

    y = 0
    cur = 0
    m = len(sections)

    splits = [[] for _ in range(n)]
    sec_count = [0]*n
    for p in range(n):
        sec_set = set()
        while cur < m and y + sections[cur]['end'] - sections[cur]['start'] <= x:
            y += sections[cur]['end'] - sections[cur]['start']
            splits[p].append(sections[cur])
            sec_set.add(sections[cur]['sec'])
            cur += 1

        pages[p] += y
        sec_count[p] += len(sec_set)
        y = 0

        if cur == m:
            break

    sec_count[-1] = 0
    for i in range(cur, m):
        pages[-1] += sections[i]['end'] - sections[i]['start']
        splits[-1].append(sections[i])

    sec_set = set()
    for sec in splits[-1]:
        sec_set.add(sec['sec'])
    sec_count[-1] += len(sec_set)

    K = 2
    L = loss(x, pages)
    L += sum((K * max(c-1, 0))**2 for c in sec_count)
    return L, splits, pages


def main(config_path, n, show_pages=True):
    with open(config_path, 'r') as yml:
        cfg = yaml.safe_load(yml)

    sections = cfg['sections']
    end = cfg['end']

    max_len = 0
    for sec_dict in sections[::-1]:
        assert sec_dict['start'] <= end
        sec_dict['end'] = end
        end = sec_dict['start']
        max_len = max(max_len, get_east_asian_width_count(sec_dict['title']))

    lb = 1
    ub = 10**9
    while ((lb+2*ub) // 3 - (2*lb+ub) // 3) > 1:
        left = (2*lb+ub) // 3
        right = (lb+2*ub) // 3

        left_loss, left_splits, lpages = objective(left, sections, n)
        right_loss, right_splits, rpages = objective(right, sections, n)

        if left_loss < right_loss:
            ub = right
        else:
            lb = left

    if left_loss < right_loss:
        splits = left_splits
        pages = lpages
        print(f'left: {left}')
    else:
        splits = right_splits
        pages = rpages
        print(f'right: {right}')
    print(pages)

    name = Path(config_path).stem
    output_path = Path('results') / f'{name}_{n}splits.txt'
    with open(str(output_path), 'w') as f:

        def order_n(i):
            return {1: '1st', 2: '2nd', 3: '3rd'}.get(i) or f'{i}th'

        texts = []
        for i, page in enumerate(pages):
            if show_pages:
                texts.append(f'{order_n(i+1)} Part, about {page} pages')
            else:
                texts.append(f'{order_n(i+1)} Part')
            for split in splits[i]:
                title, start, sec, sub = \
                    split['title'], split['start'], split['sec'], split['sub']
                if show_pages:
                    title += f' {start}'
                texts.append(f'{sec}.{sub} {title}')
            texts.append('='*(max_len+10))
        text = '\n'.join(texts)
        print(text, file=f)


if __name__ == '__main__':
    import fire
    fire.Fire(main)
