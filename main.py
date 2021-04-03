import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import sqlite3


all_files = glob.glob("names" + "/*.txt")
list = []

def task2_3(frame):
    frame_unique_names = frame.drop_duplicates(subset=['name'])
    print("Task 2:", "Unique names: ", len(frame_unique_names))

    unique_male_frame = frame_unique_names.loc[frame_unique_names["sex"] == "M", :]
    unique_female_names = len(frame_unique_names) - len(unique_male_frame)
    print("Task 3:", "Unique male names:", len(unique_male_frame), ", Unique female names:", unique_female_names)
def task4(frame):
    frame_year_pop = frame.groupby(by=["year","sex"]).sum()
    frame_year_pop.columns = ['year_pop']
    frame_year_pop = frame_year_pop.reset_index()

    frame = pd.merge(frame, frame_year_pop, on=["sex", "year"])
    frame['frequency_male'] = np.where(frame["sex"] == "M", frame['pop'] / frame["year_pop"], "NaN")
    frame['frequency_female'] = np.where(frame["sex"] == "F", frame['pop'] / frame["year_pop"], "NaN")
    frame = frame.drop('year_pop', axis=1)

    print("Task 4:", frame)
def task5(frame):
    frame_year_pop = frame.groupby(by=["year", "sex"]).sum()
    frame_year_pop = frame_year_pop.reset_index()


    male_frame = frame_year_pop[frame_year_pop['sex'] == "M"]
    female_frame = frame_year_pop[frame_year_pop['sex'] == "F"]

    male_frame = male_frame.reset_index()
    female_frame = female_frame.reset_index()
    male_frame.rename(columns={'pop': 'male_pop'}, inplace=True)
    female_frame.rename(columns={'pop': 'female_pop'}, inplace=True)
    frame_year_pop = pd.merge(male_frame, female_frame, on=["year"])
    frame_year_pop['ratio'] = frame_year_pop['female_pop'] / frame_year_pop['male_pop']
    frame_year_pop['difference'] = abs(frame_year_pop['female_pop'] - frame_year_pop['male_pop'])

    max_diff = frame_year_pop.loc[frame_year_pop['difference'] == frame_year_pop.max()['difference']]
    min_diff = frame_year_pop.loc[frame_year_pop['difference'] == frame_year_pop.min()['difference']]

    frame_year_pop_sum = frame.groupby(by=["year"]).sum()
    frame_year_pop_sum = frame_year_pop_sum.reset_index()

    frame_year_pop_sum = frame_year_pop_sum.set_index('year')
    frame_year_pop = frame_year_pop.set_index('year')

    fig5, axs5 = plt.subplots(2, 1)
    fig5.canvas.set_window_title('Task 5')
    frame_year_pop_sum.plot(use_index=True, y='pop', ax=axs5[0], label='Births')
    frame_year_pop.plot(use_index=True, y='ratio', ax=axs5[1], label='Female to male birth ratio')
    axs5[0].title.set_text('Number of births per year in USA')
    axs5[1].title.set_text('Female to male birth ration in USA')

    print("Task 5:")
    print("max difference:",max_diff.iloc[0]['difference'], "in", max_diff.iloc[0]['year'])
    print("min difference:",min_diff.iloc[0]['difference'], "in", min_diff.iloc[0]['year'])
