"""
OpenAPI Documentation Generator

This module generates OpenAPI 3.0 specifications from FastAPI analysis results.
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from analyzer.fastapi_analyzer import APIAnalysis, APIEndpoint, APIModel


class OpenAPIGenerator:
    """Generates OpenAPI 3.0 specifications from FastAPI analysis"""
    
    def __init__(self):
        self.openapi_spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "API Documentation",
                "version": "1.0.0",
                "description": "Auto-generated API documentation"
            },
            "servers": [
                {
                    "url": "http://localhost:8000",
                    "description": "Development server"
                }
            ],
            "paths": {},
            "components": {
                "schemas": {},
                "responses": {},
                "parameters": {}
            },
            "tags": []
        }
    
    def generate_from_analysis(self, analysis: APIAnalysis) -> Dict[str, Any]:
        """Generate OpenAPI spec from APIAnalysis"""
        # Update basic info
        if analysis.app_title:
            self.openapi_spec["info"]["title"] = analysis.app_title
        if analysis.app_description:
            self.openapi_spec["info"]["description"] = analysis.app_description
        if analysis.app_version:
            self.openapi_spec["info"]["version"] = analysis.app_version
        
        # Generate schemas from models
        self._generate_schemas(analysis.models)
        
        # Generate paths from endpoints
        self._generate_paths(analysis.endpoints)
        
        # Generate tags
        self._generate_tags(analysis.endpoints)
        
        return self.openapi_spec
    
    def _generate_schemas(self, models: List[APIModel]):
        """Generate OpenAPI schemas from Pydantic models"""
        for model in models:
            schema = {
                "type": "object",
                "properties": {},
                "required": []
            }
            
            if model.description:
                schema["description"] = model.description
            
            for field_name, field_type in model.fields.items():
                schema["properties"][field_name] = self._convert_type_to_openapi(field_type)
                # For now, assume all fields are required
                schema["required"].append(field_name)
            
            self.openapi_spec["components"]["schemas"][model.name] = schema
    
    def _convert_type_to_openapi(self, field_type: str) -> Dict[str, Any]:
        """Convert Python type annotation to OpenAPI type"""
        type_mapping = {
            "str": {"type": "string"},
            "int": {"type": "integer"},
            "float": {"type": "number"},
            "bool": {"type": "boolean"},
            "list": {"type": "array"},
            "dict": {"type": "object"},
            "Any": {"type": "string"}  # Default fallback
        }
        
        # Handle generic types
        if "List[" in field_type or "list[" in field_type:
            # Extract inner type
            inner_type = field_type.split("[")[1].split("]")[0]
            return {
                "type": "array",
                "items": type_mapping.get(inner_type, {"type": "string"})
            }
        elif "Optional[" in field_type:
            # Extract inner type
            inner_type = field_type.split("[")[1].split("]")[0]
            return type_mapping.get(inner_type, {"type": "string"})
        
        return type_mapping.get(field_type, {"type": "string"})
    
    def _generate_paths(self, endpoints: List[APIEndpoint]):
        """Generate OpenAPI paths from endpoints"""
        for endpoint in endpoints:
            path = endpoint.path
            
            if path not in self.openapi_spec["paths"]:
                self.openapi_spec["paths"][path] = {}
            
            operation = {
                "summary": endpoint.summary or f"{endpoint.method} {endpoint.path}",
                "operationId": endpoint.function_name,
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {"type": "object"}
                            }
                        }
                    }
                }
            }
            
            if endpoint.description:
                operation["description"] = endpoint.description
            
            if endpoint.tags:
                operation["tags"] = endpoint.tags
            
            if endpoint.deprecated:
                operation["deprecated"] = True
            
            # Add request body for POST/PUT/PATCH
            if endpoint.method in ["POST", "PUT", "PATCH"]:
                operation["requestBody"] = {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"type": "object"}
                        }
                    }
                }
            
            self.openapi_spec["paths"][path][endpoint.method.lower()] = operation
    
    def _generate_tags(self, endpoints: List[APIEndpoint]):
        """Generate OpenAPI tags from endpoint tags"""
        all_tags = set()
        
        for endpoint in endpoints:
            all_tags.update(endpoint.tags)
        
        for tag in all_tags:
            self.openapi_spec["tags"].append({
                "name": tag,
                "description": f"Operations related to {tag}"
            })
    
    def save_to_file(self, file_path: str):
        """Save OpenAPI spec to JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.openapi_spec, f, indent=2, ensure_ascii=False)


