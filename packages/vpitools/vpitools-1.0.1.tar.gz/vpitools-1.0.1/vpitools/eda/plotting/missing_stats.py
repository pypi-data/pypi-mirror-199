import pandas as pd
import plotly.express as px

def missing_stats(data:pd.DataFrame = None,
                  title: str = None,
                  ):
    missing = data.isnull().sum()*100/data.isnull().sum().sum()
    missing = missing[missing >= 0].reset_index()
    missing.columns = ['Columns', 'Count missing (%)']
    
    fig = px.bar(missing, y='Count missing (%)', x='Columns', text_auto='.2s',
            title=title)
    fig.show()