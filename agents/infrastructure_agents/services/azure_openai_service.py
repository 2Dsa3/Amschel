"""
Azure OpenAI Service Integration with Security Proxy
Integración segura con Azure OpenAI Service para agentes de infraestructura
"""

import asyncio
import logging
import json
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime
import openai
from openai import AzureOpenAI

from ..config.azure_config import AzureOpenAIConfig


@dataclass
class SecurityProxyConfig:
    """Configuración del proxy de seguridad para Azure OpenAI"""
    enable_content_filtering: bool = True
    enable_pii_detection: bool = True
    enable_audit_logging: bool = True
    max_tokens_per_request: int = 4000
    rate_limit_requests_per_minute: int = 60
    blocked_keywords: List[str] = None
    
    def __post_init__(self):
        if self.blocked_keywords is None:
            self.blocked_keywords = [
                "password", "ssn", "credit_card", "bank_account",
                "personal_id", "cedula", "ruc_personal"
            ]


@dataclass
class OpenAIRequest:
    """Solicitud a Azure OpenAI Service"""
    request_id: str
    user_id: str
    agent_id: str
    prompt: str
    max_tokens: int
    temperature: float
    timestamp: datetime
    metadata: Dict[str, Any] = None


@dataclass
class OpenAIResponse:
    """Respuesta de Azure OpenAI Service"""
    request_id: str
    response_text: str
    tokens_used: int
    processing_time_ms: int
    filtered_content: bool
    confidence_score: float
    timestamp: datetime
    metadata: Dict[str, Any] = None


