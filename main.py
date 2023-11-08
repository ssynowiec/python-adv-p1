# File: main.py
#
# Project name: Projekt 1 - Analiza danych i tworzenie wykresów
# Date created: 11.10.2023
# Authors:
#   -> Krystian Ozga
#   -> Stanisław Synowiec
#
# License: UNLICENSED

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from matplotlib import gridspec


class TravelAnalysis:
    def __init__(self, data_file):
        self.data = pd.read_csv('data/' + data_file, sep='\t')
        self.data['Koszt_wyj'] = self.data['Koszt_wyj'].str.replace(',', '.', regex=True).astype(float)

    def plot_city_travel_counts(self):
        city_counts_men = self.data[self.data['Imie'].str[-1] != 'a']['Miasto'].value_counts()
        city_counts_women = self.data[self.data['Imie'].str[-1] == 'a']['Miasto'].value_counts()

        city_counts_men = city_counts_men.sort_values(ascending=True)
        city_counts_women = city_counts_women.sort_values(ascending=True)

        plt.figure(figsize=(13, 8))
        plt.subplot(2, 1, 1)
        city_counts_men.plot(kind='bar', color='lightblue')
        plt.title('Liczba mężczyzn podróżujących do miasta')
        plt.xlabel('Miasto')
        plt.ylabel('Liczba mężczyzn')
        plt.xticks(rotation=45)

        plt.subplot(2, 1, 2)
        city_counts_women.plot(kind='bar', color='pink')
        plt.title('Liczba kobiet podróżujących do miasta')
        plt.xlabel('Miasto')
        plt.ylabel('Liczba kobiet')
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

    def plot_city_entries_by_month(self):
        self.data['D_wyj'] = pd.to_datetime(self.data['D_wyj'])
        self.data['D_powr'] = pd.to_datetime(self.data['D_powr'])
        self.data['Miesiąc'] = self.data['D_wyj'].dt.month
        grouped = self.data.groupby(['Miasto', 'Miesiąc'])

        cities = []
        months = []
        entries = []

        for (city, month), group in grouped:
            cities.append(city)
            months.append(month)
            entries.append(len(group))

        avg_costs = self.data.groupby('Miasto')['Koszt_wyj'].mean()

        fig, ax1 = plt.subplots(figsize=(12, 8))

        ax1.bar(cities, entries, color='lightgreen', alpha=0.5, label='Ilość wjeżdżających')
        ax1.set_xlabel('Miasto')
        ax1.set_ylabel('Ilość wjeżdżających')
        ax1.set_title('Stosunek Ilości Wjeżdżających do Miasta a Miesiącem')

        ax2 = ax1.twinx()
        ax2.plot(avg_costs.index, avg_costs.values, color='r', marker='o', label='Średni koszt (PLN)')
        ax2.set_ylabel('Średni koszt (PLN)')

        plt.xticks(rotation=45)
        plt.grid(True)
        fig.tight_layout()

        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        plt.show()

    def analyze_top_travelers(self):
        self.data['D_wyj'] = pd.to_datetime(self.data['D_wyj'])
        self.data['D_powr'] = pd.to_datetime(self.data['D_powr'])

        grouped_data = self.data.groupby(['Imie', 'Nazwisko'])
        summary_data = grouped_data.agg({'Miasto': 'count', 'Koszt_wyj': 'sum', 'D_powr': 'max', 'D_wyj': 'min'})
        summary_data['Długość_podróży'] = (summary_data['D_powr'] - summary_data['D_wyj']).dt.days
        top_10_travelers = summary_data.sort_values(by='Miasto', ascending=False).head(10)

        fig, ax1 = plt.subplots(figsize=(20, 8))
        ax2 = ax1.twinx()

        ax1.bar(top_10_travelers.index.map(lambda x: f'{x[0]} {x[1]}'), top_10_travelers['Miasto'], color='orange',
                alpha=0.5, label='Ilość podróży')
        ax2.plot(top_10_travelers.index.map(lambda x: f'{x[0]} {x[1]}'), top_10_travelers['Koszt_wyj'],
                 color='darkblue', marker='o', label='Suma kosztów za podróże')

        ax1.set_xlabel('Podróżnicy')
        ax1.set_ylabel('Ilość podróży')
        ax2.set_ylabel('Suma kosztów')

        plt.title('Analiza 10 najczęściej podróżujących osób')
        plt.xticks(rotation=45)

        # Dodanie legendy
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        plt.figure(figsize=(7, 6))
        city_counts = self.data['Miasto'].value_counts()
        top_city = city_counts.idxmax()
        explode = [0.1 if city == top_city else 0 for city in city_counts.index]

        plt.pie(city_counts, labels=None, autopct='%1.1f%%', startangle=140, explode=explode, pctdistance=0.85)

        center_circle = plt.Circle((0, 0), 0.40, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)

        plt.axis('equal')
        plt.legend(city_counts.index, title='Miasta', bbox_to_anchor=(0.85, 0.5))
        plt.title(f'Najczęściej wybierane miasto: {top_city}')

        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    analysis = TravelAnalysis('podroze.txt')

    analysis.analyze_top_travelers()
    analysis.plot_city_travel_counts()
    analysis.plot_city_entries_by_month()
