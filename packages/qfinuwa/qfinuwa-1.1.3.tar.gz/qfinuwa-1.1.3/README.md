# QFIN's Algorithmic Backtester (QFAB)

## Setup

To install on your system, use pip:

```
pip install qfinuwa
```

## API


## Strategy

You strategy can be initialised as follows:

```py

class MyCustomStrategy(Strategy):
  
    def __init__(self):
        return
        
    def on_data(self, data, indicators, portfolio):
        return

```

Any hyperparameters you want to add to your model you can do in ``__init__``.


### on_data

``on_data`` takes in data and indicators which are both type ``dict``, keyed by the stocks. The portfolio class manages buying and selling stocks. 

### Indicators

To add an indicator to be passed into ``on_data`` during evalutation, define a new function in your strategy class that takes in data and returns a data column of the same length.

```py
# super bad example I need to change this
class MyCustomStrategy(Strategy):
  
    def __init__(self):
        return
        
    def on_data(self, data, indicators, portfolio):
        return

    @Strategy.indicator
    def vol_difference(data):
        return data['volume'].diff() + addition
```

In the above example we added an indicator called ``"vol_difference"`` that can be accessed during execution by 

```py
        
    def on_data(self, data, indicators, portfolio):

        V = indicators["vol_difference"]

        return
```

We can also add parameters to the indicator and strategy itself, but we'll see that later.

## Backtester 

The ``Backtester`` class runs backtests given the inputs:
- An strategy to test
- Data to test it on
- Hyperparameters for the strategy including
  - Strategy Hyperparameters
  - Indicator Hyperparameters
- Starting Balance and Fee
- Evaluation time

A backtester can be initialised like so:

```py
backtester = Backtester(['AAPL', 'GOOG'])
```

You can pass in your strategy when initialising, or later.

```py
backtester = Backtester(['AAPL', 'GOOG'], strategy=MyCustomStrategy)
```

TODO finish this section.

## Additional Info


### Time Scaling 

![Time scaling of Backtester.__init__](./imgs/__init__.png?raw=true)

![Time scaling of Backtester.run](./imgs/run.png?raw=true)