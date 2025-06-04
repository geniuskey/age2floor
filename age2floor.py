import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
YEAR_MIN = 1960
YEAR_MAX = 2072


def load_population_csv(file_path, sex='전체') -> pd.DataFrame:
    df = pd.read_csv(file_path, encoding='euc-kr')
    df = df[df['성별'] == sex]
    df.drop(columns=['성별'], inplace=True)
    df = df.set_index('연령별')
    target_columns = [col for col in df.columns if col.strip().endswith('년')]

    # 각 컬럼의 데이터 타입 변환
    for col in target_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int32')  # 결측값도 처리
    return df


def get_life_floors(df, born_year=1985) -> pd.DataFrame:
    start_year = max(YEAR_MIN, born_year)
    end_year = min(YEAR_MAX, born_year + 99)
    years = np.arange(start_year, end_year + 1)
    ages = years - born_year
    # total_counts = [df.loc['계', f'{year} 년'] for year in years]
    age_rates = []
    for year, age in zip(years, ages):
        total_count = df.loc['계', f'{year} 년']
        cnt = 0
        for i in range(age):
            cnt += df.loc[f'{i}세', f'{year} 년']
        cnt += df.loc[f'{age}세', f'{year} 년'] // 2
        age_rates.append(cnt / total_count)
    floors = np.array(age_rates) * 100
    # floors = np.ceil(floors).astype(int)
    return pd.DataFrame({'years': years, 'ages': ages,
                         'age_rates': age_rates,
                         'floors': floors})


def plot_life_floors(df, born_years=(1985,)) -> None:
    fig, ax = plt.subplots()
    for born_year in born_years:
        df2 = get_life_floors(df, born_year=born_year)
        ax.plot(df2['ages'], df2['floors'], label=f'{born_year}년생')
        ax.xaxis.set_major_locator(MultipleLocator(10))
        ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.set_title('나이 vs 사회적 나이(층)')
    ax.set_xlabel('ages')
    ax.set_ylabel('floors')
    ax.grid()
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    data = load_population_csv(r"korean_population.csv")
    plot_life_floors(data, range(1950, 2021, 10))