def task6_7(frame):

    male_frame = frame[frame['sex'] == "M"]
    female_frame = frame[frame['sex'] == "F"]

    male_frame_1000 = male_frame.groupby('year').apply(lambda x: x.nlargest(1000, 'pop')).reset_index(drop=True)
    female_frame_1000 = female_frame.groupby('year').apply(lambda x: x.nlargest(1000, 'pop')).reset_index(drop=True)


    male_hiscore = male_frame_1000.groupby(by=["name"]).sum().nlargest(1000, 'pop')
    female_hiscore = female_frame_1000.groupby(by=["name"]).sum().nlargest(1000, 'pop')

    print("Task 6:")
    print("top 1000 male names: ",male_hiscore)
    print("top 1000 female names: ",female_hiscore)

    top_male_name = male_hiscore.index[0]
    top_female_name = female_hiscore.index[0]

    sex_merged_frame = frame.groupby(by=["year","name"]).sum()
    sex_merged_frame = sex_merged_frame.reset_index()

    harry_frame = sex_merged_frame.loc[sex_merged_frame['name'] == "Harry"]
    marilin_frame = sex_merged_frame.loc[sex_merged_frame['name'] == "Marilin"]

    top_male = sex_merged_frame.loc[sex_merged_frame['name'] == top_male_name]
    top_female = sex_merged_frame.loc[sex_merged_frame['name'] == top_female_name]

    #Plotting
    fig7, axs7 = plt.subplots(2, 2)
    fig7.canvas.set_window_title('Task 7')
    male_names_by_year = male_frame.groupby(by=["year"]).sum()
    female_names_by_year = female_frame.groupby(by=["year"]).sum()


    harry_frame = harry_frame.set_index('year')
    harry_frame = pd.merge(harry_frame, male_names_by_year, on=["year"])
    harry_frame['popularity'] = harry_frame['pop_x'] / harry_frame['pop_y']
    harry_frame = harry_frame.rename(columns={'pop_x': 'pop'})
    harry_frame = harry_frame.drop(columns='pop_y')

    marilin_frame = marilin_frame.set_index('year')
    marilin_frame = pd.merge(marilin_frame, female_names_by_year, on=["year"])
    marilin_frame['popularity'] = marilin_frame['pop_x'] / marilin_frame['pop_y']
    marilin_frame = marilin_frame.rename(columns={'pop_x': 'pop'})
    marilin_frame = marilin_frame.drop(columns='pop_y')

    top_male = top_male.set_index('year')
    top_male = pd.merge(top_male, male_names_by_year, on=["year"])
    top_male['popularity'] = top_male['pop_x'] / top_male['pop_y']
    top_male = top_male.rename(columns={'pop_x': 'pop'})
    top_male = top_male.drop(columns='pop_y')

    top_female = top_female.set_index('year')
    top_female = pd.merge(top_female, male_names_by_year, on=["year"])
    top_female['popularity'] = top_female['pop_x'] / top_female['pop_y']
    top_female = top_female.rename(columns={'pop_x': 'pop'})
    top_female = top_female.drop(columns='pop_y')


    print(top_female)
    harry_frame.plot(use_index = True, y='pop', ax=axs7[0][0], label='Population')
    harry_frame.plot(use_index = True, y='popularity', ax=axs7[0][0], secondary_y = True, label='Popularity')
    axs7[0][0].title.set_text('Harry')
    marilin_frame.plot(use_index=True, y='pop', ax=axs7[1][0], label='Population')
    marilin_frame.plot(use_index=True, y='popularity', ax=axs7[1][0], secondary_y=True, label='Popularity')
    axs7[1][0].title.set_text('Marilin')
    top_male.plot(use_index=True, y='pop', ax=axs7[0][1], label='Population')
    top_male.plot(use_index=True, y='popularity', ax=axs7[0][1], secondary_y=True, label='Popularity')
    axs7[0][1].title.set_text(top_male_name)
    top_female.plot(use_index=True, y='pop', ax=axs7[1][1], label='Population')
    top_female.plot(use_index=True, y='popularity', ax=axs7[1][1], secondary_y=True, label='Popularity')
    axs7[1][1].title.set_text(top_female_name)

    #Print 1940, 1980 and 2019
    harry_years = harry_frame.loc[["1940", "1980", "2019"]]
    marilin_years = marilin_frame.loc[["1980", "2019"]]
    top_male_years = top_male.loc[["1940", "1980", "2019"]]
    top_female_years = top_female.loc[["1940", "1980", "2019"]]

    print("Task 7:")
    print(harry_years)
    print(marilin_years)
    print(top_male_years)
    print(top_female_years)

