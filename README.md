# AutoDocGen - Automated API Documentation & SDK Generator

[![GitHub stars](https://img.shields.io/github/stars/yourusername/autoapigen?style=social)](https://github.com/yourusername/autoapigen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)

> **Never worry about API documentation falling out of sync again!** AutoDocGen automatically generates comprehensive API documentation and SDKs from your FastAPI code whenever you push to GitHub.

## 🚀 Features

- 🔄 **Automatic Updates** - Triggers on every GitHub push
- 📚 **API Documentation** - Generates OpenAPI 3.0 specs and markdown docs
- 🛠️ **SDK Generation** - Creates client libraries in multiple languages
- 🎯 **FastAPI Support** - Analyzes FastAPI applications automatically
- 📁 **Repo Integration** - Stores docs directly in your GitHub repository
- 🔒 **Secure** - No API keys or secrets required
- ⚡ **Fast** - Lightweight and efficient

## 🏗️ How It Works
─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ GitHub Push │───▶│ FastAPI Code │───▶│ Analysis │
└─────────────────┘ └─────────────────┘ └─────────────────┘
│
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Documentation │◀───│ Markdown Gen │◀───│ OpenAPI Spec │
└─────────────────┘ └─────────────────┘ └─────────────────┘
│
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ SDK Files │◀───│ SDK Generator │◀───│ │
└─────────────────┘ └─────────────────┘ └─────────────────┘


## 📁 Project Structure
autoapigen/
├── analyzer/ # FastAPI code analysis
│ └── fastapi_analyzer.py
├── generators/ # Documentation and SDK generators
│ └── openapi_generator.py
├── github_action/ # GitHub Actions workflow
│ └── .github/workflows/
│ └── autodocgen.yml
├── examples/ # Example FastAPI applications
│ └── sample_app.py
├── docs/ # Generated documentation
├── sdk/ # Generated SDKs
├── requirements.txt # Python dependencies
└── README.md # This file



## 🚀 Quick Start

### 1. Setup Your Repository

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/autoapigen.git
   cd autoapigen
   ```

2. **Copy the GitHub Action workflow** to your repository:
   ```bash
   mkdir -p .github/workflows
   cp github_action/.github/workflows/autodocgen.yml .github/workflows/
   ```

3. **Copy the AutoDocGen files** to your repository:
   ```bash
   cp -r analyzer/ generators/ requirements.txt ./
   ```

### 2. Configure Your FastAPI App

Make sure your FastAPI application includes proper metadata:

```python
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
```

### 3. Push to GitHub

Simply push your code to GitHub, and the automation will:

1. ✅ Analyze your FastAPI code
2. ✅ Generate OpenAPI documentation
3. ✅ Create markdown documentation
4. ✅ Build Python and JavaScript SDKs
5. ✅ Commit everything back to your repository

## 📚 Generated Documentation

After pushing, you'll find these files in your repository:

### Documentation Files
- `docs/openapi.json` - OpenAPI 3.0 specification
- `docs/api_documentation.md` - Human-readable API documentation
- `docs/README.md` - Documentation index

### SDK Files
- `sdk/python/` - Python client library
- `sdk/javascript/` - JavaScript/TypeScript client library

## 🛠️ Manual Usage

You can also run the documentation generation manually:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the analyzer on your FastAPI code
python analyzer/fastapi_analyzer.py

# Generate documentation and SDKs
python generators/openapi_generator.py
```

## 📖 Example Usage

### Python SDK Usage

```python
from sdk.python.client import APIClient

# Initialize client
client = APIClient('http://localhost:8000')

# Use API methods
users = client.get_users()
new_user = client.create_user({
    "username": "johndoe",
    "email": "john@example.com"
})
```

### JavaScript SDK Usage

```javascript
import APIClient from './sdk/javascript/client.js';

// Initialize client
const client = new APIClient('http://localhost:8000');

// Use API methods
const users = await client.get('/users');
const newUser = await client.post('/users', {
    username: 'johndoe',
    email: 'john@example.com'
});
```

## 🧪 Testing

Test the system with the provided example:

```bash
# Run the example FastAPI app
cd examples/
python sample_app.py

# In another terminal, test the analyzer
python ../analyzer/fastapi_analyzer.py
```

## 🔧 Customization

### Customizing Generated Documentation

1. **Add detailed docstrings** to your FastAPI endpoints
2. **Use Pydantic models** with proper field descriptions
3. **Include examples** in your models
4. **Add tags** to organize endpoints

Example:
```python
@app.post("/users", tags=["Users"], summary="Create User")
async def create_user(user: UserCreate):
    """
    Create a new user in the system.
    
    This endpoint allows you to create a new user with the provided information.
    The user will be assigned a unique ID and created timestamp.
    """
    # Implementation here
```

### Customizing SDK Generation

The SDK generators can be extended to support additional languages or customize the generated code. Modify the generator classes in `generators/openapi_generator.py`.

## 🔄 GitHub Action Configuration

The GitHub Action workflow (`autodocgen.yml`) can be customized:

- **Triggers**: Modify the `on` section to change when the action runs
- **Python version**: Update the Python version in the setup step
- **Dependencies**: Add additional dependencies if needed
- **Output paths**: Change where documentation and SDKs are saved

## 📊 Supported Features

### FastAPI Features Supported
- ✅ Basic endpoint definitions
- ✅ HTTP methods (GET, POST, PUT, DELETE, PATCH)
- ✅ Path parameters
- ✅ Query parameters
- ✅ Request/Response models
- ✅ Pydantic models
- ✅ Tags and metadata
- ✅ Docstrings and descriptions

### Generated Outputs
- ✅ OpenAPI 3.0 specification
- ✅ Markdown documentation
- ✅ Python client SDK
- ✅ JavaScript/TypeScript SDK
- ✅ Type definitions
- ✅ Example usage

## 🚧 Roadmap

- [ ] Support for Flask applications
- [ ] Support for Django REST Framework
- [ ] Additional SDK languages (Go, Java, C#)
- [ ] Custom documentation templates
- [ ] API versioning support
- [ ] Authentication documentation
- [ ] Interactive API explorer

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/autoapigen.git
cd autoapigen

# Install dependencies
pip install -r requirements.txt

# Run tests
python analyzer/fastapi_analyzer.py
python generators/openapi_generator.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. **Check the GitHub Action logs** in your repository
2. **Verify your FastAPI code structure**
3. **Ensure all dependencies are installed**
4. **Open an issue** on GitHub with:
   - Description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your FastAPI code (if relevant)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The amazing Python web framework
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation using Python type annotations
- [OpenAPI](https://swagger.io/specification/) - The OpenAPI Specification
- [GitHub Actions](https://github.com/features/actions) - For seamless automation

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/autoapigen?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/autoapigen?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/autoapigen)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/autoapigen)

---



**Made with ❤️ for the vibea coders community**

*Happy coding! 🎉 Your API documentation will never be out of sync again!*


