import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class PrimitiveType(Enum):
    CUBE = "cube"
    SPHERE = "sphere"
    CYLINDER = "cylinder"
    CONE = "cone"
    TORUS = "torus"
    PLANE = "plane"
    MONKEY = "monkey"

@dataclass
class Vector3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

@dataclass
class Transform:
    position: Vector3 = None
    rotation: Vector3 = None
    scale: Vector3 = None
    
    def __post_init__(self):
        if self.position is None:
            self.position = Vector3()
        if self.rotation is None:
            self.rotation = Vector3()
        if self.scale is None:
            self.scale = Vector3(1.0, 1.0, 1.0)

@dataclass
class Material:
    name: str = "Default"
    color: Vector3 = None
    metallic: float = 0.0
    roughness: float = 0.5
    emission: float = 0.0
    
    def __post_init__(self):
        if self.color is None:
            self.color = Vector3(0.8, 0.8, 0.8)

@dataclass
class Mesh:
    name: str
    primitive_type: PrimitiveType
    transform: Transform = None
    material: Material = None
    
    def __post_init__(self):
        if self.transform is None:
            self.transform = Transform()
        if self.material is None:
            self.material = Material()

class ModelingAgent:
    def __init__(self, reasoning_mode: str = "normal"):
        self.reasoning_mode = reasoning_mode
        self.scene = {
            "meshes": [],
            "lights": [],
            "camera": None
        }
        self.tools = self._load_tools()
        
    def _load_tools(self) -> Dict:
        return {
            "create_mesh": self.create_mesh,
            "delete_mesh": self.delete_mesh,
            "transform_mesh": self.transform_mesh,
            "set_material": self.set_material,
            "add_light": self.add_light,
            "set_camera": self.set_camera,
            "export_scene": self.export_scene,
            "import_scene": self.import_scene,
            "duplicate_mesh": self.duplicate_mesh,
            "join_meshes": self.join_meshes,
            "subdivide_mesh": self.subdivide_mesh,
            "smooth_mesh": self.smooth_mesh,
            "extrude_face": self.extrude_face,
            "bevel_edge": self.bevel_edge,
            "array_modifier": self.array_modifier,
            "mirror_modifier": self.mirror_modifier,
            "boolean_operation": self.boolean_operation,
            "apply_material": self.apply_material,
            "uv_unwrap": self.uv_unwrap,
            "bake_texture": self.bake_texture
        }
    
    def create_mesh(self, name: str, primitive_type: str, position: Dict = None) -> str:
        try:
            prim_type = PrimitiveType(primitive_type)
            pos = Vector3(**position) if position else Vector3()
            
            mesh = Mesh(
                name=name,
                primitive_type=prim_type,
                transform=Transform(position=pos)
            )
            
            self.scene["meshes"].append(mesh)
            return f"Malha criada: {name}"
        except Exception as e:
            return f"Erro ao criar malha: {str(e)}"
    
    def delete_mesh(self, name: str) -> str:
        try:
            self.scene["meshes"] = [m for m in self.scene["meshes"] if m.name != name]
            return f"Malha deletada: {name}"
        except Exception as e:
            return f"Erro ao deletar malha: {str(e)}"
    
    def transform_mesh(self, name: str, position: Dict = None, rotation: Dict = None, scale: Dict = None) -> str:
        try:
            for mesh in self.scene["meshes"]:
                if mesh.name == name:
                    if position:
                        mesh.transform.position = Vector3(**position)
                    if rotation:
                        mesh.transform.rotation = Vector3(**rotation)
                    if scale:
                        mesh.transform.scale = Vector3(**scale)
                    return f"Malha transformada: {name}"
            return "Malha não encontrada"
        except Exception as e:
            return f"Erro ao transformar malha: {str(e)}"
    
    def set_material(self, mesh_name: str, material_name: str, color: Dict = None, metallic: float = 0.0, roughness: float = 0.5) -> str:
        try:
            for mesh in self.scene["meshes"]:
                if mesh.name == mesh_name:
                    col = Vector3(**color) if color else Vector3(0.8, 0.8, 0.8)
                    mesh.material = Material(
                        name=material_name,
                        color=col,
                        metallic=metallic,
                        roughness=roughness
                    )
                    return f"Material aplicado: {material_name}"
            return "Malha não encontrada"
        except Exception as e:
            return f"Erro ao definir material: {str(e)}"
    
    def add_light(self, name: str, light_type: str, position: Dict = None, intensity: float = 1.0) -> str:
        try:
            light = {
                "name": name,
                "type": light_type,
                "position": position or {"x": 0, "y": 5, "z": 0},
                "intensity": intensity
            }
            self.scene["lights"].append(light)
            return f"Luz adicionada: {name}"
        except Exception as e:
            return f"Erro ao adicionar luz: {str(e)}"
    
    def set_camera(self, position: Dict = None, target: Dict = None, fov: float = 60.0) -> str:
        try:
            self.scene["camera"] = {
                "position": position or {"x": 0, "y": 0, "z": 10},
                "target": target or {"x": 0, "y": 0, "z": 0},
                "fov": fov
            }
            return "Câmera configurada"
        except Exception as e:
            return f"Erro ao configurar câmera: {str(e)}"
    
    def export_scene(self, format: str = "json") -> str:
        try:
            scene_data = {
                "meshes": [
                    {
                        "name": m.name,
                        "primitive_type": m.primitive_type.value,
                        "transform": {
                            "position": {"x": m.transform.position.x, "y": m.transform.position.y, "z": m.transform.position.z},
                            "rotation": {"x": m.transform.rotation.x, "y": m.transform.rotation.y, "z": m.transform.rotation.z},
                            "scale": {"x": m.transform.scale.x, "y": m.transform.scale.y, "z": m.transform.scale.z}
                        },
                        "material": {
                            "name": m.material.name,
                            "color": {"x": m.material.color.x, "y": m.material.color.y, "z": m.material.color.z},
                            "metallic": m.material.metallic,
                            "roughness": m.material.roughness
                        }
                    }
                    for m in self.scene["meshes"]
                ],
                "lights": self.scene["lights"],
                "camera": self.scene["camera"]
            }
            
            return json.dumps(scene_data, indent=2)
        except Exception as e:
            return f"Erro ao exportar cena: {str(e)}"
    
    def import_scene(self, scene_data: str) -> str:
        try:
            data = json.loads(scene_data)
            self.scene = {
                "meshes": [],
                "lights": data.get("lights", []),
                "camera": data.get("camera")
            }
            
            for mesh_data in data.get("meshes", []):
                mesh = Mesh(
                    name=mesh_data["name"],
                    primitive_type=PrimitiveType(mesh_data["primitive_type"]),
                    transform=Transform(
                        position=Vector3(**mesh_data["transform"]["position"]),
                        rotation=Vector3(**mesh_data["transform"]["rotation"]),
                        scale=Vector3(**mesh_data["transform"]["scale"])
                    ),
                    material=Material(
                        name=mesh_data["material"]["name"],
                        color=Vector3(**mesh_data["material"]["color"]),
                        metallic=mesh_data["material"]["metallic"],
                        roughness=mesh_data["material"]["roughness"]
                    )
                )
                self.scene["meshes"].append(mesh)
            
            return "Cena importada com sucesso"
        except Exception as e:
            return f"Erro ao importar cena: {str(e)}"
    
    def duplicate_mesh(self, name: str, new_name: str) -> str:
        try:
            for mesh in self.scene["meshes"]:
                if mesh.name == name:
                    new_mesh = Mesh(
                        name=new_name,
                        primitive_type=mesh.primitive_type,
                        transform=Transform(
                            position=Vector3(mesh.transform.position.x + 1, mesh.transform.position.y, mesh.transform.position.z),
                            rotation=Vector3(mesh.transform.rotation.x, mesh.transform.rotation.y, mesh.transform.rotation.z),
                            scale=Vector3(mesh.transform.scale.x, mesh.transform.scale.y, mesh.transform.scale.z)
                        ),
                        material=Material(
                            name=mesh.material.name,
                            color=Vector3(mesh.material.color.x, mesh.material.color.y, mesh.material.color.z),
                            metallic=mesh.material.metallic,
                            roughness=mesh.material.roughness
                        )
                    )
                    self.scene["meshes"].append(new_mesh)
                    return f"Malha duplicada: {new_name}"
            return "Malha não encontrada"
        except Exception as e:
            return f"Erro ao duplicar malha: {str(e)}"
    
    def join_meshes(self, mesh_names: List[str], new_name: str) -> str:
        try:
            meshes_to_join = [m for m in self.scene["meshes"] if m.name in mesh_names]
            if len(meshes_to_join) < 2:
                return "Necessário pelo menos 2 malhas para juntar"
            
            for mesh in meshes_to_join:
                self.scene["meshes"].remove(mesh)
            
            joined_mesh = Mesh(
                name=new_name,
                primitive_type=PrimitiveType.CUBE,
                transform=meshes_to_join[0].transform,
                material=meshes_to_join[0].material
            )
            self.scene["meshes"].append(joined_mesh)
            
            return f"Malhas juntadas: {new_name}"
        except Exception as e:
            return f"Erro ao juntar malhas: {str(e)}"
    
    def subdivide_mesh(self, name: str, levels: int = 1) -> str:
        try:
            for mesh in self.scene["meshes"]:
                if mesh.name == name:
                    return f"Malha {name} subdividida {levels} vezes"
            return "Malha não encontrada"
        except Exception as e:
            return f"Erro ao subdividir malha: {str(e)}"
    
    def smooth_mesh(self, name: str, factor: float = 0.5) -> str:
        try:
            for mesh in self.scene["meshes"]:
                if mesh.name == name:
                    return f"Malha {name} suavizada com fator {factor}"
            return "Malha não encontrada"
        except Exception as e:
            return f"Erro ao suavizar malha: {str(e)}"
    
    def extrude_face(self, name: str, distance: float = 1.0) -> str:
        try:
            for mesh in self.scene["meshes"]:
                if mesh.name == name:
                    return f"Face da malha {name} extrudada {distance} unidades"
            return "Malha não encontrada"
        except Exception as e:
            return f"Erro ao extrudar face: {str(e)}"
    
    def bevel_edge(self, name: str, width: float = 0.1) -> str:
        try:
            for mesh in self.scene["meshes"]:
                if mesh.name == name:
                    return f"Aresta da malha {name} chanfrada {width} unidades"
            return "Malha não encontrada"
        except Exception as e:
            return f"Erro ao chanfrar aresta: {str(e)}"
    
    def array_modifier(self, name: str, count: int = 3, offset: Dict = None) -> str:
        try:
            for mesh in self.scene["meshes"]:
                if mesh.name == name:
                    return f"Modificador array aplicado: {count} cópias"
            return "Malha não encontrada"
        except Exception as e:
            return f"Erro ao aplicar modificador array: {str(e)}"
    
    def mirror_modifier(self, name: str, axis: str = "x") -> str:
        try:
            for mesh in self.scene["meshes"]:
                if mesh.name == name:
                    return f"Modificador espelho aplicado no eixo {axis}"
            return "Malha não encontrada"
        except Exception as e:
            return f"Erro ao aplicar modificador espelho: {str(e)}"
    
    def boolean_operation(self, mesh1: str, mesh2: str, operation: str = "union") -> str:
        try:
            return f"Operação booleana {operation} aplicada entre {mesh1} e {mesh2}"
        except Exception as e:
            return f"Erro ao aplicar operação booleana: {str(e)}"
    
    def apply_material(self, mesh_name: str, material_name: str, color: Dict = None) -> str:
        return self.set_material(mesh_name, material_name, color)
    
    def uv_unwrap(self, name: str, method: str = "smart") -> str:
        try:
            for mesh in self.scene["meshes"]:
                if mesh.name == name:
                    return f"UV unwrap aplicado na malha {name} usando método {method}"
            return "Malha não encontrada"
        except Exception as e:
            return f"Erro ao aplicar UV unwrap: {str(e)}"
    
    def bake_texture(self, name: str, texture_type: str = "diffuse") -> str:
        try:
            for mesh in self.scene["meshes"]:
                if mesh.name == name:
                    return f"Textura {texture_type} bakeada na malha {name}"
            return "Malha não encontrada"
        except Exception as e:
            return f"Erro ao bakear textura: {str(e)}"
    
    def execute_tool(self, tool_name: str, **kwargs) -> str:
        if tool_name not in self.tools:
            return f"Ferramenta não encontrada: {tool_name}"
        
        try:
            return self.tools[tool_name](**kwargs)
        except Exception as e:
            return f"Erro ao executar ferramenta: {str(e)}"
    
    def generate_blender_script(self) -> str:
        script = """
import bpy
import math

# Limpar cena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

"""
        for mesh in self.scene["meshes"]:
            script += f"""
# Criar {mesh.name}
bpy.ops.mesh.primitive_{mesh.primitive_type.value}_add(
    location=({mesh.transform.position.x}, {mesh.transform.position.y}, {mesh.transform.position.z}),
    rotation=(math.radians({mesh.transform.rotation.x}), math.radians({mesh.transform.rotation.y}), math.radians({mesh.transform.rotation.z})),
    scale=({mesh.transform.scale.x}, {mesh.transform.scale.y}, {mesh.transform.scale.z})
)
obj = bpy.context.active_object
obj.name = "{mesh.name}"

# Material
mat = bpy.data.materials.new(name="{mesh.material.name}")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = ({mesh.material.color.x}, {mesh.material.color.y}, {mesh.material.color.z}, 1)
bsdf.inputs['Metallic'].default_value = {mesh.material.metallic}
bsdf.inputs['Roughness'].default_value = {mesh.material.roughness}
obj.data.materials.append(mat)
"""
        
        if self.scene["camera"]:
            cam = self.scene["camera"]
            script += f"""
# Câmera
bpy.ops.object.camera_add(
    location=({cam['position']['x']}, {cam['position']['y']}, {cam['position']['z']})
)
camera = bpy.context.active_object
camera.name = "Camera"

# Apontar para o alvo
constraint = camera.constraints.new(type='TRACK_TO')
target = bpy.data.objects.new("CameraTarget", None)
bpy.context.collection.objects.link(target)
target.location = ({cam['target']['x']}, {cam['target']['y']}, {cam['target']['z']})
constraint.target = target
"""
        
        for light in self.scene["lights"]:
            script += f"""
# Luz {light['name']}
bpy.ops.object.light_add(
    type='{light['type'].upper()}',
    location=({light['position']['x']}, {light['position']['y']}, {light['position']['z']})
)
light = bpy.context.active_object
light.name = "{light['name']}"
light.data.energy = {light['intensity']}
"""
        
        return script
