import re
from typing import List, Tuple

class ContentFilter:
    def __init__(self):
        self.blocked_patterns = [
            r'\b(kill|murder|assassinate|execute)\b',
            r'\b(suicide|self[-\s]harm|cut myself)\b',
            r'\b(explicit|pornographic|nsfw)\b',
            r'\b(hack|exploit|malware|virus)\b',
            r'\b(bomb|weapon|gun|firearm)\b',
            r'\b(drug|cocaine|heroin|methamphetamine)\b',
            r'\b(racist|sexist|homophobic|transphobic)\b',
            r'\b(deepfake|fake|forgery|counterfeit)\b',
            r'\b(human trafficking|slavery|exploitation)\b'
        ]
        
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.blocked_patterns]
        
    def check_input(self, text: str) -> Tuple[bool, str]:
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return False, "Conteúdo bloqueado por violar os termos de segurança"
        
        return True, "Aprovado"
    
    def check_output(self, text: str) -> Tuple[bool, str]:
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return False, "Saída bloqueada por violar os termos de segurança"
        
        return True, "Aprovado"

class TokenMatcher:
    def __init__(self):
        self.sensitive_tokens = {
            'violência': ['matar', 'assassinar', 'executar', 'eliminar'],
            'exploração': ['tráfico', 'escravidão', 'exploração'],
            'drogas': ['cocaína', 'heroína', 'metanfetamina', 'maconha'],
            'discriminação': ['racismo', 'sexismo', 'homofobia', 'transfobia'],
            'ilegal': ['hackear', 'explorar', 'malware', 'vírus']
        }
        
    def match_tokens(self, text: str) -> List[str]:
        text_lower = text.lower()
        matched_categories = []
        
        for category, tokens in self.sensitive_tokens.items():
            for token in tokens:
                if token in text_lower:
                    matched_categories.append(category)
                    break
        
        return matched_categories

class OutputAnalyzer:
    def __init__(self):
        self.anomaly_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe[^>]*>',
            r'<object[^>]*>',
            r'<embed[^>]*>'
        ]
        
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.anomaly_patterns]
        
    def analyze(self, content: str) -> Tuple[bool, str]:
        for pattern in self.compiled_patterns:
            if pattern.search(content):
                return False, "Conteúdo contém código potencialmente malicioso"
        
        if len(content) > 100000:
            return False, "Conteúdo excede o limite de tamanho"
        
        return True, "Conteúdo seguro"

class SafetyFilter:
    def __init__(self):
        self.content_filter = ContentFilter()
        self.token_matcher = TokenMatcher()
        self.output_analyzer = OutputAnalyzer()
        
    def check_input(self, text: str) -> Tuple[bool, str]:
        is_safe, message = self.content_filter.check_input(text)
        if not is_safe:
            return False, message
        
        categories = self.token_matcher.match_tokens(text)
        if categories:
            return False, f"Conteúdo bloqueado por conter termos sensíveis: {', '.join(categories)}"
        
        return True, "Entrada aprovada"
    
    def check_output(self, content: str) -> Tuple[bool, str]:
        is_safe, message = self.content_filter.check_output(content)
        if not is_safe:
            return False, message
        
        is_safe, message = self.output_analyzer.analyze(content)
        if not is_safe:
            return False, message
        
        return True, "Saída aprovada"
