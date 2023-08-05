import pandas as pd
import plotly.express as px
import seaborn as sns
import altair as alt

#Histogram Line-------------------------------------------------------------------------------------------------------
def linehist(data, curve):
    if curve in ["LLD", "LLS"]:
        fig = sns.displot(data, x=curve, hue="WELL", kind="kde", height=5,aspect=1.2, log_scale=True)
        fig.set(ylabel="Values")
    else:
        fig = sns.displot(data, x=curve, hue="WELL", kind="kde", height=5,aspect=1.2)
        fig.set(ylabel="Values")
        
#CrossPlot------------------------------------------------------------------------------------------------------------
def cross_plot(data, x_axis, y_axis, log_x:bool=False, log_y:bool=False, hue:str=None):     
    fig = sns.jointplot(data=data, x=x_axis, y=y_axis, hue=hue)
    if log_x:
        fig.ax_joint.set_xscale('log')
        fig.ax_marg_x.set_xscale('log')
    if log_y:
        fig.ax_joint.set_yscale('log')
        fig.ax_marg_y.set_yscale('log')
        
#PairPlot-------------------------------------------------------------------------------------------------------------
def pair_plot(data, rows, cols,color_):
    return alt.Chart(data).mark_circle().encode(
            alt.X(alt.repeat("column"), type='quantitative', scale=alt.Scale(zero=False)),
            alt.Y(alt.repeat("row"), type='quantitative', scale=alt.Scale(zero=False)),
            color=color_
            ).properties(
                width=100,
                height=100
            ).repeat(
                row = rows,
                column = cols
            ).configure_axis(
                grid=False
            )
#Heatmap--------------------------------------------------------------------------------------------------------------
def heatmap(df):            
    fig = sns.heatmap(df, annot=True)
    
#3D-------------------------------------------------------------------------------------------------------------------
def scatter_3d(data:pd.DataFrame = None, 
              x_value: str = None, 
              y_value: str = None, 
              z_value: str = None, 
              color: str = None, 
              opacity : float = 1,
              symnbol_size : str = None, 
              size_max : int = 18,
              symbol : str = None, 
              log_x : bool = False, 
              log_y : bool = False, 
              log_z : bool = False,
              size: list = [1000, 700],
              ):
    
    fig = px.scatter_3d(data, 
                        x=x_value, 
                        y=y_value, 
                        z=z_value,
                        color=color, 
                        size=symnbol_size, 
                        size_max=size_max,
                        symbol=symbol, 
                        opacity=opacity,
                        log_x=log_x,
                        log_y=log_y,
                        log_z=log_z,
                        width=size[0], height=size[1],
                        color_continuous_scale="blugrn",
                        )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), #tight layout
                    #   paper_bgcolor="LightSteelBlue"
                    template="none")
    fig.show()