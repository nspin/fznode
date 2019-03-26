def lines_of(f, eol=b'\0', chunk_size=0x2000):
    assert len(eol) == 1
    chunks = []
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            if any(chunks):
                raise Exception('no trailing eol')
            return
        if eol in chunk:
            lines = chunk.split(eol)
            chunks = [lines.pop()]
            it = iter(lines)
            yield b''.join(chunks) + next(it)
            yield from it
        else:
            chunks.append(chunk)
