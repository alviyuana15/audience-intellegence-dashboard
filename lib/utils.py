import numpy as np
from scipy import stats


def apply_filters(
    df,
    location_filter,
    interest_filter,
    age_group_filter,
    phone_filter,
    time_filter,
    engagement_filter
):
    filtered_df = df[
        (df["Tipe Lokasi"].isin(location_filter)) &
        (df["Minat Digital"].isin(interest_filter)) &
        (df["Kelompok Usia"].isin(age_group_filter)) &
        (df["Merk HP"].isin(phone_filter)) &
        (df["Time Segment"].isin(time_filter)) &
        (df["Engagement Level"].isin(engagement_filter))
    ]

    return filtered_df


def calculate_confidence_interval(series, confidence_level=0.95):
    data = series.dropna()

    if len(data) <= 1:
        return None

    n = len(data)
    mean_value = np.mean(data)
    std_value = np.std(data, ddof=1)

    alpha = 1 - confidence_level
    t_critical = stats.t.ppf(1 - alpha / 2, df=n - 1)
    margin_error = t_critical * (std_value / np.sqrt(n))

    lower_bound = mean_value - margin_error
    upper_bound = mean_value + margin_error

    return {
        "n": n,
        "mean": mean_value,
        "std": std_value,
        "confidence_level": confidence_level,
        "margin_error": margin_error,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound
    }


def create_summary_count(df, column_name, count_name="Jumlah User"):
    if df.empty:
        return None

    summary = df[column_name].value_counts().reset_index()
    summary.columns = [column_name, count_name]

    return summary


def create_average_summary(df, group_col, value_col):
    if df.empty:
        return None

    summary = df.groupby(group_col)[value_col].mean().reset_index()
    summary.columns = [group_col, f"Rata-rata {value_col}"]

    return summary


def get_top_value(df, column_name):
    if df.empty:
        return "-"

    return df[column_name].mode()[0]


def get_total_users(df):
    return len(df)


def get_average_value(df, column_name):
    if df.empty:
        return 0

    return df[column_name].mean()


def format_number(value):
    return f"{value:,.0f}"


def format_decimal(value, decimal=2):
    return f"{value:.{decimal}f}"