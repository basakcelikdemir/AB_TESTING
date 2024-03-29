######################################################
# AB Testing & Dynamic Pricing
######################################################

# Temel İstatistik Kavramları
# - Sampling (Örnekleme)
# - Descriptive Statistics (Betimsel İstatistikler)
# - Confidence Intervals (Güven Aralıkları)
# - Hypothesis Testing (Hipotez Testleri)
# - Correlation (Korelasyon)

# AB Testing
# - İki Grup Ortalamasını Karşılaştırma (Bağımsız İki Örneklem T Testi)
#       - Parametrik Karşılaştırma
#       - Nonparametrik Karşılaştırma
# - İki Grup Oran Karşılaştırma (İki Örneklem Oran Testi)
# - İkiden Fazla Grup Ortalaması Karşılaştırma (ANOVA)


# Projeler
# AB Testing for Facebook Bidding Strategies
# Dynamic Pricing for Item Price



######################################################
# Temel İstatistik Kavramları
######################################################
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, \
    f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

############################
# Sampling (Örnekleme)
############################

populasyon = np.random.randint(0, 80, 1000000)
populasyon[0:10]
populasyon.mean()

np.random.seed(115)
orneklem = np.random.choice(a=populasyon, size=100)
orneklem.mean()

np.random.seed(10)
orneklem1 = np.random.choice(a=populasyon, size=100)
orneklem2 = np.random.choice(a=populasyon, size=100)
orneklem3 = np.random.choice(a=populasyon, size=100)
orneklem4 = np.random.choice(a=populasyon, size=100)
orneklem5 = np.random.choice(a=populasyon, size=100)
orneklem6 = np.random.choice(a=populasyon, size=100)
orneklem7 = np.random.choice(a=populasyon, size=100)
orneklem8 = np.random.choice(a=populasyon, size=100)
orneklem9 = np.random.choice(a=populasyon, size=100)
orneklem10 = np.random.choice(a=populasyon, size=100)



(orneklem1.mean() + orneklem2.mean() + orneklem3.mean() + orneklem4.mean() + orneklem5.mean()
 + orneklem6.mean() + orneklem7.mean() + orneklem8.mean() + orneklem9.mean() + orneklem10.mean()) / 10



############################
# Descriptive Statistics (Betimsel İstatistikler)
############################

df = sns.load_dataset("tips")
df.describe().T



############################
# Confidence Intervals (Güven Aralıkları)
############################


# Tips Veri Setindeki Sayısal Değişkenler için Güven Aralığı Hesabı
df = sns.load_dataset("tips")
df.describe().T


sms.DescrStatsW(df["total_bill"]).tconfint_mean()

sms.DescrStatsW(df["tip"]).tconfint_mean()

# Titanic Veri Setindeki Sayısal Değişkenler için Güven Aralığı Hesabı
df = sns.load_dataset("titanic")
sms.DescrStatsW(df["age"].dropna()).tconfint_mean()
sms.DescrStatsW(df["fare"].dropna()).tconfint_mean()


# Retail Veri Setindeki Sayısal Değişkenler için Güven Aralığı Hesabı
df_ = pd.read_excel("datasets/online_retail_II.xlsx",
                    sheet_name="Year 2010-2011")
df = df_.copy()

sms.DescrStatsW(df["Quantity"].dropna()).tconfint_mean()
sms.DescrStatsW(df["Price"].dropna()).tconfint_mean()


############################
# Hypothesis Testing (Hipotez Testi)
############################

# Tek Örneklem T Testi

# H0: Web sitemizde geçirilen ortalama süre 170 saniyedir.
# H1: ..değildir


session_duration = pd.DataFrame(np.random.normal(175, 10, 1000),
                                columns=["session_duration"])
session_duration.describe().T


ttest_1samp(session_duration, popmean=170)

p_value = ttest_1samp(session_duration, popmean=170)[1][0]

print(f"{p_value:.5f}")

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################


# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı
#   - 2. Varyans Homojenliği
# 3. Hipotezin Uygulanması
#   - p-value < 0.05 ise HO red.
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
# Not:
# - Normallik sağlanmıyorsa direk 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.



############################
# Uygulama 1: Sigara İçenler ile İçmeyenlerin Hesap Ortalamaları Arasında İst Ol An Fark var mı?
############################

############################
# 1. Hipotezi Kur
############################


# H0: M1 = M2
# H1: M1!= M2

df = sns.load_dataset("tips")
df.groupby("smoker").agg({"total_bill": "mean"})

############################
# 2. Varsayım Kontrolü
############################

# Normallik Varsayımı
# Varyans Homojenliği