def task8(frame):

    male_frame = frame[frame['sex'] == "M"]
    female_frame = frame[frame['sex'] == "F"]

    male_top_frame = male_frame.groupby('year').apply(lambda x: x.nlargest(1000, 'pop')).reset_index(drop=True)
    female_top_frame = female_frame.groupby('year').apply(lambda x: x.nlargest(1000, 'pop')).reset_index(drop=True)

    male_hiscore = male_top_frame.groupby(by=["name"]).sum().nlargest(1000, 'pop')
    female_hiscore = female_top_frame.groupby(by=["name"]).sum().nlargest(1000, 'pop')

    male_top1k_frame = pd.merge(male_frame, male_hiscore, on=["name"])
    female_top1k_frame = pd.merge(female_frame, female_hiscore, on=["name"])


    male_sum = male_frame.groupby(by=["year"]).sum().reset_index(drop=False)
    female_sum = female_frame.groupby(by=["year"]).sum().reset_index(drop=False)
    male_top1k_sum_year = male_top1k_frame.groupby(by=["year"]).sum().drop(['pop_y'], axis=1).reset_index(drop=False)
    female_top1k_sum_year = female_top1k_frame.groupby(by=["year"]).sum().drop(['pop_y'], axis=1).reset_index(drop=False)


    male_merged_frame = pd.merge(male_sum, male_top1k_sum_year, on=["year"])
    female_merged_frame = pd.merge(female_sum, female_top1k_sum_year, on=["year"])
    male_merged_frame['ratio'] = male_merged_frame['pop_x'] / male_merged_frame['pop']
    female_merged_frame['ratio'] = female_merged_frame['pop_x'] / female_merged_frame['pop']

    merged_frame =  pd.merge(male_merged_frame, female_merged_frame, on=["year"])
    merged_frame['difference'] = abs(merged_frame['ratio_x'] - merged_frame['ratio_y'])



    difference_index = merged_frame['difference'].idxmax()
    year = merged_frame.loc[difference_index, ['year']].to_string(index=False)
    difference = merged_frame.loc[difference_index, ['difference']].to_string(index=False)

    print("Task 8:")
    print("Difference of: ", float(difference) * 100, "percentage points in", year)

    fig8, axs8 = plt.subplots(1, 1)
    fig8.canvas.set_window_title('Task 8')
    male_merged_frame.plot(x = 'year', y='ratio',ax=axs8)
    female_merged_frame.plot(x='year', y='ratio',ax=axs8)
    axs8.legend(["Top 1000 male population", "Top 1000 female population"], loc='upper left')
    axs8.title.set_text("Task 8 - Top 1000 names contribution per year")


def task9(frame):

    print("Task 9:")
    print("9.1:")

    frame['last_letter'] = frame['name'].str.slice_replace(stop=-1)
    frame = frame.groupby(by=["year", "sex", "last_letter"]).sum()
    print(frame)
    print("9.2:")

    frame_cut = frame.loc[["1910","1960","2015"],:]
    frame_cut = frame_cut.reset_index(drop=False)
    print(frame_cut)

    print("9.3:")
    # crosstab = pd.crosstab([frame['year'],frame['sex']], frame['last_letter'], values=frame['pop'], aggfunc=np.sum, normalize='index')
    crosstab = pd.crosstab(frame_cut['last_letter'], [frame_cut['year'], frame_cut['sex']], values=frame_cut['pop'], aggfunc=np.sum, normalize='columns')
    print(crosstab)

    print("9.4:")
    fig9, axs9 = plt.subplots(2, 1)
    fig9.canvas.set_window_title('Task 9')

    crosstab_copy = crosstab.drop('F', axis=1, level=1)

    crosstab_copy.plot.bar(ax=axs9[1])
    axs9[0].title.set_text("Popularity of male names' last character")
    axs9[0].legend(title='Popularity in different years')

    crosstab['male_change'] = abs(crosstab_copy.loc[:, ("1910", "M")] - crosstab_copy.loc[:, ("2015", "M")])
    crosstab_copy['male_change'] = abs(crosstab_copy.loc[:, ("1910", "M")] - crosstab_copy.loc[:, ("2015", "M")])
    max_male = crosstab_copy['male_change'].idxmax()
    print("Biggest change for a letter: ", max_male)

    print("9.5:")
    crosstab = crosstab.sort_values(by=['male_change'], ascending=False)

    indexes_M = crosstab.iloc[[0,1,2]].index
    frame_cut2 = frame.reset_index(drop=False)
    crosstab_full = pd.crosstab(frame_cut2['year'], [frame_cut2['sex'], frame_cut2['last_letter']], values=frame_cut2['pop'], aggfunc=np.sum, normalize='index')
    crosstab_full = crosstab_full.drop('F', axis=1, level=0)
    crosstab_full.columns = crosstab_full.columns.droplevel()
    crosstab_full = crosstab_full[indexes_M]


    crosstab_full.plot(ax=axs9[0])
    axs9[1].legend(title='Last letter popularity')
    axs9[1].title.set_text("Last character of male names")



