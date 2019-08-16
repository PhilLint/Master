import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import datetime as dt
import math
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, confusion_matrix
import seaborn as sns
from sklearn import tree
import graphviz
from sklearn.naive_bayes import GaussianNB

data = pd.read_csv('ODI-2019-csv.csv', sep=";")

#############################################################################
# CLEAN UP
data.columns = ["time",
                "programme",
                "exp_ML",
                "exp_IR",
                "exp_stat",
                "exp_DB",
                "gender",
                "chocolate",
                "birthday",
                "num_neighbours",
                "stand_up",
                "DM_competition",
                "random_num",
                "bedtime",
                "good_day_1",
                "good_day_2",
                "stress_level"]
# COMMA SEP
data = data.stack().str.replace(',','.').unstack()

#DATETIME
data.time = pd.to_datetime(data.time)

#PROGRAMME
data.exp_ML = data.exp_ML.map({"yes": 1, "no": 0})
data.exp_ML = pd.Categorical(data.exp_ML)
data.exp_IR = data.exp_IR.map({"1": 1, "0": 0})
data.exp_stat = data.exp_stat.map({"mu": 1, "sigma": 0})
data.exp_DB = data.exp_DB.map({"ja": 1, "nee": 0})
data.exp_DB = pd.Categorical(data.exp_DB)
data.exp_IR = pd.Categorical(data.exp_IR)
data.exp_stat = pd.Categorical(data.exp_stat)
data.exp_IR.fillna(data.exp_IR.mode(),inplace=True)

data.programme[data.programme.str.contains("AI|Artificial|Intelligence|artificial|intelligence|ai")] = "AI"
data.programme[data.programme.str.contains("CS|Computer Science|cs|Computer science|computer science")] = "CS"
data.programme[data.programme.str.contains("CLS|cls|CLs|Cls|Computational Science")] = "CLS"
data.programme[data.programme.str.contains("Bioinformatics|bioinformatics")] = "Bioinformatics"
data.programme[data.programme.str.contains("business analytics|Business Analytics|Business analystics|BA")] = "BA"
data.programme[data.programme.str.contains("Finance")] = "Finance"
data.programme[data.programme.str.contains("Econometrics|econometrics")] = "Econometrics"
data.programme[data.programme.str.contains("Data Science|Data science|data science")] = "DS"
data.programme = pd.Categorical(data.programme)

#data.programme.value_counts()[(data.programme.value_counts()) != 0].plot(kind="bar")
print(data.programme.value_counts())

# SUBSET PROGRAMME
data["programme_subset"] = np.nan
for idx, row in data.iterrows():
    data.programme_subset[idx] = row.programme if row.programme == "AI" \
                                                  or row.programme == "CS" else np.nan
data.programme_subset = pd.Categorical(data.programme_subset)

prog_mask = data.programme_subset.notna()
#CHOCOLATE
data.chocolate = pd.Categorical(data.chocolate)

# STRESS LEVEL
pattern_stress = "([0-9]{0,3})"
data.stress_level = data.stress_level.str.extract(pattern_stress, expand=False)
data.stress_level = pd.to_numeric(data.stress_level)

data.stress_level.loc[(data.stress_level > 100)] = 100
print("stress notna", sum(data.stress_level.notna()))
data.stress_level.fillna(data.stress_level.mean(),inplace=True)

labels = ["low", "med", "high"]
data["stress_cat"] = pd.cut(data.stress_level, [0, 33, 66, 101], right=False, labels=labels)

data.stress_cat.value_counts().plot(kind="bar")
plt.savefig("stress_barplot.png")

# RANDOM NUMBER
data.random_num = pd.to_numeric(data.random_num, errors="coerce")

# BED TIME
# problem with different formats (hh:mm and h:mm), at the moment only include hh:mm
#pattern_bed = "((2[0-3]|[01][0-9]):([0,3]?0))$"
pattern_bed = "((0[0-9]|1[0-9]|2[0-3]|[0-9]):[0-5][0-9])$"
#pattern_bed = "(/^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/)"