############################
# Normallik Varsayımı
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(df.loc[df["smoker"] == "Yes", "total_bill"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df.loc[df["smoker"] == "No", "total_bill"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.


############################
# Varyans Homojenligi Varsayımı
############################


# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir


test_stat, pvalue = levene(df.loc[df["smoker"] == "Yes", "total_bill"],
                           df.loc[df["smoker"] == "No", "total_bill"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.


############################
# 3. Hipotezin Uygulanması
############################


# 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
# 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)

# Eğer normallik sağlanmazsa her türlü nonparametrik test yapacağız.
# Eger normallik sağlanır varyans homojenliği sağlanmazsa ne olacak?
# T test fonksiyonuna arguman gireceğiz.

# H0: M1 = M2 (... iki grup ortalamaları arasında ist ol.anl.fark yoktur.)
# H1: M1 != M2 (...vardır)


############################
# 1.1 Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
############################
test_stat, pvalue = ttest_ind(df.loc[df["smoker"] == "Yes", "total_bill"],
                              df.loc[df["smoker"] == "No", "total_bill"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.


############################
# 1.2 Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
############################

test_stat, pvalue = mannwhitneyu(df.loc[df["smoker"] == "Yes", "total_bill"],
                                 df.loc[df["smoker"] == "No", "total_bill"])


print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))



############################
# Uygulama 2: Titanic Kadın ve Erkek Yolcuların Yaş Ortalamaları Arasında İstatistiksel Olarak Anl. Fark. var mıdır?
############################

df = sns.load_dataset("titanic")
df.groupby("sex").agg({"age": "mean"})



############################
# 1. Hipotezi Kur
############################


# H0: M1 = M2
# H1: M1!= M2


############################
# 2. Varsayım Kontrolü
############################

# Normallik Varsayımı
# Varyans Homojenliği


# Normallik varsayımı
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(df.loc[df["sex"] == "female", "age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# sağlanmıyor

test_stat, pvalue = shapiro(df.loc[df["sex"] == "male", "age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# sağlanmıyor

# Varyans homojenliği
# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir
test_stat, pvalue = levene(df.loc[df["sex"] == "female", "age"].dropna(),
                           df.loc[df["sex"] == "male", "age"].dropna())


print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))



############################
# 3. Hipotezin Uygulanması
############################


# Varsayımlar sağlanmadığı için nonparametrik

# H0: M1 = M2 (... iki grup ortalamaları arasında ist ol.anl.fark yoktur.)
# H1: M1 != M2 (...vardır)
# mannwhitneyu
test_stat, pvalue = mannwhitneyu(df.loc[df["sex"] == "female", "age"].dropna(),
                                 df.loc[df["sex"] == "male", "age"].dropna())

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


############################
# Uygulama 3: Diyabet Hastası Olan ve Olmayanların Yaşları Arasında İst. Ol. Anl. Fark var mıdır?
############################

df = pd.read_csv("datasets/diabetes.csv")
df.groupby("Outcome").agg({"Age": "mean"})

# Normallik Varsayımı (H0: Normal dağılım varsayımı sağlanmaktadır.)
test_stat, pvalue = shapiro(df.loc[df["Outcome"] == 1, "Age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df.loc[df["Outcome"] == 0, "Age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Varyans Homojenliği Varsayımı (H0: Varyanslar homojendir)
test_stat, pvalue = levene(df.loc[df["Outcome"] == 1, "Age"].dropna(),
                           df.loc[df["Outcome"] == 0, "Age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# Normallik varsayımı sağlanmadığı için nonparametrik.

# Hipotez (H0: M1 = M2)
test_stat, pvalue = mannwhitneyu(df.loc[df["Outcome"] == 1, "Age"].dropna(),
                                 df.loc[df["Outcome"] == 0, "Age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))



###################################################
# İş Problemi: Udemy'de Sorulan Sorulara Yanıt Verilmeli mi?
###################################################

# H0: "Soru sorup yanıt alamayan kişilerle soru sorup yanıt alan kişilerin verdiği
# puan ortalamaları arasında istatistiki olarak anlamlı bir yoktur"

# H1: Vardır.



df = pd.read_csv("datasets/course_reviews.csv")
df.head()


# Yanıt alamayanlar:
df[(df["Questions Asked"] > 0) & (df["Questions Answered"] < 1)]["Rating"].mean()

# Yanıt alanlar:
df[(df["Questions Asked"] > 0) & (df["Questions Answered"] >= 1)]["Rating"].mean()


# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.
# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.


# Yanıt alamayanlar:
test_stat, pvalue = shapiro(df[(df["Questions Asked"] > 0) & (df["Questions Answered"] < 1)]["Rating"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Yanıt alanlar:
test_stat, pvalue = shapiro(df[(df["Questions Asked"] > 0) & (df["Questions Answered"] >= 1)]["Rating"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# H0: M1 = M2 (... iki grup ortalamaları arasında ist ol.anl.fark yoktur.)
# H1: M1 != M2 (...vardır)

test_stat, pvalue = mannwhitneyu(
    df[(df["Questions Asked"] > 0) & (df["Questions Answered"] < 1)]["Rating"],
    df[(df["Questions Asked"] > 0) & (df["Questions Answered"] >= 1)]["Rating"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))



###################################################
# İş Problemi: Kursun Büyük Çoğunluğunu İzleyenler ile İzlemeyenlerin Puanları Birbirinden Farklı mı?
###################################################

# kursun büyük çoğunluğunu izleyenler
df[(df["Progress"] > 75)]["Rating"].mean()


# kursun büyük çoğunluğunu izlemeyenler
df[(df["Progress"] < 40)]["Rating"].mean()


# H0: M1 = M2 (... iki grup ortalamaları arasında ist ol.anl.fark yoktur.)
# H1: M1 != M2 (...vardır)

test_stat, pvalue = mannwhitneyu(df[(df["Progress"] > 75)]["Rating"],
                                 df[(df["Progress"] < 40)]["Rating"])



print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


###################################################
# İş Problemi: Yine de bazı soruları yanıtlayacak olsak hangi kişilerin sorularını yanıtlamalıyız?
###################################################

# H0: İlerlemesi düşük olup sorularına yanıt alamayanlar ile ilerlemesi yüksek olup sorusuna yanıt alamayanlar
# arasında istatistiksel olarak anlamlı bir puan var farkı var mı?


df[(df["Questions Asked"] > 0) & (df["Questions Answered"] < 1) & (df["Progress"] < 25)]["Rating"].mean()
df[(df["Questions Asked"] > 0) & (df["Questions Answered"] < 1) & (df["Progress"] > 75)]["Rating"].mean()


test_stat, pvalue = mannwhitneyu(
    df[(df["Questions Asked"] > 0) & (df["Questions Answered"] < 1) & (df["Progress"] < 25)]["Rating"],
    df[(df["Questions Asked"] > 0) & (df["Questions Answered"] < 1) & (df["Progress"] > 75)]["Rating"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


######################################################
# AB Testing (İki Örneklem Oran Testi)
######################################################

# H0: İki oran arasında ist ol an fark yoktur
# H1: vardır.


basari_sayisi = np.array([300, 250])
gozlem_sayilari = np.array([1000, 1100])
proportions_ztest(count=basari_sayisi, nobs=gozlem_sayilari)


############################
# Uygulama: Kadın ve Erkeklerin Hayatta Kalma Oranları Arasında İst. Olarak An. Farklılık var mıdır?
############################

df = sns.load_dataset("titanic")

# Hayatta kalma oranları:
df.loc[df["sex"] == "female", "survived"].mean()
df.loc[df["sex"] == "male", "survived"].mean()


female_succ_count = df.loc[df["sex"] == "female", "survived"].sum()
male_succ_count = df.loc[df["sex"] == "male", "survived"].sum()


test_stat, pvalue = proportions_ztest(count=[female_succ_count, male_succ_count],
                                      nobs=[df.loc[df["sex"] == "female", "survived"].count(),
                                            df.loc[df["sex"] == "male", "survived"].count()])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))







######################################################
# ANOVA (Analysis of Variance)
######################################################

# İkiden fazla grup ortalamasını karşılaştırmak için kullanılır.

###########################
# Varsayım Kontrolü
###########################

# Tüm grupların normallik varsayımını sağlaması gerekmektedir.

# Varsayım sağlanıyorsa one way anova
# Varsayım sağlanmıyorsa kruskal


# H0: Dağılım Normaldir.

df = sns.load_dataset("tips")


for group in list(df["day"].unique()):
    pvalue = shapiro(df.loc[df["day"] == group, "total_bill"])[1]
    print(group, 'p-value: %.4f' % pvalue)


###########################
# Hipotez Testi
###########################

# Hiçbiri sağlamıyor.
df.groupby("day").agg({"total_bill": ["mean", "median"]})


# HO: Grup ortalamaları arasında ist ol anl fark yoktur:

# Nonparametrik anova testi:
kruskal(df.loc[df["day"] == "Thur", "total_bill"],
        df.loc[df["day"] == "Fri", "total_bill"],
        df.loc[df["day"] == "Sat", "total_bill"],
        df.loc[df["day"] == "Sun", "total_bill"])


# parametrik anova testi:
f_oneway(df.loc[df["day"] == "Thur", "total_bill"],
         df.loc[df["day"] == "Fri", "total_bill"],
         df.loc[df["day"] == "Sat", "total_bill"],
         df.loc[df["day"] == "Sun", "total_bill"])



# BITTI.
from statsmodels.stats.multicomp import MultiComparison
comparison = MultiComparison(df['total_bill'], df['day'])
tukey = comparison.tukeyhsd(0.05)
print(tukey.summary())



# R tarzı çıktı ve t test ikili karşılaştırması için
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Ordinary Least Squares (OLS) model
model = ols('total_bill ~ day', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

pair_t = model.t_test_pairwise('day')
pair_t.result_frame


















