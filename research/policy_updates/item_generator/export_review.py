"""Compatibility entry point; prefer `python -m item_generator review PATH`."""
from item_generator.review import export_review

if __name__ == '__main__':
    export_review('FAMILY_REVIEW.md')
    print('Exported review-only examples. Existing review files are never overwritten.')
