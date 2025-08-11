#!/usr/bin/env python3
"""
Debug específico del agente financiero
"""

import asyncio
from dotenv import load_dotenv
from agents.azure_orchestrator import AzureOrchestrator
from agents.business_agents.financial_agent import analyze_financial_document

async def test_financial_agent():
    """Prueba específica del agente financiero"""
    
    load_dotenv()
    
    # Inicializar orchestrator
    orchestrator = AzureOrchestrator()
    success = await orchestrator.initialize()
    
    if not success:
        print("❌ Error al inicializar el orquestador")
        return
    
    print("🏦 PROBANDO AGENTE FINANCIERO")
    print("=" * 50)
    
    # Datos financieros de prueba
    financial_data = """
    ESTADO FINANCIERO - MEGASTORE RETAIL CHAIN S.A.
    Período: Enero - Diciembre 2023
    
    BALANCE GENERAL:
    Activos Totales: $25,000,000
    - Activos Corrientes: $12,000,000
    - Efectivo: $2,500,000
    - Inventarios: $8,000,000
    - Cuentas por cobrar: $1,500,000
    - Activos Fijos: $13,000,000
    
    Pasivos Totales: $18,000,000
    - Pasivos Corrientes: $8,500,000
    - Deuda a largo plazo: $9,500,000
    
    Patrimonio: $7,000,000
    
    ESTADO DE RESULTADOS:
    Ingresos: $45,000,000
    Utilidad Neta: $1,800,000
    Flujo de Caja: $3,200,000
    Margen de Utilidad: 4%
    ROE: 25.7%
    Ratio Deuda/Patrimonio: 2.57
    """
    
    print(f"📋 Datos financieros:")
    print(f"   {financial_data[:200]}...")
    
    try:
        print(f"\n🔄 Ejecutando análisis financiero...")
        result = await analyze_financial_document(orchestrator.azure_service, financial_data)
        
        print(f"\n📊 RESULTADO:")
        print(f"   ✅ Éxito: {result.success}")
        print(f"   🎫 Tokens: {result.tokens_used}")
        print(f"   💰 Solvencia: {result.solvencia}")
        print(f"   💧 Liquidez: {result.liquidez}")
        print(f"   📈 Rentabilidad: {result.rentabilidad}")
        print(f"   📊 Tendencia Ventas: {result.tendencia_ventas}")
        print(f"   📝 Resumen: {result.resumen_ejecutivo[:100]}...")
        
        # Verificar si hay problemas
        if result.solvencia == "N/A" or "N/A" in result.solvencia:
            print(f"\n🚨 PROBLEMA DETECTADO: Solvencia devuelve N/A")
        
        if result.liquidez == "N/A" or "N/A" in result.liquidez:
            print(f"🚨 PROBLEMA DETECTADO: Liquidez devuelve N/A")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

async def main():
    await test_financial_agent()

