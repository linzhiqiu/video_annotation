import t2v_metrics
from llm.base import LLM
from typing import List

class OpenSource(LLM):
    def __init__(self, model="tarsier-recap-7b"):
        self.model = t2v_metrics.get_score_model(model=model).model
    
    def generate(self,
                 prompt: str,
                #  images: List[str] = [],
                 video: str = "",
                #  extracted_frames: List[int] = [],
                 **kwargs) -> str:
        """Generate text from a prompt. Optionally provide images or video."""
        output = self.model.generate([video], [prompt])[0]
        return output

if __name__ == "__main__":
    # model = OpenSource(model="tarsier-recap-7b")
    model = OpenSource(model="tarsier2-7b")
    # model = OpenSource(model="qwen2.5-vl-7b")
    print(
        model.generate(
            prompt="Describe the subject motion in this video.",
            # video="https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/f4ZzHtww6Tc.2.2.mp4",
            video="https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/d_T0KPYgqMA.0.2.mp4",
        )
    )

    model = OpenSource(model="perception-lm-8b")
    print(
        model.generate(
            prompt="Describe the subject motion in this video.",
            # video="https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/f4ZzHtww6Tc.2.2.mp4",
            video="https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/d_T0KPYgqMA.0.2.mp4",
        )
    )

