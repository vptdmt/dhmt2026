import sys, json

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

with open('index_template.html', 'r', encoding='utf-8') as f:
    template = f.read()

output = template.replace('__DATA_PLACEHOLDER__', json_str)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(output)

print(f'Successfully built index.html! Size: {len(output):,} bytes')
