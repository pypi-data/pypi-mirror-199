# Example Implementation

from streamlit_tile_grid.TileRenderer import TileGrid
from streamlit_tile_grid.DonutRenderer import DonutRenderer 
import streamlit as st
import plotly.graph_objects as go
import numpy as np

def app():
    st.set_page_config(layout="wide")
    st.sidebar.title("Streamlit Tile Grid")
    # Define the number of tiles and grid size
    num_tiles = 4

    # Add some widgets to the sidebar
    st.sidebar.header("Settings")
    tile_color = st.sidebar.color_picker("Tile Color", value="#61dafb")
    text_color = st.sidebar.color_picker("Text Color", value="#000")
    tile_shadow = st.sidebar.color_picker("Tile Shadow", value="#4398af")
    num_tiles = st.sidebar.number_input("Number of Tiles", min_value=1, max_value=20, value=num_tiles)

    title_list = ['Customer Lost Minutes', 'Precision <br> 99%', 'Retention Rate', 'Accuracy <br> 99%']
    body_list = ['97%', '', 'Retention rate measures the percentage of users ...', '']
    icon_list = ['bell', 'book', 'people', 'download']

    # Create the tile grid component and render it
    st.title('Tiles')
    tile_grid = TileGrid(num_tiles)
    tile_grid.render(title_list, body_list, icon_list, icon_size='1.5', tile_color=tile_color, tile_shadow=tile_shadow, text_color=text_color)

    donut_params = [
            {
                "percent": 69,
                "data": "3450 widgets",
                "color": f"aqua"
            },
            {
                "percent": 30,
                "data": "1500 widgets",
                "color": "#d9e021"
            },
            {
                "percent": 20,
                "data": "50 widgets",
                "color": "#ed1e79"
            },
                {
                "percent": 81,
                "data": "3450 widgets",
                "color": "purple"
            },
            {
                "percent": 45,
                "data": "1500 widgets",
                "color": "green"
            },
            {
                "percent": 20,
                "data": "50 widgets",
                "color": "red"
            },
            
        ]
    # Create the tile grid component and render it
    st.title('Donut Metrics')
    donut_grid = DonutRenderer()
    donut_grid.render(donut_params)

    # Add a line plot
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    fig = go.Figure(data=go.Scatter(x=x, y=y))
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    app()