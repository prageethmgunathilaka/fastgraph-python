# FastGraph Documentation

Welcome to the FastGraph project documentation. This folder contains comprehensive documentation for understanding, setting up, and using the FastGraph API.

## 📚 Documentation Index

### 🚀 Getting Started
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup and installation guide
  - Quick start instructions
  - Configuration options
  - Troubleshooting common issues
  - Development guidelines

### 📖 API Reference
- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation
  - All endpoint details
  - Request/response formats
  - Code examples
  - Error handling
  - Best practices

### 🔧 Project Improvements
- **[IMPROVEMENTS.md](IMPROVEMENTS.md)** - Comprehensive project improvements
  - New features added
  - Architecture changes
  - Testing infrastructure
  - Performance optimizations
  - Future development roadmap

## 🎯 Quick Navigation

### For New Users
1. Start with **[SETUP_GUIDE.md](SETUP_GUIDE.md)** to get the project running
2. Check **[API_REFERENCE.md](API_REFERENCE.md)** for endpoint usage
3. Review **[IMPROVEMENTS.md](IMPROVEMENTS.md)** to understand capabilities

### For Developers
1. Review **[IMPROVEMENTS.md](IMPROVEMENTS.md)** for architecture understanding
2. Use **[API_REFERENCE.md](API_REFERENCE.md)** for integration details
3. Follow **[SETUP_GUIDE.md](SETUP_GUIDE.md)** for development setup

### For API Integration
1. Focus on **[API_REFERENCE.md](API_REFERENCE.md)** for endpoint details
2. Check **[SETUP_GUIDE.md](SETUP_GUIDE.md)** for configuration
3. Review **[IMPROVEMENTS.md](IMPROVEMENTS.md)** for advanced features

## 🏗️ Project Structure

```
fatgraph/
├── agents/                 # Agent implementations
│   ├── regular_agent.py   # Single command agent
│   ├── workflow_agent.py  # Multi-command workflow agent
│   ├── orchestrate_agent.py # Hierarchical orchestration agent
│   └── MParser/           # Specialized parsing module
├── docs/                  # 📁 This documentation
├── test/                  # Comprehensive test suite
├── main.py                # FastAPI application
├── config.py              # Configuration management
└── README.md              # Project overview
```

## 🔗 Key Endpoints

| Endpoint | Purpose | Complexity |
|----------|---------|------------|
| `/ask` | Single command processing | Basic |
| `/workflowask` | Multi-command workflows | Intermediate |
| `/orchestrate` | Hierarchical workflows | Advanced |

## 🧪 Testing

### Quick Test
```bash
# Run integration tests
python test/test_orchestrate_integration.py

# Run pytest tests
pytest test/test_orchestrate_pytest.py -v
```

### Individual Endpoint Tests
```bash
# Test basic functionality
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello"}'

# Test orchestration
curl -X POST "http://localhost:8000/orchestrate" \
  -H "Content-Type: application/json" \
  -d '{"tasks": [["Hello"], ["World"]]}'
```

## 📈 Recent Improvements

### ✅ Completed Features
- ✅ Hierarchical workflow orchestration
- ✅ Recursive type system for unlimited nesting
- ✅ Comprehensive testing infrastructure
- ✅ Enhanced error handling and fallbacks
- ✅ Improved configuration management
- ✅ Complete API documentation
- ✅ MParser module structure

### 🔄 In Progress
- 🔄 MParser implementation
- 🔄 Model configuration fixes
- 🔄 Performance monitoring

### 📋 Planned
- 📋 Advanced orchestration patterns
- 📋 Real-time monitoring
- 📋 Docker deployment
- 📋 CI/CD pipeline

## 🆘 Support

### Documentation
- All documentation is self-contained in this folder
- Each file focuses on a specific aspect
- Cross-references between documents

### Testing
- Comprehensive test suite covers all scenarios
- Integration tests verify real-world usage
- Pytest framework for automated testing

### Development
- Clear architecture for easy extension
- Modular design for maintainability
- Type safety throughout the codebase

---

*This documentation provides everything needed to understand, use, and extend the FastGraph project.* 