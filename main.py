from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / 'outputs'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DATA = [
    {"fighter": "Islam Makhachev", "weight_class": "Lightweight", "stance": "Southpaw", "strikes_landed_pm": 2.46, "strikes_absorbed_pm": 1.28, "takedown_avg": 3.39, "takedown_def": 0.90, "sub_avg": 1.00, "win_rate": 0.93},
    {"fighter": "Charles Oliveira", "weight_class": "Lightweight", "stance": "Orthodox", "strikes_landed_pm": 3.52, "strikes_absorbed_pm": 3.20, "takedown_avg": 2.24, "takedown_def": 0.56, "sub_avg": 2.70, "win_rate": 0.79},
    {"fighter": "Alexander Volkanovski", "weight_class": "Featherweight", "stance": "Orthodox", "strikes_landed_pm": 6.16, "strikes_absorbed_pm": 3.44, "takedown_avg": 1.78, "takedown_def": 0.70, "sub_avg": 0.20, "win_rate": 0.88},
    {"fighter": "Ilia Topuria", "weight_class": "Featherweight", "stance": "Orthodox", "strikes_landed_pm": 4.69, "strikes_absorbed_pm": 3.64, "takedown_avg": 2.03, "takedown_def": 0.92, "sub_avg": 0.20, "win_rate": 1.00},
    {"fighter": "Sean O'Malley", "weight_class": "Bantamweight", "stance": "Switch", "strikes_landed_pm": 6.70, "strikes_absorbed_pm": 3.52, "takedown_avg": 0.22, "takedown_def": 0.61, "sub_avg": 0.00, "win_rate": 0.82},
    {"fighter": "Merab Dvalishvili", "weight_class": "Bantamweight", "stance": "Orthodox", "strikes_landed_pm": 4.36, "strikes_absorbed_pm": 2.34, "takedown_avg": 6.30, "takedown_def": 0.80, "sub_avg": 0.10, "win_rate": 0.88},
    {"fighter": "Leon Edwards", "weight_class": "Welterweight", "stance": "Southpaw", "strikes_landed_pm": 2.68, "strikes_absorbed_pm": 2.39, "takedown_avg": 1.25, "takedown_def": 0.65, "sub_avg": 0.30, "win_rate": 0.82},
    {"fighter": "Belal Muhammad", "weight_class": "Welterweight", "stance": "Orthodox", "strikes_landed_pm": 4.39, "strikes_absorbed_pm": 3.57, "takedown_avg": 2.28, "takedown_def": 0.92, "sub_avg": 0.10, "win_rate": 0.86},
    {"fighter": "Alex Pereira", "weight_class": "Light Heavyweight", "stance": "Orthodox", "strikes_landed_pm": 5.23, "strikes_absorbed_pm": 3.42, "takedown_avg": 0.22, "takedown_def": 0.70, "sub_avg": 0.00, "win_rate": 0.89},
    {"fighter": "Magomed Ankalaev", "weight_class": "Light Heavyweight", "stance": "Switch", "strikes_landed_pm": 3.64, "strikes_absorbed_pm": 2.02, "takedown_avg": 0.92, "takedown_def": 0.86, "sub_avg": 0.00, "win_rate": 0.90},
    {"fighter": "Tom Aspinall", "weight_class": "Heavyweight", "stance": "Orthodox", "strikes_landed_pm": 8.07, "strikes_absorbed_pm": 2.25, "takedown_avg": 3.62, "takedown_def": 1.00, "sub_avg": 0.60, "win_rate": 0.93},
    {"fighter": "Ciryl Gane", "weight_class": "Heavyweight", "stance": "Orthodox", "strikes_landed_pm": 5.10, "strikes_absorbed_pm": 2.16, "takedown_avg": 0.53, "takedown_def": 0.42, "sub_avg": 0.00, "win_rate": 0.83},
]


