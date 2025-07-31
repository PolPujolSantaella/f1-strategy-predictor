import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd

LINE_MODE = "lines+markers"

def plot_driver_stats(season_summary, pilot_name):
    """Crear gráfico de evolución por temporada"""
    if season_summary is None or season_summary.empty:
        return None
    
    fig = go.Figure()
    
    # Puntos por temporada
    fig.add_trace(go.Scatter(
        x=season_summary['year'],
        y=season_summary['points'],
        mode=LINE_MODE,
        name='Puntos',
        line={"color": "#FF1801", "width": 3},
        marker={"size": 8}
    ))
    
    # Victorias por temporada (eje secundario)
    fig.add_trace(go.Scatter(
        x=season_summary['year'],
        y=season_summary['wins'],
        mode=LINE_MODE,
        name='Victorias',
        yaxis='y2',
        line={"color": "#FFD700", "width": 3},
        marker={"size": 8}
    ))
    
    fig.update_layout(
        title=f'Evolución de {pilot_name} por Temporada',
        xaxis_title='Temporada',
        yaxis_title='Puntos',
        yaxis2 = {
            'title': 'Victories',
            'overlaying': 'y',
            
            'side': 'right',
        },
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig

# 2. Distribución de posiciones
def plot_position_distribution(position_dist, pilot_name):
    """Crear gráfico de distribución de posiciones"""
    if position_dist is None or position_dist.empty:
        return None
    
    # Filtrar solo las primeras 10 posiciones + DNF para mejor visualización
    top_positions = position_dist.head(11)
    
    fig = px.bar(
        top_positions,
        x='Position',
        y='Count',
        title=f'Distribución de Posiciones - {pilot_name}',
        color='Count',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        xaxis_title='Posición Final',
        yaxis_title='Número de Carreras',
        showlegend=False,
        template='plotly_white'
    )
    
    return fig

# 3. Mapa de rendimiento por circuito
def plot_circuit_performance(circuit_stats, pilot_name):
    """Crear gráfico de rendimiento por circuito"""
    if circuit_stats is None or circuit_stats.empty:
        return None
    
    # Filtrar solo circuitos con victorias para mejor visualización
    winning_circuits = circuit_stats[circuit_stats['wins'] > 0].sort_values('wins', ascending=True)
    
    if winning_circuits.empty:
        # Si no hay victorias, mostrar todos los circuitos con más carreras
        top_circuits = circuit_stats.nlargest(10, 'races')
        fig = px.bar(
            top_circuits,
            x='races',
            y='name',
            orientation='h',
            title=f'Circuitos más Corridos - {pilot_name}',
            color='races',
            color_continuous_scale='Reds'
        )
        fig.update_layout(
            xaxis_title='Número de Carreras',
            yaxis_title='Circuito'
        )
    else:
        fig = px.bar(
            winning_circuits,
            x='wins',
            y='name',
            orientation='h',
            title=f'Victorias por Circuito - {pilot_name}',
            color='wins',
            color_continuous_scale='Reds'
        )
        fig.update_layout(
            xaxis_title='Número de Victorias',
            yaxis_title='Circuito'
        )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=False
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
        mode=LINE_MODE,
        line={"color": "blue"}
    ))

    fig.add_trace(go.Scatter(
        x=merged['year'],
        y=merged[f'points_{name2}'],
        name=name2,
        mode=LINE_MODE,
        line={"color": "red"}
    ))

    fig.update_layout(
        title=f'Comparativa de Puntos por Temporada: {name1} vs {name2}',
        xaxis_title='Año',
        yaxis_title='Puntos',
        template='plotly_white'
    )
    return fig
    