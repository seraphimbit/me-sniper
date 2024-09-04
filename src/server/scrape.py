from datetime import datetime
import json
from curl_cffi import requests # type: ignore

class Scrape:
    def __init__(self):
       self.state = {
            'collection_name': None,
            'user_pubkey': None,
            'mint_token': None,
            'seller': None,
            'price': None,
            'auction_house': None,
            'seller_referral': None,
            'token_ata': None,
            'timestamp': None
        }
    
    def scrape_and_construct(self):  
        try:  
            url = f"https://api-mainnet.magiceden.io/rpc/getCollectionEscrowStats/{self.state['collection_name']}?status=all&edge_cache=true&agg=3&enableFloorWithFee=true"
            r = requests.get(url, impersonate="chrome")
            
            self.state['mint_token'] = r.json()["results"]["floorNFT"]["mintAddress"]
            self.state['price'] = r.json()["results"]["floorNFT"]["price"]
            self.state['seller'] = r.json()["results"]["floorNFT"]["owner"]
         
            self.scrape_mint_by_address()
        
            return self.construct_tx()
        except json.JSONDecodeError:
            #print("Response content is not in JSON format:", r.text)
            return json.dumps({"error": "Response content is not in JSON format", "content": "Error Getting Collection Escrow Stats"})
                  
    def scrape_mint_by_address(self):        
        try:
            url = f"https://api-mainnet.magiceden.io/rpc/getNFTByMintAddress/{self.state['mint_token']}"
            r = requests.get(url, impersonate="chrome")
            self.state['auction_house'] = r.json()["results"]["v2"]["auctionHouseKey"]
            self.state['seller_referral'] = r.json()["results"]["v2"]["sellerReferral"]
            self.state['token_ata'] = r.json()["results"]["id"]

        except json.JSONDecodeError:
            #print("Response content is not in JSON format:", r.text)
            return json.dumps({"error": "Response content is not in JSON format", "content": "Error Getting NFT By Mint Address"})
            
    def construct_tx(self):      
        try:
            timestamp = datetime.now().strftime("%H-%d-%Y")
            self.state['timestamp'] = timestamp     
   
            url = f"https://api-mainnet.magiceden.io/v2/instructions/buy_now?buyer={self.state['user_pubkey']}&seller={self.state['seller']}&auctionHouseAddress={self.state['auction_house']}&tokenMint={self.state['mint_token']}&tokenATA={self.state['token_ata']}&price={self.state['price']}&sellerReferral={self.state['seller_referral']}&sellerExpiry=-1&rtimestamp={self.state['timestamp']}"
            r = requests.get(url, impersonate="chrome")
            
            return r.json()
        except json.JSONDecodeError:
          #print("Response content is not in JSON format:", r.text)
          return json.dumps({"error": "Response content is not in JSON format", "content": "Error Constructing Transaction"})
  
    def get_listed_tokens(self):        
        try:
            url = f"https://api-mainnet.magiceden.io/idxv2/getAllNftsByCollectionSymbol?collectionSymbol={self.state['collection_name']}&onChainCollectionAddress=&direction=2&field=1&limit=100&token22StandardFilter=1&mplCoreStandardFilter=1&agg=3&compressionMode=both"
            r = requests.get(url, impersonate="chrome")
            
            return r.json()
        except json.JSONDecodeError:
           #print("Response content is not in JSON format:", r.text)
           return json.dumps({"error": "Response content is not in JSON format", "content": "Error Getting Listed Tokens"})
              
    def get_candy_machines(self):
        try:
            url = f"https://api-mainnet.magiceden.io/launchpad_collections"
            r = requests.get(url, impersonate="chrome")
   
            return r.json()
        except json.JSONDecodeError:
           #print("Response content is not in JSON format:", r.text)
           return json.dumps({"error": "Response content is not in JSON format", "content": "Error Getting Candy Machines"})