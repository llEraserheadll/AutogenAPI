"""
FastAPI Code Analyzer

This module analyzes FastAPI applications to extract API definitions,
endpoints, models, and documentation for automatic documentation generation.
"""

import ast
import os
import sys
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class APIEndpoint:
    """Represents a single API endpoint"""
    path: str
    method: str
    function_name: str
    summary: Optional[str] = None
    description: Optional[str] = None
    parameters: List[Dict[str, Any]] = None
    responses: Dict[str, Any] = None
    tags: List[str] = None
    deprecated: bool = False
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = []
        if self.responses is None:
            self.responses = {}
        if self.tags is None:
            self.tags = []


@dataclass
class APIModel:
    """Represents a Pydantic model"""
    name: str
    fields: Dict[str, Any]
    description: Optional[str] = None
    example: Optional[Dict[str, Any]] = None


@dataclass
class APIAnalysis:
    """Complete analysis of a FastAPI application"""
    endpoints: List[APIEndpoint]
    models: List[APIModel]
    app_title: Optional[str] = None
    app_description: Optional[str] = None
    app_version: Optional[str] = None


class FastAPIAnalyzer:
    """Analyzes FastAPI applications to extract API definitions"""
    
    def __init__(self):
        self.endpoints: List[APIEndpoint] = []
        self.models: List[APIModel] = []
        self.app_info: Dict[str, Any] = {}
    
    def analyze_file(self, file_path: str) -> APIAnalysis:
        """Analyze a single Python file for FastAPI definitions"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Extract app info and endpoints
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    self._analyze_assignment(node)
                elif isinstance(node, ast.FunctionDef):
                    self._analyze_function(node)
                elif isinstance(node, ast.ClassDef):
                    self._analyze_class(node)
            
            return APIAnalysis(
                endpoints=self.endpoints,
                models=self.models,
                app_title=self.app_info.get('title'),
                app_description=self.app_info.get('description'),
                app_version=self.app_info.get('version')
            )
            
        except Exception as e:
            print(f"Error analyzing file {file_path}: {e}")
            return APIAnalysis(endpoints=[], models=[])
    
    def analyze_directory(self, directory_path: str) -> APIAnalysis:
        """Analyze all Python files in a directory"""
        all_endpoints = []
        all_models = []
        app_info = {}
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    analysis = self.analyze_file(file_path)
                    
                    all_endpoints.extend(analysis.endpoints)
                    all_models.extend(analysis.models)
                    
                    if analysis.app_title:
                        app_info['title'] = analysis.app_title
                    if analysis.app_description:
                        app_info['description'] = analysis.app_description
                    if analysis.app_version:
                        app_info['version'] = analysis.app_version
        
        return APIAnalysis(
            endpoints=all_endpoints,
            models=all_models,
            app_title=app_info.get('title'),
            app_description=app_info.get('description'),
            app_version=app_info.get('version')
        )
    
    def _analyze_assignment(self, node: ast.Assign):
        """Analyze assignment statements for FastAPI app creation"""
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            target_name = node.targets[0].id
            
            if target_name == 'app' and isinstance(node.value, ast.Call):
                # FastAPI app creation
                if isinstance(node.value.func, ast.Name) and node.value.func.id == 'FastAPI':
                    self._extract_app_info(node.value)
    
    def _extract_app_info(self, call_node: ast.Call):
        """Extract information from FastAPI app creation"""
        for keyword in call_node.keywords:
            if keyword.arg == 'title' and isinstance(keyword.value, ast.Constant):
                self.app_info['title'] = keyword.value.value
            elif keyword.arg == 'description' and isinstance(keyword.value, ast.Constant):
                self.app_info['description'] = keyword.value.value
            elif keyword.arg == 'version' and isinstance(keyword.value, ast.Constant):
                self.app_info['version'] = keyword.value.value
    
    def _analyze_function(self, node: ast.FunctionDef):
        """Analyze function definitions for API endpoints"""
        # Look for decorators that indicate API endpoints
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Attribute):
                    # Check for app.get, app.post, etc.
                    if (isinstance(decorator.func.value, ast.Name) and 
                        decorator.func.value.id == 'app' and
                        decorator.func.attr in ['get', 'post', 'put', 'delete', 'patch']):
                        
                        endpoint = self._create_endpoint(node, decorator)
                        if endpoint:
                            self.endpoints.append(endpoint)
    
    def _create_endpoint(self, func_node: ast.FunctionDef, decorator: ast.Call) -> Optional[APIEndpoint]:
        """Create an APIEndpoint from function and decorator"""
        method = decorator.func.attr.upper()
        
        # Extract path from decorator arguments
        path = "/"
        if decorator.args and isinstance(decorator.args[0], ast.Constant):
            path = decorator.args[0].value
        
        # Extract additional info from decorator keywords
        summary = None
        description = None
        tags = []
        
        for keyword in decorator.keywords:
            if keyword.arg == 'summary' and isinstance(keyword.value, ast.Constant):
                summary = keyword.value.value
            elif keyword.arg == 'description' and isinstance(keyword.value, ast.Constant):
                description = keyword.value.value
            elif keyword.arg == 'tags' and isinstance(keyword.value, ast.List):
                tags = [item.value for item in keyword.value.elts if isinstance(item, ast.Constant)]
        
        # Extract docstring for description if not provided
        if not description and func_node.body and isinstance(func_node.body[0], ast.Expr):
            if isinstance(func_node.body[0].value, ast.Constant) and isinstance(func_node.body[0].value.value, str):
                description = func_node.body[0].value.value.strip()
        
        return APIEndpoint(
            path=path,
            method=method,
            function_name=func_node.name,
            summary=summary,
            description=description,
            tags=tags
        )
    
    def _analyze_class(self, node: ast.ClassDef):
        """Analyze class definitions for Pydantic models"""
        # Check if it's a Pydantic model (BaseModel)
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == 'BaseModel':
                model = self._create_model(node)
                if model:
                    self.models.append(model)
                break
    
    def _create_model(self, class_node: ast.ClassDef) -> Optional[APIModel]:
        """Create an APIModel from class definition"""
        fields = {}
        description = None
        
        # Extract docstring
        if class_node.body and isinstance(class_node.body[0], ast.Expr):
            if isinstance(class_node.body[0].value, ast.Constant) and isinstance(class_node.body[0].value.value, str):
                description = class_node.body[0].value.value.strip()
        
        # Extract field definitions
        for node in class_node.body:
            if isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name):
                    field_name = node.target.id
                    field_type = self._get_type_annotation(node.annotation)
                    fields[field_name] = field_type
        
        return APIModel(
            name=class_node.name,
            fields=fields,
            description=description
        )
    
    def _get_type_annotation(self, annotation: ast.expr) -> str:
        """Convert AST type annotation to string"""
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Constant):
            return str(annotation.value)
        elif isinstance(annotation, ast.Subscript):
            # Handle generic types like List[str], Optional[str]
            if isinstance(annotation.value, ast.Name):
                base_type = annotation.value.id
                if annotation.slice:
                    if isinstance(annotation.slice, ast.Name):
                        return f"{base_type}[{annotation.slice.id}]"
                    elif isinstance(annotation.slice, ast.Constant):
                        return f"{base_type}[{annotation.slice.value}]"
        return "Any"


def main():
    """Example usage of the FastAPI analyzer"""
    analyzer = FastAPIAnalyzer()
    
    # Analyze current directory
    analysis = analyzer.analyze_directory(".")
    
    print(f"Found {len(analysis.endpoints)} endpoints")
    print(f"Found {len(analysis.models)} models")
    
    for endpoint in analysis.endpoints:
        print(f"- {endpoint.method} {endpoint.path} ({endpoint.function_name})")
    
    for model in analysis.models:
        print(f"- Model: {model.name} with {len(model.fields)} fields")


if __name__ == "__main__":
    main()
