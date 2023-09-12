import yfinance as yf
import pandas as pd
import datetime as dt
import time
import streamlit as st
import streamlit.components.v1 as components

# Set the display option to show 2 decimal places and 1000 rows
pd.set_option('display.float_format', '{:.2f}'.format)
st.set_page_config(page_title='TTM Squeeze Screener', page_icon=None, layout="wide")

# Initialize S&P500 Tickers
sp500 = [
    "MMM", "AOS", "ABT", "ABBV", "ACN", "ATVI", "ADM", "ADBE", "ADP", "AAP",
    "AES", "AFL", "A", "APD", "AKAM", "ALK", "ALB", "ARE", "ALGN", "ALLE",
    "LNT", "ALL", "GOOGL", "GOOG", "MO", "AMZN", "AMCR", "AMD", "AEE", "AAL",
    "AEP", "AXP", "AIG", "AMT", "AWK", "AMP", "ABC", "AME", "AMGN", "APH", "ADI",
    "ANSS", "AON", "APA", "AAPL", "AMAT", "APTV", "ACGL", "ANET", "AJG", "AIZ",
    "T", "ATO", "ADSK", "AZO", "AVB", "AVY", "AXON", "BKR", "BALL", "BAC", "BBWI",
    "BAX", "BDX", "WRB", "BBY", "BIO", "TECH", "BIIB", "BLK", "BK", "BA",
    "BKNG", "BWA", "BXP", "BSX", "BMY", "AVGO", "BR", "BRO", "BG", "CHRW",
    "CDNS", "CZR", "CPT", "CPB", "COF", "CAH", "KMX", "CCL", "CARR", "CTLT", "CAT",
    "CBOE", "CBRE", "CDW", "CE", "CNC", "CNP", "CDAY", "CF", "CRL", "SCHW", "CHTR",
    "CVX", "CMG", "CB", "CHD", "CI", "CINF", "CTAS", "CSCO", "C", "CFG", "CLX",
    "CME", "CMS", "KO", "CTSH", "CL", "CMCSA", "CMA", "CAG", "COP", "ED", "STZ",
    "CEG", "COO", "CPRT", "GLW", "CTVA", "CSGP", "COST", "CTRA", "CCI", "CSX",
    "CMI", "CVS", "DHI", "DHR", "DRI", "DVA", "DE", "DAL", "XRAY", "DVN", "DXCM",
    "FANG", "DLR", "DFS", "DIS", "DG", "DLTR", "D", "DPZ", "DOV", "DOW", "DTE",
    "DUK", "DD", "DXC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "ELV", "LLY",
    "EMR", "ENPH", "ETR", "EOG", "EPAM", "EQT", "EFX", "EQIX", "EQR", "ESS", "EL",
    "ETSY", "EG", "EVRG", "ES", "EXC", "EXPE", "EXPD", "EXR", "XOM", "FFIV", "FDS",
    "FICO", "FAST", "FRT", "FDX", "FITB", "FSLR", "FE", "FIS", "FI", "FLT", "FMC",
    "F", "FTNT", "FTV", "FOXA", "FOX", "BEN", "FCX", "GRMN", "IT", "GEHC", "GEN",
    "GNRC", "GD", "GE", "GIS", "GM", "GPC", "GILD", "GL", "GPN", "GS", "HAL", "HIG",
    "HAS", "HCA", "PEAK", "HSIC", "HSY", "HES", "HPE", "HLT", "HOLX", "HD", "HON",
    "HRL", "HST", "HWM", "HPQ", "HUM", "HBAN", "HII", "IBM", "IEX", "IDXX", "ITW",
    "ILMN", "INCY", "IR", "PODD", "INTC", "ICE", "IFF", "IP", "IPG", "INTU", "ISRG",
    "IVZ", "INVH", "IQV", "IRM", "JBHT", "JKHY", "J", "JNJ", "JCI", "JPM", "JNPR",
    "K", "KDP", "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KHC", "KR", "LHX",
    "LH", "LRCX", "LW", "LVS", "LDOS", "LEN", "LNC", "LIN", "LYV", "LKQ", "LMT",
    "L", "LOW", "LYB", "MTB", "MRO", "MPC", "MKTX", "MAR", "MMC", "MLM", "MAS",
    "MA", "MTCH", "MKC", "MCD", "MCK", "MDT", "MRK", "META", "MET", "MTD", "MGM",
    "MCHP", "MU", "MSFT", "MAA", "MRNA", "MHK", "MOH", "TAP", "MDLZ", "MPWR",
    "MNST", "MCO", "MS", "MOS", "MSI", "MSCI", "NDAQ", "NTAP", "NFLX", "NWL",
    "NEM", "NWSA", "NWS", "NEE", "NKE", "NI", "NDSN", "NSC", "NTRS", "NOC",
    "NCLH", "NRG", "NUE", "NVDA", "NVR", "NXPI", "ORLY", "OXY", "ODFL", "OMC",
    "ON", "OKE", "ORCL", "OGN", "OTIS", "PCAR", "PKG", "PANW", "PARA", "PH",
    "PAYX", "PAYC", "PYPL", "PNR", "PEP", "PFE", "PCG", "PM", "PSX", "PNW",
    "PXD", "PNC", "POOL", "PPG", "PPL", "PFG", "PG", "PGR", "PLD", "PRU",
    "PEG", "PTC", "PSA", "PHM", "QRVO", "PWR", "QCOM", "DGX", "RL", "RJF",
    "RTX", "O", "REG", "REGN", "RF", "RSG", "RMD", "RVTY", "RHI", "ROK",
    "ROL", "ROP", "ROST", "RCL", "SPGI", "CRM", "SBAC", "SLB", "STX",
    "SEE", "SRE", "NOW", "SHW", "SPG", "SWKS", "SJM", "SNA", "SEDG",
    "SO", "LUV", "SWK", "SBUX", "STT", "STLD", "STE", "SYK", "SYF",
    "SNPS", "SYY", "TMUS", "TROW", "TTWO", "TPR", "TRGP", "TGT", "TEL",
    "TDY", "TFX", "TER", "TSLA", "TXN", "TXT", "TMO", "TJX", "TSCO",
    "TT", "TDG", "TRV", "TRMB", "TFC", "TYL", "TSN", "USB", "UDR",
    "ULTA", "UNP", "UAL", "UPS", "URI", "UNH", "UHS", "VLO",
    "VTR", "VRSN", "VRSK", "VZ", "VRTX", "VFC", "VTRS", "VICI",
    "V", "VMC", "WAB", "WBA", "WMT", "WBD", "WM", "WAT", "WEC",
    "WFC", "WELL", "WST", "WDC", "WRK", "WY", "WHR", "WMB", "WTW",
    "GWW", "WYNN", "XEL", "XYL", "YUM", "ZBRA", "ZBH", "ZION", "ZTS"
]

