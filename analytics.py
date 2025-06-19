import os
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np

def generate_performance_chart(submissions, chart_type='line'):
    """
    Генерируем график успеваемости на основе отправленных решений.
    
    Args:
        submissions (list): Список отправленных решений
        chart_type (str): Тип графика ('line', 'bar', 'pie')
        
    Returns:
        str: HTML-код графика или Base64-закодированное изображение
    """
    if not submissions:
        return None
    
    # Группировка данных по датам
    dates = [sub.date_submitted for sub in submissions]
    results = [1 if sub.result == 'Passed' else 0 for sub in submissions]
    
    # Создаем временной ряд
    data = {}
    for date, result in zip(dates, results):
        date_key = date.strftime('%Y-%m-%d')
        if date_key not in data:
            data[date_key] = {'total': 0, 'passed': 0}
        data[date_key]['total'] += 1
        if result:
            data[date_key]['passed'] += 1
    
    # Сортировка дат
    sorted_dates = sorted(data.keys())
    
    # Расчет процента успеха
    success_rates = [data[date]['passed'] / data[date]['total'] * 100 for date in sorted_dates]
    
    if chart_type == 'line':
        # Создание графика с plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=sorted_dates, 
            y=success_rates,
            mode='lines+markers',
            name='Процент успешных решений',
            line=dict(color='#2ecc71', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Динамика успеваемости',
            xaxis_title='Дата',
            yaxis_title='Процент успешных решений (%)',
            template='plotly_dark',
            yaxis=dict(range=[0, 100]),
            height=500
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    elif chart_type == 'bar':
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=sorted_dates,
            y=[data[date]['passed'] for date in sorted_dates],
            name='Успешные решения',
            marker_color='#2ecc71'
        ))
        fig.add_trace(go.Bar(
            x=sorted_dates,
            y=[data[date]['total'] - data[date]['passed'] for date in sorted_dates],
            name='Неуспешные решения',
            marker_color='#e74c3c'
        ))
        
        fig.update_layout(
            title='Количество успешных и неуспешных решений по дням',
            xaxis_title='Дата',
            yaxis_title='Количество решений',
            barmode='stack',
            template='plotly_dark',
            height=500
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    elif chart_type == 'pie':
        # Суммарная статистика для круговой диаграммы
        total_passed = sum(data[date]['passed'] for date in sorted_dates)
        total_failed = sum(data[date]['total'] - data[date]['passed'] for date in sorted_dates)
        
        fig = go.Figure(data=[go.Pie(
            labels=['Успешные решения', 'Неуспешные решения'],
            values=[total_passed, total_failed],
            marker=dict(colors=['#2ecc71', '#e74c3c']),
            hole=.3
        )])
        
        fig.update_layout(
            title='Общая статистика решений',
            template='plotly_dark',
            height=500
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    return None

def generate_difficulty_distribution(assignments, submissions):
    """
    Генерируем график распределения успеваемости по уровням сложности.
    
    Args:
        assignments (list): Список заданий
        submissions (list): Список отправленных решений
        
    Returns:
        str: HTML-код графика
    """
    if not assignments or not submissions:
        return None
    
    # Создаем словарь для маппинга заданий и их сложности
    assignment_difficulty = {a.id: a.difficulty for a in assignments}
    
    # Группируем данные по сложности
    difficulty_data = defaultdict(lambda: {'total': 0, 'passed': 0})
    
    for sub in submissions:
        difficulty = assignment_difficulty.get(sub.assignment_id, 'Unknown')
        difficulty_data[difficulty]['total'] += 1
        if sub.result == 'Passed':
            difficulty_data[difficulty]['passed'] += 1
    
    # Преобразуем данные для графика
    difficulties = list(difficulty_data.keys())
    success_rates = [difficulty_data[d]['passed'] / difficulty_data[d]['total'] * 100 
                    if difficulty_data[d]['total'] > 0 else 0 for d in difficulties]
    
    # Создаем цветовую схему: зеленый для легких, желтый для средних, красный для сложных
    colors = {
        'Easy': '#2ecc71',  # Зеленый
        'Medium': '#f39c12',  # Желтый
        'Hard': '#e74c3c',  # Красный
        'Unknown': '#95a5a6'
    }
    
    bar_colors = [colors.get(d, '#95a5a6') for d in difficulties]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=difficulties,
        y=success_rates,
        marker_color=bar_colors,
        text=[f"{rate:.1f}%" for rate in success_rates],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='Процент успешных решений по уровням сложности',
        xaxis_title='Уровень сложности',
        yaxis_title='Процент успешных решений (%)',
        template='plotly_dark',
        yaxis=dict(range=[0, 100]),
        height=500
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def generate_topic_performance(assignments, submissions):
    """
    Генерируем тепловую карту успеваемости по разным темам.
    
    Args:
        assignments (list): Список заданий
        submissions (list): Список отправленных решений
        
    Returns:
        str: HTML-код тепловой карты
    """
    if not assignments or not submissions:
        return None
    
    # Извлекаем темы из названий заданий
    topics = {}
    for a in assignments:
        # Примитивное определение темы - берем первое слово из названия
        topic = a.title.split()[0] if a.title else 'Unknown'
        topics[a.id] = topic
    
    # Группируем данные по темам
    topic_data = defaultdict(lambda: {'total': 0, 'passed': 0})
    
    for sub in submissions:
        topic = topics.get(sub.assignment_id, 'Unknown')
        topic_data[topic]['total'] += 1
        if sub.result == 'Passed':
            topic_data[topic]['passed'] += 1
    
    # Отбираем  темы с достаточным количеством данных
    significant_topics = {t: data for t, data in topic_data.items() if data['total'] >= 3}
    
    if not significant_topics:
        return None
    
    # Создаем таблицу для тепловой карты
    topic_list = list(significant_topics.keys())
    success_rates = [significant_topics[t]['passed'] / significant_topics[t]['total'] * 100 
                    for t in topic_list]
    
    fig = go.Figure(data=go.Heatmap(
        z=[success_rates],
        x=topic_list,
        y=['Успеваемость'],
        colorscale='RdYlGn',  # Красный -> Желтый -> Зеленый
        zmin=0,
        zmax=100,
        text=[[f"{rate:.1f}%" for rate in success_rates]],
        texttemplate="%{text}",
        textfont={"size":14}
    ))
    
    fig.update_layout(
        title='Тепловая карта успеваемости по темам',
        template='plotly_dark',
        height=400
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')