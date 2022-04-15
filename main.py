#!/usr/bin/env python3
import httpx
import csv


cro_address = "INSERT ADDRESS"

# conversion from base_cro to cro
base_cro = 100000000

def main():
    base_url = "https://crypto.org/explorer/api/v1/accounts/%s/transactions" % cro_address

    headers = ["Date and Time", "Transaction Type", "Sent Quantity", "Sent Currency", "Sending Source", "Received Quantity","Received Currency", "Receiving Destination", "Fee", "Fee Currency", "Exchange Transaction ID", "Blockchain Transaction Hash"]
    # transaction_types = ["Buy","Sale", "Trade", "Transfer in", "Transfer out", "Income", "Expense", "Gifts"]

    q = {
        "pagination": "offset", 
        "page": 1,
        "limit": 10,
        "order": "height.desc"
        }

    r = httpx.get(base_url, params=q)

    if r.status_code == httpx.codes.OK:
        resp = r.json()

        num_pages = resp['pagination']['total_page']
        # create the output csv
        with open('eggs.csv', 'w', newline='') as csvfile:
            # write the headers
            transactions = csv.writer(csvfile)
            transactions.writerow(headers)

            # write the first response
            write_transactions(resp, transactions)
            # transactions.writerow(getrowdata(resp))

            for page in range(2, num_pages + 1):
                # retrieve the next page
                q['page'] = page
                r = httpx.get(base_url, params=q)
                resp = r.json()

                # write the data to csv
                write_transactions(resp, transactions)
                # transactions.writerow(getrowdata(resp))


                # for result in resp['result']:
                #     print(result['messageTypes'])
                    # print(resp['result'][0]['blockHeight'])

def write_transactions(resp, transactions=csv.writer):
    row = [None] * 12
    for result in resp['result']:
        row[0] = result['blockTime']
        if row[0] == '2022-01-22T15:21:55.572562012Z':
            print(row)
        fee = int(result['fee'][0]['amount']) / base_cro
        # txid = result['']


        # Available TaxBit transaction types
        #  "Buy","Sale", "Trade", "Transfer in", "Transfer out", "Income", "Expense", "Gifts"
        for message in result['messages']:
            if message['type'] == 'MsgSend':
                if message['content']['toAddress'] == cro_address:
                    row[1] = "Transfer In"
                    # recieved quantity
                    row[5] = int(message['content']['amount'][0]['amount']) / base_cro
                    # received currency
                    row[6] = 'CRO'
                    # recieving destination
                    row[7] = 'Crypto.com DeFi'
                    row[8] = fee
                    row[9] = 'CRO'
                    row[10] = message['content']['uuid']
                    row[11] = message['content']['txHash']
                else:
                    row[1] = "Transfer Out"
                    # sent quantity
                    row[2] = int(message['content']['amount'][0]['amount']) / base_cro
                    row[3] = 'CRO'
                    row[4] = 'Crypto.com DeFi'
                    row[8] = fee
                    row[9] = 'CRO'
                    row[10] = message['content']['uuid']
                    row[11] = message['content']['txHash']
            elif message['type'] == 'MsgDelegate':
                if int(message['content']['autoClaimedRewards']['amount']) > 0:
                    row[1] = "Income"
                    # recieved quantity
                    row[5] = int(message['content']['autoClaimedRewards']['amount']) / base_cro
                    # received currency
                    row[6] = 'CRO'
                    # recieving destination
                    row[7] = 'Crypto.com DeFi'
                    # row[8] = fee
                    # row[9] = 'CRO'
                    row[10] = message['content']['uuid']
                    row[11] = message['content']['txHash']
                else:
                    continue
            elif message['type'] == 'MsgUndelegate':
                return
            elif message['type'] == 'MsgWithdrawDelegatorReward':
                row[1] = "Income"
                # recieved quantity
                row[5] = int(message['content']['amount'][0]['amount']) / base_cro
                # received currency
                row[6] = 'CRO'
                # recieving destination
                row[7] = 'Crypto.com DeFi'
                # row[8] = fee
                # row[9] = 'CRO'
                row[10] = message['content']['uuid']
                row[11] = message['content']['txHash']
            elif message['type'] == 'MsgBeginRedelegate':
                continue
            
            transactions.writerow(row)

# headers = ["Date and Time", 
# "Transaction Type", "Sent Quantity", "Sent Currency", 
# "Sending Source", "Received Quantity","Received Currency", 
# "Receiving Destination", "Fee", "Fee Currency", 
# "Exchange Transaction ID", "Blockchain Transaction Hash"]


    try:
        resp['result']
    except:
        exit(1)

if __name__ == "__main__":
    main()
