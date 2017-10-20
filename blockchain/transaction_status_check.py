from qtum_cli import qtum_cli as qcli


def transaction_check(transaction, wallet):
    for vin_transaction in transaction['vin']:
        vin_tx = qcli(['getrawtransaction', vin_transaction['txid'], '1'])
        for vin_item in vin_tx['vout']:
            try:
                tr_address = vin_item['scriptPubKey']['addresses'][0]
                if tr_address == wallet:
                    return 'Sent'
            except KeyError:
                pass

    for vout_transaction in transaction['vout']:
        flag = ''
        try:
            tr_address = vout_transaction['scriptPubKey']['addresses'][0]
            if tr_address == wallet:
                if flag == 'mined':
                    return 'ToStaking'
                else:
                    return 'Received'
        except KeyError:
            flag = 'mined'

txid = ''
transaction = qcli(['getrawtransaction', txid, '1'])
wallet = ''

print(transaction_check(transaction, wallet))