def task10(frame):

    print("Task 10:")
    male_frame = frame[frame['sex'] == "M"]
    female_frame = frame[frame['sex'] == "F"]

    male_unique_names = male_frame.drop_duplicates(subset=['name'])
    female_unique_names = female_frame.drop_duplicates(subset=['name'])

    frame_list = [male_unique_names,female_unique_names]
    unique_frame = pd.concat(frame_list, ignore_index=True)

    unisex_names = unique_frame[unique_frame.duplicated(['name'])]['name'].reset_index(drop=True)

    print(unisex_names)

    male_frame = male_frame.set_index('name')
    female_frame = female_frame.set_index('name')

    male_frame = male_frame.groupby(male_frame.index)['pop'].sum().reset_index()
    male_frame = male_frame.sort_values(by=['pop'])
    male_frame = male_frame.set_index('name')
    female_frame = female_frame.groupby(female_frame.index)['pop'].sum().reset_index()
    female_frame = female_frame.sort_values(by=['pop'])
    female_frame = female_frame.set_index('name')

    merged = male_frame.merge(female_frame, left_index=True, right_index=True)
    print(merged)
    merged['unisex'] = merged.min(axis=1)
    merged = merged.sort_values(by=['unisex'], ascending=False)


    print("Najpopularniejsze imie uniseksualne:", merged.index[0])

def task11(frame):

    print("Task 11: ")

    before = frame.loc[(frame['year'] >= "1880") & (frame['year'] <= "1920")]
    after = frame.loc[(frame['year'] >= "2000") & (frame['year'] <= "2020")]

    before = before.groupby(['name','sex'])['pop'].sum().reset_index()
    after = after.groupby(['name','sex'])['pop'].sum().reset_index()

    F_before = before.loc[(before['sex'] == "F")].set_index('name')
    M_before = before.loc[(before['sex'] == "M")].set_index('name')
    before = pd.merge(M_before, F_before, how='outer', on='name')

    F_after = after.loc[(after['sex'] == "F")].set_index('name')
    M_after = after.loc[(after['sex'] == "M")].set_index('name')
    after = pd.merge(M_after, F_after, how='outer', on='name')


    before['before_MTFratio'] = before['pop_x'] / before['pop_y']
    after['after_MTFratio'] = after['pop_x'] / after['pop_y']

    merged = pd.merge(before, after, how='outer', on='name')
    merged['ratio_change'] = merged['before_MTFratio']/merged['after_MTFratio']

    merged['ratio_temporary'] = 1/merged['ratio_change']
    merged['ratio_change'] = merged[['ratio_change', 'ratio_temporary']].max(axis=1)
    merged = merged.drop(columns='ratio_temporary')

    merged = merged.sort_values(by=['ratio_change'],ascending=False)


    name1_frame = frame.loc[(frame['name'] == merged.index[0])]
    name2_frame = frame.loc[(frame['name'] == merged.index[1])]

    F_name1_frame = name1_frame.loc[(name1_frame['sex'] == "F")].set_index('year')
    M_name1_frame = name1_frame.loc[(name1_frame['sex'] == "M")].set_index('year')
    F_name2_frame = name2_frame.loc[(name2_frame['sex'] == "F")].set_index('year')
    M_name2_frame = name2_frame.loc[(name2_frame['sex'] == "M")].set_index('year')


    fig11, axs11 = plt.subplots(2, 1)
    fig11.canvas.set_window_title('Task 11')

    F_name1_frame.plot(use_index=True, y='pop', ax=axs11[0])
    M_name1_frame.plot(use_index=True, y='pop', ax=axs11[0])

    axs11[0].title.set_text(F_name1_frame['name'][0])
    axs11[0].legend(["Female population", "Male population"], loc='upper left')
    F_name2_frame.plot(use_index=True, y='pop', ax=axs11[1])
    M_name2_frame.plot(use_index=True, y='pop', ax=axs11[1])
    axs11[1].title.set_text(F_name2_frame['name'][0])
    axs11[1].legend(["Female population", "Male population"], loc='upper left')