def build_df() -> pd.DataFrame:
    df = pd.DataFrame(DATA)
    df['strike_diff_pm'] = df['strikes_landed_pm'] - df['strikes_absorbed_pm']
    df['grappling_score'] = df['takedown_avg'] * 0.7 + df['sub_avg'] * 0.3
    df['control_score'] = df['takedown_def'] * 5 + df['strike_diff_pm']
    return df


def matchup_score(a: pd.Series, b: pd.Series) -> dict:
    striking_edge = (a['strike_diff_pm'] - b['strike_diff_pm']) * 12
    wrestling_edge = (a['takedown_avg'] - b['takedown_avg']) * 8
    defense_edge = (a['takedown_def'] - b['takedown_def']) * 10
    submission_edge = (a['sub_avg'] - b['sub_avg']) * 6
    total = striking_edge + wrestling_edge + defense_edge + submission_edge
    lean = a['fighter'] if total >= 0 else b['fighter']
    return {
        'fighter_a': a['fighter'],
        'fighter_b': b['fighter'],
        'striking_edge': round(striking_edge, 2),
        'wrestling_edge': round(wrestling_edge, 2),
        'defense_edge': round(defense_edge, 2),
        'submission_edge': round(submission_edge, 2),
        'total_edge': round(total, 2),
        'lean': lean,
    }


def chart_style_map(df: pd.DataFrame):
    styles = {
        'Orthodox': '#1f77b4',
        'Southpaw': '#d62728',
        'Switch': '#2ca02c',
    }
    return [styles.get(s, '#7f7f7f') for s in df['stance']]


def make_charts(df: pd.DataFrame) -> tuple[Path, Path]:
    plt.style.use('ggplot')

    fig, ax = plt.subplots(figsize=(10, 6))
    ranked = df.sort_values('control_score', ascending=False)
    ax.barh(ranked['fighter'], ranked['control_score'], color=chart_style_map(ranked))
    ax.set_title('UFC fighter control score by style profile')
    ax.set_xlabel('Control score')
    ax.invert_yaxis()
    fig.tight_layout()
    control_path = OUTPUT_DIR / 'fighter_control_scores.png'
    fig.savefig(control_path, dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(df['strike_diff_pm'], df['grappling_score'], s=df['win_rate'] * 500, c=chart_style_map(df), alpha=0.85)
    for _, row in df.iterrows():
        ax.annotate(row['fighter'].split()[-1], (row['strike_diff_pm'], row['grappling_score']), xytext=(4, 4), textcoords='offset points', fontsize=8)
    ax.set_title('UFC style map: striking edge vs grappling score')
    ax.set_xlabel('Strike differential per minute')
    ax.set_ylabel('Grappling score')
    fig.tight_layout()
    scatter_path = OUTPUT_DIR / 'style_matchup_map.png'
    fig.savefig(scatter_path, dpi=180)
    plt.close(fig)

    return control_path, scatter_path


def main() -> None:
    df = build_df()
    control_path, scatter_path = make_charts(df)

    comparisons = [
        matchup_score(df.loc[df['fighter'] == 'Islam Makhachev'].iloc[0], df.loc[df['fighter'] == 'Charles Oliveira'].iloc[0]),
        matchup_score(df.loc[df['fighter'] == 'Sean O\'Malley'].iloc[0], df.loc[df['fighter'] == 'Merab Dvalishvili'].iloc[0]),
        matchup_score(df.loc[df['fighter'] == 'Alex Pereira'].iloc[0], df.loc[df['fighter'] == 'Magomed Ankalaev'].iloc[0]),
    ]
    matchup_df = pd.DataFrame(comparisons)
    matchup_df.to_csv(OUTPUT_DIR / 'sample_matchup_edges.csv', index=False)

    print('UFC style matchup decider')
    print(f'- Fighters analyzed: {len(df)}')
    print(f'- Saved chart: {control_path}')
    print(f'- Saved chart: {scatter_path}')
    print(f'- Saved table: {OUTPUT_DIR / "sample_matchup_edges.csv"}')
    print('\nSample matchup leans:')
    print(matchup_df.to_string(index=False))


if __name__ == '__main__':
    main()
