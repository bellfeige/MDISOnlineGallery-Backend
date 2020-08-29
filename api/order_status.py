import json


def order_status_value(index):
    with open('api\orderStatus.json', 'r') as f:
        order_status = json.load(f)

    # for status in order_status:
    #     # print(status)
    #     print(status['Value'])
    #     print(status['Status'])

    if index <= 3:
        return order_status[index - 1]['Status']
    else:
        return ''

# print(order_status_value(2))
