import streamlit as st
import pandas as pd
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config(layout='wide')  # Configura a página para layout alongado

# imagem de cabeçalho
cabecalho = Image.open('header.png')
st.image(cabecalho, use_column_width='always')

# título do app
logo_app = Image.open('app.png')
st.image(logo_app, use_column_width='false')

# layout do app
col1, col2 = st.beta_columns(2)  # Laoyout de duas colunas

# Ingestao de dados para o mapa
df1 = pd.read_csv("Ubs_reg_gyn.csv")

# Variavéis com os nomes das doencas escolhidas para serem atribuídos pesos (escopo global)
covid_19 = 0
gripe = 0
asma = 0

def mapa_test(df1): # Funcao que constroe o mapa
    test_map = folium.Map(location= [df1['latitude'].mean(),df1['longitude'].mean()], default_zoom_start=5)

    for i in range(0, len(df1)):
        folium.Marker(
            location=[df1.iloc[i]['latitude'], df1.iloc[i]['longitude']],
            popup=df1.iloc[i][['nome.1', 'telefone']],
        ).add_to(test_map)

    folium_static(test_map)
    return None
#Sintomas
with col1:
    # Imagem instrucao
    instrucoes = Image.open('instrucoes.png')
    st.image(instrucoes, use_column_width='auto')

    # Checkbox excludentes para a gripe e asma
    checkcontato = st.checkbox("Teve contato nos últimos 15 dias com pessoas que deram positivo para Covid-19?")
    check_arpulmoes = st.checkbox("Está com dificuldade de encher os pulmoes de ar?")
    check_far = st.checkbox("Está com falta de ar?")
    check_paladar = st.checkbox("Teve ou está com perda de olfato ou paladar?")
    check_sintomasincomuns = st.checkbox(
        "Teve algum desses sintomas: diarréia, conjuntivite, erupção na pele, descoloração nos dedos das mãos ou pés?")
    check_pfala = st.checkbox("Teve ou está com perda da fala ou algum movimento?")

   # Checkboxes nao excluentes
    checkfebre = st.checkbox("Teve ou está com febre?")
    if checkfebre:
        covid_19 += .5
        gripe += .5
        asma += 0

    checktosseseca= st.checkbox("Teve ou está com Tosse seca?")
    if checktosseseca:
        covid_19 += .5
        gripe += 0
        asma += .5

    checktossenormal = st.checkbox("Teve ou está com Tosse normal?")
    if checktossenormal:
        covid_19 += 0
        gripe += 1
        asma += 0

    check_dgarganta = st.checkbox("Teve ou está com dor de garganta?")
    if check_dgarganta:
        covid_19 += .5
        gripe += .5
        asma += 0

    check_dmuscular = st.checkbox("Teve ou está com dor muscular principalmente nas costas ou pernas?")
    if check_dmuscular:
        covid_19 += .4
        gripe += .6
        asma += 0

    check_dcabeca = st.checkbox("Teve ou está com dor de cabeça?")
    if check_dcabeca:
        covid_19 += .3
        gripe += .7
        asma += 0

    check_espirros = st.checkbox("Está espirrando, com nariz escorrendo e sentindo calafrios?")
    if check_espirros:
        covid_19 += 0
        gripe += 1
        asma += 0

    check_cansado = st.checkbox("Está com um cansaço maior do que o normal?")
    if check_cansado:
        covid_19 += .32
        gripe += .35
        asma += .33

    check_dpeito = st.checkbox("Teve ou está com dor ou pressão no peito?")
    if check_dpeito:
        covid_19 += .5
        gripe += 0
        asma += .5

    check_chiado = st.checkbox("Teve ou está com chiado ou ruído característico ao respirar?")
    if check_chiado:
        covid_19 += 0
        gripe += .2
        asma += .8

# Resultados
with col2:
    # Primeiro if testa se nao foi marcado algum sintoma que confirma a necessidade de teste
    # se for True Faz o Teste!

    if (checkcontato == True) or (check_pfala == True) or (check_arpulmoes == True) or (check_far == True) or (
            check_paladar == True) or (check_sintomasincomuns == True):
        teste = Image.open('teste.png')
        st.image(teste, use_column_width='false')

        st.header('No mapa abaixo você pode saber onde fazer o teste pelo SUS em Goiânia, ' \
                  'Aparecida de Goiânia e Senador Canedo')
        st.header('Caso você não esteja em uma dessas cidades , clique na caixinha abaixo do mapa, será  ' \
                  'mostrado um quadro com todas as cidades do estado de Goiás que fazem o teste pelo SUS.')
        mapa_test(df1)
        checkcidades = st.checkbox(
            'Não está em Goiânia, Aparecida de Goiânia ou Senador Canedo? Clique e veja se sua cidade está fazendo o teste')
        if checkcidades:
            lst_cidades = Image.open('lista_cidades.png')
            st.image(lst_cidades, caption='https://www.saude.go.gov.br/coronavirus/dadosdobem', use_column_width='always')

    # Se a condicao for falsa passa a atribuir pesos para checks marcados
    else:
        if covid_19 == 0 and asma == 0 and gripe == 0: # Se True informa ao usuário que está aguardando sintomas
            info = Image.open('info.png')
            st.image(info, use_column_width='false')

            info_covid = Image.open('info_covid.png')
            st.image(info_covid, caption='paho.org', use_column_width='always')
        else:
            if (gripe <= covid_19 >= asma) and covid_19 != 0: #Se True Faz o Teste!
                teste = Image.open('teste.png')
                st.image(teste, use_column_width='false')

                st.header('No mapa abaixo você pode saber onde fazer o teste pelo SUS em Goiânia, '\
                          'Aparecida de Goiânia e Senador Canedo')
                st.header('Caso você não esteja em uma dessas cidades , abaixo está um quadro com todas as cidades '\
                          'do estado de Goiás que fazem o teste pelo SUS.')
                mapa_test(df1)
                checkcidades = st.checkbox('Não está em Goiânia, Aparecida de Goiânia ou Senador Canedo? Clique e veja se sua cidade está fazendo o teste')
                if checkcidades:
                    lst_cidades = Image.open('lista_cidades.png')
                    st.image(lst_cidades, caption='https://www.saude.go.gov.br/coronavirus/dadosdobem', use_column_width='always')
            elif (covid_19 < gripe > asma) and gripe != 0:
                gripe_img = Image.open('gripe.png') # Se for True descarta a necessidade de teste
                st.image(gripe_img, use_column_width='false')
                st.header('Pelo sintomas apresentados no momento não é preciso fazer o teste COVID-19' \
                          ', porém se você teve contato com pessoas que testaram positivo para o ' \
                          'COVID-19 ou se chegou de viagem recentemente é recomendado ' \
                          'que se faça o teste.')
                prev_covid = Image.open('prevencao_covid.png')
                st.image(prev_covid, caption='https://www.princesa.pb.gov.br/', use_column_width='always')
            else:
                asma_img = Image.open('asma.png')  # Se for True descarta a necessidade de teste
                st.image(asma_img, use_column_width='false')
                st.header('Pelo sintomas apresentados no momento não é preciso fazer o teste COVID-19' \
                          ', porém se você teve contato com pessoas que testaram positivo para o ' \
                          'COVID-19 ou se chegou de viagem recentemente é recomendado ' \
                          'que se faça o teste.')
                prev_covid = Image.open('prevencao_covid.png')
                st.image(prev_covid, caption='https://www.princesa.pb.gov.br/', use_column_width='always')

st.text('Desenvolvido por Robison Nunes, Pedro Luna, Christiano de Oliveira - Abril/2021')
