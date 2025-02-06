from typing import Dict, Type
from .base_model import BaseCaptionModel
from .tarsier_model import Tarsier7bModel, Tarsier35bModel
from .gemini_model import Gemini2FlashModel

class ModelFactory:
    """Factory for creating caption model instances."""
    
    _models: Dict[str, Type[BaseCaptionModel]] = {
        'Tarsier-7b': Tarsier7bModel,
        'Tarsier-35b': Tarsier35bModel,
        'Gemini 2.0 Flash': Gemini2FlashModel
    }
    
    @classmethod
    def get_model(cls, model_name: str) -> BaseCaptionModel:
        """Get a model instance by name.
        
        Args:
            model_name: Name of the model to create
            
        Returns:
            Instance of the requested model
            
        Raises:
            ValueError: If model_name is not recognized
        """
        if model_name not in cls._models:
            raise ValueError(f"Unknown model: {model_name}")
            
        model_class = cls._models[model_name]
        return model_class() 