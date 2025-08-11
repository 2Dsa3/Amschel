"""
Test Rápido - Ambos Modelos Azure OpenAI
Prueba rápida de GPT-4o y o3-mini
"""

import asyncio
from dotenv import load_dotenv

load_dotenv()

async def test_both_models_quick():
    """Test rápido de ambos modelos"""
    
    try:
        from agents.infrastructure_agents.services.azure_openai_service import AzureOpenAIService, OpenAIRequest
        from agents.infrastructure_agents.config.azure_config import AzureOpenAIConfig
        from datetime import datetime
        
        print("🧪 Quick Test - Both Models")
        print("=" * 40)
        
        # Load config
        config = AzureOpenAIConfig.from_env()
        service = AzureOpenAIService(config)
        
        print(f"📍 Endpoint: {config.endpoint}")
        print(f"🤖 GPT-4o: {config.deployment_name}")
        print(f"⚡ o3-mini: {config.deployment_name_mini}")
        
        # Test data
        test_data = {"company": "Test Corp", "revenue": 100000}
        
        # Test 1: GPT-4o
        print(f"\n🧠 Testing GPT-4o...")
        gpt4o_request = OpenAIRequest(
            request_id="test_gpt4o",
            user_id="system",
            agent_id="test",
            prompt=f"Analyze this company briefly: {test_data}",
            max_tokens=200,
            temperature=0.3,
            timestamp=datetime.now()
        )
        
        gpt4o_response = await service.generate_completion(
            gpt4o_request, 
            "You are a financial analyst. Be concise.",
            use_mini_model=False
        )
        
        print(f"✅ GPT-4o Success!")
        print(f"🎯 Tokens: {gpt4o_response.tokens_used}")
        print(f"📝 Response: {gpt4o_response.response_text[:100]}...")
        
        # Test 2: o3-mini
        print(f"\n⚡ Testing o3-mini...")
        o3mini_request = OpenAIRequest(
            request_id="test_o3mini",
            user_id="system", 
            agent_id="test",
            prompt=f"Validate this data quickly: {test_data}",
            max_tokens=100,
            temperature=0.1,
            timestamp=datetime.now()
        )
        
        o3mini_response = await service.generate_completion(
            o3mini_request,
            "You are a data validator. Be brief.",
            use_mini_model=True
        )
        
        print(f"✅ o3-mini Success!")
        print(f"🎯 Tokens: {o3mini_response.tokens_used}")
        print(f"📝 Response: {o3mini_response.response_text[:100]}...")
        
        print(f"\n🎉 Both models working perfectly!")
        print(f"💰 Cost optimization: o3-mini for quick tasks")
        print(f"🧠 Quality analysis: GPT-4o for complex tasks")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_both_models_quick())
    if success:
        print("\n✅ DUAL MODELS READY FOR PRODUCTION!")
    else:
        print("\n❌ Fix configuration and try again")