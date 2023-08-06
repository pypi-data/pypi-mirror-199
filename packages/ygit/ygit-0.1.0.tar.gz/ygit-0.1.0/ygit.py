import gc, socket, ssl, struct, os, zlib, io, binascii, hashlib, json, collections, time

if not hasattr(gc, 'mem_free'):
  class FakeGC:
    def __init__(self):
      pass
    def mem_free(self):
      return 0
    def collect(self):
      pass
  gc = FakeGC()

try:
  from zlib import DecompIO
except ImportError:
  def DecompIO(f):
    bytes = f.read()
    dco = zlib.decompressobj()
    dec = dco.decompress(bytes)
    f.seek(f.tell()-len(dco.unused_data))
    return io.BytesIO(dec)

try:
  from btree import open as btree
except ImportError:
  import pickle

try: FileNotFoundError
except NameError:
  FileNotFoundError = OSError

Commit = collections.namedtuple("Commit", ("tree", "author"))

class DB:
  def __init__(self, fn):
    self._fn = fn
    self._f = None

  def __enter__(self):
    try:
      btree
      try:
        self._f = open(self._fn, "r+b")
      except OSError:
        self._f = open(self._fn, "w+b")
      self._db = btree(self._f, pagesize=512)
    except NameError:
      try:
        with open(self._fn,'rb') as f:
          self._db = pickle.load(f)
      except FileNotFoundError:
        self._db = {}
    return self
    
  def __exit__(self, type, value, traceback):
    if hasattr(self._db, 'close'):
      self._db.close()
    else:
      with open(self._fn,'wb') as f:
        pickle.dump(self._db, f)
        #print('saving', self._fn, self._db)
    if self._f: self._f.close()

  def __setitem__(self, key, item):
    self._db[key] = item

  def __getitem__(self, key):
    return self._db[key]

  def get(self, key, default=None):
    return self._db.get(key, default=default)

  def __delitem__(self, key):
    del self._db[key]

  def keys(self):
    return self._db.keys()

  def values(self):
    return self._db.values()

  def items(self):
    return self._db.items()

  def __contains__(self, item):
    return item in self._db

  def __iter__(self):
    return iter(self._db)

  def flush(self):
    if hasattr(self._db, 'flush'):
      self._db.flush()
     

def _read_headers(x):
  while line:=x.readline():
    #print('resp header', line)
    if not line.strip(): break

def _read_kind_size(f):
  byt = struct.unpack("B", f.read(1))[0]
  kind = (byt & 0x70) >> 4
  size = byt & 0x0F
  offset = 4
  while byt & 0x80:
    byt = struct.unpack("B", f.read(1))[0]
    size += (byt & 0x7F) << offset
    offset += 7
  return kind, size

def _read_little_size(f):
  size = bshift = 0
  while True:
    byt = f.read(1)[0]
    size |= (byt & 0x7f) << bshift
    if byt & 0x80 == 0:
      break
    bshift += 7
  return size

def _read_offset(f):
  offset = 0
  while True:
    byt = f.read(1)[0]
    offset = (offset << 7) | (byt & 0x7f)
    if byt & 0x80 == 0:
      break
    offset += 1
  return offset
  
  
_ODSDeltaCmd = collections.namedtuple("_ODSDeltaCmd", ('start','append','base_start','nbytes'))

