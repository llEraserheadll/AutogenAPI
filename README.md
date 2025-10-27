# AutoDocGen - Automated API Documentation & SDK Generator

An automated system that generates API documentation and SDKs from FastAPI code whenever you push to GitHub. Never worry about documentation falling out of sync again!

## ðŸš€ Features

- ðŸ”„ **Automatic Updates**: Triggers on every GitHub push
- ðŸ“š **API Documentation**: Generates OpenAPI specs and markdown docs
- ðŸ› ï¸ **SDK Generation**: Creates client libraries in multiple languages
- ðŸŽ¯ **FastAPI Support**: Analyzes FastAPI applications automatically
- ðŸ“ **Repo Integration**: Stores docs directly in your GitHub repository

## ðŸ—ï¸ Architecture

`
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   GitHub Push   â”‚â”€â”€â”€â–¶â”‚  FastAPI Code   â”‚â”€â”€â”€â–¶â”‚   Analysis      â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                                       â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   Documentation â”‚â—€â”€â”€â”€â”‚ Markdown Gen    â”‚â—€â”€â”€â”€â”‚  OpenAPI Spec   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
`

## ðŸ“ Project Structure

`
docgen/
â”œâ”€â”€ analyzer/                 # FastAPI code analysis
â”‚   â””â”€â”€ fastapi_analyzer.py
â”œâ”€â”€ generators/               # Documentation generators
â”‚   â””â”€â”€ openapi_generator.py
â”œâ”€â”€ github_action/           # GitHub Actions workflow
â”‚   â””â”€â”€ .github/workflows/
â”‚       â””â”€â”€ autodocgen.yml
â”œâ”€â”€ examples/                # Example FastAPI applications
â”‚   â””â”€â”€ sample_app.py
â”œâ”€â”€ docs/                    # Generated documentation
â”œâ”€â”€ sdk/                     # Generated SDKs
â”œâ”€â”€ requirements.txt         # Python dependencies
â””â”€â”€ README.md               # This file
`

## ðŸš€ Quick Start

### 1. Setup Your Repository

1. **Copy the GitHub Action workflow** to your repository:
   `ash
   mkdir -p .github/workflows
   cp github_action/.github/workflows/autodocgen.yml .github/workflows/
   `

2. **Copy the AutoDocGen files** to your repository:
   `ash
   cp -r analyzer/ generators/ requirements.txt ./
   `

### 2. Configure Your FastAPI App

Make sure your FastAPI application includes proper metadata:

`python
from fastapi import FastAPI

app = FastAPI(
    title="Your API Name",
    description="Your API description",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Hello World"}
`

### 3. Push to GitHub

Simply push your code to GitHub, and the automation will:

1. âœ… Analyze your FastAPI code
2. âœ… Generate OpenAPI documentation
3. âœ… Create markdown documentation
4. âœ… Commit everything back to your repository

## ðŸ“š Generated Documentation

After pushing, you'll find these files in your repository:

### Documentation Files
- docs/openapi.json - OpenAPI 3.0 specification
- docs/api_documentation.md - Human-readable API documentation

## ðŸ› ï¸ Manual Usage

You can also run the documentation generation manually:

`ash
# Install dependencies
pip install -r requirements.txt

# Run the analyzer on your FastAPI code
python analyzer/fastapi_analyzer.py

# Generate documentation
python generators/openapi_generator.py
`

## ðŸ“– Example Usage

Test the system with the provided example:

`ash
# Run the example FastAPI app
cd examples/
python sample_app.py

# In another terminal, test the analyzer
python ../analyzer/fastapi_analyzer.py
`

## ðŸ”§ Customization

### Customizing Generated Documentation

1. **Add detailed docstrings** to your FastAPI endpoints
2. **Use Pydantic models** with proper field descriptions
3. **Include examples** in your models
4. **Add tags** to organize endpoints

Example:
`python
@app.post("/users", tags=["Users"], summary="Create User")
async def create_user(user: UserCreate):
    """
    Create a new user in the system.
    
    This endpoint allows you to create a new user with the provided information.
    The user will be assigned a unique ID and created timestamp.
    """
    # Implementation here
`

## ðŸ”„ GitHub Action Configuration

The GitHub Action workflow (utodocgen.yml) can be customized:

- **Triggers**: Modify the on section to change when the action runs
- **Python version**: Update the Python version in the setup step
- **Dependencies**: Add additional dependencies if needed
- **Output paths**: Change where documentation is saved

## ðŸ“Š Supported Features

### FastAPI Features Supported
- âœ… Basic endpoint definitions
- âœ… HTTP methods (GET, POST, PUT, DELETE, PATCH)
- âœ… Path parameters
- âœ… Query parameters
- âœ… Request/Response models
- âœ… Pydantic models
- âœ… Tags and metadata
- âœ… Docstrings and descriptions

### Generated Outputs
- âœ… OpenAPI 3.0 specification
- âœ… Markdown documentation
- âœ… Type definitions
- âœ… Example usage

## ðŸš§ Roadmap

- [ ] Support for Flask applications
- [ ] Support for Django REST Framework
- [ ] Additional SDK languages (Go, Java, C#)
- [ ] Custom documentation templates
- [ ] API versioning support
- [ ] Authentication documentation
- [ ] Interactive API explorer

## ðŸ¤ Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## ðŸ“„ License

MIT License - see LICENSE file for details

## ðŸ†˜ Support

If you encounter any issues:

1. Check the GitHub Action logs
2. Verify your FastAPI code structure
3. Ensure all dependencies are installed
4. Open an issue on GitHub

---

**Happy coding! ðŸŽ‰ Your API documentation will never be out of sync again!**
