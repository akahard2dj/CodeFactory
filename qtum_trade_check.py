from qtum_cli import qtum_cli as qcli

txid = 'e981824435db0dcb6379687501c772677905ea04cf6a39b14eb65c19784b150f'
#txid = '810502df07a9395237fa6f25ebad3f3e6b531a35bb6f9dc54998e31e534e98c5'

# if the number of vout item in transaction is 1, it means a general remittance
# if the number of vout itme in transaction is 12, it means a payment for PoS rewards
wallet = 'QUwgBsg6PndgpUDJoub2UCULacDg94qWcm'
transaction = qcli(['getrawtransaction', txid, '1'])
print(len(transaction['vout']))
vin_value = 0.0
print(transaction["vin"])
for vin_transaction in transaction["vin"]:
    print(vin_transaction['txid'])
    vin_tx = qcli(['getrawtransaction', vin_transaction['txid'], '1'])
    for vin_item in vin_tx["vout"]:
        try:
            tr_address = vin_item['scriptPubKey']['addresses'][0]
            if tr_address == wallet:
                print(vin_item['value'])
                vin_value += vin_item['value']
        except KeyError:
            pass

print(vin_value)

