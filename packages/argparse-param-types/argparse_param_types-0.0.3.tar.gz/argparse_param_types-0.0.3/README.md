# Argparse Param Types
## Introduction

Argparse is an excellent standard library for managing input in command-line python script, but it ships with only basic types. This project provides a library of option types that covers a lot of common use case to avoid rewriting again and again the same basic code.

## Installation

```
pip install argparse_param_types
```

## How to use


## Available option types

### file_type

### directory_type

### host_type

### ip_type

### rawip_type

### ip4_type

### rawip4_type

### ip6_type

### rawip6_type

### net_type

### rawnet_type

### net4_type

### rawnet4_type

### net6_type

### rawnet6_type

### port_type

## Changelog

#### 0.0.3
- Add missing dependencies in pyproject (dependencies not automatically installed when pip install)
- Add a `logs` flag on each param type to allow function nesting without erroneous error logging
- Bug fix: Do not log error when param_type function is used as a test in a success scenario
- Use more precise except exception class to better fit business logic and not broadly catch exceptions

#### 0.0.2
- Refactor to be PEP8 compliant, improve/add documentation, add type hinting
- Add easy import from module \_\_init__
- Add .gitignore to project
- Add param type host_type & ip_type & rawip_type & ip4_type & rawip4_type & ip6_type & rawip6_type & net_type & rawnet_type & net4_type & rawnet4_type & net6_type & rawnet6_type & port_type
- Add unit tests for every param type

#### 0.0.1
- Initial commit
- Implement param type file_type & directory_type

## License

[MIT License](https://opensource.org/licenses/MIT) © [ndmalc]