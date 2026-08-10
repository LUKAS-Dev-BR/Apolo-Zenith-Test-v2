from enum import Enum
from typing import Dict, Any

class ReasoningMode(Enum):
    NORMAL = "normal"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    ULTRA_HIGH = "ultra_high"
    ULTRA_MEGA_HIGH = "ultra_mega_high"

class ReasoningEngine:
    def __init__(self):
        self.modes = {
            ReasoningMode.NORMAL: {
                "depth": 1,
                "max_tokens": 1024,
                "temperature": 0.7,
                "top_p": 0.9,
                "repetition_penalty": 1.1,
                "thinking_steps": 1,
                "analysis_level": "básico"
            },
            ReasoningMode.MEDIUM: {
                "depth": 2,
                "max_tokens": 2048,
                "temperature": 0.6,
                "top_p": 0.85,
                "repetition_penalty": 1.15,
                "thinking_steps": 2,
                "analysis_level": "intermediário"
            },
            ReasoningMode.HIGH: {
                "depth": 4,
                "max_tokens": 4096,
                "temperature": 0.5,
                "top_p": 0.8,
                "repetition_penalty": 1.2,
                "thinking_steps": 4,
                "analysis_level": "avançado"
            },
            ReasoningMode.VERY_HIGH: {
                "depth": 8,
                "max_tokens": 8192,
                "temperature": 0.4,
                "top_p": 0.75,
                "repetition_penalty": 1.25,
                "thinking_steps": 8,
                "analysis_level": "profundo"
            },
            ReasoningMode.ULTRA_HIGH: {
                "depth": 16,
                "max_tokens": 16384,
                "temperature": 0.3,
                "top_p": 0.7,
                "repetition_penalty": 1.3,
                "thinking_steps": 16,
                "analysis_level": "extremo"
            },
            ReasoningMode.ULTRA_MEGA_HIGH: {
                "depth": 32,
                "max_tokens": 32768,
                "temperature": 0.2,
                "top_p": 0.65,
                "repetition_penalty": 1.35,
                "thinking_steps": 32,
                "analysis_level": "máximo"
            }
        }
        
    def get_config(self, mode: ReasoningMode) -> Dict[str, Any]:
        return self.modes.get(mode, self.modes[ReasoningMode.NORMAL])
    
    def process_with_reasoning(self, prompt: str, mode: ReasoningMode, llm_generate_func) -> str:
        config = self.get_config(mode)
        
        thinking_prompt = self._create_thinking_prompt(prompt, config)
        
        output = llm_generate_func(thinking_prompt, mode.value)
        
        if config["depth"] > 1:
            output = self._self_review(output, config)
        
        return output
    
    def _create_thinking_prompt(self, prompt: str, config: Dict) -> str:
        thinking_steps = config["thinking_steps"]
        
        thinking_template = f"""Analise o seguinte prompt cuidadosamente em {thinking_steps} etapas de raciocínio:

Prompt: {prompt}

Etapa de Análise:
1. Compreenda o contexto e os requisitos
2. Identifique os pontos principais
3. Considere diferentes perspectivas
4. Formule uma resposta completa e precisa

Nível de Análise: {config['analysis_level']}
Profundidade de Raciocínio: {config['depth']} camadas

Resposta:"""
        
        return thinking_template
    
    def _self_review(self, output: str, config: Dict) -> str:
        review_template = f"""Revise e refine a seguinte resposta com atenção aos detalhes:

Resposta Original:
{output}

Critérios de Revisão:
- Precisão técnica
- Completude da informação
- Clareza na comunicação
- Consistência lógica

Resposta Refinada:"""
        
        return output
    
    def analyze_complexity(self, prompt: str) -> ReasoningMode:
        complexity_score = 0
        
        technical_terms = ["implementar", "desenvolver", "criar", "programar", "código", "algoritmo", "função", "classe"]
        for term in technical_terms:
            if term.lower() in prompt.lower():
                complexity_score += 1
        
        if len(prompt) > 500:
            complexity_score += 2
        elif len(prompt) > 200:
            complexity_score += 1
        
        question_words = ["como", "por que", "explique", "descreva", "analise"]
        for word in question_words:
            if word.lower() in prompt.lower():
                complexity_score += 1
        
        if complexity_score >= 6:
            return ReasoningMode.ULTRA_MEGA_HIGH
        elif complexity_score >= 5:
            return ReasoningMode.ULTRA_HIGH
        elif complexity_score >= 4:
            return ReasoningMode.VERY_HIGH
        elif complexity_score >= 3:
            return ReasoningMode.HIGH
        elif complexity_score >= 2:
            return ReasoningMode.MEDIUM
        else:
            return ReasoningMode.NORMAL
