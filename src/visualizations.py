import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

from src.url_images import get_image_from_wikipedia


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


def plot_evolution_points_season(season1, season2, name1, name2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=season1['year'],
        y=season1['points'], 
        mode = LINE_MODE,
        name=name1,
        line={"color": "red"}
    ))
    fig.add_trace(go.Scatter(
        x=season2['year'],
        y=season2['points'],
        mode=LINE_MODE,
        name=name2, 
        line={"color": "blue"}
    ))
    
    fig.update_layout(title="Points per Season", xaxis_title="Season", yaxis_title="Points")
    return fig


def plot_key_performance(data1, data2, name1, name2):
    df_compare = pd.DataFrame({
        "Metric": list(data1.keys()),
        name1: list(data1.values()),
        name2: list(data2.values())
    })

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_compare["Metric"], y=df_compare[name1], name=name1, marker_color='crimson'))
    fig.add_trace(go.Bar(x=df_compare["Metric"], y=df_compare[name2], name=name2, marker_color='royalblue'))
    fig.update_layout(barmode='group', title="Key Stats", yaxis_title="Count")
    
    return fig


def plot_final_position_distribution(pos1, pos2, name1, name2):
    df_pos = pd.DataFrame({
        "Position": ["Wins", "Podiums", "Others"],
        name1: pos1.values,
        name2: pos2.values
    })

    fig = go.Figure()
    fig.add_trace(go.Bar(name=name1, x=df_pos["Position"], y=df_pos[name1], marker_color='tomato'))
    fig.add_trace(go.Bar(name=name2, x=df_pos["Position"], y=df_pos[name2], marker_color='dodgerblue'))
    fig.update_layout(barmode='stack', title="Race Result Distribution")
    
    return fig


def plot_average_points_season(avg1, avg2, name1, name2):
    df_avg = pd.DataFrame({
        "Driver": [name1, name2],
        "Avg Points / Season": [avg1, avg2]
    })

    fig = px.bar(df_avg, x="Driver", y="Avg Points / Season", color="Driver", 
                color_discrete_map={name1: "firebrick", name2: "navy"},
                text_auto='.2s')
    fig.update_layout(title="Average Points per Season", showlegend=False)
    
    return fig


def display_top3_winners_cards(df_top3):
    st.markdown("## 🏆 Top 3 Winners")

    cols = st.columns(3)

    for i, (_, row) in enumerate(df_top3.iterrows()):
        with cols[i]:
            image_url = get_image_from_wikipedia(row['url']) or "default_driver.png"

            st.markdown(f"""
            <div style="
                background-color: white;
                border: 2px solid #ccc;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            ">
                <h3 style="margin-bottom: 15px; color: black">{row['driver']}</h3>
                <img src="{image_url}" alt="{row['driver']}" style="width:150px; border-radius: 10px;" />
                <div style="font-size: 24px; font-weight: bold; margin-top: 10px; color: black;">
                    🏁 Victorias: {row['wins']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            
def display_top3_constructors_cards(df_top3):
    st.markdown("## 🏆 Top 3 Constructor Winners")

    cols = st.columns(3)

    for i, (_, row) in enumerate(df_top3.iterrows()):
        with cols[i]:
            image_url = get_image_from_wikipedia(row['url']) or "default_driver.png"

            st.markdown(f"""
            <div style="
                background-color: white;
                border: 2px solid #ccc;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            ">
                <h3 style="margin-bottom: 15px; color: black">{row['constructor']}</h3>
                <img src="{image_url}" alt="{row['constructor']}" style="width:150px; border-radius: 10px;" />
                <div style="font-size: 24px; font-weight: bold; margin-top: 10px; color: black;">
                    🏁 Victorias: {row['wins']}
                </div>
            </div>
            """, unsafe_allow_html=True)