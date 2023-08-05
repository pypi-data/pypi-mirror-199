import streamlit as st

class DonutRenderer:
    def render(self, donut_params):
        """
        Render a set of donut charts using the provided parameters.

        Parameters
        ----------
        donut_params : list of dict
            A list of dictionaries, where each dictionary represents the parameters
            for a single donut chart. Each dictionary should have the following keys:
            - percent (float): the percentage of the donut chart to fill (between 0 and 100)
            - data (str): the data to display inside the donut chart
            - color (str): the color of the donut chart (in any valid CSS format)
        
        Example:
        --------
         params = [
                    {
                        "percent": 69,
                        "data": "3450 widgets",
                        "color": f"aqua"
                    },
                    {
                        "percent": 30,
                        "data": "1500 widgets",
                        "color": "#d9e021"
                    }
                    ]

        Returns
        -------
        Renders streamlit donuts
        """
        svg = """
                    <head>
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css">
                    </head>
                    <div id='donut-container'>
                    """
        for i, params in enumerate(donut_params):      
            svg += f"""
            <div class="svg-item">
            <svg width="100%" height="100%" viewBox="0 0 40 40" class="donut">
                <circle class="donut-hole" cx="20" cy="20" r="15.91549430918954" fill="#fff"></circle>
                <circle class="donut-ring" cx="20" cy="20" r="15.91549430918954" fill="transparent" stroke-width="3.5"></circle>
                <circle class="donut-segment donut-segment-{i+2}" cx="20" cy="20" r="15.91549430918954" fill="transparent" stroke-width="3.5" stroke-dasharray="{params['percent']} {100-params['percent']}" stroke-dashoffset="25"></circle>
                <g class="donut-text donut-text-{i+1}">
                <text y="50%" transform="translate(0, 2)">
                    <tspan x="50%" text-anchor="middle" class="donut-percent">{params['percent']}%</tspan>   
                </text>
                <text y="60%" transform="translate(0, 2)">
                    <tspan x="50%" text-anchor="middle" class="donut-data">{params['data']}</tspan>   
                </text>
                </g>
            </svg>
            </div>
            """
        svg += "</div>"
        
        st.markdown(svg, unsafe_allow_html=True)

        css = """
        #donut-container {
            display: flex;
            justify-content: center;
        }
        .svg-item {
            width: 100%;
            font-size: 16px;
            margin: 0 auto;
            animation: donutfade 1s;
        }

        .svg-item:hover {
            transform: scale(1.04);
            animation: donut{i+1} 1s ease-in-out forwards;
        }

        @keyframes donutfade {
        /* this applies to the whole svg item wrapper */
            0% {
                opacity: .2;
            }
            100% {
                opacity: 1;
            }
        }

        @media (min-width: 992px) {
            .svg-item {
                width: 80%;
            }
        }

        .donut-ring {
            stroke: #EBEBEB;
        }

        .donut-text {
        font-family: Arial, Helvetica, sans-serif;
        fill: #FF6200;
        }

        .donut-percent {
            font-size: 0.5em;
            line-height: 1;
            transform: translateY(0.5em);
            font-weight: bold;
        }

        .donut-data {
            font-size: 0.12em;
            line-height: 1;
            transform: translateY(0.5em);
            text-align: center;
            text-anchor: middle;
            color:#666;
            fill: #666;
            animation: donutfadelong 1s;
        }
        """

        for i, params in enumerate(donut_params):
            css += f"""
            .donut-segment-{i+2} {{
                transform-origin: center;
                stroke: {params['color']};
                animation: donut{i+1} 1s ease-in-out forwards;
            }}

            .donut-text-{i+1} {{
                fill: {params['color']};
            }}

            .segment-{i+1} {{
                fill: {params['color']};
            }}

            @keyframes donut{i+1} {{
                0% {{
                    stroke-dasharray: 0, 100;
                }}
                100% {{
                    stroke-dasharray: {params['percent']}, {100-params['percent']};
                    }}
                }}

            .donut-text-{i+1} {{
            fill: {params['color']};
            }}
            """

        # Render the CSS
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
