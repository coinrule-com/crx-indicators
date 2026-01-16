import yaml
import sys
import os
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, field_validator, ValidationError

class Argument(BaseModel):
    type: str
    default: Any
    label: str
    description: str

    @field_validator('type')
    def validate_type(cls, v):
        allowed_types = {'int', 'float', 'str', 'bool', 'list'}
        if v not in allowed_types:
            raise ValueError(f"Type must be one of {allowed_types}")
        return v

class IndicatorVersion(BaseModel):
    class_: str = Field(alias="class")
    description: str
    arguments: Optional[Dict[str, Argument]] = None

class IndicatorMetadata(BaseModel):
    latest: str
    label: str
    versions: Dict[str, IndicatorVersion]

    @field_validator('versions')
    def validate_latest_version_exists(cls, v, info):
        # We can't access 'latest' field easily in field validator before validation
        # But we can check consistency in model validator or outside
        return v

class IndicatorRegistry(BaseModel):
    indicators: Dict[str, IndicatorMetadata]

def validate_yaml(file_path: str):
    """validates the indicators registry.yaml file."""
    print(f"Validating {file_path}...")
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Pydantic validation
        registry = IndicatorRegistry(**data)
        
        # Logical consistency checks
        for name, meta in registry.indicators.items():
            if meta.latest not in meta.versions:
                raise ValueError(f"Indicator '{name}': Latest version '{meta.latest}' not found in versions list")

        print(f"✅ {file_path} is valid!")
        return True

    except ValidationError as e:
        print(f"❌ Validation Error in {file_path}:")
        for err in e.errors():
            loc = ".".join(str(l) for l in err['loc'])
            print(f"  - {loc}: {err['msg']}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except ValueError as e:
        print(f"❌ Logical Error in {file_path}: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error in {file_path}: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_registry.py <path_to_registry.yaml>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Simple direct file validation since it's a monolithic registry
    if os.path.exists(file_path):
        success = validate_yaml(file_path)
        sys.exit(0 if success else 1)
    else:
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