class _ObjReader:

  def __init__(self, f):
    self.f = f
    self.start = f.tell()
    self.kind, self.size = _read_kind_size(f)
    #print('osize:', self.size)
  
  def __del__(self):
    print('__del__')

  # https://git-scm.com/docs/pack-format#_deltified_representation
  def _parse_ods_delta(self):
    if hasattr(self, 'cmds'): return
    #print('_parse_ods_delta')
    offset = _read_offset(self.f)
    self.base_object_offset = self.start - offset
    #print('obase_object_offset', self.base_object_offset, self.start, offset)
    #print('DecompIO')
    gc.collect()
    try:
      dec_stream = DecompIO(self.f)
      self.cmds = []
      pos = 0
      base_size = _read_little_size(dec_stream)
      self.size = obj_size = _read_little_size(dec_stream)
      #print('_handle_delta2', 'base_size', base_size, 'obj_size', obj_size)
      while ch := dec_stream.read(1):
        byt = ch[0]
        if byt == 0x00: continue
        if (byt & 0x80) != 0: # copy command
          vals = io.BytesIO()
          for i in range(7):
            bmask = 1 << i
            if (byt & bmask) != 0:
              vals.write(dec_stream.read(1))
            else:
              vals.write(b'\x00')
          start = int.from_bytes(vals.getvalue()[0:4], 'little')
          nbytes = int.from_bytes(vals.getvalue()[4:6], 'little')
          if nbytes == 0:
            nbytes = 0x10000
          self.cmds.append(_ODSDeltaCmd(pos, None, start, nbytes))
          pos += nbytes
        else: # append command
          nbytes = byt & 0x7f
          to_append = dec_stream.read(nbytes)
          assert nbytes==len(to_append)
          self.cmds.append(_ODSDeltaCmd(pos, to_append, None, nbytes))
          pos += nbytes
    finally:
      del dec_stream
      gc.collect()
     
    #print(self.cmds)
    gc.collect()

  def __enter__(self):
    #print('__enter__', self, self.kind)
    #print('before', gc.mem_free(), gc.collect() or 'after', gc.mem_free(), '@', self)
    gc.collect()
    try:
      if self.kind==6: # ofs-delta
        self._parse_ods_delta()
        self.return_to_pos = self.f.tell()
        self.pos = 0
        self.f.seek(self.base_object_offset)
        self.base_obj_reader = _ObjReader(self.f)
        self.base_obj_pos = None
        return self
      else:
        self.decompressed_stream = DecompIO(self.f)
        return self.decompressed_stream
    finally:
      gc.collect()
    
  def __exit__(self, type, value, traceback):
    #print('__exit__', self, self.kind, hasattr(self,'decompressed_stream'))
    if self.kind==6:
      del self.base_obj_pos
      self.base_obj_reader.__exit__(None, None, None)
      del self.base_obj_reader
      if hasattr(self, 'decompressed_stream'):
        del self.decompressed_stream
      self.f.seek(self.return_to_pos)
      gc.collect()
    else:
      if hasattr(self, 'decompressed_stream'):
        # if exception is thrown during __enter__, this won't exist and trying to delete it will hide/swallow the original
        del self.decompressed_stream
      gc.collect()
    #print(self, self.kind, hasattr(self, 'base_obj_stream'), hasattr(self, 'base_obj_reader'), hasattr(self, 'decompressed_stream'))
    #assert gc.mem_free()>80000
    #if gc.mem_free()<80000: help(self)
  
  # DecompIO doesn't support seek, so fake it
  # every seek either moves forward or reloads the stream
  # fortunately pack files *mostly* copy from increasing offsets, so the performance isn't horrible
  # alt: we could temp write the base object to disk, but that has other concerns.  (what if not enough space? how many writes will wear out the flash?)
  def _base_obj_stream_seek(self, pos):
    if self.base_obj_pos is None:
      gc.collect()
      self.base_obj_reader.__enter__()
      self.base_obj_pos = 0
    if pos < self.base_obj_pos:
      # reset
      gc.collect()
#      print('resetting', self.base_obj_reader.decompressed_stream)
      try:
        self.base_obj_reader.__exit__(None, None, None)
      finally:
        del self.base_obj_reader
      gc.collect()
      self.f.seek(self.base_object_offset)
      self.base_obj_reader = _ObjReader(self.f)
      gc.collect()
      self.base_obj_reader.__enter__()
      self.base_obj_pos = 0
    while self.base_obj_pos < pos:
      toss = self.base_obj_reader.decompressed_stream.read(min(512,pos-self.base_obj_pos))
      self.base_obj_pos += len(toss)
    #print('self.base_obj_pos == pos',self.base_obj_pos, pos)
    assert self.base_obj_pos == pos
  
  def read(self, nbytes):
    ret = io.BytesIO()
    for cmd in self.cmds:
      #print('self.pos', self.pos, cmd)
      if not nbytes: break
      if cmd.start+cmd.nbytes < self.pos: continue
      if cmd.append:
        to_append = cmd.append[self.pos-cmd.start:min(nbytes,cmd.nbytes)]
        #print('append',to_append,len(to_append), nbytes,cmd.nbytes)
      else:
        #print('cmd.base_start+self.pos-cmd.start',cmd.base_start+self.pos-cmd.start)
        self._base_obj_stream_seek(cmd.base_start+self.pos-cmd.start)
        to_append = self.base_obj_reader.decompressed_stream.read(min(nbytes,cmd.nbytes-(self.pos-cmd.start)))
        self.base_obj_pos += len(to_append)
        #print('copy',to_append,len(to_append), nbytes,cmd.nbytes)
      ret.write(to_append)
      nbytes -= len(to_append)
      self.pos += len(to_append)
    ret = ret.getvalue()
    #print('read', len(ret), ret)
    return ret

  def digest(self):
    kind = self.kind
    with self as f:
      #print('cmd.base_start+self.pos-cmd.start','xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
      if kind==6:
        kind = self.base_obj_reader.kind
      h = hashlib.sha1()
      if kind==1: h.update(b'commit ')
      elif kind==2: h.update(b'tree ')
      elif kind==3: h.update(b'blob ')
      else: raise Exception('unknown kind', kind)
      #print('kind', kind, self.size)
      h.update(str(self.size).encode())
      h.update(b'\x00')
      #xxx = b''
      while data := f.read(512):
        #print('gotbytes', len(data))
        h.update(data)
        #xxx += data
      del f
      gc.collect()
    gc.collect()
    #assert gc.mem_free()>80000
    digest = h.digest()
    #print('xxx', len(xxx), xxx)
    #print('self.digest', kind, self.size, 'sig', binascii.hexlify(digest))
    #with open('xxxxx.py', 'wb') as f:
    #  f.write(xxx)
    #assert not xxx.startswith(b'# This workflow will install Python dependencies')
    return digest
    
  
