# Amdahl's Law Performance Analyzer

A Python-based computational analysis tool that applies **Amdahl's Law** to calculate processing speedup, efficiency, and parallel performance across varying processor counts. The tool is containerized in Docker to ensure reproducibility and cross-platform compatibility on Linux and Windows systems.

## 📋 Overview

This project provides an interactive and automated utility for evaluating performance scaling in parallel systems. It enables educational and research applications in performance modeling, parallel computing, and high-performance systems.

### Key Features

- **Amdahl's Law Computation**: Calculate speedup, efficiency, and execution time ratios
- **Parallel Scaling Simulation**: Analyze performance across processor counts from 1 to millions
- **Visualization**: Generate plots showing speedup, efficiency, and execution time trends
- **Command-Line Interface**: Easy-to-use CLI with configuration file support
- **Docker Support**: Fully containerized for consistent behavior across platforms
- **Comprehensive Testing**: Unit tests with known mathematical results

## 🏗️ System Architecture

```
Cython/
├── amdahl.py              # Core computation functions (speedup, efficiency, execution time)
├── visualize.py           # Matplotlib plotting functions
├── cli.py                 # Main CLI entry point (runs via Docker or directly)
├── utils.py               # Validation, file I/O, helper functions
├── config.yaml            # Default configuration template
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker container definition
├── docker-compose.yml     # Optional Docker Compose setup
├── Makefile               # Build and run convenience commands
├── README.md              # This file
├── LICENSE                # MIT License
├── tests/
│   └── test_amdahl.py     # pytest unit tests
└── .gitignore             # Git ignore patterns
```

## 🔧 Installation

### Prerequisites

- **Python 3.12+** (for local development)
- **Docker** (for containerized execution)
- **Make** (optional, for convenience commands)

### Local Installation

1. Clone or download this repository
2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

Or using the Makefile:

```bash
make install
```

### Docker Installation

Build the Docker image:

```bash
docker build -t amdahl-analyzer .
```

Or using the Makefile:

```bash
make build
```

## 🚀 Usage

### Command-Line Interface

#### Basic Usage

```bash
python cli.py --fraction 0.05 --max_procs 100
```

#### With Custom Output Directory

```bash
python cli.py -f 0.1 -p 50 --output-dir ./results
```

#### Using Configuration File

```bash
python cli.py --config config.yaml
```

#### Skip Plot Generation

```bash
python cli.py --fraction 0.2 --max_procs 200 --no-plots
```

### Docker Usage

#### Run with Default Arguments

```bash
docker run --rm amdahl-analyzer
```

#### Run with Custom Arguments

```bash
docker run --rm amdahl-analyzer --fraction 0.05 --max_procs 100
```

#### Run with Volume Mount for Output

```bash
docker run --rm -v $(pwd)/output:/app/output amdahl-analyzer
```

#### Using Docker Compose

```bash
docker-compose up
```

### Makefile Commands

```bash
make build    # Build Docker image
make run      # Run Docker container with default arguments
make test     # Run pytest tests locally
make install  # Install Python dependencies locally
make clean    # Remove Docker images and output files
make help     # Show all available commands
```

## 📊 Amdahl's Law Formulas

The tool implements the following mathematical formulas:

### Speedup
\[
S_p = \frac{1}{f + \frac{1 - f}{p}}
\]

where:
- \( S_p \) = Speedup with p processors
- \( f \) = Fraction of the program that is sequential (0 ≤ f ≤ 1)
- \( p \) = Number of processors (p ≥ 1)

### Efficiency
\[
E_p = \frac{S_p}{p}
\]

### Execution Time Ratio
\[
\frac{T_p}{T_1} = \frac{1}{S_p}
\]

## ⚙️ Configuration

The tool supports configuration via YAML file (`config.yaml`):

```yaml
# Fraction of the program that is sequential (0 <= fraction <= 1)
fraction: 0.05

# Maximum number of processors to simulate
max_procs: 100

# Output directory for generated plots (relative to project root or current working directory)
output_dir: "./output"

# Whether to generate plots (true/false)
generate_plots: true
```

**Note**: Command-line arguments override configuration file values.

## 📈 Output

The tool generates:

1. **Console Table**: Formatted table showing processors, speedups, efficiencies, and time ratios
2. **Plot Files** (if enabled):
   - `speedup.png`: Speedup vs. Number of Processors
   - `efficiency.png`: Efficiency vs. Number of Processors
   - `execution_time.png`: Execution Time Ratio vs. Number of Processors

