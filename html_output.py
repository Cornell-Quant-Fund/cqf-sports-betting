import pandas as pd

data = pd.read_csv('output.txt', delimiter=',', index_col=False)


def probability_to_color(prob):
    red = int((1 - prob) * 255)
    green = int(prob * 255)
    blue = 0
    return f'rgb({red},{green},{blue})'


data['color'] = data[' probability'].apply(probability_to_color)


def generate_html(data):
    rows = []
    for _, row in data.iterrows():
        html_row = '<tr>'
        for col in data.columns:
            if col == 'probability':
                html_row += f'<td style="background-color: {row["color"]};">{row[col]}</td>'
            elif col != 'color':
                html_row += f'<td>{row[col]}</td>'
        html_row += '</tr>'
        rows.append(html_row)
    return rows


header_html = '<tr>' + \
    ''.join(f'<th>{col}</th>' for col in data.columns if col !=
            'color') + '</tr>'
rows_html = generate_html(data)
full_html = f"<table>{header_html}{''.join(rows_html)}</table>"

styled_html = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    {full_html}
</body>
</html>
"""

with open('styled_output.html', 'w') as f:
    f.write(styled_html)
