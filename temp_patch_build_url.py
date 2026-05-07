import pathlib
import re
root = pathlib.Path('opds_abs')
changes = 0
for path in root.rglob('*.py'):
    text = path.read_text(encoding='utf-8')
    new_text = re.sub(r'(build_url\(|self\.build_url\()(f?["\'])(/opds/)', r'\1\2/', text)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        changes += 1
print(f'files changed: {changes}')
