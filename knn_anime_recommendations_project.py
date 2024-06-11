# -*- coding: utf-8 -*-
"""KNN_Anime_Recommendations_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1heRwzRg555K2vEGhfuo_4SETpmlTgqVk
"""

# Gerekli kütüphaneleri yükleyin
!pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

#Gerekli kütüphaneleri import ederek başlıyoruz
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

#Drive'mi bağladığım kısım.
from google.colab import drive
drive.mount('/content/drive')

# Veri setini okuyun ve boş değerleri atın
veri_seti = pd.read_csv("/content/drive/My Drive/anime.csv")
veri_seti = veri_seti.dropna()

# Sütunların adlarını ayarlayın
veri_seti.columns = ["anime_id", "name", "genre", "type", "episodes", "rating", "members"]
# Türleri sınıflandırın
veri_seti = pd.get_dummies(veri_seti, columns=["genre"])

# "type" değişkenini sayısal değerlerle değiştirin
veri_seti["type"] = veri_seti["type"].map({"TV": 1, "Movie": 2, "OVA": 3, "Special": 4, "ONA": 5})
veri_seti["type"] = veri_seti["type"].fillna(2)  # Diğer değerleri 2 olarak kodlayın

# KNN sınıfını yükledik
nn = NearestNeighbors(n_neighbors=5, algorithm="kd_tree")

# Modeli eğittik
nn.fit(veri_seti[["rating", "type"]], veri_seti["name"])

#'members' sütununa göre sıralı 'name' ve 'members' sütunlarını içeren bir DataFrame oluşturun ve en üst 10 animeyi seçin
top10_animemembers=veri_seti[['name', 'rating']].sort_values(by = 'rating',ascending = False).head(5)

#'members' sütununa göre sıralı 'name' ve 'members' sütunlarını içeren bir DataFrame oluşturun ve en üst 10 animeyi seçin
top10_animemembers=veri_seti[['name', 'rating']].sort_values(by = 'rating',ascending = False).head(5)
#Seaborn kullanarak bir barplot oluşturun
ax=sns.barplot(x="name", y="rating", data=top10_animemembers, palette="gnuplot2")
#X eksenindeki etiketlerin font boyutunu, yöne ve etiketlerin yazımını ayarlayın
ax.set_xticklabels(ax.get_xticklabels(), fontsize=11, rotation=40, ha="right")
#Başlığı ve eksen etiketlerini ayarlayın
ax.set_title('Ratinge göre en iyi 5 anime',fontsize = 22)
ax.set_xlabel('Anime',fontsize = 20) 
ax.set_ylabel('My anime list puanı', fontsize = 20)

#Yabancı karakterleri düzenledik.
#'name' sütunundaki HTML kodlarını temizleme işlevini tanımlayın
#veri_seti = pd.read_csv("/content/drive/My Drive/anime.csv")
#veri_seti = veri_seti.dropna()
#import re
#def text_cleaning(text):
#    text = re.sub(r'&quot;', '', text)# " kodunu kaldırın
#    text = re.sub(r'.hack//', '', text)# .hack// kodunu kaldırın
#    text = re.sub(r'&#039;', '', text)# ' kodunu kaldırın
#    text = re.sub(r'A&#039;s', '', text)# A's kodunu kaldırın
#    text = re.sub(r'I&#039;', 'I\'', text)# I' kodunu kaldırın
#    text = re.sub(r'&amp;', 'and', text)# & kodunu kaldırın
#    text = re.sub(r'°', ' ', text)# & kodunu kaldırın
    
    # Temizlenmiş metni döndürün
#    return text

#'name' sütununu text_cleaning işlevine göre temizleyin
#veri_seti['name'] = veri_seti['name'].apply(text_cleaning)
#veri_seti.head(10)

#'episodes' sütununda "Unknown" olarak işaretlenmiş satırları seçin
veri_seti[veri_seti['episodes']=='Unknown'].head(5)

while True:
    try:
        # Kullanıcıdan örnek anime ismini alın
        anime_name = input("Lütfen benzerini istediğiniz anime ismini girin(Lütfen tam adı giriniz büyük küçük harfe duyarlıdır.): ")
        if anime_name == "0":
            break

        # Seçilen animeyi bulun
        anime = veri_seti[veri_seti["name"] == anime_name]
        if anime.empty:
            print("Girdiğiniz anime ismi veri setimizde bulunamadı. Lütfen geçerli bir anime ismi girin.")
        else:
            # Benzer animeleri bulun
            _, indices = nn.kneighbors(anime[["rating", "type"]].values.reshape(1, -1))

            # Benzer animeleri gösterin
            print("Örnek anime:", anime["name"])
            print("Benzer animeler:")
            for i in indices[0]:
                print("-", veri_seti.iloc[i]["name"])

            # Benzer animelerin grafiğini çizin
            fig, ax = plt.subplots()
            ax.barh(veri_seti.iloc[indices[0]]["name"], veri_seti.iloc[indices[0]]["rating"])
            ax.set_xlabel("Rating")
            ax.set_ylabel("Anime")
            ax.set_xlim(0, 10)  # Rating değerlerinin 0 ile 10 arasında gösterilmesini sağlar
            ax.set_ylim(-1, 6)  # Benzer animelerin sırasını -1 ile 6 arasında gösterir
            ax.set_xlabel("Oylamalar")  # X ekseninin etiketini "Oylamalar" olarak değiştirir
            ax.set_ylabel("Anime İsimleri")  # Y ekseninin etiketini "Anime İsimleri" olarak değiştirir
            
            plt.show()
    except KeyboardInterrupt:
        print("Program kullanıcı tarafından durduruldu.")
        break