from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from cb import get_c, get_data
from itertools import chain
import statistics




def forecasts(c_list):
    c_dict = {}
    for c in c_list:
        data = get_data(c.upper())
        rate = []
        for value in data:
            rate.append([value['rate']])

        x = rate[:7]
        y = rate[7:14]

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(x_train, y_train)
        predict = model.predict(x)

        predict_list = list(chain.from_iterable(predict))
        avg = statistics.mean(predict_list)
        value = round(min(predict_list, key=lambda num: abs(num - avg)), 2)

        c_dict[c] = [round(*rate[0], 2), value]

    return c_dict



def main():
    print(forecasts(get_c('https://finance.rambler.ru/currencies/')))

if __name__ == '__main__':
    main()


