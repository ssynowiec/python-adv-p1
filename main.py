# File: main.py
#
# Project name: Projekt 1 - Analiza danych i tworzenie wykresów
# Project link: https://github.com/ssynowiec/python-adv-p1
# Date created: 11.10.2023
# Authors:
#   -> Krystian Ozga
#   -> Stanisław Synowiec
#
# License: UNLICENSED

import pandas as pd
import matplotlib.pyplot as plt


class TravelAnalysis:
    def __init__(self, data_file):
        self.data = pd.read_csv('data/' + data_file, sep='\t')

    def plot_city_counts(self):
        city_counts = self.data['Miasto'].value_counts()

        plt.figure(figsize=(15, 5))
        city_counts.plot(kind='bar')
        plt.xlabel('Miasto')
        plt.ylabel('Liczba wyjazdów')
        plt.title('Ilość wyjazdów z każdego miasta')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_monthly_costs(self):
        self.data['Koszt_wyj'] = self.data['Koszt_wyj'].str.replace(',', '.', regex=True).astype(float)
        self.data['D_wyj'] = pd.to_datetime(self.data['D_wyj'])
        self.data['Miesiac'] = self.data['D_wyj'].dt.strftime('%Y-%m')

        total_month = self.data.groupby('Miesiac')['Koszt_wyj'].sum()
        plt.figure(figsize=(10, 5))
        total_month.plot(kind='bar', color='skyblue')
        plt.xlabel('Miesiąc')
        plt.ylabel('Suma kosztów')
        plt.title('Suma kosztów wyjazdów w poszczególnych miesiącach')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_duration_by_city(self):
        self.data['D_wyj'] = pd.to_datetime(self.data['D_wyj'])
        self.data['D_powr'] = pd.to_datetime(self.data['D_powr'])
        self.data['Czas_trwania'] = (self.data['D_powr'] - self.data['D_wyj']).dt.days

        plt.figure(figsize=(10, 5))
        plt.bar(self.data['Miasto'], self.data['Czas_trwania'])
        plt.xlabel('Miasto')
        plt.ylabel('Czas trwania wyjazdu (dni)')
        plt.title('Czas trwania wyjazdu w poszczególnych miastach')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_price_by_sex(self):
        # Zamiana na słupkowy grupowy
        # https://jug.dpieczynski.pl/lab-ead/Lab%2003%20-%20Wykresy.html

        self.data['man'] = 0
        self.data['wom'] = 0
        names = self.data['Imie'].tolist()
        prices = self.data['Koszt_wyj'].str.replace(',', '.', regex=True).astype(float)

        for i in range(len(names)):
            if names[i][len(names[i])-1] == 'a':
                self.data['wom'] += prices[i]
            else:
                self.data['man'] += prices[i]

        total = round(self.data['Koszt_wyj'].str.replace(',', '.', regex=True).astype(float).sum(), 2)

        labels = [f'Man ({round(self.data["man"][2], 2)})zł', f'Woman ({round(self.data["wom"][2], 2)})zł']
        men_price = (self.data['man'][2]/total) * 100
        women_price = (self.data['wom'][2].sum()/total) * 100
        sizes = [men_price, women_price]

        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.legend(loc='best', labels=labels)
        plt.title(f'Procentowy udział płci w kosztach wyjazdów\nŁączny koszt wyjazdów {round(total, 2)}zł')
        plt.show()


if __name__ == '__main__':
    analysis = TravelAnalysis('podroze.txt')

    analysis.plot_price_by_sex()
    # analysis.plot_city_counts()
    # analysis.plot_monthly_costs()
    # analysis.plot_duration_by_city()