class MarkdownGenerator:
    """Generates markdown documentation from OpenAPI spec"""
    
    def __init__(self, openapi_spec: Dict[str, Any]):
        self.spec = openapi_spec
    
    def generate_markdown(self) -> str:
        """Generate markdown documentation"""
        md_content = []
        
        # Title and description
        md_content.append(f"# {self.spec['info']['title']}")
        md_content.append("")
        
        if self.spec['info'].get('description'):
            md_content.append(self.spec['info']['description'])
            md_content.append("")
        
        # API Info
        md_content.append("## API Information")
        md_content.append("")
        md_content.append(f"- **Version**: {self.spec['info']['version']}")
        md_content.append(f"- **OpenAPI Version**: {self.spec['openapi']}")
        md_content.append("")
        
        # Servers
        if self.spec.get('servers'):
            md_content.append("## Servers")
            md_content.append("")
            for server in self.spec['servers']:
                md_content.append(f"- **{server['description']}**: {server['url']}")
            md_content.append("")
        
        # Tags
        if self.spec.get('tags'):
            md_content.append("## Tags")
            md_content.append("")
            for tag in self.spec['tags']:
                md_content.append(f"- **{tag['name']}**: {tag.get('description', '')}")
            md_content.append("")
        
        # Endpoints
        md_content.append("## API Endpoints")
        md_content.append("")
        
        for path, path_item in self.spec['paths'].items():
            md_content.append(f"### {path}")
            md_content.append("")
            
            for method, operation in path_item.items():
                if method in ['get', 'post', 'put', 'delete', 'patch']:
                    method_upper = method.upper()
                    md_content.append(f"#### {method_upper} {path}")
                    md_content.append("")
                    
                    if operation.get('summary'):
                        md_content.append(f"**Summary**: {operation['summary']}")
                        md_content.append("")
                    
                    if operation.get('description'):
                        md_content.append(f"**Description**: {operation['description']}")
                        md_content.append("")
                    
                    if operation.get('tags'):
                        md_content.append(f"**Tags**: {', '.join(operation['tags'])}")
                        md_content.append("")
                    
                    md_content.append("---")
                    md_content.append("")
        
        # Schemas
        if self.spec.get('components', {}).get('schemas'):
            md_content.append("## Data Models")
            md_content.append("")
            
            for schema_name, schema in self.spec['components']['schemas'].items():
                md_content.append(f"### {schema_name}")
                md_content.append("")
                
                if schema.get('description'):
                    md_content.append(schema['description'])
                    md_content.append("")
                
                if schema.get('properties'):
                    md_content.append("| Field | Type | Required | Description |")
                    md_content.append("|-------|------|----------|-------------|")
                    
                    required_fields = schema.get('required', [])
                    
                    for field_name, field_spec in schema['properties'].items():
                        field_type = field_spec.get('type', 'string')
                        required = "Yes" if field_name in required_fields else "No"
                        description = field_spec.get('description', '')
                        md_content.append(f"| {field_name} | {field_type} | {required} | {description} |")
                    
                    md_content.append("")
        
        return "\n".join(md_content)
    
    def save_to_file(self, file_path: str):
        """Save markdown documentation to file"""
        markdown_content = self.generate_markdown()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)


def main():
    """Example usage of the OpenAPI generator"""
    from analyzer.fastapi_analyzer import FastAPIAnalyzer
    
    # Analyze FastAPI code
    analyzer = FastAPIAnalyzer()
    analysis = analyzer.analyze_directory(".")
    
    # Generate OpenAPI spec
    generator = OpenAPIGenerator()
    openapi_spec = generator.generate_from_analysis(analysis)
    
    # Save to files
    generator.save_to_file("docs/openapi.json")
    
    # Generate markdown
    md_generator = MarkdownGenerator(openapi_spec)
    md_generator.save_to_file("docs/api_documentation.md")
    
    print("OpenAPI documentation generated successfully!")
    print("- docs/openapi.json")
    print("- docs/api_documentation.md")


if __name__ == "__main__":
    main()