def _read_until(f, stop_byte):
  buf = io.BytesIO()
  while byt:=f.read(1):
    buf.write(byt)
    if byt==stop_byte: break
  return buf.getvalue()

    
def _parse_pkt_file(git_dir, fn, db):
  #print('parse_pkt_file', git_dir, fn)
  pkt_id = int(fn.split('.')[0])
  #print('pkt_digest',pkt_digest)
  with open(f'{git_dir}/{fn}','rb') as f:
    assert f.read(4)==b'PACK'
    version = struct.unpack('!I', f.read(4))[0]
    #print('git pack version:', version)
    del version
    cnt = struct.unpack('!I', f.read(4))[0]
    print('reading', cnt, 'objs from', fn)
    for i in range(cnt):
      fpos = f.tell()
      o = _ObjReader(f)
      kind = o.kind
      size = o.size
      #print('kind:', kind, o.kind)
      #print('size:', size)
      #print('where', f.tell())
      assert kind!=0
      idx = struct.pack('QBQQQ', pkt_id, kind, f.tell(), size, fpos)
      sig = o.digest()
      db[sig] = idx
      #db.flush()
      #print('idx', f.tell(), binascii.hexlify(sig), fn, struct.unpack('BQQQ', idx[20:]))
#      print('unused_data', len(dco.unused_data), dco.unused_data)
#      print('unconsumed_tail', dco.unconsumed_tail)
#      print('eof', dco.eof)
      #print('where', f.tell())
#      f.seek(f.tell()-len(dco.unused_data))
    print('done at', f.tell(), 'remaining', len(f.read()))
    #TODO parse tail, which is hash of packet

def _read_pkt_lines(x, git_dir):
  #print('_read_pkt_lines')
  HEAD = None
  tfn = f'{git_dir}/tmp.pack'
  pack_size = 0
  with open(tfn,'wb') as f:
    while pkt_bytes := x.read(4):
      #print('pkt_bytes', pkt_bytes)
      pkt_bytes = int(pkt_bytes,16)
      #print('pkt_bytesi', pkt_bytes)
      pkt_bytes -= 4
      if pkt_bytes>0:
        buf = io.BytesIO()
        channel = x.read(1)
        pkt_bytes -= 1
        if channel==b'\x01':
          while pkt_bytes>0:
            data = x.read(min(512,pkt_bytes))
            pkt_bytes -= len(data)
            #print('pack', len(data), data)
            f.write(data)
            pack_size += len(data)
        else:
          buf.write(channel)
          while pkt_bytes>0:
            bits = x.read(min(512,pkt_bytes))
            if not bits: break
            pkt_bytes -= len(bits)
            buf.write(bits)
            #print('bits', pkt_bytes, bits)
          #print('channel', channel, buf.getvalue())
          data = buf.getvalue()
          if data[40:46]==b' HEAD ':
            HEAD = data[:40]
            print('HEAD:',HEAD.decode())
          if data.startswith(b'\x02'):
            print('info:', data[1:].decode().strip())
          else:
            print('UNK:', data)
  if pack_size:
#    with open(tfn,'rb') as f:
      #f.seek(-20, 2) #SEEK_END
