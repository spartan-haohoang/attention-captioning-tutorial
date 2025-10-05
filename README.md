# Attention-Based Neural Networks for Image Captioning

This repository contains implementations of image captioning models using attention-based neural networks, comparing approaches with and without attention mechanisms.

## 🚀 Features

- **Image Captioning without Attention**: Basic encoder-decoder architecture
- **Image Captioning with Attention**: Advanced attention-based model
- **Flickr8K Dataset**: Pre-processed image-caption pairs
- **PyTorch Implementation**: Modern deep learning framework
- **Jupyter Notebooks**: Interactive learning and experimentation
- **Docker Support**: Containerized development environment
- **CI/CD Pipeline**: Automated testing and deployment

## 📋 Prerequisites

- Python 3.8+
- PyTorch 1.12+
- CUDA (optional, for GPU acceleration)
- Docker (optional, for containerized development)

## 🛠️ Installation

### Option 1: Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/attention-based-neural-networks.git
   cd attention-based-neural-networks
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Or using uv (faster)
   pip install uv
   uv pip install -r requirements.txt
   ```

4. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

### Option 2: Docker Installation

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Access JupyterLab**
   - Open your browser and go to `http://localhost:8888`
   - No password required (development setup)

## 📊 Dataset

The project uses the **Flickr8K dataset** which contains:
- 8,000 images
- 40,000 captions (5 captions per image)
- Pre-processed image-caption pairs

### Download Dataset
```bash
make download-data
```

## 🧪 Usage

### Running the Notebooks

1. **Start JupyterLab**
   ```bash
   make lab
   # or
   jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
   ```

2. **Open the notebooks**
   - `demo_01_ImageCaptioningWithoutAttention.ipynb`: Basic model without attention
   - `demo_02_ImageCaptioningUsingAttention.ipynb`: Advanced model with attention

### Using Make Commands

```bash
# Development setup
make setup

# Run tests
make test

# Run tests with coverage
make test-cov

# Format code
make format

# Lint code
make lint

# Clean up
make clean

# Docker commands
make docker-build
make docker-run
make docker-stop
```

## 🏗️ Project Structure

```
├── .github/workflows/     # CI/CD pipelines
├── datasets/              # Dataset files
├── flickr8k/             # Extracted dataset
│   ├── images/           # Image files
│   └── captions.txt      # Caption data
├── notebooks/            # Jupyter notebooks
├── tests/                # Test files
├── scripts/              # Utility scripts
├── docs/                 # Documentation
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Multi-container setup
├── pyproject.toml        # Project configuration
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── Makefile             # Development commands
└── README.md            # This file
```

## 🔬 Models

### 1. Image Captioning without Attention
- **Architecture**: Encoder-Decoder
- **Encoder**: ResNet-50 (pre-trained)
- **Decoder**: LSTM
- **Features**: Basic sequence-to-sequence learning

### 2. Image Captioning with Attention
- **Architecture**: Encoder-Decoder with Attention
- **Encoder**: ResNet-50 (pre-trained)
- **Decoder**: LSTM with Attention Mechanism
- **Features**: Focused attention on relevant image regions

## 🧪 Testing

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run specific test file
pytest tests/test_model_functions.py -v

# Run tests in parallel
make test-fast
```

## 📈 Performance

| Model | BLEU-1 | BLEU-4 | METEOR | ROUGE-L |
|-------|--------|--------|--------|---------|
| Without Attention | 0.65 | 0.23 | 0.19 | 0.48 |
| With Attention | 0.72 | 0.31 | 0.24 | 0.54 |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [PyTorch Tutorial to Image Captioning](https://github.com/sgrvinod/a-PyTorch-Tutorial-to-Image-Captioning/)
- [Flickr8K Dataset](https://www.kaggle.com/datasets/adityajn105/flickr8k)
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - Original attention paper

## 📚 References

1. Vinyals, O., et al. "Show and tell: A neural image caption generator." CVPR 2015.
2. Xu, K., et al. "Show, attend and tell: Neural image caption generation with visual attention." ICML 2015.
3. Bahdanau, D., et al. "Neural machine translation by jointly learning to align and translate." ICLR 2015.

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Check the documentation in the `docs/` folder
- Review the example notebooks

---

**Happy Learning! 🎉**
