# imports
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



def area(df, parm, target):
    df = df[[parm, target]]
    df = df.groupby([parm]).mean()
    fig = px.area(df, title=parm)
    return fig


def histogram(df, parm, target):
    df = df[[parm, target]]
    fig = px.histogram(df, x=parm, y=target, histfunc='avg')
    fig.update_xaxes(type='category')
    return fig


def heatmap(df, par1, par2, target):
    # format data
    df = df.pivot_table(values=target, index=par1, columns=par2)

    # plot and save image
    fig = px.imshow(
        # data
        df,

        # inside text
        text_auto='.2f',

        # coloring
        range_color=[-3, 3],
        color_continuous_scale=['red', 'white', 'green'],
        color_continuous_midpoint=0,
        labels={'color': target}
    )

    fig.update_xaxes(type='category')
    fig.update_yaxes(type='category')
    return fig


def surface_3d(df, par1, par2, target):
    # format data
    df = df.pivot_table(values=target, index=par1, columns=par2)
    x = df.columns
    y = df.index
    z = df.values

    # plot image
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z)])
    fig.update_scenes(
        xaxis_title_text=par2,
        yaxis_title_text=par1,
        zaxis_title_text=target,
    )
    return fig