#      sig = f.read(20)
      #assert f.read(1)==b''
    l = len([s for s in os.listdir(git_dir) if s.endswith('.pack')])
    fn = f'{l}.pack'
    #print('tfn',tfn, f'{git_dir}/{fn}')
    
    #print('pack_size',pack_size)
    os.rename(tfn, f'{git_dir}/{fn}')
    return HEAD, [fn]
  else:
    os.remove(tfn)
    return HEAD, []


def _post(repo, data=None):
  proto, _, host, path = repo.split("/", 3)
  port = 443 if proto=='https:' else 80
  if ':' in host:
    host, port = host.split(':',1)
    port = int(port)
  s = socket.socket()
  s.connect((host, port))
  if proto=='https:':
    s = ssl.wrap_socket(s)
  x = s.makefile("rb") if hasattr(s,'makefile') else s
  send = s.send if hasattr(s,'send') else s.write
  req = f'POST /{path}/git-upload-pack HTTP/1.0\r\n'
  send(req.encode())
  headers = {
    'Host': host,
    'User-Agent': 'git/2.37.2',
    'Accept-Encoding': 'deflate, gzip, br, zstd',
    'Content-Type': 'application/x-git-upload-pack-request',
    'Accept': 'application/x-git-upload-pack-result',
    'Git-Protocol': 'version=2',
    'Content-Length': str(len(data)),
  }
  for k,v in headers.items():
    send(f'{k}: {v}\r\n'.encode())
  send(b'\r\n')
  if data:
    send(data)
  return s,x


def _isdir(fn):
  try:
    return (os.stat(fn)[0] & 0x4000) != 0
  except OSError:
    return False


def rmrf(directory):
  git_dir = f'{directory}/.ygit'
  if _isdir(git_dir):
    print('removing ygit repo at', git_dir)
    for fn in os.listdir(git_dir):
      os.remove(f'{directory}/.ygit/{fn}')
    os.rmdir(git_dir)


def init(repo, directory, cone=None):
  git_dir = f'{directory}/.ygit'
  if _isdir(git_dir):
    raise Exception(f'fatal: ygit repo already exists at {git_dir}')
  if not _isdir(directory):
    os.mkdir(directory)
  os.mkdir(git_dir)
  with DB(f'{git_dir}/config') as db:
    db[b'repo'] = repo.encode()
    if cone:
      db[b'cone'] = cone.encode()


def clone(repo, directory, shallow=True, cone=None, quiet=False, commit=b'HEAD'):
  print(f'cloning {repo} into {directory}')
  init(repo, directory, cone=cone)
  pull(directory, quiet=quiet, shallow=shallow, commit=commit)


def checkout(directory, commit=b'HEAD'):
  if isinstance(commit,str):
    commit = commit.encode()
  git_dir = f'{directory}/.ygit'
  with DB(f'{git_dir}/idx') as db:
    if commit==b'HEAD':
      commit = db[b'HEAD']
    print('checking out', commit.decode())
    commit = _get_commit(git_dir, db, commit)
    #print(commit)
    for mode, fn, digest in _walk_tree(git_dir, db, directory, commit.tree):
      #print('entry', repr(mode), int(mode), fn, binascii.hexlify(digest) if digest else None)
      if int(mode)==40000:
        if not _isdir(fn):
          os.mkdir(fn)
      else:
        _checkout_file(git_dir, db, fn, digest)


def _checkout_file(git_dir, db, fn, ref):
  #print('_checkout_file',git_dir, db, fn, ref)
  if not ref: return
  if ref not in db:
    raise Exception(f'unknown ref for file:{fn} sig:{binascii.hexlify(ref)}')
  ref_data = db[ref]
  pkt_id, kind, pos, size, ostart = struct.unpack('QBQQQ', ref_data)
  #print('kind', kind)
  assert kind in (3,6)
  h = hashlib.sha1()
  h.update(b'blob ')
  h.update(str(size).encode())
  h.update(b'\x00')
  try:
    with open(fn,'rb') as f:
      while data:=f.read(1024):
        h.update(data)
    #print('actual', binascii.hexlify(h.digest()), 'desired', binascii.hexlify(ref))
    update = h.digest()!=ref
  except FileNotFoundError:
    update = True
  if update:
    if kind==3: kind = 'BLOB'
    if kind==6: kind = 'OFS_DELTA'
    print('writing:', fn, f'({kind})')
    pkt_fn = f'{git_dir}/{pkt_id}.pack'
    with open(pkt_fn, 'rb') as pkt_f:
      pkt_f.seek(ostart)
      with _ObjReader(pkt_f) as fin:
        with open(fn, 'wb') as fout:
          while data:=fin.read(512):
            fout.write(data)
        del fin
  gc.collect()

        #print('cccccbefore', gc.mem_free(), gc.collect() or 'after', gc.mem_free())
  