data.bedtime = data.bedtime.str.extract(pattern_bed)
print("sum na bedtime" , sum(data.bedtime.notna()))

data.bedtime = pd.Categorical(data.bedtime, categories=[u"21:00", u"21:30", u"22:00", u"22:30", u"23:00", u"23:30", u"00:00",
                                                        u"00:30", u"01:00", u"01:30", u"02:00", u"02:30", u"03:00", u"03:30",
                                                        u"12:30", u"18:00"], ordered=True)


data["bedtime_cat"] = np.nan
data["bedtime_cat"][data.bedtime < u"00:00"] = "before_mid"
data["bedtime_cat"][data.bedtime >= u"00:00"] = "after_midnight"
data.bedtime_cat = data.bedtime_cat.astype("category")

print(data.bedtime_cat)
# GENDER
data.gender = data.gender.astype("category")


# BIRTHDAY
# patter accepts either format dd-mm-yyyy or dd/mm/yyyy
pattern_birthday = "((0[1-9]|[12]\d|3[01])[-/.](0[1-9]|1[0-2])[-/.][12]\d{3})|$"
data.birthday = data.birthday.str.extract(pattern_birthday)
data.birthday = pd.to_datetime(data.birthday, dayfirst=True, errors="coerce")
birthday_mask = data.birthday.notna()

# AGE
data["age"] = 0
now = dt.datetime.now()
for idx,entry in enumerate(data.birthday):
    if isinstance(entry, dt.datetime):
        data.age[idx] = round((now - entry).days / 365.25)


# NUMBER OF NEIGHBOURS
data.num_neighbours = pd.to_numeric(data.num_neighbours, errors="coerce")


# STANDUP
data.stand_up = pd.Categorical(data.stand_up)

# MONEY DESERVED
data.DM_competition = pd.to_numeric(data.DM_competition, errors="coerce")

####################################################################################################
# PLOTS

#SCATTERPLOT STRESS/RANDOM
#plt.scatter(data.stress_level, data.random_num)
#plt.xlim(0, 100)
#plt.ylim(0, 100)



#HIST STRESS
"""
plt.subplot(1,2,1)
data["stress_level_sqrt"] = 0
for idx, row in data.iterrows():
    data.stress_level_sqrt[idx] = math.sqrt(row.stress_level) if row.stress_level > 0 else 0
sns.distplot(data.stress_level_sqrt, hist=True)
plt.xlabel("sqrt(stress_level)")
plt.yticks([])
"""


# AGE STRESS LEVEL PLOT
"""
plt.subplot(2,1,1)
sns.distplot(data.age.dropna(), hist=True)
plt.xlabel("Age)")


plt.subplot(2,1,2)
sns.distplot(data.stress_level, hist=True)
plt.xlabel("stress_level")

plt.gcf().set_size_inches(3,6)

plt.savefig("hists_age_stress.png")
"""

"""
#BARPLOT GENDER
data.gender.value_counts().plot(kind="bar")
plt.show()
"""

"""
#HIST STRESS BY GENDER
data.hist("stress_level", by="gender", range=(0,100))
"""
"""
#BARPLOT BEDTIME
plt.subplot(1,2,1)
data.bedtime.value_counts(sort=False).plot.bar()
plt.gcf().autofmt_xdate()
plt.xlabel("Bedtime")

#################################################################   BARPLOT BEDTIME & STRESS
plt.subplot(1,2,2)
sns.boxplot(data.bedtime, data.stress_level)
plt.gcf().autofmt_xdate()
plt.xlabel("Bedtime")
plt.ylabel("Stress level")
plt.gcf().set_size_inches(8,4)
plt.savefig("bedtime.png")
"""

