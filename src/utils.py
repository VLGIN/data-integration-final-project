import re


def process_name(tex):
   tex = str(tex)
   punctuations = "\+/-.,{}|();:\"'` []"
   with open("data/brand_name") as f:
      brand_name = f.read().splitlines()
   with open("data/color") as f:
      colors = f.read().splitlines()
   tex = re.sub("\n", "", tex).lower()
   for item in brand_name:
      tex = re.sub(item, "", tex)

   # remove detail
   tex = re.sub("Chính Hãng (VN/A)", "", tex)
   tex = re.sub("Chính Hãng", "", tex)
   tex = re.sub("[0-9]+ gb", "", tex)
   tex = re.sub("[0-9]+gb", "", tex)
   tex = re.sub("[0-9]+g", "", tex)
   tex = re.sub("[0-9]+ g", "", tex)
   tex = re.sub("[0-9]+tb", "", tex)
   tex = re.sub("[0-9]+ tb", "", tex)
   tex = re.sub("điện thoại", "", tex)
   tex = re.sub("[\+\\\.{}\-()/]", "", tex)
   for item in colors:
      tex = re.sub(item, "", tex)
   tex = re.sub(" +", " ", tex)

   return tex

def process_text(tex):
   return tex
