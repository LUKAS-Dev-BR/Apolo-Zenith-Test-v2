from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

router = APIRouter()

class CodeRequest(BaseModel):
    command: str
    params: Optional[Dict[str, Any]] = None
    reasoning_mode: str = "normal"

class ModelingRequest(BaseModel):
    command: str
    params: Optional[Dict[str, Any]] = None
    reasoning_mode: str = "normal"

@router.post("/code/execute")
async def execute_code_command(request: CodeRequest):
    from app.core.agents.coding_agent import CodeAgent
    
    agent = CodeAgent(reasoning_mode=request.reasoning_mode)
    
    if request.params:
        result = agent.execute_tool(request.command, **request.params)
    else:
        result = agent.execute_tool(request.command)
    
    return {"result": result}

@router.post("/code/analyze")
async def analyze_code(code: str):
    from app.core.agents.coding_agent import CodeAgent
    
    agent = CodeAgent()
    analysis = agent.analyze_code(code)
    
    return {"analysis": analysis}

@router.post("/modeling/execute")
async def execute_modeling_command(request: ModelingRequest):
    from app.core.agents.modeling_agent import ModelingAgent
    
    agent = ModelingAgent(reasoning_mode=request.reasoning_mode)
    
    if request.params:
        result = agent.execute_tool(request.command, **request.params)
    else:
        result = agent.execute_tool(request.command)
    
    return {"result": result}

@router.get("/modeling/scene")
async def get_scene():
    from app.core.agents.modeling_agent import ModelingAgent
    
    agent = ModelingAgent()
    scene = agent.export_scene()
    
    return {"scene": scene}

@router.post("/modeling/import")
async def import_scene(scene_data: str):
    from app.core.agents.modeling_agent import ModelingAgent
    
    agent = ModelingAgent()
    result = agent.import_scene(scene_data)
    
    return {"result": result}

@router.get("/modeling/blender-script")
async def generate_blender_script():
    from app.core.agents.modeling_agent import ModelingAgent
    
    agent = ModelingAgent()
    script = agent.generate_blender_script()
    
    return {"script": script}

@router.get("/reasoning/modes")
async def get_reasoning_modes():
    return {
        "modes": {
            "normal": {"depth": 1, "tokens": 1024, "analysis": "básico"},
            "medium": {"depth": 2, "tokens": 2048, "analysis": "intermediário"},
            "high": {"depth": 4, "tokens": 4096, "analysis": "avançado"},
            "very_high": {"depth": 8, "tokens": 8192, "analysis": "profundo"},
            "ultra_high": {"depth": 16, "tokens": 16384, "analysis": "extremo"},
            "ultra_mega_high": {"depth": 32, "tokens": 32768, "analysis": "máximo"}
        }
    }

@router.post("/reasoning/analyze")
async def analyze_complexity(prompt: str):
    from app.core.agents.reasoning import ReasoningEngine
    
    engine = ReasoningEngine()
    mode = engine.analyze_complexity(prompt)
    
    return {"recommended_mode": mode.value}
