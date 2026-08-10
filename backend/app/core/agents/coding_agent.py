import os
import subprocess
from typing import Dict, List, Optional
from pathlib import Path

class CodeAgent:
    def __init__(self, reasoning_mode: str = "normal"):
        self.reasoning_mode = reasoning_mode
        self.tools = self._load_tools()
        
    def _load_tools(self) -> Dict:
        return {
            "read_file": self.read_file,
            "write_file": self.write_file,
            "edit_file": self.edit_file,
            "list_directory": self.list_directory,
            "create_directory": self.create_directory,
            "delete_file": self.delete_file,
            "run_command": self.run_command,
            "search_files": self.search_files,
            "git_status": self.git_status,
            "git_diff": self.git_diff,
            "git_commit": self.git_commit,
            "npm_install": self.npm_install,
            "npm_run": self.npm_run,
            "python_run": self.python_run,
            "pip_install": self.pip_install
        }
    
    def read_file(self, path: str) -> str:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Erro ao ler arquivo: {str(e)}"
    
    def write_file(self, path: str, content: str) -> str:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Arquivo criado com sucesso: {path}"
        except Exception as e:
            return f"Erro ao escrever arquivo: {str(e)}"
    
    def edit_file(self, path: str, old_text: str, new_text: str) -> str:
        try:
            content = self.read_file(path)
            if old_text not in content:
                return "Texto não encontrado no arquivo"
            
            new_content = content.replace(old_text, new_text)
            return self.write_file(path, new_content)
        except Exception as e:
            return f"Erro ao editar arquivo: {str(e)}"
    
    def list_directory(self, path: str = ".") -> str:
        try:
            items = os.listdir(path)
            return "\n".join(items)
        except Exception as e:
            return f"Erro ao listar diretório: {str(e)}"
    
    def create_directory(self, path: str) -> str:
        try:
            os.makedirs(path, exist_ok=True)
            return f"Diretório criado: {path}"
        except Exception as e:
            return f"Erro ao criar diretório: {str(e)}"
    
    def delete_file(self, path: str) -> str:
        try:
            if os.path.isfile(path):
                os.remove(path)
                return f"Arquivo deletado: {path}"
            elif os.path.isdir(path):
                import shutil
                shutil.rmtree(path)
                return f"Diretório deletado: {path}"
            else:
                return "Arquivo não encontrado"
        except Exception as e:
            return f"Erro ao deletar: {str(e)}"
    
    def run_command(self, command: str) -> str:
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout
            if result.stderr:
                output += f"\nErro: {result.stderr}"
            return output
        except subprocess.TimeoutExpired:
            return "Comando excedeu o limite de tempo"
        except Exception as e:
            return f"Erro ao executar comando: {str(e)}"
    
    def search_files(self, pattern: str, path: str = ".") -> str:
        try:
            import glob
            matches = glob.glob(os.path.join(path, "**", pattern), recursive=True)
            return "\n".join(matches) if matches else "Nenhum arquivo encontrado"
        except Exception as e:
            return f"Erro ao buscar arquivos: {str(e)}"
    
    def git_status(self) -> str:
        return self.run_command("git status")
    
    def git_diff(self) -> str:
        return self.run_command("git diff")
    
    def git_commit(self, message: str) -> str:
        self.run_command("git add .")
        return self.run_command(f'git commit -m "{message}"')
    
    def npm_install(self, path: str = ".") -> str:
        return self.run_command(f"cd {path} && npm install")
    
    def npm_run(self, script: str, path: str = ".") -> str:
        return self.run_command(f"cd {path} && npm run {script}")
    
    def python_run(self, script: str) -> str:
        return self.run_command(f"python {script}")
    
    def pip_install(self, package: str) -> str:
        return self.run_command(f"pip install {package}")
    
    def execute_tool(self, tool_name: str, **kwargs) -> str:
        if tool_name not in self.tools:
            return f"Ferramenta não encontrada: {tool_name}"
        
        try:
            return self.tools[tool_name](**kwargs)
        except Exception as e:
            return f"Erro ao executar ferramenta: {str(e)}"
    
    def analyze_code(self, code: str) -> Dict:
        analysis = {
            "lines": len(code.split("\n")),
            "characters": len(code),
            "has_functions": "def " in code or "function " in code,
            "has_classes": "class " in code,
            "has_imports": "import " in code or "require(" in code,
            "languages": self._detect_language(code)
        }
        return analysis
    
    def _detect_language(self, code: str) -> List[str]:
        languages = []
        
        if "def " in code and "import " in code:
            languages.append("python")
        if "function " in code and "const " in code:
            languages.append("javascript")
        if "function " in code and "let " in code:
            languages.append("typescript")
        if "<div" in code or "<html" in code:
            languages.append("html")
        if "SELECT " in code and "FROM " in code:
            languages.append("sql")
        
        return languages if languages else ["unknown"]