# Define Squeeze Function and download data
@st.cache_data(ttl=3600)
def squeeze_screener(tickers):

  # start timer
  st = time.time()

  # Indicator parameters
  period = 20       # Indicator smoothing legth for BB and ATR
  atr_mult = 1.4    # ATR Multiplier for Keltner Channels
  bb_stdev = 2      # Std multiplier for BB

  # Download historical data for each ticker as a bulk package (MultiIndex df)
  print('Step 1. Downloading tickers')
  data = yf.download(tickers=tickers, period='200d')

  # For all tickers submitted, download historical stock data, and calculate
  # technical indiators using the parameters above
  print('Step 2. Processing data')
  squeeze_tickers = pd.DataFrame()

  for ticker in tickers:
    # Create a working dataframe for the active ticker. This transforms it to a Single Index df
    df = data.loc[:, (slice(None), ticker)].copy()
    df.columns = df.columns.droplevel(1)

    # Convert columns to lowercase for finta/TA
    df.columns = df.columns.str.lower()

    # Add ticker ID column. Calculate Average Volume
    df['ticker'] = ticker
    df['avg volume'] = df['volume'].rolling(len(df)).mean() / 1000000

    # Calculate Range and EMA. Needed for downstream calculations
    df['EMA'] = df['close'].ewm(span=period, adjust=False).mean()
    df['Range'] = df['high'] - df['low']
    df['ATR'] = df['Range'].ewm(span=period, adjust=False).mean()
    df['Std'] = df['close'].rolling(period).std()

    # Calculate BB for EMA
    df['BB Low'] = df['EMA'] - bb_stdev*df['Std']
    df['BB High'] = df['EMA'] + bb_stdev*df['Std']

    # Calculate Keltner for EMA. ATR is needed for this calc
    df['Keltner Low'] = df['EMA'] - atr_mult*df['ATR']
    df['Keltner High'] = df['EMA'] + atr_mult*df['ATR']

    # Calculate EMAs
    df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['EMA100'] = df['close'].ewm(span=100, adjust=False).mean()
    df['EMA200'] = df['close'].ewm(span=200, adjust=False).mean()

    # Determine if Squeeze TRUE or FALSE (Partial or Full)
    squeeze_on = (df['BB Low'] > df['Keltner Low']) | (df['BB High'] < df['Keltner High'])
    df['Squeeze'] = squeeze_on

    ### Initialized 'Condition' column (0 day, 1 day, or 2 day)
    df['Condition'] = None
    df['Trend'] = None

    # Condition = Multiple EMAs are stacked upwards or downward
    c1_up = (df['close'].iloc[-1] > df['EMA20'].iloc[-1]) and (df['EMA20'].iloc[-1] > df['EMA50'].iloc[-1]) and (df['EMA50'].iloc[-1] > df['EMA100'].iloc[-1]) and (df['EMA100'].iloc[-1] > df['EMA200'].iloc[-1])
    c1_down = (df['close'].iloc[-1] < df['EMA20'].iloc[-1]) and (df['EMA20'].iloc[-1] < df['EMA50'].iloc[-1]) and (df['EMA50'].iloc[-1] < df['EMA100'].iloc[-1]) and (df['EMA100'].iloc[-1] < df['EMA200'].iloc[-1])

    # Condition = Squeeze fired today (0 day prior)
    c2 = df['Squeeze'].iloc[-3]==True and df['Squeeze'].iloc[-2]==True and df['Squeeze'].iloc[-1]==False

    # Condition = Squeeze fired 1 day prior
    c3 = df['Squeeze'].iloc[-4]==True and df['Squeeze'].iloc[-3]==True and df['Squeeze'].iloc[-2]==False

    # Condition = Squeeze fired 2 day prior
    c4 = df['Squeeze'].iloc[-5]==True and df['Squeeze'].iloc[-4]==True and df['Squeeze'].iloc[-3]==False

    # Condition = Squeeze not yet fired (in accumulation for at least 2 days)
    c5 = df['Squeeze'].iloc[-1]==True and df['Squeeze'].iloc[-2]==True and df['Squeeze'].iloc[-3]==True

    if c1_up or c1_down:

      if c1_up:
        df.loc[df.index[-1], 'Trend'] = 'Up'
      else:
        df.loc[df.index[-1], 'Trend'] = 'Down'

      if c2 or c3 or c4 or c5:
        if c2:
          df.loc[df.index[-1], 'Condition'] = '0 day'
        elif c3:
          df.loc[df.index[-1], 'Condition'] = '1 day'
        elif c4:
          df.loc[df.index[-1], 'Condition'] = '2 day'
        elif c5:
          df.loc[df.index[-1], 'Condition'] = 'Accumulating'

        #print(f'{ticker}')
        squeeze_tickers = pd.concat([squeeze_tickers, df.iloc[[-1]]], axis=0)

  squeeze_tickers = squeeze_tickers.sort_values('avg volume', ascending=False)

  # Stop timer and report runtime
  et = time.time()
  res = et - st
  print('Execution time:', round(res/60,2), 'minutes')

  return squeeze_tickers
