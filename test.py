from pathlib import Path

BASE_DIR= Path(__file__).parent

print(BASE_DIR)

indir = BASE_DIR / 'testdir'
out = BASE_DIR / 'newdir'
print ("in",indir , "out", out)

indir.replace(out)
