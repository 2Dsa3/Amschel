#!/usr/bin/env python3
"""
Test del sistema de análisis de riesgo crediticio con 5 empresas diferentes
Simula casos reales de empresas con diferentes perfiles de riesgo
"""

import asyncio
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from agents.azure_orchestrator import AzureOrchestrator, CompanyData

# Datos de las 5 empresas para testing usando CompanyData
def create_companies_data():
    """Crea las 5 empresas de prueba usando el modelo CompanyData correcto"""
    
    companies = []
    
    # Empresa 1: Tecnología - Perfil sólido
    companies.append(CompanyData(
        company_id="TECH001",
        company_name="InnovaTech Solutions S.A.",
        financial_statements="""
        ESTADO FINANCIERO - INNOVATECH SOLUTIONS S.A.
        Período: Enero - Diciembre 2023
        
        BALANCE GENERAL:
        Activos Totales: $8,500,000
        - Activos Corrientes: $4,200,000
        - Efectivo: $1,800,000
        - Cuentas por cobrar: $1,900,000
        - Inventarios: $500,000
        - Activos Fijos: $4,300,000
        
        Pasivos Totales: $3,200,000
        - Pasivos Corrientes: $1,800,000
        - Deuda a largo plazo: $1,400,000
        
        Patrimonio: $5,300,000
        
        ESTADO DE RESULTADOS:
        Ingresos: $15,000,000
        Utilidad Neta: $2,250,000
        Flujo de Caja: $2,800,000
        Margen de Utilidad: 15%
        ROE: 42.5%
        """,
        social_media_data="""
        ANÁLISIS DE REPUTACIÓN DIGITAL - INNOVATECH SOLUTIONS
        
        Google Reviews: 4.2/5 estrellas (156 reseñas)
        - "Excelente servicio técnico y soporte 24/7"
        - "Innovación constante en sus productos"
        - "Equipo muy profesional y competente"
        - "Precios competitivos para la calidad ofrecida"
        
        Glassdoor: 3.8/5 estrellas (89 empleados)
        - Ambiente laboral positivo
        - Oportunidades de crecimiento
        - Beneficios competitivos
        
        LinkedIn: 5,200 seguidores
        - Contenido técnico de calidad
        - Participación activa en eventos del sector
        
        Certificaciones: ISO 9001, SOC 2
        Premios: Best Tech Startup 2023
        """,
        commercial_references="""
        REFERENCIAS COMERCIALES - INNOVATECH SOLUTIONS
        
        1. Banco Pichincha (Cliente desde 2019)
        - Línea de crédito: $2,000,000
        - Comportamiento: Excelente
        - Pagos siempre puntuales
        - Calificación: AAA
        
        2. Microsoft Ecuador (Proveedor, 4 años)
        - Límite comercial: $500,000
        - Pagos promedio: 25 días
        - Sin incidencias reportadas
        - Relación comercial sólida
        
        3. Cliente Corporativo - Banco del Pacífico
        - Contrato por $3,000,000 anuales
        - Renovación automática por 3 años
        - Satisfacción del cliente: Muy alta
        """,
        payment_history="""
        HISTORIAL DE PAGOS - ÚLTIMOS 24 MESES
        
        2023:
        - Enero a Marzo: Pagos puntuales
        - Abril: Retraso de 5 días (problema bancario)
        - Mayo a Diciembre: Pagos puntuales
        
        2024:
        - Enero a Junio: 100% pagos puntuales
        - Promedio días de pago: 22 días
        - Términos de pago: 30 días
        - Score crediticio: 850/900
        
        Resumen: 95% pagos puntuales, excelente historial
        """,
        metadata={
            "industry": "technology",
            "test_type": "solid_company",
            "risk_profile": "low"
        }
    ))
    
    
    
    return companies

