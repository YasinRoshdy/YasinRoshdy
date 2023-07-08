import os

cfd = os.path.dirname(os.path.abspath(__file__))
# base_dir = os.path.join(cfd, 'quran my export')


print(os.listdir(cfd))
len = 0
for item in os.listdir(cfd):
    len = len + 1
    if item == "quran_blue.pdf" or item == "script.py":
        continue

    print(item)

    # name = item.split("/")[-1]

    if True:

        # old = os.path.join(cfd, item)
        new = item.replace("_--", "") .replace(".png", "")

        # print(new.split('/')[-1])
        val = int(new)

        new = os.path.join(cfd, f"{val}.png")

        print(new)

        os.rename(os.path.join(cfd, item), os.path.join(cfd, new))


print(len)

print(int("001"))
