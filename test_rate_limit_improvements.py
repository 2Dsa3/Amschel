#!/usr/bin/env python3
"""
Test de las mejoras de rate limit
Verifica que el sistema maneja correctamente los rate limits
"""

import asyncio
import time
from datetime import datetime
from dotenv import load_dotenv

from agents.azure_orchestrator import AzureOrchestrator, CompanyData

async def test_rate_limit_handling():
    """Prueba el manejo de rate limits con múltiples requests"""
    
    load_dotenv()
    
    print("🚀 PROBANDO MEJORAS DE RATE LIMIT")
    print("=" * 60)
    
    # Inicializar orchestrator con servicio mejorado
    orchestrator = AzureOrchestrator()
    success = await orchestrator.initialize()
    
    if not success:
        print("❌ Error al inicializar el orquestador")
        return
    
    print("✅ Orquestador inicializado con servicio mejorado")
    
    # Verificar que está usando el servicio mejorado
    service_type = type(orchestrator.azure_service).__name__
    print(f"🔧 Tipo de servicio: {service_type}")
    
    # Crear empresa de prueba simple
    test_company = CompanyData(
        company_id="RATE_TEST_001",
        company_name="Empresa Test Rate Limit S.A.",
        financial_statements="""
        DATOS FINANCIEROS BÁSICOS:
        Activos: $500,000
        Pasivos: $300,000
        Patrimonio: $200,000
        Ingresos: $800,000
        Utilidad: $50,000
        """,
        social_media_data="""
        REPUTACIÓN BÁSICA:
        Google Reviews: 4.0/5 estrellas
        Comentarios: "Buen servicio", "Empresa confiable"
        """,
        commercial_references="""
        REFERENCIAS BÁSICAS:
        Banco XYZ - Cliente desde 2020
        Proveedor ABC - Pagos puntuales
        """,
        payment_history="""
        HISTORIAL BÁSICO:
        Últimos 6 meses: Pagos puntuales
        Score crediticio: 750/900
        """,
        metadata={
            "industry": "test",
            "test_type": "rate_limit_test"
        }
    )
    
    print(f"\n🏢 Empresa de prueba: {test_company.company_name}")
    
    # Test 1: Evaluación individual con timing
    print(f"\n📊 TEST 1: Evaluación individual con timing")
    start_time = time.time()
    
    try:
        result = await orchestrator.evaluate_company_risk(test_company)
        end_time = time.time()
        
        print(f"   ✅ Evaluación completada")
        print(f"   ⏱️  Tiempo: {end_time - start_time:.2f} segundos")
        print(f"   🎯 Score: {result.final_score}/1000")
        print(f"   🚦 Riesgo: {result.risk_level}")
        print(f"   📊 Éxito: {'Sí' if result.success else 'No'}")
        
        # Mostrar estadísticas del servicio si están disponibles
        if hasattr(orchestrator.azure_service, 'get_service_stats'):
            stats = orchestrator.azure_service.get_service_stats()
            print(f"   📈 Requests totales: {stats.get('total_requests', 'N/A')}")
            print(f"   ✅ Requests exitosos: {stats.get('successful_requests', 'N/A')}")
            print(f"   🚫 Rate limited: {stats.get('rate_limited_requests', 'N/A')}")
            print(f"   🔄 Tasa de éxito: {stats.get('success_rate', 'N/A'):.1f}%")
        
    except Exception as e:
        end_time = time.time()
        print(f"   ❌ Error: {str(e)}")
        print(f"   ⏱️  Tiempo hasta error: {end_time - start_time:.2f} segundos")
    
    # Test 2: Múltiples evaluaciones rápidas (stress test)
    print(f"\n📊 TEST 2: Múltiples evaluaciones (stress test)")
    print("   🔄 Ejecutando 3 evaluaciones consecutivas...")
    
    results = []
    total_start = time.time()
    
    for i in range(3):
        print(f"   📋 Evaluación {i+1}/3...")
        eval_start = time.time()
        
        try:
            # Crear una variación de la empresa para cada test
            test_company_variant = CompanyData(
                company_id=f"RATE_TEST_{i+1:03d}",
                company_name=f"Empresa Test {i+1} S.A.",
                financial_statements=f"Activos: ${500000 + i*10000}, Pasivos: ${300000 + i*5000}",
                social_media_data=f"Google Reviews: {4.0 + i*0.1}/5 estrellas",
                commercial_references=f"Banco XYZ - Cliente desde {2020 + i}",
                payment_history=f"Score crediticio: {750 + i*10}/900",
                metadata={"test_iteration": i+1}
            )
            
            result = await orchestrator.evaluate_company_risk(test_company_variant)
            eval_time = time.time() - eval_start
            
            results.append({
                "iteration": i+1,
                "success": result.success,
                "score": result.final_score,
                "time": eval_time,
                "risk_level": result.risk_level
            })
            
            print(f"      ✅ Completada en {eval_time:.2f}s - Score: {result.final_score}")
            
        except Exception as e:
            eval_time = time.time() - eval_start
            results.append({
                "iteration": i+1,
                "success": False,
                "error": str(e),
                "time": eval_time
            })
            print(f"      ❌ Error en {eval_time:.2f}s: {str(e)[:50]}...")
        
        # Pequeña pausa entre evaluaciones
        await asyncio.sleep(1)
    
    total_time = time.time() - total_start
    
    # Resumen del stress test
    print(f"\n📊 RESUMEN DEL STRESS TEST:")
    successful_evals = sum(1 for r in results if r.get('success', False))
    print(f"   ✅ Evaluaciones exitosas: {successful_evals}/3")
    print(f"   ⏱️  Tiempo total: {total_time:.2f} segundos")
    print(f"   📈 Tiempo promedio: {total_time/3:.2f} segundos por evaluación")
    
    # Mostrar estadísticas finales del servicio
    if hasattr(orchestrator.azure_service, 'get_service_stats'):
        print(f"\n📈 ESTADÍSTICAS FINALES DEL SERVICIO:")
        final_stats = orchestrator.azure_service.get_service_stats()
        
        for key, value in final_stats.items():
            if key == 'rate_limit_stats':
                print(f"   🚫 Rate Limit Stats:")
                for sub_key, sub_value in value.items():
                    print(f"      {sub_key}: {sub_value}")
            else:
                if isinstance(value, float):
                    print(f"   {key}: {value:.2f}")
                else:
                    print(f"   {key}: {value}")
    
    # Test 3: Health check del servicio
    print(f"\n📊 TEST 3: Health Check del Servicio")
    
    if hasattr(orchestrator.azure_service, 'health_check'):
        try:
            health = await orchestrator.azure_service.health_check()
            print(f"   🏥 Estado: {health.get('status', 'unknown')}")
            print(f"   ⏱️  Tiempo de respuesta: {health.get('response_time_seconds', 'N/A'):.3f}s")
            print(f"   🔗 Endpoint: {health.get('endpoint', 'N/A')}")
            print(f"   🤖 Modelos: {health.get('models_available', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Error en health check: {str(e)}")
    else:
        print(f"   ⚠️  Health check no disponible en este servicio")
    
    print(f"\n🎯 PRUEBAS DE RATE LIMIT COMPLETADAS")
    print("=" * 60)

async def main():
    """Función principal"""
    await test_rate_limit_handling()

if __name__ == "__main__":
    asyncio.run(main())