if __name__ == "__main__":
    asyncio.run(main())

    # Empresa 2: Retail - Perfil medio con algunos problemas
    companies.append(CompanyData(
        company_id="RETAIL002",
        company_name="MegaStore Retail Chain S.A.",
        financial_statements="""
        ESTADO FINANCIERO - MEGASTORE RETAIL CHAIN S.A.
        Período: Enero - Diciembre 2023
        
        BALANCE GENERAL:
        Activos Totales: $25,000,000
        - Activos Corrientes: $12,000,000
        - Efectivo: $2,500,000
        - Inventarios: $8,000,000
        - Cuentas por cobrar: $1,500,000
        - Activos Fijos: $13,000,000
        
        Pasivos Totales: $18,000,000
        - Pasivos Corrientes: $8,500,000
        - Deuda a largo plazo: $9,500,000
        
        Patrimonio: $7,000,000
        
        ESTADO DE RESULTADOS:
        Ingresos: $45,000,000
        Utilidad Neta: $1,800,000
        Flujo de Caja: $3,200,000
        Margen de Utilidad: 4%
        ROE: 25.7%
        Ratio Deuda/Patrimonio: 2.57
        """,
        social_media_data="""
        ANÁLISIS DE REPUTACIÓN DIGITAL - MEGASTORE RETAIL
        
        Google Reviews: 3.1/5 estrellas (2,341 reseñas)
        - "Buenos precios pero servicio al cliente mejorable"
        - "Variedad de productos, pero largas colas"
        - "Algunas sucursales mejor que otras"
        - "Promociones atractivas en temporadas"
        
        Yelp: 2.8/5 estrellas (567 reseñas)
        - Quejas sobre tiempos de espera
        - Problemas ocasionales con devoluciones
        
        Facebook: 45,000 seguidores
        - Engagement moderado
        - Respuestas a quejas en 24-48 horas
        
        Incidentes: Disputa laboral resuelta en 2023
        """,
        commercial_references="""
        REFERENCIAS COMERCIALES - MEGASTORE RETAIL
        
        1. Banco Guayaquil (Cliente desde 2015)
        - Línea de crédito: $5,000,000
        - Comportamiento: Regular
        - Algunos retrasos menores
        - Calificación: B+
        
        2. Proveedor Unilever (5 años)
        - Límite comercial: $1,200,000
        - Pagos promedio: 45 días
        - Ocasionales retrasos de 7-15 días
        - Relación comercial estable
        
        3. Proveedor Nestlé (8 años)
        - Volumen anual: $8,000,000
        - Pagos irregulares pero cumple
        - Requiere seguimiento constante
        """,
        payment_history="""
        HISTORIAL DE PAGOS - ÚLTIMOS 12 MESES
        
        2024:
        - Enero: Retraso 15 días
        - Febrero: Pago puntual
        - Marzo: Retraso 7 días
        - Abril: Retraso 10 días
        - Mayo: Pago puntual
        - Junio: Retraso 5 días
        
        Promedio días de pago: 38 días
        Términos de pago: 30 días
        Score crediticio: 650/900
        
        Resumen: 60% pagos puntuales, requiere seguimiento
        """,
        metadata={
            "industry": "retail",
            "test_type": "medium_risk_company",
            "risk_profile": "medium"
        }
    ))
    
    # Empresa 3: Manufactura - Perfil excelente
    companies.append(CompanyData(
        company_id="MANUF003",
        company_name="Precision Manufacturing Corp S.A.",
        financial_statements="""
        ESTADO FINANCIERO - PRECISION MANUFACTURING CORP S.A.
        Período: Enero - Diciembre 2023
        
        BALANCE GENERAL:
        Activos Totales: $28,000,000
        - Activos Corrientes: $8,500,000
        - Efectivo: $3,200,000
        - Cuentas por cobrar: $3,800,000
        - Inventarios: $1,500,000
        - Activos Fijos: $19,500,000
        
        Pasivos Totales: $12,000,000
        - Pasivos Corrientes: $4,200,000
        - Deuda a largo plazo: $7,800,000
        
        Patrimonio: $16,000,000
        
        ESTADO DE RESULTADOS:
        Ingresos: $32,000,000
        Utilidad Neta: $4,800,000
        Flujo de Caja: $5,200,000
        Margen de Utilidad: 15%
        ROE: 30%
        Ratio Deuda/Patrimonio: 0.75
        """,
        social_media_data="""
        ANÁLISIS DE REPUTACIÓN DIGITAL - PRECISION MANUFACTURING
        
        Google Reviews: 4.5/5 estrellas (78 reseñas)
        - "Calidad excepcional en todos sus productos"
        - "Cumplimiento perfecto de tiempos de entrega"
        - "Empresa seria y confiable"
        - "Excelente servicio postventa"
        
        Better Business Bureau: 4.1/5 estrellas (23 reseñas)
        - Sin quejas sin resolver
        - Respuesta rápida a consultas
        
        LinkedIn: 1,800 seguidores
        - Contenido técnico especializado
        - Participación en ferias industriales
        
        Certificaciones: ISO 14001, ISO 45001, IATF 16949
        Premios: Excellence in Manufacturing 2023, Green Business Award
        """,
        commercial_references="""
        REFERENCIAS COMERCIALES - PRECISION MANUFACTURING
        
        1. Banco del Pacífico (Cliente desde 2010)
        - Línea de crédito: $8,000,000
        - Comportamiento: Excelente
        - Pagos anticipados frecuentes
        - Calificación: AAA+
        
        2. General Motors Ecuador (Cliente, 12 años)
        - Contrato anual: $15,000,000
        - Proveedor preferencial
        - Certificación de calidad A1
        - Renovación automática
        
        3. Aceros del Ecuador (Proveedor, 15 años)
        - Límite comercial: $2,000,000
        - Pagos siempre puntuales
        - Descuentos por pronto pago
        - Relación ejemplar
        """,
        payment_history="""
        HISTORIAL DE PAGOS - ÚLTIMOS 24 MESES
        
        2023-2024: Historial impecable
        - 100% pagos puntuales o anticipados
        - Promedio días de pago: 18 días
        - Términos de pago: 30 días
        - 40% pagos anticipados
        - Score crediticio: 920/900 (excepcional)
        
        Sin reportes negativos en centrales de riesgo
        Historial crediticio limpio por 22 años
        
        Resumen: Excelente, cliente modelo
        """,
        metadata={
            "industry": "manufacturing",
            "test_type": "excellent_company",
            "risk_profile": "very_low"
        }
    ))
    
    # Empresa 4: Startup - Perfil riesgoso pero prometedor
    companies.append(CompanyData(
        company_id="STARTUP004",
        company_name="GreenEnergy Innovations S.A.",
        financial_statements="""
        ESTADO FINANCIERO - GREENENERGY INNOVATIONS S.A.
        Período: Enero - Diciembre 2023
        
        BALANCE GENERAL:
        Activos Totales: $3,500,000
        - Activos Corrientes: $1,200,000
        - Efectivo: $400,000
        - Cuentas por cobrar: $600,000
        - Inventarios: $200,000
        - Activos Fijos: $2,300,000
        
        Pasivos Totales: $2,100,000
        - Pasivos Corrientes: $800,000
        - Deuda a largo plazo: $1,300,000
        
        Patrimonio: $1,400,000
        
        ESTADO DE RESULTADOS:
        Ingresos: $2,800,000
        Pérdida Neta: ($450,000)
        Flujo de Caja: $150,000
        Margen de Utilidad: -16%
        ROE: -32%
        Ratio Deuda/Patrimonio: 1.5
        """,
        social_media_data="""
        ANÁLISIS DE REPUTACIÓN DIGITAL - GREENENERGY INNOVATIONS
        
        Google Reviews: 4.7/5 estrellas (34 reseñas)
        - "Innovación increíble en energía renovable"
        - "Equipo joven y muy comprometido"
        - "Proyectos sostenibles de alta calidad"
        - "Futuro prometedor en el sector"
        
        LinkedIn: 1,250 seguidores
        - Alto engagement en contenido
        - Reconocimiento en medios especializados
        - Participación en eventos de sostenibilidad
        
        Medios:
        - Artículo en Forbes Ecuador: "Startups que cambiarán el futuro"
        - Mención en El Comercio: "Innovación energética nacional"
        
        Certificaciones: B Corp Certified
        Premios: Clean Tech Innovation Award 2024
        """,
        commercial_references="""
        REFERENCIAS COMERCIALES - GREENENERGY INNOVATIONS
        
        1. Banco Bolivariano (Cliente desde 2022)
        - Línea de crédito: $500,000
        - Comportamiento: Bueno con seguimiento
        - Pagos ocasionalmente tardíos
        - Calificación: B
        
        2. CFN - Corporación Financiera Nacional
        - Crédito de desarrollo: $1,200,000
        - Programa de apoyo a startups
        - Cumplimiento de metas: 85%
        - Potencial de crecimiento: Alto
        
        3. Cliente Ministerio de Energía
        - Proyecto piloto: $800,000
        - Resultados satisfactorios
        - Posible expansión del contrato
        """,
        payment_history="""
        HISTORIAL DE PAGOS - ÚLTIMOS 18 MESES
        
        2023-2024:
        - Enero: Pago puntual
        - Febrero: Retraso 3 días
        - Marzo: Pago puntual
        - Abril: Pago puntual
        - Mayo: Retraso 2 días
        - Junio: Pago puntual
        
        Promedio días de pago: 32 días
        Términos de pago: 30 días
        Score crediticio: 580/900 (en construcción)
        
        Resumen: 80% pagos puntuales, empresa joven en crecimiento
        """,
        metadata={
            "industry": "renewable_energy",
            "test_type": "startup_company",
            "risk_profile": "high_potential"
        }
    ))
    
    # Empresa 5: Construcción - Perfil problemático
    companies.append(CompanyData(
        company_id="LEGACY005",
        company_name="Heritage Construction Ltd.",
        financial_statements="""
        ESTADO FINANCIERO - HERITAGE CONSTRUCTION LTD.
        Período: Enero - Diciembre 2023
        
        BALANCE GENERAL:
        Activos Totales: $15,200,000
        - Activos Corrientes: $5,600,000
        - Efectivo: $800,000
        - Cuentas por cobrar: $3,200,000
        - Inventarios: $1,600,000
        - Activos Fijos: $9,600,000
        
        Pasivos Totales: $11,800,000
        - Pasivos Corrientes: $4,200,000
        - Deuda a largo plazo: $7,600,000
        
        Patrimonio: $3,400,000
        
        ESTADO DE RESULTADOS:
        Ingresos: $18,500,000
        Utilidad Neta: $925,000
        Flujo de Caja: $1,850,000
        Margen de Utilidad: 5%
        ROE: 27%
        Ratio Deuda/Patrimonio: 3.47
        """,
        social_media_data="""
        ANÁLISIS DE REPUTACIÓN DIGITAL - HERITAGE CONSTRUCTION
        
        Google Reviews: 2.9/5 estrellas (145 reseñas)
        - "Trabajos de calidad pero muy lentos"
        - "Problemas con cumplimiento de fechas"
        - "Precios competitivos pero servicio deficiente"
        - "Varios proyectos con retrasos significativos"
        
        Better Business Bureau: 2.1/5 estrellas (67 reseñas)
        - 12 quejas sin resolver
        - Problemas recurrentes con clientes
        - Respuesta lenta a reclamos
        
        Medios:
        - Artículo negativo en El Universo: "Constructora con múltiples demandas"
        - Mención en Teleamazonas: "Problemas en obra pública"
        
        Incidentes legales:
        - Disputa contractual activa (2024)
        - Violación de seguridad resuelta (2023)
        """,
        commercial_references="""
        REFERENCIAS COMERCIALES - HERITAGE CONSTRUCTION
        
        1. Banco Internacional (Cliente desde 2010)
        - Línea de crédito: $3,000,000
        - Comportamiento: Problemático
        - Múltiples reestructuraciones
        - Calificación: C+
        
        2. Proveedor Cemento Chimborazo (10 años)
        - Límite comercial: $800,000
        - Pagos consistentemente tardíos
        - Requiere garantías adicionales
        - Relación tensa
        
        3. Ex-cliente Municipio de Quito
        - Contrato terminado anticipadamente
        - Problemas de cumplimiento
        - Demanda legal en proceso
        - Referencia negativa
        """,
        payment_history="""
        HISTORIAL DE PAGOS - ÚLTIMOS 12 MESES
        
        2024:
        - Enero: Retraso 30 días
        - Febrero: Retraso 45 días
        - Marzo: Retraso 20 días
        - Abril: Retraso 25 días
        - Mayo: Retraso 15 días
        - Junio: Retraso 35 días
        
        Promedio días de pago: 58 días
        Términos de pago: 30 días
        Score crediticio: 420/900 (problemático)
        
        Múltiples reportes negativos en centrales de riesgo
        
        Resumen: 0% pagos puntuales, alto riesgo crediticio
        """,
        metadata={
            "industry": "construction",
            "test_type": "problematic_company",
            "risk_profile": "high_risk"
        }
    ))