class SecurityProxy:
    """
    Proxy de seguridad para Azure OpenAI Service
    Filtra contenido sensible y registra todas las interacciones
    """
    
    def __init__(self, config: SecurityProxyConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.request_count = 0
        self.last_minute_requests = []
    
    def validate_request(self, request: OpenAIRequest) -> tuple[bool, str]:
        """Valida una solicitud antes de enviarla a OpenAI"""
        
        # Rate limiting check
        if not self._check_rate_limit():
            return False, "Rate limit exceeded"
        
        # Content filtering
        if self.config.enable_content_filtering:
            if self._contains_blocked_content(request.prompt):
                return False, "Blocked content detected"
        
        # PII detection
        if self.config.enable_pii_detection:
            if self._contains_pii(request.prompt):
                return False, "PII detected in request"
        
        # Token limit check
        if request.max_tokens > self.config.max_tokens_per_request:
            return False, f"Token limit exceeded: {request.max_tokens} > {self.config.max_tokens_per_request}"
        
        return True, "Request validated"
    
    def _check_rate_limit(self) -> bool:
        """Verifica límites de rate limiting"""
        current_time = datetime.now()
        
        # Remove requests older than 1 minute
        self.last_minute_requests = [
            req_time for req_time in self.last_minute_requests
            if (current_time - req_time).seconds < 60
        ]
        
        # Check if we're under the limit
        if len(self.last_minute_requests) >= self.config.rate_limit_requests_per_minute:
            return False
        
        self.last_minute_requests.append(current_time)
        return True
    
    def _contains_blocked_content(self, text: str) -> bool:
        """Detecta contenido bloqueado en el texto"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.config.blocked_keywords)
    
    def _contains_pii(self, text: str) -> bool:
        """Detecta información personal identificable"""
        # Simple PII detection patterns
        import re
        
        # Ecuadorian ID patterns
        cedula_pattern = r'\b\d{10}\b'
        ruc_pattern = r'\b\d{13}\b'
        phone_pattern = r'\b\d{9,10}\b'
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        patterns = [cedula_pattern, ruc_pattern, phone_pattern, email_pattern]
        
        for pattern in patterns:
            if re.search(pattern, text):
                return True
        
        return False
    
    def sanitize_response(self, response: str) -> str:
        """Sanitiza la respuesta de OpenAI"""
        # Remove any potential PII from response
        import re
        
        # Mask potential sensitive information
        response = re.sub(r'\b\d{10}\b', '[CEDULA_MASKED]', response)
        response = re.sub(r'\b\d{13}\b', '[RUC_MASKED]', response)
        response = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_MASKED]', response)
        
        return response
    
    def log_interaction(self, request: OpenAIRequest, response: OpenAIResponse, success: bool):
        """Registra la interacción para auditoría"""
        if self.config.enable_audit_logging:
            log_entry = {
                "request_id": request.request_id,
                "user_id": request.user_id,
                "agent_id": request.agent_id,
                "timestamp": request.timestamp.isoformat(),
                "success": success,
                "tokens_used": response.tokens_used if response else 0,
                "processing_time_ms": response.processing_time_ms if response else 0,
                "filtered_content": response.filtered_content if response else False
            }
            
            self.logger.info(f"OpenAI Interaction: {json.dumps(log_entry)}")


class AzureOpenAIService:
    """
    Servicio seguro para integración con Azure OpenAI
    Incluye proxy de seguridad y manejo de errores
    Soporta múltiples modelos (GPT-4o y o3-mini)
    """
    
    def __init__(self, config: AzureOpenAIConfig, security_config: SecurityProxyConfig = None):
        self.config = config
        self.security_proxy = SecurityProxy(security_config or SecurityProxyConfig())
        self.logger = logging.getLogger(__name__)
        
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            api_key=config.api_key,
            api_version=config.api_version,
            azure_endpoint=config.endpoint
        )
        
        self.logger.info(f"Azure OpenAI Service initialized with models: {config.deployment_name} (primary), {config.deployment_name_mini} (mini)")
    
    async def generate_completion(self, 
                                request: OpenAIRequest,
                                system_prompt: str = None,
                                use_mini_model: bool = False) -> OpenAIResponse:
        """Genera completion usando Azure OpenAI con validación de seguridad"""
        
        start_time = datetime.now()
        
        # Validate request through security proxy
        is_valid, validation_message = self.security_proxy.validate_request(request)
        if not is_valid:
            self.logger.warning(f"Request validation failed: {validation_message}")
            raise ValueError(f"Request validation failed: {validation_message}")
        
        try:
            # Prepare messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": request.prompt})
            
            # Select model based on use_mini_model flag
            model_to_use = self.config.deployment_name_mini if use_mini_model else self.config.deployment_name
            model_name = self.config.model_name_mini if use_mini_model else self.config.model_name
            
            # Prepare parameters based on model type
            params = {
                "model": model_to_use,
                "messages": messages
            }
            
            # o3-mini has different parameter requirements
            if use_mini_model and "o3" in model_to_use.lower():
                # o3-mini only supports basic parameters
                params["max_completion_tokens"] = request.max_tokens
                # o3-mini doesn't support temperature, top_p, etc.
            else:
                # GPT-4o supports all parameters
                params.update({
                    "max_tokens": request.max_tokens,
                    "temperature": request.temperature,
                    "top_p": 0.95,
                    "frequency_penalty": 0,
                    "presence_penalty": 0
                })
            
            # Make API call
            response = self.client.chat.completions.create(**params)
            
            # Extract response
            response_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            # Sanitize response
            sanitized_text = self.security_proxy.sanitize_response(response_text)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Create response object
            openai_response = OpenAIResponse(
                request_id=request.request_id,
                response_text=sanitized_text,
                tokens_used=tokens_used,
                processing_time_ms=int(processing_time),
                filtered_content=sanitized_text != response_text,
                confidence_score=0.95,  # Would be calculated based on response quality
                timestamp=datetime.now(),
                metadata={"model": self.config.model_name}
            )
            
            # Log interaction
            self.security_proxy.log_interaction(request, openai_response, True)
            
            return openai_response
            
        except Exception as e:
            self.logger.error(f"OpenAI API call failed: {e}")
            
            # Log failed interaction
            self.security_proxy.log_interaction(request, None, False)
            
            raise
    
    async def generate_financial_analysis(self, 
                                        company_data: Dict[str, Any],
                                        agent_id: str,
                                        user_id: str = "system") -> OpenAIResponse:
        """Genera análisis financiero usando prompts especializados"""
        
        system_prompt = """
        Eres un experto analista financiero especializado en evaluación de riesgo crediticio para PYMEs.
        Tu tarea es analizar los datos financieros proporcionados y generar un análisis detallado.
        
        Debes considerar:
        - Ratios de liquidez y solvencia
        - Tendencias de ingresos y gastos
        - Capacidad de pago
        - Estabilidad financiera
        
        Proporciona un análisis estructurado con puntuaciones numéricas y explicaciones claras.
        """
        
        prompt = f"""
        Analiza los siguientes datos financieros de una PYME:
        
        Datos Financieros:
        {json.dumps(company_data, indent=2, ensure_ascii=False)}
        
        Proporciona un análisis que incluya:
        1. Puntuación de liquidez (0-1)
        2. Puntuación de solvencia (0-1)
        3. Puntuación de rentabilidad (0-1)
        4. Puntuación general financiera (0-1)
        5. Factores de riesgo identificados
        6. Recomendaciones específicas
        """
        
        request = OpenAIRequest(
            request_id=f"financial_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            user_id=user_id,
            agent_id=agent_id,
            prompt=prompt,
            max_tokens=2000,
            temperature=0.3,
            timestamp=datetime.now(),
            metadata={"analysis_type": "financial"}
        )
        
        return await self.generate_completion(request, system_prompt)
    
    async def generate_risk_explanation(self,
                                      scoring_data: Dict[str, Any],
                                      agent_id: str,
                                      user_id: str = "system") -> OpenAIResponse:
        """Genera explicación detallada del scoring de riesgo"""
        
        system_prompt = """
        Eres un experto en explicabilidad de modelos de riesgo crediticio.
        Tu tarea es generar explicaciones claras y comprensibles sobre las decisiones de scoring.
        
        Debes:
        - Explicar los factores más importantes que influyen en el score
        - Proporcionar recomendaciones específicas para mejorar el perfil de riesgo
        - Usar lenguaje claro y profesional
        - Incluir ejemplos concretos cuando sea apropiado
        """
        
        prompt = f"""
        Genera una explicación detallada para el siguiente scoring de riesgo:
        
        Datos de Scoring:
        {json.dumps(scoring_data, indent=2, ensure_ascii=False)}
        
        La explicación debe incluir:
        1. Resumen del nivel de riesgo
        2. Factores principales que influyen en el score
        3. Áreas de fortaleza identificadas
        4. Áreas de mejora recomendadas
        5. Impacto potencial de mejoras específicas
        6. Recomendaciones de crédito justificadas
        """
        
        request = OpenAIRequest(
            request_id=f"explanation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            user_id=user_id,
            agent_id=agent_id,
            prompt=prompt,
            max_tokens=2500,
            temperature=0.2,
            timestamp=datetime.now(),
            metadata={"analysis_type": "explanation"}
        )
        
        return await self.generate_completion(request, system_prompt)
    
    async def generate_scenario_analysis(self,
                                       scenario_data: Dict[str, Any],
                                       agent_id: str,
                                       user_id: str = "system") -> OpenAIResponse:
        """Genera análisis de escenarios de simulación"""
        
        system_prompt = """
        Eres un experto en análisis de escenarios financieros y simulaciones de riesgo.
        Tu tarea es analizar diferentes escenarios y proporcionar insights valiosos.
        
        Debes:
        - Comparar escenarios de manera objetiva
        - Identificar los cambios más impactantes
        - Evaluar la viabilidad de los escenarios
        - Proporcionar recomendaciones estratégicas
        """
        
        prompt = f"""
        Analiza los siguientes escenarios de simulación:
        
        Datos de Escenarios:
        {json.dumps(scenario_data, indent=2, ensure_ascii=False)}
        
        Proporciona un análisis que incluya:
        1. Comparación entre escenarios
        2. Variables con mayor impacto en el scoring
        3. Escenarios más y menos favorables
        4. Viabilidad de cada escenario
        5. Recomendaciones estratégicas
        6. Riesgos y oportunidades identificados
        """
        
        request = OpenAIRequest(
            request_id=f"scenario_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            user_id=user_id,
            agent_id=agent_id,
            prompt=prompt,
            max_tokens=2000,
            temperature=0.4,
            timestamp=datetime.now(),
            metadata={"analysis_type": "scenario"}
        )
        
        return await self.generate_completion(request, system_prompt)
    
    # === MÉTODOS ESPECÍFICOS PARA CADA MODELO ===
    
    async def generate_quick_validation(self,
                                      data: Dict[str, Any],
                                      validation_type: str,
                                      agent_id: str,
                                      user_id: str = "system") -> OpenAIResponse:
        """Genera validaciones rápidas usando o3-mini (más económico y rápido)"""
        
        system_prompt = """
        Eres un validador rápido y eficiente. Tu tarea es validar datos de manera concisa.
        Responde de forma directa y estructurada.
        """
        
        prompt = f"""
        Valida los siguientes datos para {validation_type}:
        
        Datos:
        {json.dumps(data, indent=2, ensure_ascii=False)}
        
        Proporciona:
        1. Estado: VÁLIDO/INVÁLIDO
        2. Errores encontrados (si los hay)
        3. Recomendaciones breves
        """
        
        request = OpenAIRequest(
            request_id=f"validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            user_id=user_id,
            agent_id=agent_id,
            prompt=prompt,
            max_tokens=500,  # Menos tokens para validaciones rápidas
            temperature=0.1,  # Más determinístico
            timestamp=datetime.now(),
            metadata={"analysis_type": "quick_validation", "validation_type": validation_type}
        )
        
        # Usar o3-mini para validaciones rápidas
        return await self.generate_completion(request, system_prompt, use_mini_model=True)
    
    async def generate_complex_analysis(self,
                                      data: Dict[str, Any],
                                      analysis_type: str,
                                      agent_id: str,
                                      user_id: str = "system") -> OpenAIResponse:
        """Genera análisis complejos usando GPT-4o (más potente para análisis profundos)"""
        
        system_prompt = """
        Eres un analista experto especializado en análisis financiero profundo.
        Tu tarea es proporcionar análisis detallados, insights profundos y recomendaciones estratégicas.
        Usa tu conocimiento avanzado para identificar patrones complejos y riesgos sutiles.
        """
        
        prompt = f"""
        Realiza un análisis complejo de tipo {analysis_type} para los siguientes datos:
        
        Datos:
        {json.dumps(data, indent=2, ensure_ascii=False)}
        
        Proporciona un análisis exhaustivo que incluya:
        1. Análisis detallado de cada componente
        2. Identificación de patrones y tendencias
        3. Evaluación de riesgos y oportunidades
        4. Comparación con benchmarks del sector
        5. Recomendaciones estratégicas específicas
        6. Proyecciones y escenarios futuros
        """
        
        request = OpenAIRequest(
            request_id=f"complex_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            user_id=user_id,
            agent_id=agent_id,
            prompt=prompt,
            max_tokens=3000,  # Más tokens para análisis complejos
            temperature=0.3,
            timestamp=datetime.now(),
            metadata={"analysis_type": "complex_analysis", "analysis_subtype": analysis_type}
        )
        
        # Usar GPT-4o para análisis complejos
        return await self.generate_completion(request, system_prompt, use_mini_model=False)
    
    async def generate_summary(self,
                             data: Dict[str, Any],
                             summary_type: str,
                             agent_id: str,
                             user_id: str = "system") -> OpenAIResponse:
        """Genera resúmenes concisos usando o3-mini"""
        
        system_prompt = """
        Eres un experto en crear resúmenes concisos y claros.
        Tu tarea es extraer los puntos más importantes y presentarlos de manera estructurada.
        """
        
        prompt = f"""
        Crea un resumen conciso de tipo {summary_type} para:
        
        Datos:
        {json.dumps(data, indent=2, ensure_ascii=False)}
        
        Resumen debe incluir:
        1. Puntos clave (máximo 5)
        2. Conclusión principal
        3. Acción recomendada
        """
        
        request = OpenAIRequest(
            request_id=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            user_id=user_id,
            agent_id=agent_id,
            prompt=prompt,
            max_tokens=800,
            temperature=0.2,
            timestamp=datetime.now(),
            metadata={"analysis_type": "summary", "summary_type": summary_type}
        )
        
        # Usar o3-mini para resúmenes
        return await self.generate_completion(request, system_prompt, use_mini_model=True)
    
    def get_model_recommendations(self, task_type: str) -> Dict[str, Any]:
        """Recomienda qué modelo usar según el tipo de tarea"""
        
        # Tareas que deben usar o3-mini (rápido y económico)
        mini_model_tasks = [
            "validation",
            "summary",
            "simple_classification",
            "data_extraction",
            "format_conversion",
            "quick_check"
        ]
        
        # Tareas que deben usar GPT-4o (análisis complejo)
        complex_model_tasks = [
            "financial_analysis",
            "risk_assessment",
            "scenario_analysis",
            "strategic_planning",
            "complex_reasoning",
            "explanation_generation"
        ]
        
        if task_type in mini_model_tasks:
            return {
                "recommended_model": "o3-mini",
                "model_deployment": self.config.deployment_name_mini,
                "reason": "Task is suitable for fast, cost-effective processing",
                "estimated_cost": "low",
                "estimated_speed": "fast"
            }
        elif task_type in complex_model_tasks:
            return {
                "recommended_model": "gpt-4o",
                "model_deployment": self.config.deployment_name,
                "reason": "Task requires advanced reasoning and analysis",
                "estimated_cost": "higher",
                "estimated_speed": "moderate"
            }
        else:
            return {
                "recommended_model": "gpt-4o",
                "model_deployment": self.config.deployment_name,
                "reason": "Default to more capable model for unknown tasks",
                "estimated_cost": "higher",
                "estimated_speed": "moderate"
            }
    
    def get_service_health(self) -> Dict[str, Any]:
        """Verifica el estado de salud del servicio OpenAI"""
        try:
            # Test connection with a simple request
            test_response = self.client.chat.completions.create(
                model=self.config.deployment_name,
                messages=[{"role": "user", "content": "Test connection"}],
                max_tokens=10
            )
            
            return {
                "status": "healthy",
                "endpoint": self.config.endpoint,
                "model": self.config.deployment_name,
                "last_check": datetime.now().isoformat(),
                "response_time_ms": 100  # Would measure actual response time
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "endpoint": self.config.endpoint,
                "last_check": datetime.now().isoformat()
            }
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de uso del servicio"""
        return {
            "total_requests": self.security_proxy.request_count,
            "requests_last_minute": len(self.security_proxy.last_minute_requests),
            "rate_limit": self.security_proxy.config.rate_limit_requests_per_minute,
            "security_filtering_enabled": self.security_proxy.config.enable_content_filtering,
            "pii_detection_enabled": self.security_proxy.config.enable_pii_detection
        }