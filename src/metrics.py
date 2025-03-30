import json
import math
from functools import reduce
from datetime import datetime, timezone

def calculate_min(values):
    return min(values) if values else 0

def calculate_max(values):
    return max(values) if values else 0

def calculate_mean(values):
    return reduce(lambda acc, x: acc + x, values, 0) / len(values) if values else 0

def calculate_median(values):
    if not values:
        return 0
    sorted_vals = sorted(values)
    mid = len(sorted_vals) // 2
    if len(sorted_vals) % 2 == 0:
        return (sorted_vals[mid] + sorted_vals[mid - 1]) / 2
    else:
        return sorted_vals[mid]

def calculate_stddev(values):
    if not values:
        return 0
    mean = calculate_mean(values)
    variance = reduce(lambda acc, x: acc + (x - mean) ** 2, values, 0) / len(values)
    return math.sqrt(variance)

def calculate_account_age(created_at, reference):
    created_at_date = datetime.fromisoformat(created_at.replace('Z', '+00:00')).astimezone(timezone.utc)
    days_lived = (reference - created_at_date).days
    return days_lived / 365.25

def extract_metrics(users, reference):
    return reduce(lambda acc, u: {
        'followers_count': acc['followers_count'] + [u['followers_count']],
        'following_count': acc['following_count'] + [u['following_count']],
        'account_age': acc['account_age'] + [calculate_account_age(u['created_at'], reference)]
    }, users, {'followers_count': [], 'following_count': [], 'account_age': []})

def generate_statistics(values):
    return {
        'min': round(calculate_min(values), 2),
        'max': round(calculate_max(values), 2),
        'avg': round(calculate_mean(values), 2),
        'median': round(calculate_median(values), 2),
        'std': round(calculate_stddev(values), 2)
    }

def generate_csv(statistics):
    header = "Metric,min,max,avg,median,std"
    rows = [f"{metric},{stats['min']},{stats['max']},{stats['avg']},{stats['median']},{stats['std']}"
            for metric, stats in statistics.items()]
    return header + "\n" + "\n".join(rows)

def process_metrics(users, reference):
    metrics = extract_metrics(users, reference)
    statistics = {metric: generate_statistics(metrics[metric]) for metric in metrics}
    return generate_csv(statistics)

if __name__ == "__main__":
    with open('dados.json', 'r') as f:
        users = json.load(f)
    reference = datetime.now(timezone.utc)
    metrics_csv = process_metrics(users, reference)
    print(metrics_csv)