### Example Output

```
======================================================================
Amdahl's Law Performance Analysis
======================================================================
Sequential Fraction (f): 0.05
Maximum Processors: 100
======================================================================

Performance Results:
+------------+-----------+------------+-------------+
| Processors | Speedup   | Efficiency | Time Ratio  |
+============+===========+============+=============+
| 1          | 1.000000  | 1.000000   | 1.000000    |
| 2          | 1.904762  | 0.952381   | 0.525000    |
| ...        | ...       | ...        | ...         |
| 100        | 19.047619 | 0.190476   | 0.052500    |
+------------+-----------+------------+-------------+
```

## 🧪 Testing

Run the test suite:

```bash
pytest tests/ -v
```

Or using the Makefile:

```bash
make test
```

### Test Coverage

The test suite validates:
- Correctness of mathematical calculations with known values
- Input validation (negative values, out-of-range values)
- Edge cases (fully sequential, fully parallel, single processor)
- Scaling simulation accuracy
- Consistency between individual calculations and batch simulations

## 📝 Command-Line Arguments

| Argument | Short | Description | Required |
|----------|-------|-------------|----------|
| `--fraction` | `-f` | Sequential fraction (0 ≤ f ≤ 1) | Yes* |
| `--max_procs` | `-p` | Maximum processors to simulate | No (default: 100) |
| `--config` | | Path to YAML config file | No |
| `--output-dir` | | Output directory for plots | No (default: ./output) |
| `--no-plots` | | Skip generating plots | No |

*Required if not provided in config file

## 🐳 Docker Details

### Dockerfile

The Dockerfile uses:
- Base image: `python:3.12-slim`
- Working directory: `/app`
- Entrypoint: `python cli.py`
- Non-interactive matplotlib backend (`Agg`)

### Docker Compose

The `docker-compose.yml` provides:
- Volume mounts for output directory
- Configurable environment variables
- Easy service management

## 🔍 Example Use Cases

### Educational Use

Demonstrate Amdahl's Law concepts:
```bash
python cli.py --fraction 0.10 --max_procs 50
```

### Research Analysis

Analyze scaling behavior for different sequential fractions:
```bash
for f in 0.01 0.05 0.10 0.20; do
    python cli.py --fraction $f --max_procs 100 --output-dir "./results/f_${f}"
done
```

### Performance Benchmarking

Compare efficiency across processor counts:
```bash
python cli.py --fraction 0.05 --max_procs 1000 --no-plots
```

## 🛠️ Development

### Project Structure

- **amdahl.py**: Core computation module with Amdahl's Law formulas
- **visualize.py**: Matplotlib plotting utilities
- **cli.py**: Command-line interface and main entry point
- **utils.py**: Validation, configuration loading, and helper functions
- **tests/**: Unit tests using pytest

### Code Standards

- PEP 257 docstrings for all functions
- Type hints for function parameters and returns
- Input validation at function and CLI levels
- Cross-platform path handling using `pathlib.Path`
- No hardcoded absolute paths

### Contributing

1. Follow PEP 8 style guidelines
2. Add docstrings to all new functions
3. Write tests for new functionality
4. Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Denzel Prince**

## 🔮 Future Enhancements

- Web interface using Flask or FastAPI
- GPU acceleration via CUDA for visualization tasks
- Integration with benchmarking datasets
- CI/CD integration for auto-build and testing
- Interactive Jupyter notebook support

## 📚 References

- [Amdahl's Law - Wikipedia](https://en.wikipedia.org/wiki/Amdahl%27s_law)
- [Parallel Computing Fundamentals](https://en.wikipedia.org/wiki/Parallel_computing)

## 🐛 Troubleshooting

### Common Issues

**Issue**: Matplotlib plots not displaying in Docker
- **Solution**: The tool uses non-interactive backend (`Agg`) by default for Docker compatibility. Plots are saved as PNG files.

**Issue**: Config file not found
- **Solution**: Ensure `config.yaml` exists in the current directory or provide full path with `--config` argument.

**Issue**: Permission errors in output directory
- **Solution**: Ensure write permissions for the output directory or use `--output-dir` to specify a writable location.

---

For questions or issues, please refer to the project documentation or create an issue in the repository.

