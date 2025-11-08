# diagnose_api.py
import requests
import json

def diagnose_api():
    print("🔍 DIAGNOSING API RESPONSE FORMAT")
    print("=" * 50)
    
    try:
        # Test the API endpoint
        response = requests.get('http://localhost:5000/api/pending-registrations', timeout=10)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API returned data: {type(data)}")
            
            if data:
                print(f"📦 First record structure:")
                print(json.dumps(data[0], indent=2))
                
                # Check what keys are available
                if data:
                    first_record = data[0]
                    print(f"🔑 Available keys: {list(first_record.keys())}")
            else:
                print("ℹ️ API returned empty list (no pending registrations)")
        else:
            print(f"❌ API error: {response.text}")
            
    except Exception as e:
        print(f"❌ API diagnostic failed: {str(e)}")

if __name__ == "__main__":
    diagnose_api()