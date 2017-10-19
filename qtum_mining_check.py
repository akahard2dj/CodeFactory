from qtum_cli import qtum_cli as qcli

block_hash = qcli(['getblockhash', '29462'])
print(block_hash)
block = qcli(['getblock', block_hash])

wallet = 'QfBAPNKrABgBQakd57Nd6vpp5cPPEFQsCz'
print(block["tx"][1])
transaction = qcli(['getrawtransaction', block["tx"][1], '1'])
vin_value = 0.0
print(len(transaction['vout']))
for vin_item in transaction["vin"]:
    print(vin_item['txid'])
    vin_tx = qcli(['getrawtransaction', vin_item['txid'], '1'])
    for vout_item in vin_tx["vout"]:
        try:
            tr_address = vout_item['scriptPubKey']['addresses'][0]
            if tr_address == wallet:
                print(vout_item['value'])
                vin_value += vout_item['value']
        except KeyError:
            pass

vou_value = 0.0

for vout_item in transaction["vout"]:
    #vin_tx = qcli(['getrawtransaction', vout_item['txid'], '1'])
    try:
        tr_address = vout_item['scriptPubKey']['addresses'][0]
        if tr_address == wallet:
            print(vout_item['value'])

            vou_value += vout_item['value']
    except KeyError:
        pass

print('{}: {} -> {}'.format(wallet, vin_value, vou_value))
