import yfinance as yf
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
import models 
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import uvicorn
from pydantic import BaseModel
from models import Stock


PORT = '8080'

app = FastAPI() 

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory='templates')


class StockRequest(BaseModel):
    symbol: str


def get_db():
    try:
       db = SessionLocal() 
       yield db
    finally:
       db.close() 



@app.get("/")
def home(request: Request, forward_pe = None, dividend_yield = None, ma50 = None, ma200 = None, db: Session = Depends(get_db)):
    """
    show all stocks in the database and button to add more
    button next to each stock to delete from database
    filters to filter this list of stocks
    button next to each to add a note or save for later
    """

    stocks = db.query(Stock)

    if forward_pe:
        stocks = stocks.filter(Stock.forward_pe < forward_pe)

    if dividend_yield:
        stocks = stocks.filter(Stock.dividend_yield > dividend_yield)
    
    if ma50:
        stocks = stocks.filter(Stock.price > Stock.ma50)
    
    if ma200:
        stocks = stocks.filter(Stock.price > Stock.ma200)
    
    stocks = stocks.all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "stocks": stocks, 
        "dividend_yield": dividend_yield,
        "forward_pe": forward_pe,
        "ma200": ma200,
        "ma50": ma50
    })

def fetch_stock_data(id: int):
    db = SessionLocal()
    stock = db.query(Stock).filter(Stock.id == id).first()
    yahoo_data = yf.Ticker(stock.symbol)

    stock.ma200 = yahoo_data.info['twoHundredDayAverage']
    stock.ma50 = yahoo_data.info['fiftyDayAverage']
    stock.price = yahoo_data.info['previousClose']
    stock.forward_pe = yahoo_data.info['forwardPE']
    stock.forward_eps = yahoo_data.info['forwardEps']
    stock.dividend_yield = (yahoo_data.info['dividendYield'] or 1) * 100
    db.add(stock)
    db.commit()

@app.post("/stock")
async def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    add one or more tickers to the database
    background task to use yfinance and load key statistics
    """

    stock = Stock()
    print(stock_request.symbol)
    stock.symbol = stock_request.symbol
    db.add(stock)
    db.commit()

    background_tasks.add_task(fetch_stock_data, stock.id)

    return {
        "code": "success",
        "message": "stock was added to the database"
    }   
# example



@app.get("/jinja")
def jinjaa(request: Request):
    """
    displays the stock screener dashboard / homepage
    """
    return templates.TemplateResponse('example_jinja.html', {
        "request" : request, 
        "somevar" : 2
        })

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), reload=True, debug=True, workers=2)
