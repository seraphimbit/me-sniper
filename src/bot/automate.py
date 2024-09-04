from solders.keypair import Keypair # type: ignore
from solana.rpc.api import Client # type: ignore
from curl_cffi import requests # type: ignore
from solana.transaction import Transaction # type: ignore

class Automate:
    def __init__(self):
        self._state = {
            'USER_KEY': None,
            'RPC': None,
            'COLLECTION_NAME': None,
            'USER_PUBKEY': None
        }
        
    async def Snipe(self):
        wallet = await self.load_wallet()
        client = await self.load_client()
        self._state['USER_PUBKEY'] = str(wallet.pubkey())  # Ensure USER_PUBKEY is a string
        
        data = self.post_request()
       
        self.send_tx(data, client, wallet)
        
    def send_tx(self, tx, client, wallet):   #This is function doesn't work, this was from 2 years ago      
         DATA = tx
         print(f"INSTRUCTION DATA: {DATA}")
         #if isinstance(DATA, list):
          # DATA = bytes(DATA)  
 
          #TX = Transaction.deserialize(DATA)
         
          #tx_details = {
          #"recent_blockhash": TX.recent_blockhash,
          #"fee_payer": TX.fee_payer,
          #"instructions": TX.instructions,
          #"signatures": TX.signatures,
          #} 
     
         #recent_blockhash_resp = client.get_latest_blockhash()
         #recent_blockhash = recent_blockhash_resp.value.blockhash
     
         #TX.recent_blockhash = recent_blockhash
         #TX.sign(wallet)
         
         #finalTX = client.send_transaction(TX, *signers, opts=None, recent_blockhash=recent_blockhash)
         
         #TXSEREAL = TX.serialize().hex()
         
         #finalTX = client.send_raw_transaction(bytes.fromhex(TXSEREAL), opts=None)        
         #print(f"TX :{finalTX}")
    
    def post_request(self):
        data = {
            "collection_name": self._state['COLLECTION_NAME'],
            "user_pubkey": self._state['USER_PUBKEY']
        }

        r = requests.post("http://localhost:3000/snipe", json=data)
        data_tx = r.json()
        
        return data_tx["data"]["txSigned"]["data"]
        
    async def load_wallet(self):
        keypair = Keypair.from_base58_string(self._state['USER_KEY'])
        return keypair
    
    async def load_client(self):
        http_client = Client(self._state['RPC'])
        return http_client