from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("C:\\Users\\flavi\\Downloads\\ecommerce_estatistica.csv")


def cria_graficos(df):
    # Histograma de Notas


    fig1 = px.histogram(df['Nota'], x='Nota',nbins=10)
    fig1.update_layout(
    title='Histograma - Distribuição de Notas',
    xaxis_title='Nota',
    yaxis_title='Frequência'
    )
    fig2 = px.scatter(df, x=df['Preço'], y=df['Desconto'], color=df['Desconto'])
    fig2.update_layout(
        title = 'Dispersão: Preço dos produtos em relação à porcentagem de desconto',
        xaxis_title='Preço',
        yaxis_title='Porcentagem de Desconto'
    )
    df_corr = df[['Qtd_Vendidos_Cod', 'Preço', 'Marca_Cod', 'Desconto', 'N_Avaliações_MinMax']].corr()
    fig3 = px.imshow(df_corr, text_auto=True, aspect="auto", color_continuous_scale="Viridis", title="Mapa de calor da correlação da quantidade de itens vendidos com algumas variáveis")

    df1 = df.drop(df['Gênero'].index[[146]], axis=0)
    group_bar = df1.groupby(by="Gênero").size().reset_index(name="counts")

    fig4 = px.bar(group_bar, x="Gênero", y="counts", barmode="group", color_discrete_sequence=px.colors.qualitative.Bold, opacity = 1)
    fig4.update_layout(
        title='Divisão de itens por gênero',
        xaxis_title='Gênero',
        yaxis_title='Quantidade de itens',
        plot_bgcolor='rgba(222, 255, 253, 1)',
        paper_bgcolor='rgba(186, 245, 241, 1)'
    )

    df2 = df['Temporada']
    fig5 = px.pie(df2[ (df['Temporada'].str.len() <= 15) & (df['Temporada'].str.len() > 4)], names='Temporada', color='Temporada', hole=0.1, color_discrete_sequence=px.colors.sequential.RdBu)
    fig5.update_layout(title='Divisão de itens por temporada')

    fig6 = px.density_contour(df, df['Preço'])
    fig6.update_traces(contours_coloring="fill", contours_showlabels=True)
    fig6.update_layout(
        title='Densidade de Preços',
        xaxis_title='Preço'
    )

    fig7 = px.scatter(df, x='N_Avaliações', y='Qtd_Vendidos_Cod', trendline='ols', trendline_color_override='red')
    fig7.update_layout(
        title='Regressão de Vendas por Número de Avaliações',
        xaxis_title = 'Número de Avaliações',
        yaxis_title = 'Quantidade de itens vendidos'
    )

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7

def cria_app(df):

    app = Dash(__name__)

    fig1, fig2, fig3, fig4, fig5, fig6, fig7 = cria_graficos(df)

    app.layout = html.Div([
        html.H1("Gráficos para análise de e-commmerce"),
        html.Div('''
            Projeto EBAC
            '''),
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig3),
        dcc.Graph(figure=fig4),
        dcc.Graph(figure=fig5),
        dcc.Graph(figure=fig6),
        dcc.Graph(figure=fig7),
    ])
    return app
if __name__ == '__main__':
    app = cria_app(df)
    app.run_server(debug=True, port=8050)
