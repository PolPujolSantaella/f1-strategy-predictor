import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go

from src.url_images import get_image_from_wikipedia


LINE_MODE = "lines+markers"

def plot_driver_stats(season_summary, driver_name):
    """Plot season evolution of points and wins for a driver"""
    if season_summary is None or season_summary.empty:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=season_summary['year'],
        y=season_summary['points'],
        mode=LINE_MODE,
        name='Points',
        line={"color": "#FF1801", "width": 3},
        marker={"size": 8}
    ))
    
    fig.add_trace(go.Scatter(
        x=season_summary['year'],
        y=season_summary['wins'],
        mode=LINE_MODE,
        name='Wins',
        yaxis='y2',
        line={"color": "#FFD700", "width": 3},
        marker={"size": 8}
    ))
    
    fig.update_layout(
        title=f'Season Evolution - {driver_name}',
        xaxis_title='Season',
        yaxis_title='Points',
        yaxis2 = {
            'title': 'Wins',
            'overlaying': 'y',
            'side': 'right'
        },
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig

def plot_position_distribution(position_dist, pilot_name):
    """Plot finishing position distribution for a driver."""
    if position_dist is None or position_dist.empty:
        return None
    
    top_positions = position_dist[position_dist['Position'].isin(
        [str(i) for i in range(1, 11)] + ['DNF']
    )]
    
    fig = px.bar(
        top_positions,
        x='Position',
        y='Count',
        title=f'Position Distribution - {pilot_name}',
        color='Count',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        xaxis_title='Final Position',
        yaxis_title='Number of Races',
        showlegend=False,
        template='plotly_white'
    )
    
    return fig

def plot_circuit_performance(circuit_stats, pilot_name):
    """Plot performance by circuit (wins or races)."""
    if circuit_stats is None or circuit_stats.empty:
        return None
    
    winning_circuits = circuit_stats[circuit_stats['wins'] > 0].sort_values('wins', ascending=True)
    
    if winning_circuits.empty:
        top_circuits = circuit_stats.nlargest(10, 'races')
        fig = px.bar(
            top_circuits,
            x='races',
            y='name',
            orientation='h',
            title=f'Most Frequent Circuits - {pilot_name}',
            color='races',
            color_continuous_scale='Reds'
        )
        fig.update_layout(xaxis_title='Races', yaxis_title='Circuits')
    else:
        fig = px.bar(
            winning_circuits,
            x='wins',
            y='name',
            orientation='h',
            title=f'Wins by Circuit - {pilot_name}',
            color='wins',
            color_continuous_scale='Reds'
        )
        fig.update_layout(xaxis_title='Wins', yaxis_title='Circuits')
    
    fig.update_layout(template='plotly_white', showlegend=False)
    
    return fig


def plot_evolution_points_season(season1, season2, name1, name2):
    """Compare season points evolution between two drivers."""
    
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
    
    fig.update_layout(
        title="Points per Season",
        xaxis_title="Season",
        yaxis_title="Points",
        template='plotly_white'
    )
    
    return fig


def plot_key_performance(data1, data2, name1, name2):
    """Compare key statistics between two drivers."""
    
    df_compare = pd.DataFrame({
        "Metric": list(data1.keys()),
        name1: list(data1.values()),
        name2: list(data2.values())
    })

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_compare["Metric"], y=df_compare[name1], name=name1, marker_color='crimson'))
    fig.add_trace(go.Bar(x=df_compare["Metric"], y=df_compare[name2], name=name2, marker_color='royalblue'))
    fig.update_layout(barmode='group', title="Key Stats", yaxis_title="Count", template='plotly_white')
    
    return fig


def plot_final_position_distribution(pos1, pos2, name1, name2):
    """Plot stacked distribution of race results."""
    
    df_pos = pd.DataFrame({
        "Position": ["Wins", "Podiums", "Others"],
        name1: pos1.values,
        name2: pos2.values
    })

    fig = go.Figure()
    fig.add_trace(go.Bar(name=name1, x=df_pos["Position"], y=df_pos[name1], marker_color='tomato'))
    fig.add_trace(go.Bar(name=name2, x=df_pos["Position"], y=df_pos[name2], marker_color='dodgerblue'))
    fig.update_layout(barmode='stack', title="Race Result Distribution", template='plotly_white')
    
    return fig


def plot_average_points_season(avg1, avg2, name1, name2):
    """Plot average points per season comparison."""
    
    df_avg = pd.DataFrame({
        "Driver": [name1, name2],
        "Avg Points / Season": [avg1, avg2]
    })

    fig = px.bar(df_avg,
                x="Driver",
                y="Avg Points / Season",
                color="Driver", 
                color_discrete_map={name1: "firebrick", name2: "navy"},
                text_auto='.2s')
    fig.update_layout(title="Average Points per Season", showlegend=False, template='plotly_white')
    
    return fig


def display_top3_winners_cards(df_top3):
    """Generic card display for top 3 winners"""
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
    """Generic card display for top 3 constructor winners."""
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