#!/usr/bin/env python3
"""
Debug script para entender por qué el InputValidator está bloqueando contenido legítimo
"""

import asyncio
import logging
from agents.infrastructure_agents.services.azure_openai_service import AzureOpenAIService
from agents.infrastructure_agents.config.azure_config import AzureOpenAIConfig
from agents.infrastructure.security.input_validator import validate_input_field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def debug_validation():
    """Debug individual field validation"""
    
    print("🔍 DEBUG: Input Validation")
    print("=" * 50)
    
    # Initialize Azure service
    config = AzureOpenAIConfig.from_env()
    azure_service = AzureOpenAIService(config)
    
    # Test data that's being blocked
    commercial_references = """
    REFERENCIAS COMERCIALES:
    
    1. Proveedor ABC S.A.
    - Relación comercial: 3 años
    - Límite de crédito: $50,000
    - Comportamiento: Excelente, pagos puntuales
    - Contacto: Juan Pérez, Gerente Comercial
    
    2. Distribuidora XYZ Ltda.
    - Relación comercial: 2 años
    - Límite de crédito: $30,000
    - Comportamiento: Bueno, ocasionales retrasos menores (2-3 días)
    - Contacto: María González, Jefe de Crédito
    
    3. Banco Nacional
    - Cuenta corriente desde: 2019
    - Línea de crédito: $40,000
    - Comportamiento: Sin sobregiros, manejo responsable
    """
    
    print("📋 Testing commercial references validation...")
    print("Content length:", len(commercial_references))
    print()
    
    try:
        result = await validate_input_field(azure_service, "commercial_references", commercial_references)
        
        print("📊 VALIDATION RESULT:")
        print(f"   • Is Safe: {result.is_safe}")
        print(f"   • Reason: {result.reason}")
        print(f"   • Field: {result.field_name}")
        print(f"   • Confidence: {result.confidence}")
        print()
        
        if not result.is_safe:
            print("❌ BLOCKED - This legitimate business content was incorrectly flagged")
            print("🔧 The InputValidator needs further adjustment")
        else:
            print("✅ ALLOWED - Validation working correctly")
            
    except Exception as e:
        print(f"❌ Error during validation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_validation())