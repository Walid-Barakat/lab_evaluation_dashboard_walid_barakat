"""Reproducible, explicitly synthetic lab data. Never use as a benchmark."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ['reasoning', 'knowledge', 'code', 'instruction_following', 'tool_calling']
MODELS = ['Candidate A', 'Candidate B', 'Candidate C', 'Candidate D']
PARAMETERS = [(2, 3), (4, 2), (3, 3), (5, 2), (3, 3)]

def generate(seed=42, end_date='2026-10-07'):
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=end_date, periods=90)
    records = []
    example_id = 0
    for date in dates:
        for category, (a, b) in zip(CATEGORIES, PARAMETERS):
            for _ in range(5):
                example_id += 1
                base = rng.beta(a, b) * 100
                for model, offset in zip(MODELS, [0, 3, -4, 1]):
                    score = round(float(np.clip(base + offset + rng.normal(0, 5), 0, 100)), 2)
                    records.append({'evaluation_id': len(records)+1, 'example_id': example_id,
                        'category': category, 'score': score, 'model_version': model,
                        'date': date.strftime('%Y-%m-%d')})
    raw = pd.DataFrame(records)
    clean = raw.copy()
    clean['score_bin'] = np.minimum((clean.score // 10).astype(int)*10, 90)
    clean['score_range'] = clean.score_bin.map(lambda x: f'{x:02d}-{x+10}')
    clean['meets_target'] = (clean.score >= 80).astype(int)
    # Difference and agreement use exported rounded scores, preventing boundary mismatches.
    judges = raw.drop(columns='score').copy()
    judges['judge_1_score'] = np.round(np.clip(raw.score + rng.normal(0, 7, len(raw)), 0, 100), 2)
    judges['judge_2_score'] = np.round(np.clip(raw.score + rng.normal(1, 9, len(raw)), 0, 100), 2)
    judges['score_difference'] = np.round(abs(judges.judge_1_score - judges.judge_2_score), 2)
    judges['agreement'] = (judges.score_difference <= 10).astype(int)
    judges['difference_bin'] = np.minimum((judges.score_difference // 10).astype(int)*10, 90)
    judges['difference_range'] = judges.difference_bin.map(lambda x: f'{x:02d}-{x+10}')
    return raw, clean, judges

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--end-date', default='2026-10-07')
    args = parser.parse_args()
    directory = ROOT / 'data'
    directory.mkdir(exist_ok=True)
    for filename, frame in zip(['evaluation_data.csv','evaluation_data_clean.csv','judge_agreement_data.csv'],
                              generate(args.seed, args.end_date)):
        frame.to_csv(directory / filename, index=False, encoding='utf-8')
        print(f'{filename}: {len(frame):,} synthetic rows')

if __name__ == '__main__':
    main()
