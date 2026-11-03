import json, re
GAP = 0.3; TAIL = 0.9
s = json.load(open('timed.json'))
segs, words, t = [], [], 0.0
for i, x in enumerate(s):
    d = x['dur']; start = t
    toks = x['text'].split()
    wts = [len(re.sub(r'\W', '', w)) + 2 + (3 if re.search(r'[.,:!?]$', w) else 0) for w in toks]
    a, b = start + 0.12, start + d - 0.15; tot = sum(wts); cur = a
    for w, wt in zip(toks, wts):
        e = cur + (b - a) * wt / tot
        words.append({'w': re.sub(r'[^\w\-]', '', w), 's': round(cur, 3), 'e': round(e, 3)}); cur = e
    t += d + GAP
    segs.append({'scene': x['scene'], 'start': round(start, 3), 'end': round(t, 3), 'audio': f'a{i}.wav'})
segs[-1]['end'] = round(t + TAIL, 3)
json.dump({'segs': segs, 'words': words, 'total': segs[-1]['end'], 'gap': GAP}, open('timeline.json', 'w'), ensure_ascii=False, indent=1)
print('total', segs[-1]['end'])