def _get_commit(git_dir, db, ref):
  data = db[binascii.unhexlify(ref)]
  pkt_id, kind, pos, size, ostart = struct.unpack('QBQQQ', data)
  assert kind==1
  fn = f'{git_dir}/{pkt_id}.pack'
  with open(fn, 'rb') as f:
    f.seek(pos)
    #print('DecompIO3')
    s1 = DecompIO(f)
    tree, author = None, None
    #print('dddddbefore', gc.mem_free(), gc.collect() or 'after', gc.mem_free())
    while line:=s1.readline():
      if line==b'\n': break
      k,v = line.split(b' ',1)
      if k==b'tree': tree = v.strip().decode()
      if k==b'author': author = v.strip().decode()
    del s1
  gc.collect()
  #print('bbbbbefore', gc.mem_free(), gc.collect() or 'after', gc.mem_free())
  return Commit(tree, author)

  
def _walk_tree(git_dir, db, directory, ref):
  if isinstance(ref, str):
    ref = binascii.unhexlify(ref)
  data = db[ref]
  pkt_id, kind, pos, size, ostart = struct.unpack('QBQQQ', data)
  assert kind==2
  fn = f'{git_dir}/{pkt_id}.pack'
  with open(fn, 'rb') as f:
#    print('gc.mem_free()',gc.mem_free())
#    gc.collect()
#    print('gc.mem_free()',gc.mem_free())
    f.seek(pos)
    next = []
    #print('DecompIO4')
    s2 = DecompIO(f)
    to_yield = []
    while line:=_read_until(s2, b'\x00'):
      digest = s2.read(20)
      mode, fn = line[:-1].decode().split(' ',1)
      fn = f'{directory}/{fn}'
      if mode=='40000':
        to_yield.append((mode, fn, None))
        next.append((fn, digest))
      if mode=='160000':
        print('ignoring submodule', fn,'(unsupported)')
      else:
        to_yield.append((mode, fn, digest))
    del s2
    gc.collect()
    #print('aaaabefore', gc.mem_free(), gc.collect() or 'after', gc.mem_free())
    yield from to_yield
    for fn, digest in next:
      yield from _walk_tree(git_dir, db, fn, digest)


def pull(directory, shallow=True, quiet=False, commit=b'HEAD'):
  if fetch(directory, quiet=quiet, shallow=shallow, commit=commit):
    checkout(directory, commit=commit)

  
def fetch(directory, shallow=True, quiet=False, commit=b'HEAD'):
  if isinstance(commit,str):
    commit = commit.encode()
  git_dir = f'{directory}/.ygit'
  with DB(f'{git_dir}/config') as db:
    repo = db[b'repo'].decode()
  print(f'fetching: {repo} @ {commit.decode()}')

  if commit==b'HEAD':
    s,x = _post(repo, b'0014command=ls-refs\n0014agent=git/2.37.20016object-format=sha100010009peel\n000csymrefs\n000bunborn\n0014ref-prefix HEAD\n001bref-prefix refs/heads/\n0000')
    _read_headers(x)
    commit = HEAD = _read_pkt_lines(x, git_dir)[0]
    s.close()

  with DB(f'{git_dir}/idx') as db:

    if commit:
      print(f'HEAD=>{commit.decode()}')
    else:
      print('fetched an empty repo')
      return False
  
    if binascii.unhexlify(commit) in db:
      print('up to date!')
      return False

    cmd = io.BytesIO()
    cmd.write(b'0011command=fetch0014agent=git/2.37.20016object-format=sha10001000dofs-delta')
    if quiet: cmd.write(b'000fno-progress')
    if shallow: cmd.write(b'000cdeepen 1')
    if False: cmd.write(b'0014filter blob:none') # blobless clone
    cmd.write(f'0032want {commit.decode()}\n'.encode())
    for k in db.keys():
      if k==b'HEAD': continue
      have = f'0032have {binascii.hexlify(k).decode()}\n'
      print(repr(have))
      cmd.write(have.encode())
    cmd.write(b'0009done\n0000')
    s,x = _post(repo, cmd.getvalue())
    _read_headers(x)
    db[b'HEAD'] = commit
    db.flush()
    for fn in _read_pkt_lines(x, git_dir)[1]:
      _parse_pkt_file(git_dir, fn, db)
  s.close()
  return True



