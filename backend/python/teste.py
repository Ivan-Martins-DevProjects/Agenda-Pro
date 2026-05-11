field_type = 'semana'
query_params = {
    # 'hoje': 'date',
    'semana': 'week',
    'mes': 'month',
}

interval = query_params[field_type]
print(interval)