async def test_single_company(orchestrator, company_data):
    """Prueba el análisis de una empresa individual"""
    print(f"\n{'='*60}")
    print(f"ANALIZANDO: {company_data.company_name} ({company_data.company_id})")
    print(f"Industria: {company_data.metadata.get('industry', 'N/A')}")
    print(f"{'='*60}")
    
    try:
        start_time = time.time()
        
        # Realizar análisis completo usando AzureOrchestrator
        result = await orchestrator.evaluate_company_risk(company_data)
        
        processing_time = time.time() - start_time
        
        # Mostrar resultados
        print(f"\n📊 RESULTADOS DEL ANÁLISIS:")
        print(f"Score Final: {result.final_score}/1000")
        print(f"Nivel de Riesgo: {result.risk_level}")
        print(f"Tiempo de Procesamiento: {processing_time:.2f}s")
        print(f"Evaluación Exitosa: {'✅' if result.success else '❌'}")
        
        if result.success:
            # Análisis Financiero
            if result.financial_analysis and result.financial_analysis.get('success', True):
                financial = result.financial_analysis
                print(f"\n💰 Análisis Financiero:")
                print(f"  • Solvencia: {financial.get('solvencia', 'N/A')[:80]}...")
                print(f"  • Liquidez: {financial.get('liquidez', 'N/A')[:80]}...")
                print(f"  • Tokens usados: {financial.get('tokens_used', 0)}")
            
            # Análisis Reputacional
            if result.reputational_analysis and result.reputational_analysis.get('success', True):
                reputational = result.reputational_analysis
                print(f"\n🌟 Análisis Reputacional:")
                print(f"  • Sentimiento: {reputational.get('sentimiento_general', 'N/A')}")
                print(f"  • Puntaje: {reputational.get('puntaje_sentimiento', 'N/A')}")
                print(f"  • Tokens usados: {reputational.get('tokens_used', 0)}")
            
            # Análisis Comportamental
            if result.behavioral_analysis and result.behavioral_analysis.get('success', True):
                behavioral = result.behavioral_analysis
                print(f"\n📈 Análisis Comportamental:")
                print(f"  • Patrón de pago: {behavioral.get('patron_de_pago', 'N/A')}")
                print(f"  • Riesgo: {behavioral.get('riesgo_comportamental', 'N/A')}")
                print(f"  • Tokens usados: {behavioral.get('tokens_used', 0)}")
            
            # Reporte Consolidado
            if result.consolidated_report and result.consolidated_report.get('success', True):
                consolidated = result.consolidated_report
                print(f"\n🎯 Reporte Consolidado:")
                print(f"  • Confianza: {consolidated.get('confidence', 0):.2f}")
                print(f"  • Recomendación: {consolidated.get('credit_recommendation', 'N/A')[:80]}...")
        else:
            print(f"\n❌ Errores: {', '.join(result.errors)}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error analizando {company_data.company_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_batch_analysis(orchestrator, companies_data):
    """Prueba análisis en lote de todas las empresas"""
    print(f"\n{'='*80}")
    print("ANÁLISIS COMPARATIVO DE LAS 5 EMPRESAS")
    print(f"{'='*80}")
    
    results = []
    
    # Analizar todas las empresas
    for company_data in companies_data:
        result = await test_single_company(orchestrator, company_data)
        if result and result.success:
            results.append({
                'company': company_data.company_name,
                'company_id': company_data.company_id,
                'industry': company_data.metadata.get('industry', 'N/A'),
                'risk_profile': company_data.metadata.get('risk_profile', 'N/A'),
                'result': result
            })
    
    # Mostrar comparativa
    if results:
        print(f"\n{'='*80}")
        print("RANKING DE EMPRESAS POR SCORE DE RIESGO")
        print(f"{'='*80}")
        
        # Ordenar por score (mayor score = menor riesgo)
        sorted_results = sorted(results, key=lambda x: x['result'].final_score, reverse=True)
        
        for i, company_result in enumerate(sorted_results, 1):
            result = company_result['result']
            risk_icon = "🟢" if result.risk_level == "BAJO" else "🟡" if result.risk_level == "MEDIO" else "🔴"
            
            print(f"{i}. {company_result['company']} ({company_result['industry']})")
            print(f"   {risk_icon} Score: {result.final_score}/1000 | Riesgo: {result.risk_level}")
            print(f"   📊 Perfil esperado: {company_result['risk_profile']}")
            
            # Mostrar recomendación si está disponible
            if result.consolidated_report and result.consolidated_report.get('credit_recommendation'):
                recommendation = result.consolidated_report['credit_recommendation'][:100]
                print(f"   💡 Recomendación: {recommendation}...")
            print()
    
    return results

async def test_edge_cases(orchestrator):
    """Prueba casos extremos y validaciones"""
    print(f"\n{'='*60}")
    print("PRUEBAS DE CASOS EXTREMOS")
    print(f"{'='*60}")
    
    # Caso 1: Datos mínimos
    print("\n🧪 Caso 1: Empresa con datos mínimos")
    minimal_company = CompanyData(
        company_id="MINIMAL001",
        company_name="Empresa Datos Mínimos S.A.",
        financial_statements="Información financiera limitada disponible. Ingresos aproximados: $1,000,000",
        social_media_data="Sin presencia digital significativa",
        commercial_references="Referencias comerciales en proceso de verificación",
        payment_history="Historial de pagos corto, empresa nueva",
        metadata={
            "industry": "unknown",
            "test_type": "minimal_data",
            "risk_profile": "unknown"
        }
    )
    
    try:
        result = await orchestrator.evaluate_company_risk(minimal_company)
        print(f"✅ Análisis completado con datos mínimos")
        print(f"Score: {result.final_score}/1000 | Riesgo: {result.risk_level}")
        print(f"Éxito: {'Sí' if result.success else 'No'}")
    except Exception as e:
        print(f"❌ Error con datos mínimos: {str(e)}")
    
    # Caso 2: Empresa en crisis
    print("\n🧪 Caso 2: Empresa en crisis financiera")
    crisis_company = CompanyData(
        company_id="CRISIS001",
        company_name="Empresa en Crisis Financiera S.A.",
        financial_statements="""
        ESTADO FINANCIERO CRÍTICO - EMPRESA EN CRISIS
        
        BALANCE GENERAL:
        Activos Totales: $500,000
        Pasivos Totales: $800,000
        Patrimonio: ($300,000) - PATRIMONIO NEGATIVO
        
        ESTADO DE RESULTADOS:
        Ingresos: $1,000,000
        Pérdida Neta: ($500,000)
        Flujo de Caja: ($250,000)
        
        SITUACIÓN CRÍTICA: Insolvencia técnica
        """,
        social_media_data="""
        REPUTACIÓN DIGITAL CRÍTICA:
        
        Google Reviews: 1.2/5 estrellas (89 reseñas)
        - "Empresa en quiebra, no cumple contratos"
        - "Perdí mi dinero, no recomiendo"
        - "Servicio pésimo, problemas legales"
        
        Noticias negativas:
        - "Empresa investigada por fraude"
        - "Múltiples demandas de clientes"
        """,
        commercial_references="""
        REFERENCIAS COMERCIALES NEGATIVAS:
        
        1. Banco Central - Cuenta cerrada por sobregiros
        2. Proveedor Principal - Cortó relación por impagos
        3. Ex-cliente - Demanda legal activa por $200,000
        
        Sin referencias positivas disponibles
        """,
        payment_history="""
        HISTORIAL DE PAGOS CRÍTICO:
        
        Últimos 6 meses:
        - Enero: Retraso 90 días
        - Febrero: Retraso 120 días  
        - Marzo: Sin pago
        - Abril: Pago parcial con retraso 60 días
        - Mayo: Sin pago
        - Junio: Sin pago
        
        Score crediticio: 200/900 (crítico)
        Múltiples reportes negativos
        """,
        metadata={
            "industry": "crisis",
            "test_type": "crisis_company",
            "risk_profile": "critical"
        }
    )
    
    try:
        result = await orchestrator.evaluate_company_risk(crisis_company)
        print(f"✅ Análisis completado para empresa en crisis")
        print(f"Score: {result.final_score}/1000 | Riesgo: {result.risk_level}")
        print(f"Éxito: {'Sí' if result.success else 'No'}")
    except Exception as e:
        print(f"❌ Error con empresa en crisis: {str(e)}")

async def main():
    """Función principal de testing"""
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA DE ANÁLISIS DE RIESGO CREDITICIO")
    print("=" * 80)
    print("Probando 5 empresas con diferentes perfiles de riesgo")
    print("=" * 80)
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Inicializar orchestrator
    print("🔧 Inicializando AzureOrchestrator...")
    orchestrator = AzureOrchestrator()
    success = await orchestrator.initialize()
    
    if not success:
        print("❌ Error al inicializar el orquestador")
        return
    
    print("✅ AzureOrchestrator inicializado correctamente")
    
    # Crear datos de las empresas
    companies_data = create_companies_data()
    print(f"📊 {len(companies_data)} empresas preparadas para análisis")
    
    try:
        # Obtener estadísticas iniciales
        initial_stats = orchestrator.get_stats()
        print(f"\n📈 Estado inicial del sistema:")
        print(f"   Total evaluaciones previas: {initial_stats['total_evaluations']}")
        print(f"   Tokens usados previamente: {initial_stats['total_tokens_used']}")
        
        # Prueba 1: Análisis individual de cada empresa
        print("\n📋 FASE 1: ANÁLISIS INDIVIDUAL DE EMPRESAS")
        individual_results = []
        for company_data in companies_data:
            result = await test_single_company(orchestrator, company_data)
            if result and result.success:
                individual_results.append(result)
        
        # Prueba 2: Análisis comparativo
        print("\n📋 FASE 2: ANÁLISIS COMPARATIVO")
        batch_results = await test_batch_analysis(orchestrator, companies_data)
        
        # Prueba 3: Casos extremos
        print("\n📋 FASE 3: CASOS EXTREMOS")
        await test_edge_cases(orchestrator)
        
        # Estadísticas finales
        final_stats = orchestrator.get_stats()
        tokens_used_this_session = final_stats['total_tokens_used'] - initial_stats['total_tokens_used']
        
        # Resumen final
        print(f"\n{'='*80}")
        print("RESUMEN FINAL DE PRUEBAS")
        print(f"{'='*80}")
        print(f"✅ Empresas analizadas exitosamente: {len(individual_results)}/5")
        print(f"✅ Análisis comparativo completado")
        print(f"✅ Casos extremos probados")
        print(f"📊 Total evaluaciones realizadas: {final_stats['total_evaluations'] - initial_stats['total_evaluations']}")
        print(f"🎫 Tokens usados en esta sesión: {tokens_used_this_session}")
        print(f"⏱️  Tiempo promedio por evaluación: {final_stats['average_processing_time']:.2f}s")
        
        if batch_results:
            best_company = max(batch_results, key=lambda x: x['result'].final_score)
            worst_company = min(batch_results, key=lambda x: x['result'].final_score)
            
            print(f"\n🏆 Mejor empresa: {best_company['company']} (Score: {best_company['result'].final_score}/1000)")
            print(f"   🟢 Riesgo: {best_company['result'].risk_level}")
            print(f"   📊 Perfil: {best_company['risk_profile']}")
            
            print(f"\n⚠️  Mayor riesgo: {worst_company['company']} (Score: {worst_company['result'].final_score}/1000)")
            print(f"   🔴 Riesgo: {worst_company['result'].risk_level}")
            print(f"   📊 Perfil: {worst_company['risk_profile']}")
        
        # Mostrar eventos de auditoría recientes
        print(f"\n📋 EVENTOS DE AUDITORÍA RECIENTES:")
        recent_events = orchestrator.get_recent_audit_events(5)
        for i, event in enumerate(recent_events[-5:], 1):
            timestamp = event.get('timestamp', 'N/A')
            event_type = event.get('event_type', 'N/A')
            agent_id = event.get('agent_id', 'N/A')
            print(f"   {i}. {timestamp} - {event_type} - {agent_id}")
        
        print(f"\n🎉 TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())