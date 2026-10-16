"""Small, non-overwriting file helpers with actionable input errors."""
import json
from pathlib import Path
from hashlib import sha256


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def read_rows(path):
    rows = []
    for line_number,line in enumerate(Path(path).read_text(encoding='utf-8-sig').splitlines(),1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f'{path}, line {line_number}: invalid JSON ({exc.msg}).') from exc
        if not isinstance(value,dict):
            raise ValueError(f'{path}, line {line_number}: expected a JSON object.')
        rows.append(value)
    return rows


def encode(value, jsonl=False):
    if jsonl:
        return ''.join(json.dumps(row,ensure_ascii=False,allow_nan=False)+'\n' for row in value)
    return json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n'


def write(path,value,jsonl=False):
    content = encode(value,jsonl)
    target = Path(path)
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(content)


def write_bundle(directory, documents, metadata):
    """Validate/serialize everything before reserving a new output directory."""
    target = Path(directory)
    if target.exists():
        raise ValueError(f'{directory} already exists. Choose a new run directory; existing results are never overwritten.')
    encoded = {name:encode(value,jsonl) for name,(value,jsonl) in documents.items()}
    encoded['manifest.json'] = encode({**metadata,'files':{
        name:sha256(text.encode('utf-8')).hexdigest() for name,text in encoded.items()}})
    target.parent.mkdir(parents=True,exist_ok=True)
    target.mkdir()  # Also rejects a directory created concurrently.
    for name,text in encoded.items():
        with (target/name).open('x',encoding='utf-8',newline='\n') as stream:
            stream.write(text)
