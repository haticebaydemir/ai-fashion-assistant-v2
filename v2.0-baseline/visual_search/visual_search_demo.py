# Visual Search Demo
# Usage: python visual_search_demo.py --image path/to/image.jpg

import argparse
from visual_search import VisualSearchEngine

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', required=True, help='Path to query image')
    parser.add_argument('--k', type=int, default=10, help='Number of results')
    args = parser.parse_args()
    
    # Load search engine
    engine = VisualSearchEngine.load('visual_search/index')
    
    # Search
    results, scores = engine.search(args.image, k=args.k)
    
    # Display
    print(f"Top-{args.k} similar products:")
    for rank, (pid, score) in enumerate(zip(results, scores), 1):
        print(f"{rank}. Product {pid}: {score:.3f}")

if __name__ == '__main__':
    main()
