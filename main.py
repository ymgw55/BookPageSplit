from pathlib import Path

import yaml


def loss(x, pages):
    n = len(pages)
    return sum((page - sum(pages) / n)**2 + (page - x)**2 for page in pages)


def objective(x, sections, n):
    pages = [0]*n

    y = 0
    cur = 0
    m = len(sections)

    splits = [[] for _ in range(n)]
    for p in range(n):
        while cur < m and y < x:
            y += sections[cur]['end'] - sections[cur]['start']
            splits[p].append(sections[cur])
            cur += 1

        pages[p] += y
        y = 0

        if cur == m:
            break

    for i in range(cur, m):
        pages[-1] += sections[i]['end'] - sections[i]['start']
        splits[p].append(sections[i])

    return loss(x, pages), splits


def main(config_path, n):
    with open(config_path, 'r') as yml:
        cfg = yaml.safe_load(yml)

    sections = cfg['sections']
    end = cfg['end']

    max_len = 0
    for sec_dict in sections[::-1]:
        assert sec_dict['start'] <= end
        sec_dict['end'] = end
        end = sec_dict['start']
        max_len = max(max_len, len(sec_dict['title']))

    lb = 1
    ub = 10**9
    while ((lb+2*ub) // 3 - (2*lb+ub) // 3) > 1:
        left = (2*lb+ub) // 3
        right = (lb+2*ub) // 3

        left_loss, left_splits = objective(left, sections, n)
        right_loss, right_splits = objective(right, sections, n)

        if left_loss < right_loss:
            ub = right
        else:
            lb = left

    if left_loss < right_loss:
        splits = left_splits
    else:
        splits = right_splits
    name = Path(config_path).stem
    output_path = Path('results') / f'{name}_{n}splits.txt'
    with open(str(output_path), 'w') as f:

        pages = [0]*n
        for i in range(n):
            if i < n - 1:
                pages[i] = splits[i+1][0]['start'] - splits[i][0]['start']
            else:
                pages[i] = cfg['end'] - splits[i][0]['start']

        def order_n(i):
            return {1: '1st', 2: '2nd', 3: '3rd'}.get(i) or f'{i}th'
        
        texts = []
        for i, page in enumerate(pages):
            texts.append(f'{order_n(i)}-split: about {page} pages')
            for split in splits[i]:
                title, start, sec, sub = \
                    split['title'], split['start'], split['sec'], split['sub']
                texts.append(f'{sec}.{sub} {title.ljust(max_len)} {start}')
            texts.append('='*(max_len+10))
        text = '\n'.join(texts)
        print(text, file=f)


if __name__ == '__main__':
    import fire
    fire.Fire(main)
