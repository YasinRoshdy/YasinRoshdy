# # def ArrayChallenge(strArr):
# #     text = strArr[0]
# #     words = strArr[1].split(",")
# #     res = []
# #     start_post = 0

# #     # for el in words:
# #     #   print(text[start_post:-1])
# #     #   print(f'{text[start_post:]}-{el}',text[start_post:].startswith(el))
# #     #   if(text[start_post:].startswith(el)):
# #     #     res.append(el)
# #     #     start_post=len(text[start_post:])+len(el)

# #     # for el in words:
# #     #     # for char in text:

# #     #     #   if(text[start_post:].startswith(el)):
# #     #     rem = strArr
# #     #     res = []
# #     #     while rem.startswith(el):
# #     #         if len(rem) == 0:
# #     #             return ",".join(res)
# #     #         rem = rem[len(el) :]
# #     res = []
# #     pos = range(len(words))
# #     el_res = []

# #     for i in range(len(text)):
# #         for el in words:
# #             if text[i:].startswith(el):
# #                 rem = text


# # # keep this function call here
# # print(ArrayChallenge(input()))

# # print("baseball"[4:])

# for i in range(0, len(["", ""]), 1):
#     print(i)
#     i -= 1


def prepare_str(val: str):
    if not val or not isinstance(val, str):
        return val

    else:
        # val = val.strip()

        return val.strip().replace("\n", " ").replace("\r", "")


data = """ بَاب مَسْجِدِ قُبَاءٍ
(1134)
حَدَّثَنَا يَعْقُوبُ بْنُ إِبْرَاهِيمَ هُوَ الدَّوْرَقِيُّ حَدَّثَنَا ابْنُ عُلَيَّةَ أَخْبَرَنَا أَيُّوبُ عَنْ نَافِعٍ أَنَّ ابْنَ عُمَرَ رَضِيَ اللَّهُ عَنْهُمَا كَانَ لَا يُصَلِّي مِنْ الضُّحَى إِلَّا فِي يَوْمَيْنِ يَوْمَ يَقْدَمُ بِمَكَّةَ فَإِنَّهُ كَانَ يَقْدَمُهَا ضُحًى فَيَطُوفُ بِالْبَيْتِ ثُمَّ يُصَلِّي رَكْعَتَيْنِ خَلْفَ الْمَقَامِ وَيَوْمَ يَأْتِي مَسْجِدَ قُبَاءٍ فَإِنَّهُ كَانَ يَأْتِيهِ كُلَّ سَبْتٍ فَإِذَا دَخَلَ الْمَسْجِدَ كَرِهَ أَنْ يَخْرُجَ مِنْهُ حَتَّى يُصَلِّيَ فِيهِ قَالَ وَكَانَ يُحَدِّثُ أَنَّ رَسُولَ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ كَانَ يَزُورُهُ رَاكِبًا وَمَاشِيًا قَالَ وَكَانَ يَقُولُ إِنَّمَا أَصْنَعُ كَمَا رَأَيْتُ أَصْحَابِي يَصْنَعُونَ وَلَا أَمْنَعُ أَحَدًا أَنْ يُصَلِّيَ فِي أَيِّ سَاعَةٍ شَاءَ مِنْ لَيْلٍ أَوْ نَهَارٍ غَيْرَ أَنْ لَا تَتَحَرَّوْا طُلُوعَ الشَّمْسِ وَلَا غُرُوبَهَا
"""

print(prepare_str(data))
