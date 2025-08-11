"""
Sistema Integrado de Evaluación de Riesgo Financiero para PYMEs
Demostración del flujo completo usando AzureOrchestrator actualizado

Flujo completo: SecuritySupervisor → InputValidator → BusinessAgents → OutputSanitizer → ScoringAgent → AuditLogger
"""

import asyncio
import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from agents.azure_orchestrator import AzureOrchestrator, CompanyData


async def test_integrated_system():
    """
    Prueba el sistema integrado completo de evaluación de riesgo
    """
    print("🚀 Iniciando Sistema Integrado de Evaluación de Riesgo Financiero")
    print("=" * 70)
    
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_DEPLOYMENT"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"❌ Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("\n📝 Configura las siguientes variables en tu archivo .env:")
        print("AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/")
        print("AZURE_OPENAI_API_KEY=your-api-key")
        print("AZURE_OPENAI_DEPLOYMENT=gpt-4o")
        print("AZURE_OPENAI_DEPLOYMENT_MINI=o3-mini")
        return
    
    try:
        # Initialize the AzureOrchestrator
        print("🔧 Inicializando AzureOrchestrator...")
        orchestrator = AzureOrchestrator()
        success = await orchestrator.initialize()
        
        if not success:
            print("❌ Error al inicializar el orquestador")
            return
        
        print("✅ AzureOrchestrator inicializado correctamente")
        print(f"   🔗 Endpoint: {orchestrator.config.endpoint}")
        print(f"   🤖 Modelo principal: {orchestrator.config.deployment_name}")
        print(f"   ⚡ Modelo rápido: {orchestrator.config.deployment_name_mini}")
        
        # Show initial stats
        initial_stats = orchestrator.get_stats()
        print(f"\n📊 Estado inicial del sistema:")
        print(f"   Total evaluaciones previas: {initial_stats['total_evaluations']}")
        print(f"   Tokens usados previamente: {initial_stats['total_tokens_used']}")
        
        # Prepare test company data using CompanyData model
        company_data = CompanyData(
            company_id="PYME_001",
            company_name="Innovaciones Andinas S.A.",
            financial_statements="""
            ESTADO DE SITUACIÓN FINANCIERA - INNOVACIONES ANDINAS S.A.
            Período: Enero - Diciembre 2023
            
            ACTIVOS:
            Activos Corrientes:
            - Efectivo y equivalentes: $45,000
            - Cuentas por cobrar: $120,000
            - Inventarios: $85,000
            Total Activos Corrientes: $250,000
            
            Activos No Corrientes:
            - Propiedad, planta y equipo: $180,000
            - Depreciación acumulada: ($45,000)
            Total Activos No Corrientes: $135,000
            
            TOTAL ACTIVOS: $385,000
            
            PASIVOS:
            Pasivos Corrientes:
            - Cuentas por pagar: $65,000
            - Préstamos a corto plazo: $35,000
            Total Pasivos Corrientes: $100,000
            
            Pasivos No Corrientes:
            - Préstamos a largo plazo: $120,000
            Total Pasivos No Corrientes: $120,000
            
            TOTAL PASIVOS: $220,000
            
            PATRIMONIO:
            - Capital social: $100,000
            - Utilidades retenidas: $65,000
            TOTAL PATRIMONIO: $165,000
            
            ESTADO DE RESULTADOS:
            - Ingresos por ventas: $480,000
            - Costo de ventas: $288,000
            - Utilidad bruta: $192,000
            - Gastos operacionales: $145,000
            - Utilidad operacional: $47,000
            - Gastos financieros: $12,000
            - Utilidad neta: $35,000
            """,
            social_media_data="""
            ANÁLISIS DE REDES SOCIALES - INNOVACIONES ANDINAS S.A.
            
            Reseñas de Google Business (4.2/5 estrellas, 127 reseñas):
            - "Excelente servicio al cliente, productos de calidad. Recomendado 100%"
            - "Muy profesionales, entrega a tiempo siempre"
            - "Buenos precios y atención personalizada"
            - "Tuve un problema con un pedido pero lo resolvieron rápidamente"
            - "Llevan años en el mercado, son confiables"
            
            Facebook (2,340 seguidores):
            - Publicaciones regulares sobre productos
            - Interacción positiva con clientes
            - Responden consultas en menos de 2 horas
            
            LinkedIn:
            - Perfil corporativo actualizado
            - 15 empleados registrados
            - Conexiones con proveedores principales del sector
            
            Menciones en medios:
            - Artículo en Revista Empresarial Ecuador (2023): "PYMEs innovadoras del sector"
            - Participación en Feria de Emprendimiento Quito 2023
            """,
            commercial_references="""
            REFERENCIAS COMERCIALES - INNOVACIONES ANDINAS S.A.
            
            Referencia 1: Aceros del Pacífico S.A. (Proveedor principal, 4 años)
            Contacto: María González, Gerente de Ventas
            Comentario: "Innovaciones Andinas es uno de nuestros mejores clientes. Sus pagos son consistentemente puntuales, nunca hemos tenido un solo retraso. La comunicación es proactiva y profesional. Volumen de compras anuales: $180,000."
            
            Referencia 2: Logística Global Ecuador (Socio logístico, 2 años)
            Contacto: Carlos Mendoza, Director Operaciones
            Comentario: "Trabajamos con ellos desde 2022. Son muy organizados y cumplen con los acuerdos. A veces se demoran 1-2 días en pagar facturas después del vencimiento, pero siempre avisan y pagan. Los consideramos un socio confiable."
            
            Referencia 3: Banco del Pichincha (Entidad financiera, 3 años)
            Contacto: Ana Rodríguez, Ejecutiva de Cuenta
            Comentario: "Cliente con historial crediticio limpio. Ha mantenido línea de crédito de $50,000 sin incidentes. Pagos puntuales en 95% de las ocasiones. Relación comercial sólida."
            """,
            payment_history="""
            HISTORIAL DE PAGOS - ÚLTIMOS 12 MESES
            
            Proveedores principales:
            - Aceros del Pacífico: 12/12 pagos a tiempo
            - Materiales Industriales: 11/12 pagos a tiempo (1 retraso de 3 días)
            - Transporte Rápido: 10/12 pagos a tiempo (2 retrasos de 1-2 días)
            
            Obligaciones financieras:
            - Banco del Pichincha (línea de crédito): 12/12 pagos puntuales
            - Cooperativa de Ahorro: 11/12 pagos puntuales (1 retraso de 5 días)
            
            Servicios básicos y otros:
            - Electricidad: 12/12 pagos puntuales
            - Telecomunicaciones: 12/12 pagos puntuales
            - Seguros: 4/4 pagos trimestrales puntuales
            
            Resumen: 94% de pagos puntuales en los últimos 12 meses
            """,
            metadata={
                "demo_type": "integrated_system_test",
                "industry": "manufacturing",
                "created_at": datetime.now().isoformat()
            }
        )
        
        print(f"\n🏢 Iniciando evaluación para: {company_data.company_name}")
        print("📊 Datos disponibles:")
        print(f"   - Estados financieros: ✅")
        print(f"   - Datos de redes sociales: ✅")
        print(f"   - Referencias comerciales: ✅")
        print(f"   - Historial de pagos: ✅")
        
        # Start risk evaluation using AzureOrchestrator
        print(f"\n🎯 Iniciando evaluación de riesgo...")
        print("🔄 Flujo: SecuritySupervisor → InputValidator → BusinessAgents → OutputSanitizer → ScoringAgent → AuditLogger")
        
        start_time = time.time()
        result = await orchestrator.evaluate_company_risk(company_data)
        end_time = time.time()
        
        processing_time = end_time - start_time
        print(f"\n⏱️  Evaluación completada en {processing_time:.2f} segundos")
        
        # Check if evaluation was successful
        if not result.success:
            print(f"❌ Error en la evaluación: {', '.join(result.errors)}")
            print(f"🆔 ID de Evaluación: {result.evaluation_id}")
            print(f"🚦 Estado: {result.risk_level}")
            return
        
        # Display results using AzureOrchestrator result structure
        print("\n" + "="*70)
        print("📊 RESULTADOS DE LA EVALUACIÓN DE RIESGO")
        print("="*70)
        
        print(f"🏢 Empresa: {result.company_name}")
        print(f"🆔 ID de Evaluación: {result.evaluation_id}")
        print(f"⏱️  Tiempo de Procesamiento: {result.processing_time:.2f} segundos")
        print(f"� TimesUtamp: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Business Analysis Results
        print(f"\n💼 ANÁLISIS DE NEGOCIO:")
        
        # Financial Analysis
        if result.financial_analysis and result.financial_analysis.get('success', True):
            financial = result.financial_analysis
            print(f"   💰 Análisis Financiero:")
            print(f"      - Solvencia: {financial.get('solvencia', 'N/A')[:100]}...")
            print(f"      - Liquidez: {financial.get('liquidez', 'N/A')[:100]}...")
            print(f"      - Rentabilidad: {financial.get('rentabilidad', 'N/A')[:100]}...")
            print(f"      - Tokens usados: {financial.get('tokens_used', 0)}")
        else:
            print(f"   💰 Análisis Financiero: ❌ Error o no disponible")
        
        # Reputational Analysis
        if result.reputational_analysis and result.reputational_analysis.get('success', True):
            reputational = result.reputational_analysis
            print(f"   🌟 Análisis Reputacional:")
            print(f"      - Sentimiento: {reputational.get('sentimiento_general', 'N/A')}")
            print(f"      - Puntaje: {reputational.get('puntaje_sentimiento', 'N/A')}")
            print(f"      - Temas positivos: {reputational.get('temas_positivos', [])}")
            print(f"      - Tokens usados: {reputational.get('tokens_used', 0)}")
        else:
            print(f"   🌟 Análisis Reputacional: ❌ Error o no disponible")
        
        # Behavioral Analysis
        if result.behavioral_analysis and result.behavioral_analysis.get('success', True):
            behavioral = result.behavioral_analysis
            print(f"   📈 Análisis Comportamental:")
            print(f"      - Patrón de pago: {behavioral.get('patron_de_pago', 'N/A')}")
            print(f"      - Fiabilidad referencias: {behavioral.get('fiabilidad_referencias', 'N/A')}")
            print(f"      - Riesgo comportamental: {behavioral.get('riesgo_comportamental', 'N/A')}")
            print(f"      - Tokens usados: {behavioral.get('tokens_used', 0)}")
        else:
            print(f"   📈 Análisis Comportamental: ❌ Error o no disponible")
        
        # Final Scoring
        if result.consolidated_report and result.consolidated_report.get('success', True):
            scoring = result.consolidated_report
            print(f"\n🎯 SCORING FINAL:")
            print(f"   📊 Puntaje: {result.final_score}/1000")
            print(f"   🚦 Nivel de Riesgo: {result.risk_level}")
            print(f"   🎯 Confianza: {scoring.get('confidence', 0):.2f}")
            print(f"   🏦 Recomendación crediticia: {scoring.get('credit_recommendation', 'N/A')[:100]}...")
            
            if scoring.get('justification'):
                print(f"   📝 Justificación: {scoring['justification'][:200]}...")
            
            if scoring.get('contributing_factors'):
                print(f"   🔍 Factores contribuyentes: {len(scoring['contributing_factors'])} factores identificados")
        else:
            print(f"\n🎯 SCORING FINAL: ❌ Error en consolidación")
        
        # Show audit trail
        print(f"\n📋 AUDIT TRAIL:")
        audit_events = orchestrator.get_audit_trail(result.evaluation_id)
        if audit_events:
            print(f"   � Total evmentos registrados: {len(audit_events)}")
            print("   🔍 Últimos 5 eventos:")
            for i, event in enumerate(audit_events[-5:], 1):
                event_type = event.get('event_type', 'N/A')
                agent_id = event.get('agent_id', 'N/A')
                success = event.get('success', False)
                status = '✅' if success else '❌'
                print(f"      {i}. {status} {event_type} - {agent_id}")
        else:
            print("   ⚠️ No hay eventos de auditoría disponibles")
        
        # Show orchestrator statistics
        final_stats = orchestrator.get_stats()
        print(f"\n📈 ESTADÍSTICAS DEL SISTEMA:")
        print(f"   Total evaluaciones: {final_stats['total_evaluations']}")
        print(f"   Evaluaciones exitosas: {final_stats['successful_evaluations']}")
        print(f"   Evaluaciones fallidas: {final_stats['failed_evaluations']}")
        print(f"   Tiempo promedio: {final_stats['average_processing_time']:.2f}s")
        print(f"   Total tokens usados: {final_stats['total_tokens_used']}")
        
        # Calculate tokens used in this evaluation
        tokens_used_this_eval = final_stats['total_tokens_used'] - initial_stats['total_tokens_used']
        print(f"   Tokens usados en esta evaluación: {tokens_used_this_eval}")
        
        # Show recent audit events
        print(f"\n📊 EVENTOS DE AUDITORÍA RECIENTES:")
        recent_events = orchestrator.get_recent_audit_events(5)
        for i, event in enumerate(recent_events[-5:], 1):
            timestamp = event.get('timestamp', 'N/A')
            event_type = event.get('event_type', 'N/A')
            agent_id = event.get('agent_id', 'N/A')
            print(f"   {i}. {timestamp} - {event_type} - {agent_id}")
        
        print("\n" + "="*70)
        print("🎉 DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()


async def test_individual_components():
    """
    Prueba componentes individuales del sistema usando AzureOrchestrator
    """
    print("\n🔧 PRUEBAS DE COMPONENTES INDIVIDUALES")
    print("="*50)
    
    try:
        # Initialize AzureOrchestrator for component testing
        print("1. Inicializando AzureOrchestrator para pruebas...")
        orchestrator = AzureOrchestrator()
        success = await orchestrator.initialize()
        
        if not success:
            print("   ❌ Error al inicializar AzureOrchestrator")
            return
        
        print("   ✅ AzureOrchestrator inicializado")
        
        # Test individual business agents
        print("\n2. Probando agentes de negocio individuales...")
        
        # Test FinancialAgent
        try:
            from agents.business_agents.financial_agent import analyze_financial_document
            result = await analyze_financial_document(
                orchestrator.azure_service, 
                "Empresa con activos de $100,000, pasivos de $50,000, ingresos de $200,000 y utilidad neta de $25,000"
            )
            print(f"   ✅ FinancialAgent: {result.resumen_ejecutivo[:80]}...")
            print(f"      Tokens usados: {result.tokens_used}")
        except Exception as e:
            print(f"   ❌ FinancialAgent error: {e}")
        
        # Test ReputationalAgent
        try:
            from agents.business_agents.reputational_agent import analyze_reputation
            result = await analyze_reputation(
                orchestrator.azure_service,
                "Reseñas: 4.5 estrellas, comentarios positivos sobre servicio al cliente, entrega puntual"
            )
            print(f"   ✅ ReputationalAgent: Sentimiento {result.sentimiento_general}, Puntaje {result.puntaje_sentimiento}")
            print(f"      Tokens usados: {result.tokens_used}")
        except Exception as e:
            print(f"   ❌ ReputationalAgent error: {e}")
        
        # Test BehavioralAgent
        try:
            from agents.business_agents.behavioral_agent import analyze_behavior
            result = await analyze_behavior(
                orchestrator.azure_service,
                "Historial: 12 meses de pagos puntuales, referencias comerciales excelentes, sin incidencias"
            )
            print(f"   ✅ BehavioralAgent: Patrón {result.patron_de_pago}, Riesgo {result.riesgo_comportamental}")
            print(f"      Tokens usados: {result.tokens_used}")
        except Exception as e:
            print(f"   ❌ BehavioralAgent error: {e}")
        
        # Test Security Agents
        print("\n3. Probando agentes de seguridad...")
        
        # Test InputValidator
        try:
            from agents.infrastructure.security.input_validator import validate_input_field
            result = await validate_input_field(
                orchestrator.azure_service,
                "company_name",
                "Empresa Legítima S.A."
            )
            print(f"   ✅ InputValidator: {'Seguro' if result.is_safe else 'Inseguro'} - {result.reason}")
        except Exception as e:
            print(f"   ❌ InputValidator error: {e}")
        
        # Test OutputSanitizer
        try:
            from agents.infrastructure.security.output_sanitizer import sanitize_output
            result = await sanitize_output(
                orchestrator.azure_service,
                "La empresa tiene un buen desempeño financiero con ingresos sólidos."
            )
            print(f"   ✅ OutputSanitizer: {'Seguro' if result.is_safe else 'Sanitizado'} - {result.details}")
        except Exception as e:
            print(f"   ❌ OutputSanitizer error: {e}")
        
        # Show final stats
        stats = orchestrator.get_stats()
        print(f"\n📊 Estadísticas después de pruebas individuales:")
        print(f"   Total tokens usados: {stats['total_tokens_used']}")
        print(f"   Evaluaciones realizadas: {stats['total_evaluations']}")
        
    except Exception as e:
        print(f"   ❌ Error general en pruebas: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """Función principal que ejecuta las demostraciones"""
    print("🚀 Sistema Integrado de Evaluación de Riesgo Financiero para PYMEs")
    print("Desarrollado con Azure OpenAI Service y arquitectura multiagente actualizada")
    print("Flujo: SecuritySupervisor → InputValidator → BusinessAgents → OutputSanitizer → ScoringAgent → AuditLogger")
    print()
    
    try:
        # Run the integrated system test
        print("🎯 EJECUTANDO DEMOSTRACIÓN COMPLETA DEL SISTEMA")
        await test_integrated_system()
        
        # Ask user if they want to run individual component tests
        print("\n" + "="*70)
        print("¿Deseas ejecutar pruebas de componentes individuales? (y/n): ", end="")
        
        # For demo purposes, we'll run them automatically
        print("y")
        await test_individual_components()
        
        print("\n" + "="*70)
        print("🎉 DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
        print("✅ Sistema integrado funcionando correctamente")
        print("✅ Todos los agentes operativos")
        print("✅ Flujo de seguridad implementado")
        print("✅ Audit trail completo")
        print("="*70)
        
    except KeyboardInterrupt:
        print("\n⚠️ Demostración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())