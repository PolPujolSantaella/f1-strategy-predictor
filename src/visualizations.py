import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd

def plot_driver_stats(season_df, driver_name):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=season_df['year'],
        y=season_df['points'],
        mode='lines+markers',
        name='Points',
        line=dict(color='firebrick', width=3)
    ))
    
    fig.add_trace(go.Bar(
        x=season_df['year'],
        y=season_df['wins'],
        name='Victorias',
        marker_color='goldenrod',
        opacity=0.6
    ))

    fig.update_layout(
        title=f'Evolución por Temporada - {driver_name}',
        xaxis_title='Temporada',
        yaxis_title='Puntos',
        barmode='overlay',
        template='plotly_white'
    )
    return fig

# 2. Distribución de posiciones
def plot_position_distribution(position_df, driver_name):
    fig = px.bar(
        position_df,
        x='Position',
        y='Count',
        title=f'Distribución de Resultados - {driver_name}',
        labels={'Count': 'Carreras', 'Position': 'Posición'},
        color='Count',
        color_continuous_scale='Tealgrn',
    )

    fig.update_layout(template='plotly_white')
    return fig

# 3. Mapa de rendimiento por circuito
def plot_circuit_performance(circuit_df, driver_name):
    filtered_df = circuit_df[circuit_df['wins'] > 0].copy()

    sorted_df = filtered_df.sort_values(by='wins', ascending=True)

    fig = px.bar(
        sorted_df,
        x='wins',
        y='name',
        orientation='h',
        text='wins',
        color='wins',
        color_continuous_scale='reds',
        labels={'wins': 'Victories', 'name': 'Circuit'},
        height=600
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(
        title=f'Performance for Circuits - {driver_name}',
        xaxis_title='Victories',
        yaxis_title='Circuit',
        margin={'r': 20, 't': 50, 'l': 100, 'b': 20},
    )
    
    return fig


# 4. Comparativa de pilotos
def plot_comparison(season_df1, season_df2, name1, name2):
    merged = pd.merge(season_df1, season_df2, on='year', how='outer', suffixes=(f'_{name1}', f'_{name2}'))
    merged = merged.sort_values('year')

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=merged['year'],
        y=merged[f'points_{name1}'],
        name=name1,
        mode='lines+markers',
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=merged['year'],
        y=merged[f'points_{name2}'],
        name=name2,
        mode='lines+markers',
        line=dict(color='crimson')
    ))

    fig.update_layout(
        title=f'Comparativa de Puntos por Temporada: {name1} vs {name2}',
        xaxis_title='Año',
        yaxis_title='Puntos',
        template='plotly_white'
    )
    return fig
    