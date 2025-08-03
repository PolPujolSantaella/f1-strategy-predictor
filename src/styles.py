import streamlit as st 

def load_css():
    st.markdown("""
    <style>
    /* CSS Variables - F1 Inspired Colors */
    :root {
        --primary-color: #FF1801;
        --primary-hover: #E31500;
        --secondary-color: #1A1A40;
        --accent-color: #FFD700;
        --accent-secondary: #C0392B;
        --bg-color: #FFFFFF;
        --bg-secondary: #F8F9FA;
        --text-color: #2C3E50;
        --text-light: #7F8C8D;
        --card-bg: #FFFFFF;
        --border-color: #E9ECEF;
        --shadow-light: rgba(0, 0, 0, 0.08);
        --shadow-medium: rgba(0, 0, 0, 0.12);
        --shadow-strong: rgba(0, 0, 0, 0.2);
        --gradient-primary: linear-gradient(135deg, var(--primary-color), var(--accent-secondary));
        --gradient-secondary: linear-gradient(135deg, #f8f9fa, #e9ecef);
        --gradient-accent: linear-gradient(45deg, var(--accent-color), #F39C12);
    }
    
    /* Reset and Base Styles */
    * {
        box-sizing: border-box;
    }
    
    .main {
        padding-top: 1rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        backgorund: black;
    }
    
    /* Typography Improvements */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        font-weight: 600;
        line-height: 1.2;
        margin-bottom: 1rem;
    }
    
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 2rem 5rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 10px 40px var(--shadow-medium);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M0 0h100v100H0z" fill="none"/><path d="M0 50h100" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></svg>');
        pointer-events: none;
    }
    
    .main-header h1 {
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 800;
        margin-bottom: 0.8rem;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
        letter-spacing: 1px;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: clamp(1rem, 2.5vw, 1.3rem);
        opacity: 0.95;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* Sidebar Enhanced Styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: var(--gradient-primary);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: var(--gradient-primary);
        border-right: 3px solid var(--accent-color);
    }
    
    .sidebar-title {
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
        margin: 2rem 0;
        color: white;
        text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.5);
        letter-spacing: 1px;
    }
    
    /* Enhanced Radio Buttons */
    .stRadio > div {
        background: rgba(200, 255, 255, 0.15);
        border-radius: 15px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        margin-left: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .stRadio > div:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateX(5px);
    }
    
    .stRadio label {
        font-size: 5.2rem !important;
        font-weight: 700 !important; 
        color: white !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Enhanced Cards & Containers */
    .stat-card {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 30px var(--shadow-light);
        border: 1px solid var(--border-color);
        border-left: 6px solid var(--primary-color);
        margin: 1.5rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: var(--gradient-accent);
        opacity: 0.05;
        border-radius: 50%;
        transform: translate(30px, -30px);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px var(--shadow-medium);
    }
    
    /* Driver Info Enhanced */
    .driver-info {
        background: var(--gradient-secondary);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px var(--shadow-medium);
        border: 1px solid var(--border-color);
        overflow: hidden;
        margin-bottom: 1.5rem;
    }

    .driver-info::after {
        content: '🏎️';
        position: absolute;
        top: 10px;
        right: 20px;
        font-size: 2rem;
        opacity: 0.08;
    }

    .driver-name {
        font-size: clamp(1.5rem, 3vw, 2.5rem);
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.2rem;
        text-align: center;
        letter-spacing: 1.5px;
    }

    .driver-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }

    .detail-item {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 12px var(--shadow-light);
        border-left: 3px solid var(--accent-color);
        transition: all 0.2s ease;
    }

    .detail-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px var(--shadow-medium);
    }

    .detail-label {
        font-weight: 700;
        color: var(--text-light);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }

    .detail-value {
        font-size: 1.1rem;
        color: var(--primary-color);
        font-weight: 500;
        line-height: 1.2;
    }
    
    /* Enhanced Metrics */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
        padding: 0.25rem 0.25rem;
    }
    
    .metric-box {
        background: white;
        padding: 0.75rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 30px var(--shadow-light);
        border-top: 5px solid var(--primary-color);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: var(--gradient-primary);
    }
    
    .metric-box:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px var(--shadow-medium);
    }
    
    .metric-number {
        font-size: 3rem;
        font-weight: 900;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: block;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-color);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(255, 24, 1, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 24, 1, 0.4);
        background: var(--primary-hover);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Enhanced Select Box */
    .stSelectbox > div > div {
        border-radius: 15px;
        border: 2px solid var(--border-color);
        transition: all 0.3s ease;
        background: black;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 4px rgba(255, 24, 1, 0.1);
        transform: translateY(-2px);
    }
    
    /* Enhanced Alerts */
    .stAlert {
        border-radius: 15px;
        border: none;
        padding: 1.5rem;
        font-weight: 500;
        box-shadow: 0 4px 15px var(--shadow-light);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        border-left: 5px solid #2196f3;
        color: #1565c0;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2);
        border-left: 5px solid #ff9800;
        color: #ef6c00;
    }
    
    .stError {
        background: linear-gradient(135deg, #ffebee, #ffcdd2);
        border-left: 5px solid #f44336;
        color: #c62828;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
        border-left: 5px solid #4caf50;
        color: #2e7d32;
    }
    
    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: var(--bg-secondary);
        padding: 0.5rem;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: var(--text-color);
        font-weight: 600;
        padding: 1rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--gradient-primary);
        color: white;
        box-shadow: 0 4px 15px rgba(255, 24, 1, 0.3);
    }
    
    /* Spinner Enhancement */
    .stSpinner > div {
        border-top-color: var(--primary-color);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: var(--gradient-primary);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            padding: 2rem 1rem;
        }
        
        .main-header h1 {
            font-size: 2.5rem;
        }
        
        .driver-name {
            font-size: 2.5rem;
        }
        
        .metric-container {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        }
        
        .driver-details {
            grid-template-columns: 1fr;
        }
        
        .stat-card {
            padding: 1.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .driver-name {
            font-size: 2rem;
        }
        
        .metric-number {
            font-size: 2.5rem;
        }
        
        .stat-card {
            padding: 1rem;
        }
    }
    
    /* Enhanced Animations */
    @keyframes fadeInUp {
        from { 
            opacity: 0; 
            transform: translateY(30px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    @keyframes slideInRight {
        from { 
            opacity: 0; 
            transform: translateX(30px); 
        }
        to { 
            opacity: 1; 
            transform: translateX(0); 
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .stat-card, .driver-info, .metric-box {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .detail-item {
        animation: slideInRight 0.6s ease-out;
        animation-fill-mode: both;
    }
    
    .detail-item:nth-child(1) { animation-delay: 0.1s; }
    .detail-item:nth-child(2) { animation-delay: 0.2s; }
    .detail-item:nth-child(3) { animation-delay: 0.3s; }
    .detail-item:nth-child(4) { animation-delay: 0.4s; }
    
    /* Loading States */
    .loading-shimmer {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    /* Smooth Scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--gradient-primary);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-hover);
    }
    
    /* Focus States for Accessibility */
    button:focus, select:focus, input:focus {
        outline: 3px solid rgba(255, 24, 1, 0.3);
        outline-offset: 2px;
    }
    
    /* Print Styles */
    @media print {
        .main-header {
            background: white !important;
            color: black !important;
            box-shadow: none !important;
        }
        
        .stat-card, .driver-info, .metric-box {
            box-shadow: none !important;
            border: 1px solid #ccc !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)