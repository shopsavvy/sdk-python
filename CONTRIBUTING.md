# Contributing to ShopSavvy Python SDK

Thank you for your interest in contributing to the ShopSavvy Python SDK! This document provides guidelines for contributing to this open-source project.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip or pipenv for package management
- A ShopSavvy Data API key (get one at [https://shopsavvy.com/data](https://shopsavvy.com/data))

### Setup Steps

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/python-sdk
   cd python-sdk
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Verify installation**
   ```bash
   python -c "import shopsavvy; print('Installation successful!')"
   ```

## Development Workflow

### Project Structure

```
src/shopsavvy/
├── __init__.py       # Package initialization and exports
├── client.py         # Main API client implementation
├── models.py         # Pydantic data models
├── exceptions.py     # Custom exception classes
└── utils.py          # Utility functions (future)

tests/
├── test_client.py    # Client tests
├── test_models.py    # Model tests
├── conftest.py       # pytest configuration
└── fixtures/         # Test data fixtures
```

### Building and Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src/shopsavvy --cov-report=html

# Run specific test file
pytest tests/test_client.py

# Run tests and generate coverage report
pytest --cov=src/shopsavvy --cov-report=term-missing

# Type checking
mypy src/shopsavvy

# Code formatting
black src tests

# Import sorting
isort src tests

# Linting
flake8 src tests
```

## Code Guidelines

### Python Standards

- Follow PEP 8 style guide
- Use type hints for all functions and methods
- Use Pydantic models for data validation
- Write comprehensive docstrings using Google style
- Maintain Python 3.8+ compatibility

### Code Style

- Use Black for code formatting (line length: 88)
- Use isort for import sorting
- Use meaningful variable and function names
- Keep functions focused and small
- Use async/await for I/O operations where appropriate

### Documentation Standards

```python
def get_product_details(
    self, 
    identifier: str, 
    format: Optional[Literal["json", "csv"]] = None
) -> APIResponse[ProductDetails]:
    """
    Look up product details by identifier.
    
    Args:
        identifier: Product identifier (barcode, ASIN, URL, model number, 
                   or ShopSavvy product ID)
        format: Response format, either 'json' or 'csv'
        
    Returns:
        APIResponse containing ProductDetails
        
    Raises:
        NotFoundError: If product is not found
        ValidationError: If identifier format is invalid
        
    Example:
        >>> product = api.get_product_details("012345678901")
        >>> print(product.data.name)
        "Example Product"
    """
```

### Error Handling

- Use custom exception classes from `exceptions.py`
- Provide meaningful error messages
- Include relevant context in exceptions
- Handle HTTP errors appropriately

```python
try:
    response = self._make_request("GET", "/products/details", params=params)
except httpx.HTTPStatusError as e:
    if e.response.status_code == 404:
        raise NotFoundError(f"Product not found: {identifier}")
    elif e.response.status_code == 401:
        raise AuthenticationError("Invalid API key")
    else:
        raise APIError(f"HTTP {e.response.status_code}: {e.response.text}")
```

## Adding New Features

### Adding New API Methods

1. **Define the method signature**
   ```python
   def new_api_method(
       self,
       required_param: str,
       optional_param: Optional[str] = None
   ) -> APIResponse[ReturnType]:
   ```

2. **Add comprehensive docstring**
   - Brief description
   - Parameter descriptions
   - Return value description
   - Possible exceptions
   - Usage example

3. **Implement the method**
   - Use existing patterns for consistency
   - Handle errors appropriately
   - Validate input parameters

4. **Add response model if needed**
   ```python
   class NewResponseModel(BaseModel):
       field1: str
       field2: Optional[int] = None
   ```

5. **Write tests**
   - Unit tests for the method
   - Integration tests with mocked responses
   - Error condition tests

6. **Update documentation**
   - Add examples to README
   - Update API reference

### Adding New Models

1. **Define Pydantic model**
   ```python
   class NewModel(BaseModel):
       """Model description"""
       
       field1: str = Field(..., description="Field description")
       field2: Optional[int] = Field(None, description="Optional field")
       
       @validator('field1')
       def validate_field1(cls, v):
           if not v.strip():
               raise ValueError('field1 cannot be empty')
           return v
   ```

2. **Add to `__init__.py` exports**
3. **Write tests for validation**
4. **Update type hints in client methods**

## Testing

### Unit Tests

Write comprehensive unit tests for all functionality:

```python
import pytest
from httpx_mock import HTTPXMock
from shopsavvy import create_client, NotFoundError

def test_get_product_details_success():
    """Test successful product lookup"""
    with HTTPXMock() as httpx_mock:
        # Mock the API response
        httpx_mock.add_response(
            url="https://api.shopsavvy.com/v1/products/details?identifier=123",
            json={
                "success": True,
                "data": {
                    "product_id": "123",
                    "name": "Test Product",
                    "brand": "Test Brand"
                }
            }
        )
        
        api = create_client("ss_test_123")
        result = api.get_product_details("123")
        
        assert result.success is True
        assert result.data.name == "Test Product"
        assert result.data.brand == "Test Brand"

def test_get_product_details_not_found():
    """Test product not found error"""
    with HTTPXMock() as httpx_mock:
        httpx_mock.add_response(
            url="https://api.shopsavvy.com/v1/products/details?identifier=invalid",
            status_code=404,
            json={"error": "Product not found"}
        )
        
        api = create_client("ss_test_123")
        
        with pytest.raises(NotFoundError):
            api.get_product_details("invalid")
```

### Integration Tests

Test against real API (use test API keys):

```python
import os
import pytest
from shopsavvy import create_client

@pytest.mark.integration
def test_real_api_product_lookup():
    """Test against real API - requires SHOPSAVVY_TEST_API_KEY env var"""
    api_key = os.getenv("SHOPSAVVY_TEST_API_KEY")
    if not api_key:
        pytest.skip("SHOPSAVVY_TEST_API_KEY not set")
    
    api = create_client(api_key)
    result = api.get_product_details("012345678901")
    
    assert result.success is True
    assert result.data.product_id is not None
```

### Test Configuration

Configure pytest in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=src/shopsavvy --cov-report=term-missing"
markers = [
    "integration: marks tests as integration tests (may be slow)",
    "unit: marks tests as unit tests",
]
```

## Documentation

### README Updates

- Keep examples current and working
- Update installation instructions
- Add new features to API reference
- Ensure all links work

### Docstring Standards

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int = 10) -> bool:
    """
    Brief description of what the function does.
    
    Longer description if needed, explaining the function's behavior,
    algorithms used, or important notes.
    
    Args:
        param1: Description of param1
        param2: Description of param2, defaults to 10
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not an integer
        
    Example:
        >>> result = example_function("hello", 5)
        >>> print(result)
        True
    """
```

## Submitting Changes

### Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests for new functionality**
5. **Update documentation**
6. **Run all tests and quality checks**
   ```bash
   pytest
   mypy src/shopsavvy
   black src tests
   isort src tests
   flake8 src tests
   ```
7. **Submit a pull request**

### Pull Request Guidelines

- **Clear title**: Describe what the PR does
- **Detailed description**: Explain the changes and why they're needed
- **Breaking changes**: Clearly mark any breaking changes
- **Test coverage**: Ensure all new code is tested
- **Documentation**: Update relevant documentation

### Commit Messages

Use conventional commit format:

```
feat: add support for batch product lookups
fix: handle timeout errors properly  
docs: update README with async examples
test: add integration tests for price history
refactor: improve error handling consistency
```

## Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Pre-release Checklist

- [ ] All tests pass
- [ ] Code coverage > 90%
- [ ] Documentation updated
- [ ] Type checking passes
- [ ] No linting errors
- [ ] CHANGELOG updated
- [ ] Version bumped in `pyproject.toml`

### Release Steps

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag v1.x.x`
4. Push tag: `git push origin v1.x.x`
5. Build package: `python -m build`
6. Upload to PyPI: `twine upload dist/*`
7. Create GitHub release

## Code Quality Standards

### Type Checking

All code must pass mypy type checking:

```bash
mypy src/shopsavvy --strict
```

### Test Coverage

Maintain >90% test coverage:

```bash
pytest --cov=src/shopsavvy --cov-fail-under=90
```

### Code Style

Code must pass all style checks:

```bash
black --check src tests
isort --check-only src tests  
flake8 src tests
```

## Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Email**: Contact us at [business@shopsavvy.com](mailto:business@shopsavvy.com)

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make the ShopSavvy Python SDK better! 🛍️