import yfinance as yf
import streamlit as st
import pandas as pd
import time
from datetime import date

st.write("""
#   Stock Price & Data App
You can pick stock to know their price, volume and some financial data here. There is a S&P 500 selection list on the left side. You can also type your favorite stock below.  
""")


def show_data(selected_company):
        
    # define the ticker symbol
    tickerSymbol = selected_company

    # get data on this ticker
    tickerData = yf.Ticker(tickerSymbol)

    # get the historical prices for this ticker and update to current day
    tickerDf = tickerData.history(period='1d', start='2012-5-11', end=date.today())




    # create a dataframe that user select
    df = pd.DataFrame(columns=['Stock',
                            'Company',
                            'Industry',
                            'GrossMargins',
                            'ebitdaMargins',
                            'ProfitMargins',
                            'Beta',                        
                            'FullTimeEmployees'])


    # notify if someone type in wrong stock symbol
    try:
        # to find exact price
        def current_price(symbol):
            ticker = yf.Ticker(symbol)
            todays_data = ticker.history(period='5d')
            return todays_data['Close']

        # to find latest date
        def current_date(symbol):
            ticker = yf.Ticker(symbol)
            todays_data = ticker.history(period='5d')
            return todays_data.index[4]


        new_price = round(current_price(selected_company)[4],2)
        yesterday_prace = round(current_price(selected_company)[3],2)
        week_ago_price = round(current_price(selected_company)[0],2)
        day_difference_p = (new_price-yesterday_prace)/yesterday_prace
        week_difference_p = (new_price-week_ago_price)/week_ago_price
        day_difference = round(new_price-yesterday_prace ,2)


        # remove the timestamp
        new_date = current_date(selected_company).date()

        col1, col2, col3= st.columns(3)

        col1.metric("Stock price (USD) "+ str(new_date), new_price, day_difference)
        col2.metric("Change percentage(day)", '{: .2%}'.format(day_difference_p), '{: .2%}'.format(day_difference_p))
        col2.metric("Change persentage(week)", '{: .2%}'.format(week_difference_p), '{: .2%}'.format(week_difference_p))
        # col3.metric("Market cap(billion)", mc, mc_difference)


        st.line_chart(round(tickerDf.Close,2))
        st.line_chart(tickerDf.Volume, height = 1)

        st.markdown(f'<h1 style="color:#B8472F;font-size:24px;">{"recent news"}</h1>', unsafe_allow_html=True)

        title = []
        link = []

        # create news title and link
        for i in range(5):
            title.append(tickerData.news[i]['title'])
            link.append("[link]("+tickerData.news[i]['link']+")")

        for i, j in zip(title, link):
            st.write(f"{i} {j}")
        st.write('\n\n')

    except:
        st.write("THIS STOCK SYMBOL IS WRONG! PLEASE TYPE THE RIGHT SYMBOL")

@st.cache_data  # you don't have to load every time
def load_sp500(): # sp500
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    df = html[0]
    return df

 # nasdag
@st.cache_data
def load_nasdaq():
    url = "https://en.wikipedia.org/wiki/Nasdaq-100"
    html = pd.read_html(url, header = 0)
    df = html[4]
    return df

#dow jones
@st.cache_data
def load_dow():
    url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
    html = pd.read_html(url, header = 0)
    df = html[1]
    return df


def create_all_stock():
    df_sp500 = load_sp500()
    df_nasdaq = load_nasdaq()
    df_dow = load_dow()

    #create a list to give selection for sidebar
    sp500 = df_sp500['Symbol'].tolist()  # Use 'tolist()' to convert the column to a list
    dow = df_dow['Symbol'].tolist()
    nasdaq= df_nasdaq['Ticker'].tolist()


    all = dow + sp500 + nasdaq
    set_all= set(all)

    return list(set_all)


if __name__ == "__main__":


    # Create a list to give selection for sidebar
    all_company_list = create_all_stock()
    st.sidebar.header("user input")

    # Use st.sidebar.multiselect to create a multi-selection dropdown
    selected_stocks = st.sidebar.multiselect('Select SP500, Dow, Nasdaq Symbols', all_company_list)

    # Print the selected stocks for testing
    for i in range(len(selected_stocks)):
        selected_company = selected_stocks[i]
        # st.write('Selected Stocks:', selected_company)
        st.write('## The current company name is', selected_company)
        show_data(selected_company)