"""
#HIST AGE
print(data.age)
data.age.dropna(inplace=True)
sns.distplot(data.age)
plt.xlabel("Age")
plt.savefig("age_hist.png")
"""
"""
plt.subplot(2,2,1)
sns.countplot(x="exp_ML", hue="programme_subset", data=data)
plt.xlabel("Prior ML course")

plt.subplot(2,2,2)
sns.countplot(x="exp_IR", hue="programme_subset", data=data)
plt.xlabel("Prior IR course")

plt.subplot(2,2,3)
sns.countplot(x="exp_DB", hue="programme_subset", data=data)
plt.xlabel("Prior DB course")

plt.subplot(2,2,4)
sns.countplot(x="exp_stat", hue="programme_subset", data=data)
plt.xlabel("Prior stat course")

plt.savefig("prior_count.png")
"""

############################################################################################
# DESCRIPTIVE STATS
#print(data.describe().round())

print(data.programme.value_counts())
print(data.exp_ML.value_counts())
print(data.exp_DB.value_counts())
print(data.exp_IR.value_counts())
print(data.exp_stat.value_counts())
print(data.stress_cat.value_counts())
print(data.bedtime_cat.value_counts())
print("age mean", data.age.mean())
print("age sd ", data.age.std())
print(data.stress_level.mean())
print(data.stress_level.std())



cordummies = pd.get_dummies(data[["programme_subset", "exp_ML", "exp_IR", "exp_stat", "exp_DB", "stress_cat", "bedtime_cat"]])
cordf = data[["age", "stress_level"]].join(cordummies)
cordf = cordf.loc[prog_mask,]
print(cordf.corr().to_string())

###########################################################################################
# CLASSIFICATION/REGRESSION
##################################################################### TREE

x_tree = pd.get_dummies(data[["exp_ML", "exp_stat", "exp_IR", "exp_DB"]])
x_tree = x_tree.loc[prog_mask,]

y_tree = data.programme_subset.loc[prog_mask,]
y_tree = y_tree.values.ravel()
x_train_tree, x_test_tree, y_train_tree, y_test_tree = train_test_split(x_tree, y_tree, test_size=0.5)


tree1 = tree.DecisionTreeClassifier(max_depth=3)

scores_tree = cross_val_score(tree1, x_tree, y_tree, scoring='accuracy', cv=3)

print('tree scores per fold tree ', scores_tree)
print(' tree mean score tree    ', np.mean(scores_tree))
print(' tree standard dev. tree ', np.std(scores_tree))

tree1 = tree1.fit(x_train_tree, y_train_tree)
y_pred_tree = tree1.predict(x_test_tree)
print("accuracy tree: ", accuracy_score(y_test_tree, y_pred_tree))

print(confusion_matrix(y_test_tree, y_pred_tree))
tn, fp, fn, tp = confusion_matrix(y_test_tree, y_pred_tree).ravel()
no_inf_rate = (float(tp)+float(tn))/(float(tn) + float(tp) + float(fn) + float(fp))
print("no information rate", no_inf_rate)

dot_data = tree.export_graphviz(tree1, out_file=None, feature_names=x_tree.columns.values.tolist(), class_names=["AI","CS" ])
graph = graphviz.Source(dot_data)
graph.render("tree")
#####################################################################################
gnb = GaussianNB()


# Train for 5 folds, returing ROC AUC. You can also try 'accuracy' as a scorer
scores = cross_val_score(gnb, x_tree, y_tree, scoring='accuracy', cv=3)

print('gnb scores per fold ', scores)
print(' gnb mean score    ', np.mean(scores))
print('gnb  standard dev. ', np.std(scores))

gnb = gnb.fit(x_train_tree, y_train_tree)
y_pred = gnb.predict(x_test_tree)

print("gnb acc: ", accuracy_score(y_test_tree, y_pred))
print("gnbVM confusion: ", confusion_matrix(y_test_tree, y_pred))

tn, fp, fn, tp = confusion_matrix(y_test_tree, y_pred_tree).ravel()
no_inf_rate = (float(tp)+float(tn))/(float(tn) + float(tp) + float(fn) + float(fp))
print("no information rate", no_inf_rate)