targets = squeeze_screener(sp500)
targets = targets.set_index('ticker')
targets = targets[['avg volume','close','Condition', 'Trend']].sort_values(by=['Condition','avg volume'], ascending=[True,False])
targets = targets[targets['avg volume'] >= 1]

# Streamlit Page Layout
col1, col2 = st.columns([2,1])
with col2:
    inner_col1, inner_col2 = st.columns([3,1])
    with inner_col1:
        st.table(targets)
    with inner_col2:
        view_ticker = st.radio('Ticker', options = targets.index)

# Tradingview embed
with col1:
  components.html(f'''
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
    <div id="tradingview_e049b"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget(
    {{
    "width": "100%",
    "height": 700,
    "symbol": "{view_ticker}",
    "interval": "D",
    "timezone": "America/Los_Angeles",
    "theme": "dark",
    "style": "9",
    "locale": "en",
    "enable_publishing": false,
    "withdateranges": true,
    "allow_symbol_change": true,
    "studies": [
        "STD;Bollinger_Bands",
        "STD;Keltner_Channels",
        "STD;MA%Ribbon"
    ],
    "hide_volume": true,
    "container_id": "tradingview_e049b"
    }}
    );
    </script>
    </div>
    <!-- TradingView Widget END -->
    ''', 
    height=700)
