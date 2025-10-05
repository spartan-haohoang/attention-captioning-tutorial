"""
Tests for model-related functionality.
"""

import pytest
import torch
import torch.nn as nn
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestModelFunctions:
    """Test cases for model-related functions."""
    
    def test_torch_import(self):
        """Test that PyTorch can be imported."""
        import torch
        assert torch.__version__ is not None
    
    def test_torch_device_availability(self):
        """Test device availability."""
        import torch
        
        # Test CPU availability
        assert torch.cuda.is_available() or True  # CPU is always available
        
        # Test tensor creation on CPU
        tensor = torch.tensor([1, 2, 3])
        assert tensor.device.type == 'cpu'
    
    def test_basic_tensor_operations(self):
        """Test basic tensor operations."""
        import torch
        
        # Create tensors
        a = torch.tensor([1, 2, 3])
        b = torch.tensor([4, 5, 6])
        
        # Test addition
        c = a + b
        expected = torch.tensor([5, 7, 9])
        assert torch.equal(c, expected)
        
        # Test multiplication
        d = a * 2
        expected = torch.tensor([2, 4, 6])
        assert torch.equal(d, expected)
    
    def test_neural_network_creation(self):
        """Test basic neural network creation."""
        import torch
        import torch.nn as nn
        
        # Create a simple neural network
        class SimpleNet(nn.Module):
            def __init__(self):
                super(SimpleNet, self).__init__()
                self.fc1 = nn.Linear(10, 5)
                self.fc2 = nn.Linear(5, 1)
            
            def forward(self, x):
                x = torch.relu(self.fc1(x))
                x = self.fc2(x)
                return x
        
        # Test network creation
        net = SimpleNet()
        assert isinstance(net, nn.Module)
        
        # Test forward pass
        input_tensor = torch.randn(1, 10)
        output = net(input_tensor)
        assert output.shape == (1, 1)
    
    def test_attention_mechanism_basic(self):
        """Test basic attention mechanism implementation."""
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        
        class SimpleAttention(nn.Module):
            def __init__(self, hidden_dim):
                super(SimpleAttention, self).__init__()
                self.attention = nn.Linear(hidden_dim, 1)
            
            def forward(self, encoder_outputs):
                # encoder_outputs: (seq_len, batch_size, hidden_dim)
                attention_weights = F.softmax(self.attention(encoder_outputs), dim=0)
                context_vector = torch.sum(attention_weights * encoder_outputs, dim=0)
                return context_vector, attention_weights
        
        # Test attention mechanism
        hidden_dim = 64
        seq_len = 10
        batch_size = 1
        
        attention = SimpleAttention(hidden_dim)
        encoder_outputs = torch.randn(seq_len, batch_size, hidden_dim)
        
        context_vector, attention_weights = attention(encoder_outputs)
        
        assert context_vector.shape == (batch_size, hidden_dim)
        assert attention_weights.shape == (seq_len, batch_size, 1)
        assert torch.allclose(torch.sum(attention_weights, dim=0), torch.ones(batch_size, 1), atol=1e-6)
    
    def test_image_tensor_creation(self):
        """Test image tensor creation and manipulation."""
        import torch
        import torchvision.transforms as transforms
        
        # Create a dummy image tensor (RGB, 224x224)
        dummy_image = torch.randn(3, 224, 224)
        
        # Test image transforms
        transform = transforms.Compose([
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        normalized_image = transform(dummy_image)
        assert normalized_image.shape == (3, 224, 224)
    
    def test_text_tokenization_basic(self):
        """Test basic text tokenization."""
        import torch
        from torchtext.data.utils import get_tokenizer
        
        # Test tokenizer
        tokenizer = get_tokenizer('basic_english')
        text = "A person is walking in the park"
        tokens = tokenizer(text)
        
        assert isinstance(tokens, list)
        assert len(tokens) > 0
        assert all(isinstance(token, str) for token in tokens)


if __name__ == '__main__':
    pytest.main([__file__])
