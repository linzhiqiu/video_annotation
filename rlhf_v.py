"""
Simple function-based API for text difference detection using Qwen2 tokenizer.

Usage:
from transformers import Qwen2TokenizerFast
from diff_utils_qwen import get_diff_indices

tokenizer = Qwen2TokenizerFast.from_pretrained("Qwen/Qwen2-7B")

orig_changed, new_changed, orig_unchanged, new_unchanged = get_diff_indices(
    "Hello world",
    "Hello there",
    tokenizer
)
"""

import difflib
from typing import List, Tuple


def get_diff_indices(
    original_text: str,
    changed_text: str,
    tokenizer,  # Qwen2TokenizerFast instance (required)
    mode: str = "rlhf-v",
    min_match_size: int = 1
) -> Tuple[List[int], List[int], List[int], List[int]]:
    """
    Find changed and unchanged token indices between two texts using Qwen tokenizer.
    
    Args:
        original_text: Original text string
        changed_text: Modified text string
        tokenizer: Qwen2TokenizerFast instance (REQUIRED)
        mode: Either "rlhf-v" (SequenceMatcher, same as RLHF-V) 
              or "differ" (difflib.Differ)
        min_match_size: Minimum length of matching block to consider unchanged
                       (only used in "rlhf-v" mode)
    
    Returns:
        Tuple of (original_changed_ids, changed_changed_ids, 
                 original_unchanged_ids, changed_unchanged_ids)
        - original_changed_ids: indices of changed tokens in original text
        - changed_changed_ids: indices of changed tokens in changed text
        - original_unchanged_ids: indices of unchanged tokens in original text
        - changed_unchanged_ids: indices of unchanged tokens in changed text
    
    Examples:
        >>> from transformers import Qwen2TokenizerFast
        >>> tkz = Qwen2TokenizerFast.from_pretrained("Qwen/Qwen2-7B")
        >>> orig_ch, new_ch, _, _ = get_diff_indices(
        ...     "The cat sat", "The dog sat", tkz
        ... )
        >>> print(orig_ch)  # Indices of changed tokens
    """
    if tokenizer is None:
        raise ValueError("tokenizer is required! Pass a Qwen2TokenizerFast instance.")
    
    # Tokenize using Qwen
    seq1 = tokenizer.tokenize(original_text)
    seq2 = tokenizer.tokenize(changed_text)
    
    # Choose algorithm
    if mode == "rlhf-v":
        return _diff_rlhfv(seq1, seq2, min_match_size)
    elif mode == "differ":
        return _diff_differ(seq1, seq2)
    else:
        raise ValueError(f"Unknown mode: {mode}. Choose 'rlhf-v' or 'differ'")


def _diff_rlhfv(
    seq1: List[str],
    seq2: List[str],
    min_match_size: int = 1
) -> Tuple[List[int], List[int], List[int], List[int]]:
    """RLHF-V method using SequenceMatcher."""
    sm = difflib.SequenceMatcher(None, seq1, seq2)
    opcodes = sm.get_opcodes()
    
    seq1_changed = []
    seq1_unchanged = []
    seq2_changed = []
    seq2_unchanged = []
    
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'equal':
            # Check if match is long enough
            if i2 - i1 >= min_match_size:
                seq1_unchanged.extend(range(i1, i2))
                seq2_unchanged.extend(range(j1, j2))
            else:
                # Too short - count as changed
                seq1_changed.extend(range(i1, i2))
                seq2_changed.extend(range(j1, j2))
        else:  # 'replace', 'delete', or 'insert'
            seq1_changed.extend(range(i1, i2))
            seq2_changed.extend(range(j1, j2))
    
    return (
        sorted(seq1_changed),
        sorted(seq2_changed),
        sorted(seq1_unchanged),
        sorted(seq2_unchanged)
    )


def _diff_differ(
    seq1: List[str],
    seq2: List[str]
) -> Tuple[List[int], List[int], List[int], List[int]]:
    """difflib.Differ method."""
    differ = difflib.Differ()
    diff = list(differ.compare(seq1, seq2))
    
    seq1_changed = []
    seq1_unchanged = []
    seq2_changed = []
    seq2_unchanged = []
    
    seq1_idx = 0
    seq2_idx = 0
    
    for token in diff:
        prefix = token[:2]
        
        if prefix == '  ':  # Unchanged
            seq1_unchanged.append(seq1_idx)
            seq2_unchanged.append(seq2_idx)
            seq1_idx += 1
            seq2_idx += 1
        elif prefix == '- ':  # Deleted
            seq1_changed.append(seq1_idx)
            seq1_idx += 1
        elif prefix == '+ ':  # Added
            seq2_changed.append(seq2_idx)
            seq2_idx += 1
    
    return (
        sorted(seq1_changed),
        sorted(seq2_changed),
        sorted(seq1_unchanged),
        sorted(seq2_unchanged)
    )


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("This version requires Qwen2TokenizerFast.")
    print("Install: pip install transformers")
    print()
    
    try:
        from transformers import Qwen2TokenizerFast
        
        print("Loading Qwen2 tokenizer...")
        # You'll need to specify your actual model path
        print("Note: Update the path to your Qwen2 model in the script")
        print()
        
        # Uncomment and update path when ready:
        # tokenizer = Qwen2TokenizerFast.from_pretrained("Qwen/Qwen2-7B")
        # 
        # text1 = "The cat sat on the mat"
        # text2 = "The dog sat on the rug"
        # 
        # orig_ch, new_ch, _, _ = get_diff_indices(text1, text2, tokenizer)
        # 
        # print(f"Original: {text1}")
        # print(f"Changed:  {text2}")
        # print(f"Changed token indices: {orig_ch}")
        
    except ImportError:
        print("ERROR: transformers not installed")
        print("Install with: pip install transformers")