def task12_13_14_15(frame):

    conn = sqlite3.connect("USA_ltper_1x1.sqlite")  # połączenie do bazy danych - pliku
    death_frame = pd.read_sql_query('SELECT USA_mltper_1x1.Age, USA_mltper_1x1.Year,USA_mltper_1x1.dx + '
                                  'USA_fltper_1x1.dx AS dx FROM USA_mltper_1x1 JOIN USA_fltper_1x1 ON USA_mltper_1x1.Year = '
                                  'USA_fltper_1x1.Year AND USA_mltper_1x1.Age = USA_fltper_1x1.Age', conn)

    conn.close()
    print("Task 12:")
    print(death_frame)
    #death_frame = death_frame.groupby(by=["Year", "Age"]).sum().reset_index(drop=False)

    death_frame_yearly = death_frame.groupby(by=["Year"]).sum()

    frame['year'] = frame['year'].astype(int)
    frame_yearly = frame.groupby(by=["year"]).sum()


    merged = frame_yearly.merge(death_frame_yearly, left_index=True, right_index=True)
    merged['NaturalIncrease'] = merged['pop'] - merged['dx']

    fig13, axs13 = plt.subplots(1, 1)
    fig13.canvas.set_window_title('Task 13')
    merged.plot(use_index=True, y='NaturalIncrease', ax=axs13)
    axs13.legend(["Natural Increase"], loc='upper left')
    axs13.title.set_text("Task 13")

    print("Task 13:")
    print(merged['NaturalIncrease'])


    death_frame_0 = death_frame.loc[(death_frame['Age'] == 0)].set_index("Year")
    merged_0 = frame_yearly.merge(death_frame_0, left_index=True, right_index=True)

    merged_0['SurvivalRatio'] = 1 - (merged_0['dx']/merged_0['pop'])
    fig14, axs14 = plt.subplots(1, 1)
    fig14.canvas.set_window_title('Task 14 and 15')
    merged_0.plot(use_index=True, y='SurvivalRatio', ax=axs14)
    print("Task 14:")
    print(merged_0['SurvivalRatio'])

    death_frame_5 = death_frame.loc[(death_frame['Age'] == 0) | (death_frame['Age'] == 1) | (death_frame['Age'] == 2) | (death_frame['Age'] == 3) | (death_frame['Age'] == 4)]

    ratios = []
    for i, j in death_frame_5.iterrows():
        if j['Age'] == 0:
            ratios.append(j['dx'])
        if j['Age'] == 1:
            try:
                ratios[-2] += j['dx']
            except IndexError:
                pass
        if j['Age'] == 2:
            try:
                ratios[-3] += j['dx']
            except IndexError:
                pass
        if j['Age'] == 3:
            try:
                ratios[-4] += j['dx']
            except IndexError:
                pass
        if j['Age'] == 4:
            try:
                ratios[-5] += j['dx']
            except IndexError:
                pass


    merged_0['dx_5'] = ratios

    merged_0['SurvivalRatio_5'] = 1 - (merged_0['dx_5']/merged_0['pop'])

    merged_0.plot(use_index=True, y='SurvivalRatio_5', ax=axs14)
    axs14.legend(["Survival Ratio of a newborn","Survival Ratio of a 5 year old"], loc='upper left')
    axs14.title.set_text("Task 14 i 15")

    print("Task 15:")
    print(merged_0['SurvivalRatio_5'])


def main():

    for filename in all_files:
        year = filename[-8:]
        year = year[:4]
        df = pd.read_csv(filename, index_col=None, header=None)
        df['year'] = year
        list.append(df)

    frame = pd.concat(list, axis=0, join='outer', ignore_index=True, keys=None,
              levels=None, names=None, verify_integrity=False, copy=True)
    frame.columns = ['name', 'sex', 'pop', 'year']

    task2_3(frame)
    task4(frame)
    task5(frame)
    task6_7(frame)
    task8(frame)
    task9(frame)
    task10(frame)
    task11(frame)
    task12_13_14_15(frame)



    plt.show()



if __name__ == '__main__':
    main()
