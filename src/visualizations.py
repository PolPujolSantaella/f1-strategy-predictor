import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

from src.url_images import get_image_from_wikipedia


LINE_MODE = "lines+markers"

def plot_driver_stats(season_summary, driver_name):
    """Plot season evolution of points and wins for a driver"""
    if season_summary is None or season_summary.empty:
        return None
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Points & Wins Evolution', 'Podiums & Races Participation'),
        specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
        vertical_spacing=0.12
    )
    
    fig.add_trace(go.Scatter(
        x=season_summary['year'],
        y=season_summary['points'],
        mode=LINE_MODE,
        name='Points',
        line={"color": "#FF1801", "width": 3},
        marker={"size": 8},
        hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Points: %{y}<extra></extra>'
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=season_summary['year'],
        y=season_summary['wins'],
        mode=LINE_MODE,
        name='Wins',
        yaxis='y2',
        line={"color": "#FFD700", "width": 3},
        marker={"size": 8},
        hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Wins: %{y}<extra></extra>'
    ), row=1, col=1, secondary_y=True)
    
    if 'podiums' in season_summary.columns:
        fig.add_trace(go.Scatter(
            x=season_summary['year'],
            y=season_summary['podiums'],
            mode=LINE_MODE,
            name='Podiums',
            line=dict(color="#32CD32", width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Podiums: %{y}<extra></extra>'
        ), row=2, col=1)
        
    if 'races' in season_summary.columns:
        fig.add_trace(go.Scatter(
            x=season_summary['year'],
            y=season_summary['races'],
            mode=LINE_MODE,
            name='Races',
            line=dict(color="#1E90FF", width=3),
            marker=dict(size=8),
            yaxis='y4',
            hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Races: %{y}<extra></extra>'
        ), row=2, col=1, secondary_y=True)
    
    fig.update_layout(
        title=dict(
            text=f'<b>Complete Season Analysis - {driver_name.title()}</b>',
            x=0.5,
            font=dict(size=20)
        ),
        hovermode='x unified',
        template='plotly_white',
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.update_xaxes(title_text="Season", row=2, col=1)
    fig.update_yaxes(title_text="Points", row=1, col=1)
    fig.update_yaxes(title_text="Wins", secondary_y=True, row=1, col=1)
    fig.update_yaxes(title_text="Podiums", row=2, col=1)
    fig.update_yaxes(title_text="Races", secondary_y=True, row=2, col=1)
    
    
    return fig

def plot_position_distribution(position_dist, pilot_name):
    """Enhanced finishing position distribution with better styling"""
    if position_dist is None or position_dist.empty:
        return None
    
    # Prepare data for better visualization
    position_dist = position_dist.copy()
    position_dist['Position_Numeric'] = pd.to_numeric(
        position_dist['Position'].replace('DNF', '21'), errors='coerce'
    )
    position_dist = position_dist.sort_values('Position_Numeric')
    
    # Create color scale based on position quality
    colors = []
    for pos in position_dist['Position']:
        if pos == '1':
            colors.append('#FFD700')  # Gold for 1st
        elif pos == '2':
            colors.append('#C0C0C0')  # Silver for 2nd
        elif pos == '3':
            colors.append('#CD7F32')  # Bronze for 3rd
        elif pos in ['4', '5', '6', '7', '8', '9', '10']:
            colors.append('#4CAF50')  # Green for points
        elif pos == 'DNF':
            colors.append('#F44336')  # Red for DNF
        else:
            colors.append('#9E9E9E')  # Gray for others
    
    fig = go.Figure(data=[
        go.Bar(
            x=position_dist['Position'],
            y=position_dist['Count'],
            marker_color=colors,
            text=position_dist['Count'],
            textposition='auto',
            hovertemplate='<b>Position %{x}</b><br>Races: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=f'<b>Position Distribution - {pilot_name.title()}</b>',
            x=0.5,
            font=dict(size=18)
        ),
        xaxis_title='Final Position',
        yaxis_title='Number of Races',
        template='plotly_white',
        showlegend=False,
        xaxis=dict(categoryorder='array', categoryarray=sorted(
            position_dist['Position_Numeric'].dropna().astype(int).astype(str).tolist() +
            ['DNF'] if 'DNF' in position_dist['Position'].values else []
        ))
    )
    
    return fig


def plot_circuit_performance(circuit_stats, pilot_name):
    """Enhanced circuit performance with dual view"""
    if circuit_stats is None or circuit_stats.empty:
        return None
    
    winning_circuits = circuit_stats[circuit_stats['wins'] > 0].sort_values('wins', ascending=True)
    
    if winning_circuits.empty:
        # Show most frequent circuits
        top_circuits = circuit_stats.nlargest(15, 'races')
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=top_circuits['name'],
            x=top_circuits['races'],
            orientation='h',
            marker=dict(
                color=top_circuits['races'],
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="Races")
            ),
            text=top_circuits['races'],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Races: %{x}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'<b>Most Frequent Circuits - {pilot_name.title()}</b>',
            xaxis_title='Number of Races',
            yaxis_title='Circuits',
            height=max(400, len(top_circuits) * 25)
        )
    else:
        # Show wins with win rate
        if 'races' in winning_circuits.columns:
            winning_circuits['win_rate'] = (winning_circuits['wins'] / winning_circuits['races'] * 100).round(1)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Total Wins', 'Win Rate (%)'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        # Wins chart
        fig.add_trace(go.Bar(
            y=winning_circuits['name'],
            x=winning_circuits['wins'],
            orientation='h',
            marker_color='crimson',
            name='Wins',
            text=winning_circuits['wins'],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Wins: %{x}<extra></extra>'
        ), row=1, col=1)
        
        # Win rate chart (if available)
        if 'win_rate' in winning_circuits.columns:
            fig.add_trace(go.Bar(
                #y=winning_circuits['name'],
                x=winning_circuits['win_rate'],
                orientation='h',
                marker_color='darkgreen',
                name='Win Rate %',
                text=[f"{rate}%" for rate in winning_circuits['win_rate']],
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>Win Rate: %{x}%<extra></extra>'
            ), row=1, col=2)
        
        fig.update_layout(
            title=f'<b>Circuit Dominance - {pilot_name.title()}</b>',
            height=max(400, len(winning_circuits) * 30),
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Wins", row=1, col=1)
        fig.update_xaxes(title_text="Win Rate (%)", row=1, col=2)
    
    fig.update_layout(template='plotly_white')
    return fig


def plot_evolution_points_season(season1, season2, name1, name2):
    """Enhanced season comparison with trend analysis"""
    
    fig = go.Figure()
    
    # Add trend lines
    if len(season1) > 1:
        z1 = np.polyfit(season1['year'], season1['points'], 1)
        p1 = np.poly1d(z1)
        fig.add_trace(go.Scatter(
            x=season1['year'],
            y=p1(season1['year']),
            mode='lines',
            name=f'{name1} Trend',
            line=dict(color='red', dash='dash', width=2),
            opacity=0.7
        ))
    
    if len(season2) > 1:
        z2 = np.polyfit(season2['year'], season2['points'], 1)
        p2 = np.poly1d(z2)
        fig.add_trace(go.Scatter(
            x=season2['year'],
            y=p2(season2['year']),
            mode='lines',
            name=f'{name2} Trend',
            line=dict(color='blue', dash='dash', width=2),
            opacity=0.7
        ))
    
    # Add actual data
    fig.add_trace(go.Scatter(
        x=season1['year'],
        y=season1['points'], 
        mode=LINE_MODE,
        name=name1,
        line=dict(color="red", width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=season2['year'],
        y=season2['points'],
        mode=LINE_MODE,
        name=name2, 
        line=dict(color="blue", width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="<b>Points Evolution Comparison</b>",
        xaxis_title="Season",
        yaxis_title="Points",
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig


def plot_key_performance(data1, data2, name1, name2):
    """Enhanced key performance comparison with percentage differences"""
    
    df_compare = pd.DataFrame({
        "Metric": list(data1.keys()),
        name1: list(data1.values()),
        name2: list(data2.values())
    })
    
    # Calculate percentage differences
    df_compare['diff_pct'] = ((df_compare[name1] - df_compare[name2]) / 
                             df_compare[name2].replace(0, 1) * 100).round(1)

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_compare["Metric"], 
        y=df_compare[name1], 
        name=name1, 
        marker_color='crimson',
        text=df_compare[name1],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        x=df_compare["Metric"], 
        y=df_compare[name2], 
        name=name2, 
        marker_color='royalblue',
        text=df_compare[name2],
        textposition='auto'
    ))
    
    fig.update_layout(
        barmode='group', 
        title="<b>Key Performance Metrics Comparison</b>", 
        yaxis_title="Count", 
        template='plotly_white',
        hovermode='x'
    )
    
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
    """Enhanced winner cards with better styling and animations"""
    st.markdown("## 🏆 Top 3 Winners")

    if df_top3.empty:
        st.info("No winner data available for this circuit.")
        return

    cols = st.columns(3)
    medal_colors = ["#FFD700", "#C0C0C0", "#CD7F32"]  # Gold, Silver, Bronze
    medal_emojis = ["🥇", "🥈", "🥉"]

    for i, (_, row) in enumerate(df_top3.head(3).iterrows()):
        with cols[i]:
            image_url = get_image_from_wikipedia(row['url']) if 'url' in row else None
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {medal_colors[i]}22 0%, {medal_colors[i]}44 100%);
                border: 2px solid {medal_colors[i]};
                border-radius: 20px;
                padding: 25px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.15);
                transition: transform 0.3s ease;
                margin-bottom: 20px;
            ">
                <div style="font-size: 48px; margin-bottom: 10px;">{medal_emojis[i]}</div>
                <h3 style="margin-bottom: 15px; color: white; font-weight: bold; text-align: center;">
                    {row['driver'] if 'driver' in row else row.get('constructor', 'Unknown')}
                </h3>
                {f'<img src="{image_url}" alt="Driver" style="width:120px; height:120px; border-radius: 60px; object-fit: cover; border: 3px solid {medal_colors[i]}; margin-bottom: 15px;" />' if image_url else ''}
                <div style="font-size: 28px; font-weight: bold; color: black;">
                    🏁 {row['wins']} Wins
                </div>
                <div style="font-size: 14px; color: #666; margin-top: 10px; text-align: center">
                    Position #{i+1}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            
def display_top3_constructors_cards(df_top3):
    """Generic card display for top 3 constructor winners."""
    st.markdown("## 🏆 Top 3 Constructor Winners")
    
    if df_top3.empty:
        st.info("No winner data available for this circuit.")
        return

    cols = st.columns(3)
    medal_colors = ["#FFD700", "#C0C0C0", "#CD7F32"]  # Gold, Silver, Bronze
    medal_emojis = ["🥇", "🥈", "🥉"]

    cols = st.columns(3)

    for i, (_, row) in enumerate(df_top3.head(3).iterrows()):
        with cols[i]:
            image_url = get_image_from_wikipedia(row['url']) if 'url' in row else None
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {medal_colors[i]}22 0%, {medal_colors[i]}44 100%);
                border: 2px solid {medal_colors[i]};
                border-radius: 20px;
                padding: 25px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.15);
                transition: transform 0.3s ease;
                margin-bottom: 20px;
            ">
                <div style="font-size: 48px; margin-bottom: 10px;">{medal_emojis[i]}</div>
                <h3 style="margin-bottom: 15px; color: white; font-weight: bold;">
                    {row['constructor'] if 'constructor' in row else row.get('constructor', 'Unknown')}
                </h3>
                {f'<img src="{image_url}" alt="Driver" style="width:120px; height:120px; border-radius: 60px; object-fit: cover; border: 3px solid {medal_colors[i]}; margin-bottom: 15px;" />' if image_url else ''}
                <div style="font-size: 28px; font-weight: bold; color: black;">
                    🏁 {row['wins']} Wins
                </div>
                <div style="font-size: 14px; color: #666; margin-top: 10px; text-align: center">
                    Position #{i+1}
                </div>
            </div>
            """, unsafe_allow_html=True)