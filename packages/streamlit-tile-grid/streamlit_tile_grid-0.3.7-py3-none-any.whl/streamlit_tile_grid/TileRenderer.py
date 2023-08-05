import streamlit as st
import pandas as pd
import numpy as np

class TileGrid:
    def __init__(self, num_tiles=4):
        self.num_tiles = num_tiles

    def render(self, title_list, body_list, icon_list=None, icon_size = '1.5', tile_color="#61dafb", tile_shadow="#4398af", text_color="#000"):
        """
        Renders the tile grid with the given parameters.

        Parameters:
        - title_list (list): A list of tile titles.
        - body_list (list): A list of tile bodies.
        - icon_list (list): A list of icon names (from Bootstrap Icons) to display in each tile.
                            Default is None, which displays no icon.
        - icon_size (str): The font size of the icon. Default is '1.5'.
        - tile_color (str): The background color of the tiles. Default is '#61dafb'.
        - tile_shadow (str): The color of the tile shadows. Default is '#4398af'.
        - text_color (str): The color of the text in the tiles. Default is '#000'.
        """
        # Define the HTML for the tile grid
        html = """
                <head>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css">
                </head>
                <div class='tile-grid'>
                """

        for i in range(self.num_tiles):
            # Define the HTML for each tile
            title = title_list[i] if i < len(title_list) else ""
            body = body_list[i] if i < len(body_list) else ""
            icon = f"<i class='bi-{icon_list[i]}' style='color:{text_color}; font-size: {icon_size}em;'></i><br>" if icon_list and i < len(icon_list) and icon_list[i] else ""
            tile_html = f"<div class='tile' ><h3 style='color:{text_color}'>{icon} {title}</h3><p style='color:{text_color}'>{body}</p></div>"
            html += tile_html
        html += "</div>"
        # Add the HTML to the Streamlit app
        st.markdown(html, unsafe_allow_html=True)

        css = f"""        
        <style>
        .tile-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 20px;
        }}

        .tile {{
            background-color: {tile_color};
            border: 1px solid #ccc;
            padding: 15px;
            box-shadow: 0 5px 10px {tile_shadow};
            border-radius: 5px;
            background: {tile_color};
            text-align: center;
            height: auto;
            padding: 30px 20px;
            overflow-y: auto;
        }}

        .tile:hover {{
            transform: scale(1.04);
        }}

        .bi {{
            display: inline-block;
            font-size: 1.5rem;
            line-height: 1;
            font-family: 'Glyphicons Halflings';
            font-weight: normal;
            font-style: normal;
            text-transform: none;
            test-align: justify;
            speak: none;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        </style>
        """

        st.markdown(css, unsafe_allow_html=True)


